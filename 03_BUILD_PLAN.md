# 03 — Build Plan (for Cowork)

> **Cowork: build this and only this. Do not expand scope. When you need a real-world fact (a rule, a URL, a document requirement), gather it from the official source and mark anything unverified as `[TO VERIFY]` — never invent it.**

## Target app file structure

```
clarity-app/
├── app.py                      # Streamlit UI: intake → answer → checklist → escalation
├── config.py                   # model name, retrieval threshold, paths
├── engine/
│   ├── intake.py               # journey selection + short question sets
│   ├── retrieval.py            # load corpus, embed/score, return top chunks + score
│   ├── generate.py             # free LLM call (Groq/Gemini) with strict grounding system prompt
│   ├── escalation.py           # threshold + high-stakes logic → directory lookup
│   └── checklist.py            # format grounded answer into ordered checklist
├── data/
│   ├── corpus.json             # the curated verified passages (from 04_CONTENT_CORPUS)
│   └── escalation_directory.json
├── prompts/
│   └── system_grounding.txt    # the strict "answer only from sources / abstain" prompt
├── requirements.txt
└── README.md                   # how to run it
```

## Build order (do in sequence — each step must work before the next)

### Step 1 — Skeleton that runs
- Streamlit app with: a journey picker (3 journeys), a text box, an answer area.
- Hardcode one fake answer first. Goal: the app opens and renders. Commit.

### Step 2 — Corpus + retrieval
- Load `data/corpus.json`. Implement `retrieval.py`: embed the query, score against chunks, return top N + the top score.
- Print the top score and chunks to verify retrieval is sane.
- **Build the threshold gate now:** if top score < threshold, return "ABSTAIN".

### Step 3 — Grounded generation
- Wire `generate.py` to the **free LLM API (Groq / Llama 3.3 70B, or Gemini Flash)** using `prompts/system_grounding.txt`. Read the key from a `.env` file — never hardcode it.
- Pass ONLY the retrieved chunks. The model must answer from them and cite source + date.
- Test: ask a question whose answer IS in the corpus → correct, cited answer.

### Step 4 — The refusal path (do not skip — this is the winning feature)
- Test: ask something NOT in the corpus → the abstain path fires → escalation message appears.
- Test: ask a high-stakes question (e.g. anything about visa status/legal) → even if answerable, append the human escalation.

### Step 5 — Checklist formatter
- `checklist.py` turns the grounded answer into an ordered list: step, documents, official link, last-verified date, confidence flag.
- Render it nicely in Streamlit (numbered, with the source/date visible per step).

### Step 6 — Escalation directory
- Load `data/escalation_directory.json`. `escalation.py` maps the journey/topic to the right human contact.
- Always show an "talk to a real person about this" option; auto-surface it on abstain/high-stakes.

### Step 7 — Polish for demo (only after 1–6 work)
- Clean the UI, add the "last verified" badge prominently, add the founder's one-line story to the home screen.
- Prepare the two demo moments: one perfect cited answer, one correct refusal+escalation.

## The strict grounding system prompt (put in `prompts/system_grounding.txt`)

```
You are Clarity, a plain-language guide that helps people understand official
rules and benefits. You help international students in the US (proof-of-concept:
F-1 students in Texas).

ABSOLUTE RULES:
1. Answer ONLY using the SOURCE PASSAGES provided below. If the passages do not
   contain the answer, reply exactly: "I don't have a verified answer for that."
   Do NOT use any outside knowledge. Never guess or fill gaps.
2. Use plain, simple language. Short sentences. No legal or bureaucratic wording.
   Assume the reader is smart but new to this system and possibly not a native
   English speaker.
3. After each fact, cite it like: (Source: <source_name>, verified <date>).
4. Do NOT give legal, immigration, or financial advice. Explain only what the
   official source says. For any judgment call, tell the user to confirm with the
   human contact provided.
5. If the question involves immigration status, legal action, or a money decision,
   answer what the sources verify, then clearly recommend talking to the listed
   human contact before acting.
6. Output the answer as an ordered checklist of steps when the user is trying to
   accomplish something: step, what to do, documents needed, official link.

SOURCE PASSAGES:
{retrieved_passages}

USER SITUATION:
{user_situation}
```

## Acceptance criteria (the build is "done" when ALL are true)

- [ ] App runs and shows the 3 journeys.
- [ ] A question answerable from the corpus returns a plain-language, **cited** answer with a last-verified date.
- [ ] An unanswerable / out-of-scope question returns the honest refusal + an escalation contact.
- [ ] A high-stakes question always appends a human escalation.
- [ ] The answer renders as an ordered checklist, not a paragraph dump.
- [ ] No fact appears on screen without a source. No `[TO VERIFY]` facts remain in the demo path.
- [ ] The demo can show, back to back: (1) a perfect cited answer, (2) a correct refusal.

## Things Cowork must NOT do
- Do not add login, multi-language, web scraping, or extra journeys.
- Do not let the model answer from general knowledge.
- Do not invent URLs, eligibility rules, document lists, or office names. Gather them or mark `[TO VERIFY]`.
- Do not over-build retrieval. For ~20 docs, simple is correct.
