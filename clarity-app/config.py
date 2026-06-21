"""Central config for Clarity. Tune thresholds and model here — nothing hardcoded elsewhere."""
import os
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"
CORPUS_PATH = DATA_DIR / "corpus.json"
ESCALATION_PATH = DATA_DIR / "escalation_directory.json"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_grounding.txt"

# --- Retrieval ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # local sentence-transformers, free, no API key
TOP_N = 4                              # passages to retrieve
# Threshold gate: if the best cosine score is below this, ABSTAIN (do not generate).
# Tuned in Step 2 against the real corpus. MiniLM cosine for a relevant hit is usually > ~0.35.
RETRIEVAL_THRESHOLD = 0.35

# --- Generation (Groq free tier) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
LLM_TEMPERATURE = 0.0                  # deterministic: we want faithful extraction, not creativity

# --- Escalation ---
# Topics that ALWAYS append a human escalation, even when we can answer.
HIGH_STAKES_KEYWORDS = [
    "visa", "status", "immigration", "uscis", "deport", "out of status",
    "legal", "lawyer", "attorney", "public charge", "sevis", "i-20",
    "work authorization", "opt", "cpt", "unauthorized",
]

# Journeys offered to the user.
JOURNEYS = {
    "A_bank_account": "Open a US bank account",
    "B_ssn_dl": "Get an SSN and/or Texas driver's license",
    "C_benefits": "What support am I eligible for?",
}
