# AI Builder OS — Community Course Structure

**60 lessons · 6 modules · max 10 per module · one reference per module**

Research basis: 262 YouTube videos pulled via the YouTube Data API (32 topic queries
ranked by view count, then hydrated with real view/like/comment stats and durations).
Research date: 2 August 2026.

Notion HQ: <https://app.notion.com/p/3b044f77e773816a8904e2f05f1a15a4>
Curriculum DB: <https://app.notion.com/p/042c73421abe48119bfc07c4a85dfc26>

---

## The edge: being legit

The differentiator is not a clever angle per video. It is a consistent editorial
standard applied to all 60 lessons:

**Be straight with people about what is possible and what is not.**

In practice that means five rules, enforced everywhere:

1. **Name the limits before the capability.** Every module has an early lesson that
   says what does not work. M0 Ep6, M1 Ep2, M2 Ep6, M3 Ep4, M4 Ep3, M5 Ep1.
2. **Show real costs in rupees.** Token bills, VPS monthly, API tiers, tool
   subscriptions. No "basically free".
3. **Leave the failures in.** Deploy errors, hallucinated figures, silent cron
   failures, losing ad campaigns. The recovery is the teaching.
4. **Talk people out of things.** When off-the-shelf beats building. When a VPS
   beats an old laptop. When you do not need an OS at all. When chat is enough and
   you never need to climb the ladder.
5. **Declare interest.** Affiliate links, sponsorships, and anything you are paid
   to recommend, said on camera.

This is a positioning bet, not just ethics: the space is saturated with people
promising outcomes they cannot produce, so the person who reliably says "that part
does not work" becomes the one worth believing on the parts that do.

---

## Staircase difficulty

Difficulty is scored 1–10 across the whole course and **never goes backwards**. Each
module starts at roughly where the previous one ended.

| Module | Difficulty band | Wave |
|--------|-----------------|------|
| M0 · From Cables to Claude | 1 → 2 | Wave 0 |
| M1 · Launch in 24 Hours | 2 → 4 | Wave 1 |
| M2 · Claude Code L1–L4 | 3 → 6 | Wave 2 |
| M3 · Agents & Automations | 5 → 7 | Wave 3 |
| M4 · AI Trading Floor | 6 → 8 | Wave 3 |
| M5 · AI Operating Systems | 7 → 10 | Wave 4 |

Because difficulty staircases, **AI Operating Systems is the finale**, not Trading.
That reverses an earlier plan to ship Trading last for pricing reasons — the
staircase requirement wins, and OS is the better capstone anyway since it assembles
every prior module.

## Format mix

- **Short** — 10–20 min, single concept. 22 lessons.
- **Deep Dive** — 40–90 min, one complete build. 32 lessons.
- **Full Course** — 2.5–8 hr, the whole module end to end. 6 lessons, one per module.

Every module ends with its Full Course episode. That is the Nate Herk–style
long-form slot: M0 2.5hr, M1 4hr, M2 5hr, M3 6hr, M4 5hr, M5 8hr.

---

## Module references

One benchmark per module — the current best performer on that module's territory.
Not a per-lesson competitor list; a single bar to clear.

