"""Clarity — plain-language, source-cited answers for F-1 students in Texas.

Full pipeline: intake -> retrieval (with threshold gate) -> grounded generation
-> checklist -> human escalation. The system answers ONLY from the curated
corpus, cites the source + last-verified date on every step, and abstains +
escalates when retrieval confidence is low, the topic is out of scope, or the
stakes are high.
"""
import streamlit as st

import config
from engine import intake, retrieval, generate, checklist, escalation

st.set_page_config(page_title="Clarity", page_icon="🧭", layout="centered")

# Map labels <-> journey keys.
LABEL_TO_KEY = {v: k for k, v in config.JOURNEYS.items()}

# --- Header / founder story ---
st.title("🧭 Clarity")
st.caption(
    "Plain-language answers to real-world rules and benefits — sourced from "
    "official websites, honest about what it doesn't know, and built to hand you "
    "to a real human when the stakes are high."
)
with st.expander("Why this exists", expanded=False):
    st.write(
        "As an F-1 student, opening a bank account meant calling a dozen people, "
        "getting five different answers, and asking a chatbot that confidently made "
        "things up. Clarity only answers from official sources, shows you where each "
        "fact comes from, and sends you to a real person when it isn't sure."
    )


# --- Intake ---
st.subheader("1 · What do you need help with?")
journey_label = st.radio("Choose a journey:", list(config.JOURNEYS.values()), index=0)
journey_key = LABEL_TO_KEY[journey_label]

answers: dict[str, str] = {}
for q in intake.questions_for(journey_key):
    answers[q["key"]] = st.selectbox(q["label"], q["options"])

question = st.text_input(
    "2 · Your question:",
    placeholder="e.g. How do I open a bank account as an F-1 student?",
)

go = st.button("Get answer", type="primary")


def render_escalation(contacts: list[dict], reason: str = "", auto: bool = False):
    """Render the human-in-the-loop escalation block."""
    if auto:
        if reason == "low_confidence":
            st.warning(
                "I don't have a verified answer for that. I won't guess — here is "
                "the right person to ask:"
            )
        elif reason == "high_stakes":
            st.warning(
                "This touches your immigration status or a high-stakes decision. "
                "Confirm with a real human before you act:"
            )
    else:
        st.markdown("**👤 Talk to a real person about this:**")

    for c in contacts:
        st.markdown(
            f"- **{c['contact_name']}** _({c['contact_type']})_  \n"
            f"  {c['how_to_reach']}  \n"
            f"  _When to use: {c['when_to_use']}_"
        )


if go:
    st.divider()
    situation = intake.build_situation(journey_label, question, answers)

    with st.spinner("Checking official sources…"):
        result = retrieval.retrieve(situation, journey=journey_key)
        escalate, reason = escalation.should_escalate(result["abstain"], situation)
        contacts = escalation.contacts_for(journey_key, situation)

    # --- ABSTAIN path: low confidence / out of scope ---
    if result["abstain"]:
        st.subheader("Answer")
        render_escalation(contacts, reason="low_confidence", auto=True)
        st.caption(f"(retrieval confidence {result['top_score']:.2f} — below the "
                   f"{config.RETRIEVAL_THRESHOLD} threshold, so Clarity does not generate an answer)")
        st.stop()

    # --- ANSWER path: grounded generation + checklist ---
    with st.spinner("Writing a plain-language, sourced answer…"):
        structured = generate.generate_structured(situation, result["chunks"])

    if not structured.get("answerable") or not structured.get("steps"):
        # The model itself found the passages insufficient — abstain honestly.
        st.subheader("Answer")
        render_escalation(contacts, reason="low_confidence", auto=True)
        st.stop()

    high_stakes = escalation.is_high_stakes(situation)
    steps = checklist.build_checklist(structured, result["chunks"], high_stakes)

    st.subheader("Answer")
    if structured.get("summary"):
        st.write(structured["summary"])

    st.markdown("#### Your checklist")
    for s in steps:
        with st.container(border=True):
            st.markdown(f"**{s['order']}. {s['action']}**")
            if s["documents"]:
                st.markdown("Documents / items: " + ", ".join(f"`{d}`" for d in s["documents"]))
            cols = st.columns([3, 2])
            with cols[0]:
                if s["source_url"]:
                    st.markdown(f"🔗 [{s['source_name']}]({s['source_url']})")
                else:
                    st.markdown(f"Source: {s['source_name']}")
                st.caption(f"Last verified: {s['last_verified_date']}")
            with cols[1]:
                st.markdown(checklist.confidence_badge(s["confidence"]))

    st.caption(
        "Clarity is not legal, immigration, or financial advice. It explains what "
        "official sources say. For any judgment call, confirm with the human contact below."
    )

    st.divider()
    # Escalation is ALWAYS offered; auto-surfaced (warning style) when high-stakes.
    render_escalation(contacts, reason="high_stakes", auto=high_stakes)
