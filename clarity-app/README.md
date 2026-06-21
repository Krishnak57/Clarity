# Clarity — app

Plain-language, source-cited answers for F-1 students in Texas, across three
journeys: (A) open a US bank account, (B) get an SSN / Texas driver's license,
(C) what support am I eligible for. Clarity answers **only** from a curated
corpus of official sources, cites the source + last-verified date on every step,
and **abstains + escalates to a real human** when confidence is low, the topic is
out of scope, or the stakes are high.

## Run it

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Put your free Groq API key in a .env file at the repo root (one level up):
#   GROQ_API_KEY=gsk_...
# Get one free at https://console.groq.com (no credit card).

streamlit run app.py
```

First run downloads the local embedding model (`all-MiniLM-L6-v2`, ~90 MB) once.

## How it works (the anti-hallucination pipeline)

```
intake → retrieval (local embeddings + threshold gate) → grounded generation
       → checklist (citations from chunk metadata) → human escalation
```

- **Retrieval threshold gate** (`config.RETRIEVAL_THRESHOLD`): if the best cosine
  score is below the threshold, Clarity does **not** generate — it abstains.
- **Model-level abstention**: the LLM is instructed to answer only from the
  provided passages and return "not answerable" otherwise. Second line of defense.
- **Citations come from chunk metadata**, not the model — source name, URL, and
  last-verified date are attached from `corpus.json`, so no citation is fabricated.
- **Escalation** is always offered and auto-surfaced on low confidence or
  high-stakes topics (immigration / legal / financial).

## Files

| File | Role |
|------|------|
| `app.py` | Streamlit UI: intake → answer → checklist → escalation |
| `config.py` | Model, threshold, paths, journeys, high-stakes keywords |
| `engine/intake.py` | Journey selection + short question sets |
| `engine/retrieval.py` | Embed + score corpus, top-N + threshold gate |
| `engine/generate.py` | Groq (Llama 3.3 70B) grounded generation |
| `engine/checklist.py` | Format steps + attach real source metadata |
| `engine/escalation.py` | Threshold/high-stakes logic + directory lookup |
| `data/corpus.json` | Curated verified passages |
| `data/escalation_directory.json` | Journey/topic → human contact |
| `prompts/system_grounding.txt` | The strict "answer only from sources" prompt |

## Tuning

Each engine module is runnable standalone for quick checks, e.g.:

```bash
python -m engine.retrieval     # prints top scores + chunks for sample queries
python -m engine.checklist     # full pipeline for one bank question
```
