# Clarity

**Plain-language answers to real-world rules and benefits for international students -- sourced from official websites, honest about what it doesn't know, and built to hand you to a real human when the stakes are high.**

Built for the USAII Global AI Hackathon 2026 | Undergraduate Track | Brief 4: Public Services -- Benefits Navigator

---

## The Problem

When an international student arrives in the US, even basic tasks -- opening a bank account, getting a driver's license, understanding what support they qualify for -- become a maze. The information technically exists, but it is scattered across dozens of federal, state, and university websites, written in bureaucratic language, and impossible to map to one person's specific situation. General-purpose AI chatbots make the problem worse by hallucinating answers to questions where a wrong answer can break a visa status or waste weeks of effort.

## What Clarity Does

Clarity is a conversational assistant that answers real-world questions for F-1 international students in Texas. It covers three end-to-end journeys:

- **Open a US bank account** -- which banks accept F-1 students, what documents are actually needed, whether an SSN is required.
- **Get an SSN and/or Texas driver's license** -- the real process, the correct order, required documents, and where to go.
- **Benefits Navigator** -- what campus and public support a student qualifies for, and just as importantly, what they do not.

Every answer includes a plain-language explanation, an ordered checklist of steps with required documents, the official source name and URL, a "last verified" date, and a per-step confidence indicator.

## The Core Principle

**The system never makes up an answer.** It answers only from a curated corpus of verified official sources. When it is not confident or the question is out of scope, it says so plainly and routes the user to the right human contact. Refusing to answer is a designed feature, not a failure.

## Architecture

Clarity is a retrieval-augmented generation (RAG) system with a hard confidence gate that makes hallucination architecturally difficult:

```
Intake --> Retrieval (local embeddings + threshold gate) --> Grounded Generation
       --> Personalized Checklist (citations from metadata) --> Human Escalation
```

1. **Intake** -- Short, plain-language questions narrow down the user's situation (visa type, state, existing documents).
2. **Retrieval** -- The query is embedded locally using sentence-transformers and matched via cosine similarity against a curated corpus of 13 verified official passages. Each passage carries its source URL, jurisdiction, and last-verified date.
3. **Threshold Gate** -- If the top retrieval score falls below a confidence threshold, the system stops. No generation. No guessing. It abstains and escalates to a human.
4. **Grounded Generation** -- The LLM (Llama 3.3 70B via Groq) answers strictly from the retrieved passages. It is explicitly instructed to never use outside knowledge. Temperature is set to 0.0 for deterministic extraction.
5. **Checklist Output** -- The answer is formatted into ordered steps. Source citations (URLs, dates) are attached from the corpus metadata, not from the model, so they cannot be fabricated.
6. **Human Escalation** -- A curated directory routes users to verified human contacts (university ISSS office, student legal services, government helplines). Escalation is always available and auto-triggered on high-stakes topics.

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| UI | Streamlit | Fast to build, clean demoable interface |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Runs locally, no API key, no data leaves the machine |
| Generation | Groq API -- Llama 3.3 70B | Free tier, strong instruction-following |
| Corpus | JSON | 13 verified passages from official sources |
| Escalation | JSON | Curated human contacts mapped by journey |
| Runtime | Python | NumPy, python-dotenv |

All tools and services used are free. No paid APIs. No credit card required.

## Data Sources

All data is publicly available and officially published. No scraping. No synthetic data. Every passage was manually verified.

**Corpus sources include:** Chase, Bank of America, Social Security Administration, Department of Homeland Security (Study in the States), Texas Department of Public Safety, Federal Student Aid, USDA Food and Nutrition Service, and UNT university offices (International Affairs, Student Affairs, Student Money Management Center).

**Escalation contacts:** UNT International Student and Scholar Services, UNT Student Legal Services, UNT Dean of Students Office.

## Project Structure

```
clarity-app/
  app.py                          Main Streamlit application
  config.py                       Thresholds, model config, journeys, paths
  requirements.txt                Python dependencies
  data/
    corpus.json                   Curated verified passages
    escalation_directory.json     Human contact directory
  engine/
    intake.py                     Journey selection and intake questions
    retrieval.py                  Embedding, scoring, threshold gate
    generate.py                   Grounded generation via Groq
    checklist.py                  Step formatting with source metadata
    escalation.py                 High-stakes detection and contact lookup
  prompts/
    system_grounding.txt          System prompt for strict grounding
```

## Responsible AI

- Answers only from curated official sources. Never uses the model's general knowledge.
- Cites the source name, URL, and last-verified date on every claim.
- Abstains and escalates when retrieval confidence is below threshold.
- Auto-escalates on high-stakes topics (immigration, legal, financial).
- Collects no personal data. Intake answers exist only in the current session.
- Explicitly states it is not legal, immigration, or financial advice.

## License

This project was built for the USAII Global AI Hackathon 2026.
