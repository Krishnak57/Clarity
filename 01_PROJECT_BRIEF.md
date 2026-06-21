# 01 — Project Brief

## The problem (in one breath)

When someone lands in a new system — a new country, a new benefit program, a new legal process — the information they need *technically exists*, but it is scattered across dozens of official pages, written in language built for lawyers and bureaucrats, contradictory across federal/state/local/institutional levels, and impossible to map to *your specific situation*. So people do what the founder did: make a dozen phone calls, get five different answers, Google in circles, and ask a general chatbot that confidently hallucinates because it doesn't understand their case. The result is wasted time, anxiety, missed deadlines, and sometimes real harm (a broken visa status, a missed benefit, a wrong document).

## Founder's lived story (this opens the demo — it is the strongest asset)

The founder is an international student (F-1) in the US. Simply opening a bank account meant calling multiple people to learn eligibility rules, which documents were needed, and which bank was actually good for international students. The same maze repeated for the SSN and driver's license: what's needed, where to go, what order. Google sent him from one page to another; Gemini gave a hallucinated answer because it didn't understand his immigration situation. **This is not one person's bad luck — every international student hits this wall. The product is the tool he wishes had existed.**

## The user (start narrow, on purpose)

**Primary persona for the MVP:** International students in the US (F-1), proof-of-concept jurisdiction = Texas / UNT.

We are *not* building "answers for everyone everywhere." We are building a deep, trustworthy tool for one persona we understand completely, that is architected so the *same engine* can later cover any persona, place, or program. Narrow and deep beats broad and shallow — both for the hackathon and for a real product.

## The vision

A conversational assistant that:
1. **Understands your situation** by asking a few short, human questions (not a wall of jargon).
2. **Retrieves the governing rule** from a curated set of *official sources only* (government sites, the university's own office, the bank's own page).
3. **Translates it to plain language** anyone can understand — no heavy legal/bureaucratic wording.
4. **Gives a personalized, ordered checklist** — the steps, the documents, the official links, and when each is due.
5. **Shows its source and a "last verified" date on every answer** so the person can trust *and* verify.
6. **Knows its limits.** When it isn't confident, or the question is high-stakes (immigration status, legal, financial), it says so plainly and **routes the person to the right human** — the actual office, helpline, or free clinic for that topic.

## The wedge (why this wins, not just "an AI that answers questions")

Most "AI assistant with citations" projects answer freely and bolt citations on. Clarity's wedge is the opposite: **it is allowed to answer only from verified sources, and refusing is a first-class feature.** The triad that makes it memorable:

> **Plain-language answer · the source you can verify · a confidence meter that escalates to a human when it's low.**

Telling an international student clearly *"You are NOT eligible for this federal benefit — stop wasting time, here's what you ARE eligible for"* is as valuable as any "yes." That honest narrowing is the product.

## Scope — IN for the MVP (build only this)

Three end-to-end journeys for the F-1 / Texas persona:

- **Journey A — Open a US bank account** as an international student.
- **Journey B — Get an SSN and/or a Texas driver's license** (process, documents, order, where to go).
- **Journey C — "What support am I eligible for?"** (the Benefits-Navigator core): which campus/public support an F-1 student *does* and *does not* qualify for — e.g. campus emergency funds, health insurance options, campus food resources — and the explicit "you are not eligible for most federal benefits, here's what that means" clarity.

Journey C is what cleanly satisfies **Direction A: Benefits Navigator** ("help people understand whether they may qualify for a public support program — and what steps to take next").

## Scope — OUT (do NOT build — these are roadmap slides only)

- Login / user accounts / authentication
- Multiple languages
- Coverage beyond F-1 / Texas
- A real, live network of human volunteers (we provide a curated *directory* of the right official contacts instead — that is real and enough)
- A native mobile app
- Web scraping the live internet at query time (we use a fixed, curated, verified corpus)

## How this maps to the 5 judging dimensions

| Dimension | How Clarity earns it |
|-----------|----------------------|
| **Problem Understanding** | The founder's lived story, told in the first 30 seconds. First-person pain is unbeatable. |
| **AI Reasoning** | Retrieval-grounded answers + confidence-based **abstention** (the model refuses when unsure). This is the hard, impressive part. |
| **Solution Architecture** | A clean pipeline: curated corpus → retrieval → grounded generation → personalized checklist → escalation. Shown as a diagram. |
| **Impact & Decision Value** | Before: hours of calls, conflicting Google results, a hallucinating chatbot. After: one conversation, a sourced answer, a clear checklist, the right human for the hard part. |
| **Responsible AI** | Retrieval-only + citations + abstention + explicit "not legal/immigration advice" + human escalation on high stakes. This is woven into the architecture, not bolted on. |

## The non-negotiable principle (repeat to Cowork constantly)

**No fabrication. Ever.** If a fact isn't in the curated corpus, the system does not state it — it abstains and escalates. This applies to the *humans building it* too: when writing the corpus, real official facts must be gathered and verified, never invented. Placeholder/unverified facts must be clearly marked `[TO VERIFY]` until checked against the official source.
