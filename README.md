# AI System Risk & Compliance Classifier

A first-pass triage tool for classifying AI systems under the EU AI Act's
four risk tiers — **prohibited**, **high-risk**, **limited-risk**, or
**minimal-risk** — with a generated one-page "Risk Card" PDF summarizing the
classification, reasoning, and required documentation.

**This tool is not legal advice.** It is a fast, structured starting point
for compliance officers, product managers, engineers, and legal teams to
triage an AI system before involving qualified legal counsel. See
[Limitations](#limitations) below.

---

## Business problem

Companies deploying AI in the EU must classify each system under the EU AI
Act's risk tiers, because obligations differ sharply by tier — a
high-risk system requires a full conformity assessment, technical
documentation, and registration in an EU database; a minimal-risk system
requires nothing. Most teams don't have someone who understands both the
legal text and the technical system well enough to classify quickly and
correctly. Getting it wrong means either over-compliance (wasted
engineering and legal effort) or under-compliance (real legal and
financial risk — fines up to €35M or 7% of global turnover for the most
serious violations).

## Target users

Compliance officers, product managers, engineers, and legal teams at
companies building or buying AI in the EU. Strong fit for AI risk/audit
advisory firms (e.g. KPMG) and policy-adjacent research organizations
(e.g. TNO).

## Assumptions & scope

- **First-pass triage only, not legal advice** — stated explicitly here
  and in the tool's own PDF output.
- Covers Annex III high-risk categories, Article 5 prohibited practices,
  and Article 50 transparency obligations.
- Does not cover Annex I product-embedded systems (e.g. AI as a safety
  component in machinery, medical devices, toys) in depth.
- English input only in this version.
- Reflects Regulation (EU) 2024/1689 as currently in force. A "Digital
  Omnibus on AI" simplification package reached provisional political
  agreement in May 2026 but was not yet formally adopted as of this
  writing — see [eur-lex.europa.eu](https://eur-lex.europa.eu) for the
  authoritative, up-to-date text.

## Tech stack

- Python 3.10+
- Google Gemini (`gemini-2.5-flash`, free tier via [AI Studio](https://aistudio.google.com/apikey))
- Streamlit (UI)
- reportlab (PDF generation)

## System architecture

```
User description (Streamlit text input)
        │
        ▼
Prompt builder (src/prompt.py)
  — embeds condensed Annex III / Article 5 / Article 50 cheat-sheet
  — embeds 6 few-shot examples covering all 4 tiers + edge cases
        │
        ▼
Gemini API call (src/classifier.py)
  — low temperature (0.1) for repeatable classification
  — strict JSON schema, validated + retried on parse failure
        │
        ▼
Structured result: tier, confidence, article/annex, reasoning,
documentation checklist, borderline flag
        │
        ▼
Streamlit display  +  PDF "Risk Card" (src/pdf_generator.py)
```

## Sample input & output

**Input:** "An AI tool that scans job applicants' CVs and ranks them for
recruiters."

**Output:**
- **Tier:** High-risk
- **Article/Annex:** Annex III(4) — Employment, recruitment and selection
- **Reasoning:** CV screening and candidate ranking falls under Annex III
  point 4, which covers AI used to screen or filter job applications and
  evaluate candidates. This materially influences hiring outcomes.
- **Documentation checklist:** risk management system (Art 9), technical
  documentation (Art 11/Annex IV), logging (Art 12), transparency (Art
  13), human oversight (Art 14), conformity assessment, EU database
  registration.
- **PDF:** see `/examples`

## Prompt design

The system prompt (`src/prompt.py`) embeds a condensed summary of Annex
III categories, Article 5 prohibitions, and Article 50 transparency
triggers (`src/legal_reference.py`), plus explicit step-by-step
classification logic (check prohibitions first, then Annex III, then
Article 50, else minimal-risk). Six few-shot examples cover all four
tiers, including one deliberately borderline case, to reduce
misclassification and demonstrate the expected reasoning style. The model
is instructed to return strict JSON matching a fixed schema and to flag
ambiguous cases as `borderline: true` rather than answering confidently.

## Evaluation & testing

16 hand-written test system descriptions span all four risk tiers, plus
two deliberately ambiguous edge cases designed to probe over- and
under-triggering (see `tests/test_cases.py`). `tests/run_tests.py` runs
every case through the live classifier and writes a scored report to
`tests/accuracy_report.md`.

**Result: `<FILL IN AFTER RUNNING tests/run_tests.py>`**

<!-- e.g. "14/16 correct (88%). 2 borderline cases documented — see
tests/accuracy_report.md for full reasoning on every case, including
misses." -->

## Limitations

- LLM classification is not a legal verdict; it may misjudge ambiguous or
  novel use cases the few-shot examples didn't anticipate.
- Does not account for jurisdiction-specific national overlays or sector
  regulators (e.g. financial services supervisors may impose additional
  requirements beyond the AI Act).
- Depends entirely on the user's description being accurate and complete
  — omitted context (e.g. "who is affected," "is this workplace or
  consumer-facing") can flip the correct tier.
- English input only; no support yet for document upload or multi-turn
  clarifying questions.
- Reflects the Act as currently in force; does not track the pending
  Digital Omnibus simplification package.

## Future improvements

- Dutch-language input support.
- Clarifying follow-up questions for ambiguous descriptions instead of a
  single-shot classification.
- Document upload instead of free-text description only.
- A numeric confidence score (not just high/medium/low) to better rank
  borderline cases for human review.

## Repository structure

```
ai-risk-classifier/
├── src/
│   ├── legal_reference.py   # condensed Annex III / Art 5 / Art 50 text
│   ├── prompt.py             # system prompt + few-shot examples
│   ├── classifier.py         # Gemini API wrapper + JSON validation
│   ├── pdf_generator.py      # Risk Card PDF generation
│   └── app.py                 # Streamlit UI
├── tests/
│   ├── test_cases.py         # 16 hand-written test descriptions
│   ├── run_tests.py          # scores classifier against test_cases.py
│   └── accuracy_report.md    # generated by run_tests.py
├── examples/                  # sample Risk Card PDFs
├── requirements.txt
├── .env.example
└── README.md
```

## Running locally

```bash
git clone <your-repo-url>
cd ai-risk-classifier
pip install -r requirements.txt

cp .env.example .env
# edit .env and paste your free Gemini API key from https://aistudio.google.com/apikey

export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d '=' -f2)
cd src
streamlit run app.py
```

To run the test suite and regenerate the accuracy report:

```bash
cd tests
python run_tests.py
```

## Live deployment

**[ai-risk-classifier.streamlit.app](https://ai-risk-classifier.streamlit.app/)**

## Demo video

`<FILL IN — 2-minute screen recording link, running 3 example descriptions
through the tool and showing the generated Risk Card PDF for each>`

## Data

- EU AI Act text: free and public at
  [eur-lex.europa.eu](https://eur-lex.europa.eu), CELEX 32024R1689.
- Test descriptions: fully synthetic, self-written, no real data used.

## Disclaimer

This tool provides an automated first-pass classification and does not
constitute legal advice. It may be incomplete, out of date, or incorrect,
particularly for ambiguous or novel use cases. Consult qualified legal
counsel before relying on any classification for compliance purposes.
