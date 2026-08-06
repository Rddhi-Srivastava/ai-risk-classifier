"""
Streamlit UI for the AI System Risk & Compliance Classifier.

Run with:
    streamlit run app.py
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from classifier import ClassificationError, classify_system
from pdf_generator import generate_risk_card

st.set_page_config(
    page_title="AI System Risk & Compliance Classifier",
    page_icon="\u2696\ufe0f",
    layout="centered",
)

TIER_COLORS = {
    "prohibited": "#7A1F2B",
    "high-risk": "#C0392B",
    "limited-risk": "#C77D14",
    "minimal-risk": "#1E8449",
}

TIER_LABELS = {
    "prohibited": "PROHIBITED \u2014 Unacceptable Risk",
    "high-risk": "HIGH-RISK",
    "limited-risk": "LIMITED-RISK",
    "minimal-risk": "MINIMAL-RISK",
}

EXAMPLES = [
    "An AI tool that scans job applicants' CVs and ranks them for recruiters.",
    "A chatbot on our e-commerce website that answers questions about order status.",
    "A system that monitors employees' facial expressions to flag 'disengagement' to managers.",
    "An internal tool that forecasts which warehouse items will run low on stock.",
]

st.title("\u2696\ufe0f AI System Risk & Compliance Classifier")
st.caption(
    "First-pass EU AI Act risk-tier triage. **Not legal advice** \u2014 a fast, "
    "structured starting point for compliance officers, PMs, and engineers."
)

if not os.environ.get("GEMINI_API_KEY"):
    st.warning(
        "No `GEMINI_API_KEY` found in the environment. Set it before running "
        "(see the README) or classification calls will fail.",
        icon="\u26a0\ufe0f",
    )

with st.expander("Try an example instead"):
    cols = st.columns(2)
    for i, example in enumerate(EXAMPLES):
        if cols[i % 2].button(example, key=f"example_{i}", use_container_width=True):
            st.session_state["description_input"] = example

description = st.text_area(
    "Describe the AI system",
    key="description_input",
    height=120,
    placeholder=(
        "e.g. An AI tool that scans job applicants' CVs and ranks them for recruiters."
    ),
)

classify_clicked = st.button("Classify system", type="primary", use_container_width=True)

if classify_clicked:
    if not description.strip():
        st.error("Please enter a system description first.")
    else:
        with st.spinner("Classifying against the EU AI Act..."):
            try:
                result = classify_system(description)
                st.session_state["last_result"] = result
            except ClassificationError as e:
                st.session_state["last_result"] = None
                st.error(f"Classification failed: {e}")

result = st.session_state.get("last_result")

if result:
    tier_color = TIER_COLORS.get(result.tier, "#666666")
    tier_label = TIER_LABELS.get(result.tier, result.tier.upper())

    st.markdown(
        f"""
        <div style="background-color:{tier_color}; color:white; padding:14px 18px;
                    border-radius:6px; font-weight:700; font-size:1.1rem; margin-top:1rem;">
            {tier_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    meta_cols = st.columns(2)
    meta_cols[0].metric("Confidence", result.confidence.capitalize())
    meta_cols[1].metric(
        "Review flag",
        "\u26a0\ufe0f Borderline" if result.borderline else "None",
    )

    st.subheader("Applicable Article / Annex")
    st.write(result.primary_article_or_annex)

    st.subheader("Reasoning")
    st.write(result.reasoning)

    if result.borderline and result.borderline_note:
        st.subheader("Borderline Note")
        st.info(result.borderline_note)

    st.subheader("Documentation Checklist")
    for item in result.documentation_checklist:
        st.markdown(f"- {item}")

    st.divider()

    pdf_bytes = generate_risk_card(result)
    st.download_button(
        label="\U0001f4c4 Download Risk Card (PDF)",
        data=pdf_bytes,
        file_name="ai_risk_card.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.caption(
        "This is an automated first-pass triage only and does not constitute "
        "legal advice. Confirm any consequential classification with qualified "
        "legal counsel."
    )
