import csv
import os
import json
import subprocess
import time
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")
HEYREACH_API_KEY = os.getenv("HEYREACH_API_KEY")
HEYREACH_CAMPAIGN_ID = os.getenv("HEYREACH_CAMPAIGN_ID")

CSV_PATH = os.path.join(os.path.dirname(__file__), "leads.csv")
CSV_HEADERS = [
    "date", "full_name", "first_name", "last_name", "title",
    "company", "domain", "linkedin_url", "email",
    "personalized_dm", "heyreach_status", "notes",
]

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
                "https://api.apollo.io/api/v1/mixed_people/api_search",
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                    "accept": "application/json",
                    "X-Api-Key": APOLLO_API_KEY,
                },
                json={
                    "api_key": APOLLO_API_KEY,
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
                "https://api.prospeo.io/search-person",
                headers={"X-KEY": PROSPEO_API_KEY, "Content-Type": "application/json"},
                json={"first_name": lead.get("first_name", ""), "last_name": lead.get("last_name", ""), "company": domain},
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


# ── STEP 3: Claude DM Personalization (humaniser) ────────────────────────────

HUMANISER_SYSTEM = """\
You write LinkedIn DMs that sound like a real person wrote them — not a bot, not a template.

Rules (humaniser):
- No em dashes. Use a comma, period, or rewrite the sentence.
- No filler openers: "I hope this finds you well", "I came across your profile", "I wanted to reach out".
- No vague significance words: "innovative", "leveraging", "game-changing", "exciting opportunity".
- No passive voice. Own the sentence.
- No rule-of-three lists. One clear point beats three watered-down ones.
- Vary sentence length. Short punches. Then a longer one that earns it.
- Have an opinion. Don't hedge everything.
- 60-80 words max. Tight is respectful of their time.
- End with a single low-pressure question, not a call to action speech.
"""

FALLBACK_DM = (
    "Hey {first_name}, noticed {company} is deep in the AI automation space. "
    "We cut manual ops for teams like yours. Worth a quick chat?"
)

def personalize_dms(leads):
    print("✍️  STEP 3 — Generating personalized DMs via Claude CLI (humaniser)...")

    for lead in leads:
        first_name = lead.get("first_name", "there")
        title = lead.get("title", "")
        company = (lead.get("organization") or {}).get("name", "your company")
        linkedin_url = lead.get("linkedin_url", "")

        user_prompt = (
            f"Write a LinkedIn DM for:\n"
            f"- Name: {first_name}\n"
            f"- Title: {title}\n"
            f"- Company: {company}\n"
            f"- LinkedIn: {linkedin_url}\n\n"
            "Open with something specific and true about their role or company. "
            "Show you get their actual pain (manual work = slow = expensive). "
            "End with one soft question."
        )

        full_prompt = HUMANISER_SYSTEM + "\n\n" + user_prompt
        try:
            result = subprocess.run(
                ["claude", "-p", full_prompt],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0 and result.stdout.strip():
                lead["personalized_dm"] = result.stdout.strip()
            else:
                raise RuntimeError(result.stderr.strip() or "empty response")
        except Exception as e:
            print(f"  ⚠ Claude CLI error for {first_name}: {e} — using fallback")
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


# ── STEP 5: CSV → GitHub ──────────────────────────────────────────────────────

def update_csv_github(leads, heyreach_added):
    print("📋 STEP 5 — Updating leads.csv and pushing to GitHub...")
    today = str(date.today())

    # Load existing rows to avoid duplicate linkedin_urls
    existing_urls = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing_urls.add(row.get("linkedin_url", ""))

    new_rows = []
    for lead in leads:
        org = lead.get("organization") or {}
        linkedin_url = lead.get("linkedin_url", "")
        if linkedin_url in existing_urls:
            continue
        new_rows.append({
            "date": today,
            "full_name": f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip(),
            "first_name": lead.get("first_name", ""),
            "last_name": lead.get("last_name", ""),
            "title": lead.get("title", ""),
            "company": org.get("name", ""),
            "domain": org.get("primary_domain", ""),
            "linkedin_url": linkedin_url,
            "email": lead.get("email", ""),
            "personalized_dm": lead.get("personalized_dm", ""),
            "heyreach_status": "added" if heyreach_added else "failed",
            "notes": "",
        })

    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)

    print(f"  ✅ {len(new_rows)} new rows written to leads.csv")

    # Commit and push
    try:
        repo_root = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(["git", "add", "leads.csv"], cwd=repo_root, check=True)
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo_root,
        )
        if result.returncode != 0:
            subprocess.run(
                ["git", "commit", "-m", f"pipeline: add {len(new_rows)} leads ({today})"],
                cwd=repo_root, check=True,
            )
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=repo_root, check=True,
            )
            print("  ✅ leads.csv committed and pushed to GitHub")
        else:
            print("  ℹ  No new leads to commit")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Git error: {e}")

    return len(new_rows)


# ── STEP 6: Summary Report ────────────────────────────────────────────────────

def print_summary(raw_count, enriched, heyreach_added, csv_count):
    today = date.today().strftime("%d-%m-%Y")
    top3 = enriched[:3]

    print(f"""
📊 METEORIFY PIPELINE — {today}

🔍 ICP Search: {raw_count} leads found (Apollo)
✅ Verified Emails: {len(enriched)} leads (Prospeo)
✍️  Personalized: {len(enriched)} DMs (OpenAI)
📤 HeyReach: {heyreach_added} added to campaign {HEYREACH_CAMPAIGN_ID}
📋 CSV: {csv_count} new rows committed to GitHub (leads.csv)

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
    csv_count = update_csv_github(personalized_leads, heyreach_added)
    print_summary(len(raw_leads), personalized_leads, heyreach_added, csv_count)
