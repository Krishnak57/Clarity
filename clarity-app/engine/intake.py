"""Intake — journey selection + a few short, plain-language questions.

Goal: turn a vague question into a precise one by collecting the variables that
change the answer (visa type, state, what the user already has). A fixed question
set per journey is intentional: it is more reliable and demos better than a
free-form AI conversation.
"""

# A short, fixed question set per journey. Each question is plain language.
INTAKE_QUESTIONS = {
    "A_bank_account": [
        {"key": "has_ssn", "label": "Do you already have a Social Security Number (SSN)?",
         "options": ["No", "Yes"]},
        {"key": "has_address", "label": "Do you have a US address yet?",
         "options": ["Yes", "Not yet"]},
    ],
    "B_ssn_dl": [
        {"key": "goal", "label": "Which do you need?",
         "options": ["SSN", "Texas driver's license", "Both"]},
        {"key": "has_job", "label": "Do you have a job offer or work authorization (on-campus job, CPT, or OPT)?",
         "options": ["No", "Yes"]},
    ],
    "C_benefits": [
        {"key": "need", "label": "What are you looking for?",
         "options": ["Health insurance", "Emergency money / hardship help", "Food resources", "General eligibility"]},
    ],
}


def questions_for(journey: str) -> list[dict]:
    return INTAKE_QUESTIONS.get(journey, [])


def build_situation(journey_label: str, question: str, answers: dict[str, str]) -> str:
    """Combine the journey, intake answers, and the user's question into one
    situation string used for both retrieval and generation."""
    parts = ["I am an F-1 international student in Texas."]
    parts.append(f"Goal: {journey_label}.")
    for k, v in answers.items():
        if v:
            parts.append(f"{k}: {v}.")
    if question:
        parts.append(f"My question: {question}")
    return " ".join(parts)