| Module | Reference | Channel | Views |
|--------|-----------|---------|-------|
| M0 | [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs) | 3Blue1Brown | 7.0M |
| M1 | [How I Coded ANOTHER Profitable App SOLO](https://www.youtube.com/watch?v=cESaIUWoCJQ) | Edmund Yong | 1.45M |
| M2 | [CLAUDE CODE FULL COURSE 4 HOURS](https://www.youtube.com/watch?v=QoQBzR1NIqI) | Nick Saraev | 2.21M |
| M3 | [Build & Sell n8n AI Agents (8+ Hour Course)](https://www.youtube.com/watch?v=Ey18PDiaAYI) | Nate Herk | 1.80M |
| M4 | [Claude Just Changed the Stock Market Forever!](https://www.youtube.com/watch?v=lH5wrfNwL3k) | Samin Yasar | 1.62M |
| M5 | [Build & Sell with Claude Code (10+ Hour Course)](https://www.youtube.com/watch?v=mpALXah_PBg) | Nate Herk | 881k |

M3 and M5 references are the 8hr/10hr full-course format you named. Note their view
counts against M2's: the long-course format performs, but not better than a tight
4-hour one, and the 10hr sits at 881k against Saraev's 4hr at 2.2M. Length is not
what wins.

---

## Curriculum

### M0 — From Cables to Claude · difficulty 1–2 · all free · Wave 0

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 1 | The internet is a physical object | Short | 15 min |
| 2 | 1 | Protocols: the boring agreement that won | Short | 15 min |
| 3 | 1 | From web pages to APIs: software talking to itself | Short | 15 min |
| 4 | 1 | What a language model actually does (no maths) | Short | 18 min |
| 5 | 2 | Chatbot, tool, agent: three different things | Short | 15 min |
| 6 | 2 | **What AI genuinely cannot do in 2026** | Short | 20 min |
| 7 | 2 | The 50-year pattern: abstraction eats jobs, creates bigger ones | Short | 18 min |
| 8 | 2 | What "AI expert" actually means now | Short | 18 min |
| 9 | 2 | Set up your machine once, properly | Deep Dive | 45 min |
| 10 | 2 | FULL COURSE — Zero to your first working thing | Full Course | 2.5 hr |

Ep 9 is the prerequisite gate for every paid module. Ep 10 is the top-of-funnel asset.

### M1 — Launch in 24 Hours · difficulty 2–4 · Wave 1

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 2 | The 24-hour method: scope, ship, stop | Short | 15 min |
| 2 | 2 | **What actually fits in 24 hours — and what's a lie** | Short | 20 min |
| 3 | 3 | Launch a landing page | Deep Dive | 40 min |
| 4 | 3 | Launch a website with real content | Deep Dive | 50 min |
| 5 | 3 | Launch a working app | Deep Dive | 60 min |
| 6 | 3 | Launch an internal workflow | Deep Dive | 50 min |
| 7 | 4 | Launch a CRM | Deep Dive | 60 min |
| 8 | 4 | Launch an ad campaign | Deep Dive | 55 min |
| 9 | 4 | Launch a doctor's visit — the method past software | Deep Dive | 40 min |
| 10 | 4 | FULL COURSE — The 24-hour sprint, uncut | Full Course | 4 hr |

24 hours is a scoping constraint, not a productivity claim. Ep 10 leaves the dead
ends in — that is the format's whole value.

### M2 — Claude Code L1 → L4 · difficulty 3–6 · Wave 2

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 3 | L1 — The ceiling you hit using Claude as a chatbot | Short | 15 min |
| 2 | 3 | L1 — Your first real Claude Code session | Deep Dive | 45 min |
| 3 | 4 | L1 — Context is the whole game | Deep Dive | 40 min |
| 4 | 4 | L1 — Prompting like an engineer | Short | 18 min |
| 5 | 5 | L2 — Skills: procedures you stop re-explaining | Deep Dive | 45 min |
| 6 | 5 | **L2 — MCP, and when not to use it** | Short | 20 min |
| 7 | 5 | L2 — Connect Claude to your actual stack | Deep Dive | 55 min |
| 8 | 6 | L3 — Subagents, hooks and guardrails | Deep Dive | 55 min |
| 9 | 6 | L4 — What a harness is, and building a minimal one | Deep Dive | 60 min |
| 10 | 6 | FULL COURSE — L1 to L4 in one sitting | Full Course | 5 hr |

Ep 10 says up front that most viewers need L1–L2 and will never need L4 — and that
this is a fine outcome.

### M3 — AI Agents & Automations · difficulty 5–7 · Wave 3

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 5 | Workflows: what they are and why now | Short | 15 min |
| 2 | 5 | Workflow or agent? Pick the cheaper one | Short | 15 min |
| 3 | 5 | n8n in one sitting | Deep Dive | 60 min |
| 4 | 6 | **n8n vs Claude routines: the honest comparison** | Short | 20 min |
| 5 | 6 | Why routines fail silently — and how to fix it | Deep Dive | 50 min |
| 6 | 6 | Reliability: retries, idempotency, alerting | Deep Dive | 50 min |
| 7 | 6 | Your first VPS, and Docker without the fear | Deep Dive | 60 min |
| 8 | 7 | Cron jobs that actually fire | Deep Dive | 40 min |
| 9 | 7 | Old laptop as your always-on box — and when that's a mistake | Deep Dive | 50 min |
| 10 | 7 | FULL COURSE — Build and ship a production automation | Full Course | 6 hr |

Covers your brief directly: cron without someone else's server, why routines are
unreliable and how to fix it, and the old-laptop-as-Docker-host question including
the honest case against it.

### M4 — AI Trading Floor · difficulty 6–8 · Wave 3

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 6 | Personal finance first: you can't trade out of bad basics | Short | 18 min |
| 2 | 6 | How markets work: India and US side by side | Short | 20 min |
| 3 | 6 | **What AI genuinely can and can't do in markets** | Short | 20 min |
| 4 | 7 | Equity research with Claude, end to end | Deep Dive | 60 min |
| 5 | 7 | Portfolio evaluation and risk management | Deep Dive | 55 min |
| 6 | 7 | Backtesting without fooling yourself | Deep Dive | 60 min |
| 7 | 7 | Forward testing: paper trading with discipline | Deep Dive | 45 min |
| 8 | 8 | Claude + TradingView, and reading gamma exposure | Deep Dive | 60 min |
| 9 | 8 | India: automating Kite, Groww and Dhan | Deep Dive | 60 min |
| 10 | 8 | FULL COURSE — Research to bot to journal | Full Course | 5 hr |

Ep 3 carries the intraday reality — measure real broker API latency on camera, add
brokerage and slippage, show why it loses. Gamma is one lesson (Ep 8), not a
sub-module; it is a genuine content gap but it is not the point of the course.
Educational, not financial advice, stated at both ends of Ep 10.

### M5 — AI Operating Systems · difficulty 7–10 · Wave 4

| Ep | D | Lesson | Format | Length |
|----|---|--------|--------|--------|
| 1 | 7 | **What an OS is — and why a tool isn't one** | Short | 15 min |
| 2 | 7 | The blueprint: connectors, memory, schedule, review | Short | 20 min |
| 3 | 8 | Content OS | Deep Dive | 90 min |
| 4 | 8 | Business OS | Deep Dive | 75 min |
| 5 | 8 | Sales OS | Deep Dive | 75 min |
| 6 | 8 | Health OS | Deep Dive | 60 min |
| 7 | 9 | Medical OS | Deep Dive | 60 min |
| 8 | 9 | Trading OS | Deep Dive | 75 min |
| 9 | 9 | Learning OS and Career OS | Deep Dive | 60 min |
| 10 | 10 | FULL COURSE — Build your own OS from scratch | Full Course | 8 hr |

**The blueprint** (Ep 2, then applied seven times): connectors → memory → schedule →
review loop. A tool has none of these; an OS has all four.

Added beyond your list: **Sales OS** (Ep 5 — teaches `pipeline.py` from this repo),
**Learning OS** and **Career OS** (Ep 9). Capstone candidates for members: Home Ops,
Legal, Travel, Fitness.

Ep 1 says plainly that most people do not need an OS — they need two good
automations — and that selling them more is the scammy move.

---

## Launch waves

**Wave 0 — clean the house.** Audit scattered classroom material: keep, re-record,
or archive. Re-file into the six-module skeleton with all modules **visible but
locked**. Publish M0 free on YouTube. Do this before announcing anything.

**Wave 1 — reactivation.** M1 as a live 24-hour build sprint with a fixed date.
Success metric is **how many members post a shipped thing**, not signups.

**Wave 2 — M2.** The sprint creates the pain; the ladder answers it.

**Wave 3 — M3 + M4.** Infrastructure, then applied domain.

**Wave 4 — M5.** The capstone and the moat.

The 400-member price gate is the deadline mechanic in every touch. It beats a fake
countdown because it is true.

---

## Research method

- **Tooling:** YouTube Data API v3 via Composio (`YOUTUBE_SEARCH_YOU_TUBE`,
  `YOUTUBE_GET_VIDEO_DETAILS_BATCH`). 32 topic queries ordered by `viewCount`, then
  262 unique video IDs hydrated with `snippet`, `statistics`, `contentDetails`.
- **Filtering:** videos under 5 minutes excluded from benchmarking (Shorts skew).
- **Not used:** FireCrawl and yt-dlp. Both `api.firecrawl.dev` and `youtube.com` are
  blocked by this environment's egress policy (403 on CONNECT). The Data API
  returned better data regardless — exact counts rather than scraped approximations.
