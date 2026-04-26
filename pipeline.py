import os
import json
import time
import requests
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")
HEYREACH_API_KEY = os.getenv("HEYREACH_API_KEY")
HEYREACH_CAMPAIGN_ID = os.getenv("HEYREACH_CAMPAIGN_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CRM_SHEET_URL = os.getenv("CRM_SHEET_URL")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

ICP_TITLES = [
    "Founder", "CEO", "CTO", "COO",
    "Head of Operations", "VP of Engineering",
    "Director of Operations",
]
ICP_KEYWORDS = [
    "AI automation", "artificial intelligence", "machine learning",
    "LLM", "GPT", "AI agents",
]
ICP_LOCATIONS = ["United States", "United Kingdom"]
MAX_LEADS = 50


# ── STEP 1: Apollo ICP Search ─────────────────────────────────────────────────

def search_apollo_leads():
    print("🔍 STEP 1 — Searching Apollo for ICP leads...")
    leads = []
    page = 1

    while len(leads) < MAX_LEADS:
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/mixed_people/search",
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                    "X-Api-Key": APOLLO_API_KEY,
                },
                json={
                    "person_titles": ICP_TITLES,
                    "person_locations": ICP_LOCATIONS,
                    "organization_num_employees_ranges": ["10,500"],
                    "q_organization_keyword_tags": ICP_KEYWORDS,
                    "page": page,
                    "per_page": min(25, MAX_LEADS - len(leads)),
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            people = data.get("people", [])
            if not people:
                break
            leads.extend(people)
            page += 1
        except Exception as e:
            print(f"  ⚠ Apollo error: {e} — skipping")
            break

    with open("leads_raw.json", "w") as f:
        json.dump(leads, f, indent=2)

    print(f"  ✅ Found {len(leads)} ICP leads from Apollo")
    return leads


# ── STEP 2: Prospeo Email Enrichment ─────────────────────────────────────────

def enrich_emails(leads):
    print("📧 STEP 2 — Enriching emails via Prospeo...")
    enriched = []

    for lead in leads:
        full_name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        domain = (lead.get("organization") or {}).get("primary_domain", "")
        linkedin_url = lead.get("linkedin_url", "")

        if not domain and not linkedin_url:
            lead["email"] = None
            lead["email_status"] = "no_domain"
            continue

        try:
            resp = requests.post(
                "https://api.prospeo.io/email-finder",
                headers={"X-KEY": PROSPEO_API_KEY, "Content-Type": "application/json"},
                json={"full_name": full_name, "company": domain, "linkedin_url": linkedin_url},
                timeout=20,
            )
            resp.raise_for_status()
            result = resp.json()
            email = result.get("response", {}).get("email")
            status = result.get("response", {}).get("verification", {}).get("result", "unknown")

            if email and status in ("valid", "accept_all"):
                lead["email"] = email
                lead["email_status"] = status
                enriched.append(lead)
            else:
                lead["email"] = None
                lead["email_status"] = "no_email"
        except Exception as e:
            print(f"  ⚠ Prospeo error for {full_name}: {e}")
            lead["email"] = None
            lead["email_status"] = "error"

        time.sleep(1)  # rate limit

    with open("leads_enriched.json", "w") as f:
        json.dump(enriched, f, indent=2)

    print(f"  ✅ {len(enriched)} leads with verified emails")
    return enriched


# ── STEP 3: OpenAI Personalization ───────────────────────────────────────────

FALLBACK_DM = (
    "Hey {first_name}, saw what you're building at {company} — really interesting space. "
    "We help teams like yours cut manual ops with AI automation. Worth a quick chat?"
)

def personalize_dms(leads):
    print("✍️  STEP 3 — Generating personalized DMs via OpenAI...")

    for lead in leads:
        first_name = lead.get("first_name", "there")
        title = lead.get("title", "")
        company = (lead.get("organization") or {}).get("name", "your company")
        linkedin_url = lead.get("linkedin_url", "")

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior B2B copywriter. You write LinkedIn DMs that sound "
                            "like a smart peer — warm, specific, no templates. 60-120 words max."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Write a LinkedIn DM for:\n"
                            f"- Name: {first_name}\n"
                            f"- Title: {title}\n"
                            f"- Company: {company}\n"
                            f"- LinkedIn: {linkedin_url}\n\n"
                            "Requirements:\n"
                            "- Open with something SPECIFIC about them or their company\n"
                            "- Reference their role or industry naturally\n"
                            "- Show you understand their pain point (manual = slow = expensive)\n"
                            "- End with soft CTA: 'worth a quick chat?' or 'mind if I share?'\n"
                            "- Sound like a peer, not a salesperson"
                        ),
                    },
                ],
                max_tokens=200,
            )
            lead["personalized_dm"] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  ⚠ OpenAI error for {first_name}: {e} — using fallback")
            lead["personalized_dm"] = FALLBACK_DM.format(
                first_name=first_name, company=company
            )

    print(f"  ✅ {len(leads)} DMs generated")
    return leads


