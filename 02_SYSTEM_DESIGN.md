# 02 — System Design

## Design goal

Make hallucination *architecturally difficult*, not just discouraged. The model is never the source of truth — the curated corpus is. The model's only jobs are: understand the question, pull the right passages, rewrite them in plain language, sequence them, and know when to refuse.

## The pipeline (this is also the architecture diagram for Devpost)

```
        ┌─────────────────────────────────────────────────────────────┐
        │  USER  ("I'm an F-1 student, how do I open a bank account?") │
        └───────────────────────────┬─────────────────────────────────┘
                                     ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  1. INTAKE                                                    │
        │  A few short, plain-language questions to pin down the        │
        │  situation (visa type, state, what they already have).        │
        │  Goal: turn a vague question into a precise one.              │
        └───────────────────────────┬─────────────────────────────────┘
                                     ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  2. RETRIEVAL  (from the CURATED CORPUS only)                 │
        │  Find the most relevant verified passages. Each passage       │
        │  carries: source URL + jurisdiction + last-verified date.     │
        │  Returns a relevance score.                                   │
        └───────────────────────────┬─────────────────────────────────┘
                                     ▼
                        ┌────────────┴────────────┐
                        ▼                         ▼
            relevance HIGH                 relevance LOW
            + in scope                     OR out of scope
                        │                         │
                        ▼                         ▼
        ┌───────────────────────────┐   ┌─────────────────────────────┐
        │  3. GROUNDED GENERATION    │   │  3b. ABSTAIN + ESCALATE     │
        │  LLM answers STRICTLY from │   │  "I don't have a verified    │
        │  retrieved passages.       │   │  answer for this."           │
        │  Plain language. Inline    │   │  → route to the right human  │
        │  citation on every claim.  │   │     from the directory.      │
        └────────────┬──────────────┘   └─────────────────────────────┘
                     ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  4. PERSONALIZED CHECKLIST                                    │
        │  Ordered steps · documents needed · official links ·          │
        │  last-verified date · per-step confidence flag.              │
        └───────────────────────────┬─────────────────────────────────┘
                                     ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  5. HUMAN-IN-THE-LOOP ESCALATION                             │
        │  Always offered. AUTO-triggered when: confidence is low,      │
        │  OR the topic is high-stakes (immigration / legal /          │
        │  financial / status-affecting).                              │
        └─────────────────────────────────────────────────────────────┘
```

## Component detail

### 1. Intake
- 2–4 short questions max, in plain language, before answering.
- Purpose: collect the variables that change the answer (visa type, state, current documents, the specific goal).
- Implementation: a short fixed question set per journey is fine for the MVP. It does NOT need to be a free-form AI conversation to be impressive — a clean guided intake is more reliable and demos better.

### 2. Retrieval (the heart of anti-hallucination)
- The corpus is chunked into small passages (~200–400 words). Each chunk stores: `text`, `source_url`, `source_name`, `jurisdiction`, `journey`, `last_verified_date`.
- Retrieval returns the top passages **with a relevance score**.
- **Threshold gate:** if the top score is below a set threshold, the system does NOT generate an answer — it abstains (step 3b). This single gate is what prevents the model from "filling in" missing knowledge.
- MVP-acceptable implementations (pick the simplest that works):
  - **Recommended:** **sentence-transformers run locally** (`all-MiniLM-L6-v2`, free, no API key) to embed chunks + cosine similarity, stored in a JSON/SQLite file. ~20 docs needs no heavy vector DB and no paid embeddings API.
  - **Fallback (totally fine for 20 docs):** keyword/BM25 search + the LLM re-reading the top chunks. Don't over-engineer.

### 3. Grounded generation
- The LLM (free tier — **Groq / Llama 3.3 70B**, or Gemini Flash) receives: the user's situation + ONLY the retrieved passages.
- **System-prompt rules for the model (critical):**
  - Answer using *only* the provided passages. If the passages don't contain the answer, say you don't have a verified answer — do not use outside knowledge.
  - Plain language. No legal/bureaucratic wording. Short sentences.
  - Cite the source after each claim (source name + last-verified date).
  - Never give legal, immigration, or financial *advice* — explain what the official source says and point to a human for judgment calls.
  - If the question touches immigration status, legal action, or money decisions → answer what's verifiable, then escalate.

### 3b. Abstain + escalate
- Triggered by the threshold gate or an out-of-scope classifier.
- Output is honest and useful: "I don't have a verified answer for that. Here's the right place/person to ask," pulled from the escalation directory.

### 4. Personalized checklist
- The valuable output format — NOT a wall of chat text.
- Fields per step: order number, action, documents needed, official link, last-verified date, confidence flag (✅ verified / ⚠️ check with a human).

### 5. Human-in-the-loop escalation
- A curated **directory** (see `04_CONTENT_CORPUS.md`) maps each journey/topic → the correct human contact (university ISSS office, official government helpline, free legal clinic, etc.).
- Escalation is **always available** and **auto-surfaced** on low confidence or high stakes.
- This is the honest answer to "what if the AI is wrong?": a human owns the high-stakes call.

## Recommended tech stack (optimized for ~48 hours + a clean demo)

| Layer | Choice | Why |
|-------|--------|-----|
| App / UI | **Streamlit** | Fast to build, you know it, gives a clean demoable chat + checklist UI with little code |
| Corpus store | **JSON or SQLite** | ~20 docs; no heavy infra needed |
| Retrieval / embeddings | **sentence-transformers run locally** (`all-MiniLM-L6-v2`) + cosine similarity; keyword fallback fine | Free, no API key, no rate limits, offline. Simple and explainable to judges. ~20 docs is instant |
| Generation | **Groq free API (Llama 3.3 70B)** — or Gemini Flash free tier | 100% free, no credit card; Groq is fast and doesn't train on your data. Strong instruction-following for the strict grounding rules |
| Escalation directory | **JSON / CSV** | Curated, easy to edit |
| Config | one `config.py` for thresholds, model name, paths | Easy to tune live |

> If a richer web UI is wanted, a simple React/HTML front end works too — but Streamlit is the pragmatic 48-hour choice. Don't trade build time for polish; judges score thinking and design over polish.

## What "good" looks like (the bar Cowork must hit)

- A hard question (e.g. bank account for F-1) is answered correctly, in plain language, **with a visible source and date**.
- An out-of-scope or unknown question is **correctly refused** and escalated — the system never bluffs.
- The answer comes back as a **clean ordered checklist**, not a paragraph dump.
- Every fact on screen traces to an official source.

## Data & privacy notes (mention in Responsible AI section)
- The MVP needs no personal accounts and stores no personal data. Intake answers live in session only.
- All source data is public, official, and disclosed (see Tool & Data Disclosure in `05_DEVPOST_SUBMISSION.md`).
