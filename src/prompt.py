"""
Prompt construction for the AI System Risk & Compliance Classifier.
"""

from legal_reference import FULL_CHEAT_SHEET

SYSTEM_PROMPT = f"""You are a first-pass EU AI Act risk-tier triage assistant.
You are NOT a lawyer and this is NOT legal advice. Your job is to give a
compliance officer, PM, or engineer a fast, structured, defensible starting
point for classifying an AI system under the EU AI Act's four risk tiers:
prohibited, high-risk, limited-risk, or minimal-risk.

Use ONLY the reference material below (a condensed summary of Regulation
(EU) 2024/1689) to reason about the classification. If a description is
ambiguous or missing key facts, say so explicitly in your reasoning and
choose the more cautious (higher-risk) tier, flagging it as borderline.

{FULL_CHEAT_SHEET}

CLASSIFICATION LOGIC (apply in this order):
1. Check Article 5 first. If the system matches a prohibited practice ->
   tier = "prohibited", regardless of anything else.
2. If not prohibited, check Annex III. If it matches a high-risk use case
   AND plausibly poses significant risk to health/safety/fundamental
   rights -> tier = "high-risk".
3. If not high-risk, check Article 50. If it triggers a transparency
   obligation (chatbot, deepfake, AI-generated public content, emotion
   recognition/biometric categorisation not otherwise prohibited) ->
   tier = "limited-risk".
4. Otherwise -> tier = "minimal-risk".

OUTPUT FORMAT: Respond with ONLY valid JSON, no markdown fences, no
preamble, matching exactly this schema:

{{
  "tier": "prohibited" | "high-risk" | "limited-risk" | "minimal-risk",
  "confidence": "high" | "medium" | "low",
  "primary_article_or_annex": "<e.g. 'Annex III(4) - Employment' or 'Article 5(1)(c)'>",
  "reasoning": "<2-4 sentences explaining the classification, referencing the specific category/article>",
  "documentation_checklist": ["<item 1>", "<item 2>", "..."],
  "borderline": true | false,
  "borderline_note": "<if borderline is true, explain the ambiguity in 1-2 sentences; else empty string>"
}}

The documentation_checklist should list the main obligations/documents
relevant to that tier (e.g. for high-risk: risk management system (Art 9),
technical documentation (Art 11/Annex IV), logging (Art 12), human
oversight (Art 14), conformity assessment, registration in EU database.
For limited-risk: transparency/disclosure statement. For minimal-risk:
none required, optional voluntary code of conduct. For prohibited: cease
development/deployment, no compliance path exists).
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "A chatbot on our e-commerce website that answers customer questions about order status and returns.",
        "output": {
            "tier": "limited-risk",
            "confidence": "high",
            "primary_article_or_annex": "Article 50(1) - Transparency for direct interaction",
            "reasoning": "The system interacts directly with natural persons and does not fall into any Annex III category or Article 5 prohibition. It only triggers the Article 50 obligation to disclose that users are interacting with an AI system.",
            "documentation_checklist": [
                "Clear disclosure that the chatbot is an AI system",
                "Disclosure should be obvious at first interaction, unless already obvious from context",
            ],
            "borderline": False,
            "borderline_note": "",
        },
    },
    {
        "input": "An AI tool that scans job applicants' CVs and ranks them for recruiters.",
        "output": {
            "tier": "high-risk",
            "confidence": "high",
            "primary_article_or_annex": "Annex III(4) - Employment, recruitment and selection",
            "reasoning": "CV screening and candidate ranking falls squarely under Annex III point 4 (employment/recruitment), which covers AI used to screen or filter job applications and evaluate candidates. This materially influences hiring outcomes, so the significant-risk threshold in Article 6(3) is met.",
            "documentation_checklist": [
                "Risk management system (Article 9)",
                "Technical documentation (Article 11, Annex IV)",
                "Record-keeping / logging (Article 12)",
                "Transparency to candidates (Article 13)",
                "Human oversight measures (Article 14)",
                "Conformity assessment and CE marking",
                "Registration in the EU high-risk AI database",
            ],
            "borderline": False,
            "borderline_note": "",
        },
    },
    {
        "input": "An automated system used by a bank to decide whether to approve or deny personal loan applications.",
        "output": {
            "tier": "high-risk",
            "confidence": "high",
            "primary_article_or_annex": "Annex III(5) - Access to essential private services, creditworthiness",
            "reasoning": "Credit scoring and creditworthiness assessment for individuals is explicitly listed under Annex III point 5 (access to essential private services). It directly determines access to a financial service, meeting the significant-risk bar.",
            "documentation_checklist": [
                "Risk management system (Article 9)",
                "Technical documentation (Article 11, Annex IV)",
                "Record-keeping / logging (Article 12)",
                "Transparency to applicants (Article 13)",
                "Human oversight measures (Article 14)",
                "Conformity assessment and CE marking",
                "Registration in the EU high-risk AI database",
            ],
            "borderline": False,
            "borderline_note": "",
        },
    },
    {
        "input": "An internal tool that uses AI to forecast which warehouse items will run low on stock next month.",
        "output": {
            "tier": "minimal-risk",
            "confidence": "high",
            "primary_article_or_annex": "None - outside Annex III, Article 5, and Article 50",
            "reasoning": "Inventory forecasting does not affect any individual's fundamental rights, safety, or access to services, and does not fall into any Annex III category or trigger a transparency obligation. No mandatory obligations apply.",
            "documentation_checklist": [
                "No mandatory documentation required",
                "Optional: adopt a voluntary code of conduct (Article 95)",
            ],
            "borderline": False,
            "borderline_note": "",
        },
    },
    {
        "input": "A system that monitors employees' facial expressions and tone of voice during work hours to flag 'disengagement' to managers.",
        "output": {
            "tier": "prohibited",
            "confidence": "high",
            "primary_article_or_annex": "Article 5(1)(f) - Emotion recognition in the workplace",
            "reasoning": "This is emotion recognition deployed in the workplace, which Article 5(1)(f) prohibits outright, absent a narrow medical or safety exception. No conformity assessment route exists to make this compliant.",
            "documentation_checklist": [
                "No compliance path exists - system must not be placed on the market or put into service",
                "Cease development/deployment or redesign entirely to remove emotion recognition",
            ],
            "borderline": False,
            "borderline_note": "",
        },
    },
    {
        "input": "A tool that uses AI to summarize long legal contracts into plain-language bullet points for internal staff.",
        "output": {
            "tier": "minimal-risk",
            "confidence": "medium",
            "primary_article_or_annex": "None - outside Annex III, Article 5, and Article 50",
            "reasoning": "Contract summarization for internal use does not fall into an Annex III category (it does not itself administer justice or apply law to facts on behalf of a court) and doesn't interact directly with external end-users in a way that triggers Article 50.",
            "documentation_checklist": [
                "No mandatory documentation required",
                "Optional: adopt a voluntary code of conduct (Article 95)",
            ],
            "borderline": True,
            "borderline_note": "If outputs were used to assist a court or tribunal in researching/interpreting facts or law (Annex III point 8), this would shift to high-risk. Confirm the actual deployment context.",
        },
    },
]


def build_user_message(system_description: str) -> str:
    """Builds the user-turn message containing few-shot examples + the real query."""
    examples_text = ""
    for ex in FEW_SHOT_EXAMPLES:
        import json

        examples_text += f"\nExample input: {ex['input']}\nExample output: {json.dumps(ex['output'])}\n"

    return f"""Here are examples of correctly classified systems:
{examples_text}

Now classify this system. Respond with ONLY the JSON object, nothing else.

System description: {system_description}
"""
