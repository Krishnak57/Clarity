# 04 — Content Corpus & Escalation Directory

> This is the knowledge base spec. **Every fact in the corpus must come from the official source listed and be marked with the date it was verified.** Nothing is invented. Where a specific rule/URL/document list is not yet confirmed, mark it `[TO VERIFY]` and confirm against the official site before the demo.

## Corpus chunk schema (each entry in `data/corpus.json`)

```json
{
  "id": "bank-01",
  "journey": "A_bank_account",
  "jurisdiction": "US / Texas / UNT",
  "source_name": "Social Security Administration",
  "source_url": "https://www.ssa.gov/...",
  "last_verified_date": "2026-06-20",
  "text": "Plain extract of the official rule/requirement, ~200-400 words."
}
```

Aim for **~15–25 chunks total** across the three journeys. Quality and verification matter more than quantity.

---

## Journey A — Open a US bank account (F-1 student)

**Questions a real student has:** Am I eligible without an SSN? Which documents do I need? Which bank is good for international students? Do I need an appointment?

**Official / authoritative sources to gather from (confirm each exists & is current):**
- The student's bank's own "open an account" / "international students" page (e.g. the major national banks' official pages) — `[TO VERIFY each bank's current document list]`
- Social Security Administration (ssa.gov) — on whether an SSN is required and the ITIN alternative path
- IRS (irs.gov) — ITIN basics, if relevant
- The university's international student office (UNT ISSS) — any campus guidance on banking for new international students `[TO VERIFY]`
- USCIS / Study in the States (studyinthestates.dhs.gov) — F-1 documentation context (I-20, passport, visa) `[TO VERIFY]`

**Note for Cowork:** "Which bank is *good* for international students" is partly opinion, not an official rule. Handle it honestly: present what the official/bank pages factually state (fees, document requirements, student account options) and **do not editorialize** beyond what's sourced. If asked for a recommendation, abstain and escalate to a human/peer resource.

---

## Journey B — SSN and/or Texas driver's license (F-1 student)

**Questions:** Do I qualify for an SSN? What documents? Where do I go and in what order? What about a Texas driver's license — what's needed, where?

**Official sources to gather from:**
- Social Security Administration (ssa.gov) — SSN eligibility for F-1 students (typically tied to authorized employment), required documents, the application process `[TO VERIFY current requirements]`
- Texas Department of Public Safety (dps.texas.gov) — driver's license requirements, documents accepted, the application steps for non-citizens `[TO VERIFY]`
- The university ISSS office (UNT) — campus-specific guidance/letters often needed for SSN `[TO VERIFY]`
- USCIS / Study in the States — F-1 work-authorization context that gates SSN eligibility `[TO VERIFY]`

---

## Journey C — "What support am I eligible for?" (Benefits Navigator core)

This is the journey that satisfies **Direction A**. Its job is to clearly tell an F-1 student what they **do** and **do not** qualify for, in plain language, and what to do next.

**Questions:** Can I get health insurance / what are my options? Is there campus emergency money if I'm in trouble? Can I use a food pantry? Do I qualify for any government benefits?

**Official sources to gather from:**
- The university's own pages on: required student health insurance, campus emergency funds / hardship grants, campus food pantry, dean of students support resources (UNT) `[TO VERIFY each program's current eligibility]`
- Federal benefit pages (e.g. benefits.gov / USDA / HHS official pages) — primarily to **establish what F-1 students are generally NOT eligible for**, stated plainly and accurately `[TO VERIFY — be precise; eligibility is nuanced]`
- USCIS / Study in the States — the "public charge" / benefits-and-status context, stated carefully and with a strong escalation to a human, because this is high-stakes for visa status `[TO VERIFY — high stakes]`

**Critical handling:** Journey C touches immigration status. The system must (a) only state what the official source verifies, and (b) **always escalate to a human** (ISSS / immigration attorney / clinic) before the user acts, because a wrong move here can affect status. This is the clearest demonstration of responsible human-in-the-loop design — feature it in the demo.

---

## Escalation Directory (`data/escalation_directory.json`)

Maps each journey/topic to the *right* human. Gather the real, current contact details before the demo; mark `[TO VERIFY]` until confirmed.

```json
[
  {
    "topic": "immigration status / visa / SSN eligibility",
    "contact_name": "UNT International Student & Scholar Services (ISSS)",
    "contact_type": "university office",
    "how_to_reach": "[TO VERIFY: official ISSS email/phone/office]",
    "when_to_use": "Anything affecting F-1 status, work authorization, or SSN eligibility."
  },
  {
    "topic": "legal questions / housing / rights",
    "contact_name": "Free legal clinic or university legal services",
    "contact_type": "legal aid",
    "how_to_reach": "[TO VERIFY: real local/campus legal aid]",
    "when_to_use": "Anything that needs legal judgment."
  },
  {
    "topic": "banking specifics",
    "contact_name": "The specific bank's new-accounts line / branch",
    "contact_type": "official institution",
    "how_to_reach": "[TO VERIFY: official bank contact]",
    "when_to_use": "Confirming current document requirements before going in."
  },
  {
    "topic": "campus support / emergency funds / food",
    "contact_name": "UNT Dean of Students / student support office",
    "contact_type": "university office",
    "how_to_reach": "[TO VERIFY: official office contact]",
    "when_to_use": "Applying for hardship support or campus resources."
  }
]
```

## Verification checklist before the demo
- [ ] Every chunk has a real `source_url` that loads and a `last_verified_date`.
- [ ] No `[TO VERIFY]` remains in any chunk used in the demo path.
- [ ] Journey C correctly states what F-1 students are NOT eligible for (verified, not assumed).
- [ ] Every escalation contact is real and current.
- [ ] The Tool & Data Disclosure list in `05_DEVPOST_SUBMISSION.md` matches exactly the sources used here.
