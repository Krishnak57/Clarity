# Clarity — Project Folder (START HERE)

> **Working product name:** Clarity *(placeholder — rename freely. Alternatives: Landing, Northstar, Wayfinder, FirstSteps.)*
>
> **One line:** Plain-language answers to real-world rules and benefits — sourced from official websites, honest about what it doesn't know, and built to hand you to a real human when the stakes are high.
>
> **Event:** USAII Global AI Hackathon 2026 · Undergraduate Track (AI for Life & Work) · **Brief 4 — Public Services · Direction A: Benefits Navigator**
> **Deadline:** June 21, 11:59 PM ET · Submit via Devpost

---

## What this folder is

This is the complete brain of the project. Every document Cowork needs to understand the idea and build the MVP is here, plus every document needed to submit to the hackathon.

## How to use this folder (read in this order)

| File | What it is | Who it's for |
|------|-----------|--------------|
| `README.md` | This file — index + the prompt to start Cowork | You |
| `01_PROJECT_BRIEF.md` | The problem, the user, the vision, the scope, the wedge | You + Cowork |
| `02_SYSTEM_DESIGN.md` | Architecture, the anti-hallucination pipeline, tech stack | Cowork |
| `03_BUILD_PLAN.md` | The exact build order, MVP scope, file structure, acceptance criteria | Cowork |
| `04_CONTENT_CORPUS.md` | The knowledge base: which official sources to gather + the escalation directory | You + Cowork |
| `05_DEVPOST_SUBMISSION.md` | Every required Devpost field, pre-written and ready to paste | You |
| `06_DEMO_SCRIPT.md` | The 2–5 min video script + the "winning moment" | You |

## The golden rule of this project

**The system never makes up an answer.** It answers *only* from the curated official sources, shows the source on every answer, and when it isn't confident or the question is out of scope, it says so plainly and routes the person to the right human. The honesty *is* the product. Every design decision serves this rule.

## The prompt to start Cowork

Copy the block in `START_HERE_COWORK_PROMPT.txt` (also pasted in chat) into Claude Cowork once this folder is open. It tells Cowork to read everything here first, then build the MVP from `03_BUILD_PLAN.md` — and critically, to stop and verify real facts instead of inventing them.
