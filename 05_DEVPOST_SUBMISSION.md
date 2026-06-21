# 05 — Devpost Submission (ready to paste)

> Fill the bracketed bits, then paste each section into the matching Devpost field. Keep it plain and concrete — judges reward clear thinking over buzzwords. Replace "Clarity" if you renamed it.

---

## Project Description — *"What you built and why"*

**Clarity** helps international students in the US understand the real-world rules and benefits they have to navigate — opening a bank account, getting an SSN or driver's license, and figuring out what support they actually qualify for — in plain language, from official sources only, and with an honest hand-off to a real person when the stakes are high.

The idea comes from lived experience. As an F-1 student, our founder spent days making phone calls and Googling in circles just to open a bank account, and a general AI chatbot gave a confidently wrong answer because it didn't understand his immigration situation. The information existed — it was just scattered, written in bureaucratic language, contradictory across federal/state/university levels, and impossible to map to one person's specific case. Every international student hits this same wall.

Clarity is built around one principle: **it never makes up an answer.** It pulls from a curated set of official sources (government sites, the university's own offices, the bank's own pages), explains the answer in plain language, shows the source and the date it was last verified, and — when it isn't confident or the question is high-stakes — it says so and routes the person to the right human. Telling someone clearly *"you are not eligible for this, here's what you are eligible for"* is as valuable as any "yes."

For the hackathon we built three end-to-end journeys for the F-1 / Texas persona: opening a US bank account, getting an SSN / driver's license, and a Benefits Navigator that explains what campus and public support a student does and doesn't qualify for.

---

## AI Architecture Explanation — *"How your AI components actually work"*

Clarity is a retrieval-grounded assistant designed so that hallucination is architecturally difficult:

1. **Intake** — a few short, plain-language questions turn a vague question into a precise one (visa type, state, what the user already has).
2. **Retrieval** — the query is matched against a curated corpus of verified official passages. Each passage carries its source URL, jurisdiction, and last-verified date, and retrieval returns a relevance score.
3. **Threshold gate** — if the best match is below a confidence threshold, the system does **not** generate an answer. This single gate is what stops the model from "filling in" missing knowledge.
4. **Grounded generation** — the LLM (a free open model via Groq, Llama 3.3 70B) answers **strictly from the retrieved passages**, in plain language, citing the source and date after each claim. It is explicitly instructed never to use outside knowledge.
5. **Personalized checklist** — the answer is formatted into an ordered set of steps with documents, official links, and a per-step confidence flag.
6. **Escalation** — a curated directory routes the user to the correct human (university ISSS office, official helpline, legal clinic). Escalation auto-triggers on low confidence or high-stakes topics.

The model is never the source of truth — the curated corpus is. The model only understands, retrieves, rewrites in plain language, sequences, and refuses when unsure.

---

## Responsible AI Guardrail — *"One realistic risk + one concrete design mitigation"*

**Risk:** Wrong information on immigration, eligibility, or finance can cause real harm — a broken visa status, a missed deadline, or a wasted application. A confident hallucination here is dangerous, not just unhelpful.

**Mitigation:** Clarity answers *only* from a curated corpus of official sources, cites the source and last-verified date on every claim, and **abstains** (refuses to answer) when retrieval confidence is below threshold or the topic is out of scope. It never gives legal/immigration/financial advice, and any high-stakes topic auto-routes the user to a verified human contact before they act. Refusing is a designed feature, not a failure.

---

## Human-in-the-Loop Design — *"Where humans stay in control and why"*

Humans own every judgment call. Clarity explains what official sources *say*; it never decides what a person *should do* on status, legal, or financial matters. Escalation to a real human (university ISSS office, official helpline, free legal clinic) is always offered and is **automatically surfaced** when (a) the system's confidence is low, or (b) the topic affects immigration status, legal standing, or a significant money decision. The system's value is making the user informed enough to have a faster, better conversation with the right human — not replacing that human.

---

## Decision Impact Statement — *"Before vs. after — what changes for the user"*

**Before:** Hours of phone calls, conflicting answers, Google sending you from page to page, and a general chatbot hallucinating because it doesn't understand your visa situation. Anxiety, wasted time, and the real risk of acting on wrong information.