# ── STEP 4: HeyReach Campaign ─────────────────────────────────────────────────

def add_to_heyreach(leads):
    print("📤 STEP 4 — Adding leads to HeyReach campaign...")
    failed = []
    added = 0

    payload_leads = []
    for lead in leads:
        org = lead.get("organization") or {}
        payload_leads.append({
            "first_name": lead.get("first_name", ""),
            "last_name": lead.get("last_name", ""),
            "company_name": org.get("name", ""),
            "title": lead.get("title", ""),
            "linkedin_profile_url": lead.get("linkedin_url", ""),
        })

    try:
        resp = requests.post(
            "https://api.heyreach.io/api/v1/campaign/add_leads",
            headers={"X-Api-Key": HEYREACH_API_KEY, "Content-Type": "application/json"},
            json={"campaign_id": HEYREACH_CAMPAIGN_ID, "leads": payload_leads},
            timeout=30,
        )
        resp.raise_for_status()
        added = len(payload_leads)
    except Exception as e:
        print(f"  ⚠ HeyReach error: {e} — logging to heyreach_failed.json")
        failed = leads
        with open("heyreach_failed.json", "w") as f:
            json.dump(failed, f, indent=2)

    print(f"  ✅ Added {added} leads to HeyReach campaign {HEYREACH_CAMPAIGN_ID}")
    return added


# ── STEP 5: Google Sheets CRM ─────────────────────────────────────────────────

def log_to_crm(leads, heyreach_added):
    print("📋 STEP 5 — Logging to Google Sheets CRM...")
    today = str(date.today())
    rows = []

    for lead in leads:
        org = lead.get("organization") or {}
        rows.append([
            today,
            f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip(),
            lead.get("first_name", ""),
            lead.get("last_name", ""),
            lead.get("title", ""),
            org.get("name", ""),
            org.get("primary_domain", ""),
            lead.get("linkedin_url", ""),
            lead.get("email", ""),
            lead.get("personalized_dm", ""),
            "added" if heyreach_added else "failed",
            "",
        ])

    try:
        resp = requests.post(
            CRM_SHEET_URL,
            json={"rows": rows},
            timeout=20,
        )
        resp.raise_for_status()
        print(f"  ✅ Logged {len(rows)} leads to CRM")
    except Exception as e:
        print(f"  ⚠ CRM logging error: {e}")

    return len(rows)


# ── STEP 6: Summary Report ────────────────────────────────────────────────────

def print_summary(raw_count, enriched, heyreach_added, crm_count):
    today = date.today().strftime("%d-%m-%Y")
    top3 = enriched[:3]

    print(f"""
📊 METEORIFY PIPELINE — {today}

🔍 ICP Search: {raw_count} leads found (Apollo)
✅ Verified Emails: {len(enriched)} leads (Prospeo)
✍️  Personalized: {len(enriched)} DMs (OpenAI)
📤 HeyReach: {heyreach_added} added to campaign {HEYREACH_CAMPAIGN_ID}
📋 CRM: {crm_count} logged to Google Sheet

Top 3 leads by company:""")

    for i, lead in enumerate(top3, 1):
        name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        company = (lead.get("organization") or {}).get("name", "Unknown")
        title = lead.get("title", "Unknown")
        print(f"  {i}. {name} @ {company} — {title}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    raw_leads = search_apollo_leads()
    enriched_leads = enrich_emails(raw_leads)
    personalized_leads = personalize_dms(enriched_leads)
    heyreach_added = add_to_heyreach(personalized_leads)
    crm_count = log_to_crm(personalized_leads, heyreach_added)
    print_summary(len(raw_leads), personalized_leads, heyreach_added, crm_count)
