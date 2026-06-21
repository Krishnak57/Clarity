"""Retrieval over the curated corpus — the heart of anti-hallucination.

Loads corpus.json, embeds each chunk locally with sentence-transformers, and
scores a query by cosine similarity. Returns the top chunks AND the top score so
the caller can apply the threshold gate (abstain when nothing is relevant).

For ~20 docs this is instant and needs no vector DB. Simple is correct here.
"""
import json
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

import config


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    """Load the local embedding model once (cached)."""
    return SentenceTransformer(config.EMBEDDING_MODEL)


def load_corpus() -> list[dict]:
    with open(config.CORPUS_PATH, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _index() -> tuple[list[dict], np.ndarray]:
    """Embed every corpus chunk once. Returns (chunks, normalized_embeddings)."""
    chunks = load_corpus()
    texts = [c["text"] for c in chunks]
    emb = _model().encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return chunks, emb


def retrieve(query: str, journey: str | None = None, top_n: int | None = None) -> dict:
    """Return the most relevant chunks for a query.

    Args:
        query: the user's question (optionally combined with intake context).
        journey: if set, restrict to chunks for that journey.
        top_n: number of chunks to return (defaults to config.TOP_N).

    Returns a dict:
        {
          "top_score": float,                 # best cosine similarity (0..1)
          "abstain": bool,                    # True if top_score < threshold
          "chunks": [ {..chunk.., "score": float}, ... ]  # top_n, score-sorted
        }
    """
    top_n = top_n or config.TOP_N
    chunks, emb = _index()

    # Optional journey filter.
    if journey:
        mask = [i for i, c in enumerate(chunks) if c.get("journey") == journey]
        if mask:
            chunks = [chunks[i] for i in mask]
            emb = emb[mask]

    if not chunks:
        return {"top_score": 0.0, "abstain": True, "chunks": []}

    q = _model().encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
    scores = emb @ q  # cosine similarity (vectors are normalized)

    order = np.argsort(scores)[::-1][:top_n]
    top_chunks = []
    for i in order:
        c = dict(chunks[i])
        c["score"] = float(scores[i])
        top_chunks.append(c)

    top_score = float(scores[order[0]])
    return {
        "top_score": top_score,
        "abstain": top_score < config.RETRIEVAL_THRESHOLD,
        "chunks": top_chunks,
    }


if __name__ == "__main__":
    # Quick sanity check: print top score + chunks for a few queries.
    tests = [
        ("How do I open a bank account as an F-1 student?", "A_bank_account"),
        ("Can I get an SSN?", "B_ssn_dl"),
        ("What is the capital of France?", None),  # should abstain
    ]
    for q, j in tests:
        r = retrieve(q, journey=j)
        print(f"\nQ: {q}  (journey={j})")
        print(f"   top_score={r['top_score']:.3f}  abstain={r['abstain']}")
        for c in r["chunks"]:
            print(f"   - [{c['id']}] {c['score']:.3f}  {c['source_name']}")