**After:** One short conversation produces a plain-language, sourced answer and a clear, ordered checklist — what to do, which documents, which official link, when it's due — plus the right human to call for the part that needs judgment. The user goes from confused and stuck to informed and moving, without ever being misled.

---

## Tool & Data Disclosure — *"Every AI tool and data source used"*

**AI tools / models:**
- **Groq API (free tier) running Llama 3.3 70B** — plain-language generation, grounded strictly in the retrieved passages (never from outside knowledge).
- **sentence-transformers (`all-MiniLM-L6-v2`), run locally** — embeddings + cosine similarity for retrieval (free, no API key, no data leaves the machine).
- **Streamlit** — application UI.

**Data sources — corpus (all public, official, and curated; no scraping; 13 passages, each verified 2026-06-20):**

*Journey A — Open a US bank account*
- Chase — Opening a Bank Account as an International Student — https://www.chase.com/personal/banking/education/basics/bank-accounts-for-international-students
- Bank of America — How to Open a Bank Account as an International Student — https://info.bankofamerica.com/en/international/student-bank-account
- Study in the States (DHS) — Individual Taxpayer Identification Number (ITIN) — https://studyinthestates.dhs.gov/students/work/individual-taxpayer-identification-number-itin

*Journey B — SSN and/or Texas driver's license*
- Social Security Administration — International Students and Social Security Numbers (Pub. 05-10181) — https://www.ssa.gov/pubs/EN-05-10181.pdf
- Study in the States (DHS) — Obtaining a Social Security Number — https://studyinthestates.dhs.gov/students/work/obtaining-a-social-security-number
- Texas Department of Public Safety — U.S. Citizenship or Lawful Presence Requirement — https://www.dps.texas.gov/section/driver-license/us-citizenship-or-lawful-presence-requirement
- Texas Department of Public Safety — Apply for a Texas Driver License — https://www.dps.texas.gov/section/driver-license/apply-texas-driver-license

*Journey C — What support am I eligible for? (Benefits Navigator)*
- Federal Student Aid (studentaid.gov) — Eligibility for Non-U.S. Citizens — https://studentaid.gov/understand-aid/eligibility/requirements/non-us-citizens
- USDA Food and Nutrition Service — SNAP Guidance on Non-Citizen Eligibility — https://www.fns.usda.gov/snap/eligibility/non-citizen-guidance
- USDA Food and Nutrition Service — Joint Letter on Public Charge — https://www.fns.usda.gov/snap/joint-letter-public-charge
- UNT International Affairs — International Student Health Insurance — https://international.unt.edu/international-students/newly-admitted-international-students/international-student-health-insurance.html
- UNT Student Affairs — Food Pantry — https://studentaffairs.unt.edu/desresources/programs/food-pantry/about-us/index.html
- UNT Student Money Management Center — Eagle Support Program (Emergency Aid) — https://studentaffairs.unt.edu/student-money-management-center/programs-and-services/emergency-aid/emergency-support

**Escalation directory — human contacts (verified 2026-06-20):**
- UNT International Student & Scholar Services (ISSS) — university office (immigration / visa / SSN eligibility) — https://international.unt.edu/international-students/index.html
- UNT Student Legal Services — legal aid (legal / rights / immigration legal advice) — https://studentaffairs.unt.edu/dean-of-students/programs-and-services/student-legal-services/index.html
- UNT Dean of Students Office — university office (campus support / emergency funds / food) — https://deanofstudents.unt.edu/resources/food-pantry
- The user's chosen bank's branch / new-accounts line — official institution (confirming current document requirements before opening an account)

**Privacy:** All data sources are public and official. No personal user data is collected or stored; intake answers exist only in the current session.

> This list is kept exactly in sync with the corpus (`clarity-app/data/corpus.json`) and escalation directory (`clarity-app/data/escalation_directory.json`). Disclosing all tools and sources is a hackathon rule.

---

## Submission checklist (from the "What You Must Submit" slide)
- [ ] Project Description (above)
- [ ] 2–5 minute demo video (see `06_DEMO_SCRIPT.md`)
- [ ] AI Architecture Explanation (above)
- [ ] Responsible AI Guardrail (above)
- [ ] Human-in-the-Loop Design (above)
- [ ] Decision Impact Statement (above)
- [ ] Tool & Data Disclosure (above)
- [ ] Built within June 14–21 window · submitted on Devpost before June 21, 11:59 PM ET
