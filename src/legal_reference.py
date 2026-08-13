"""
Condensed EU AI Act reference material used inside the LLM prompt.

Source: Regulation (EU) 2024/1689 (OJ L, 12.7.2024), eur-lex.europa.eu, CELEX 32024R1689.
Last checked against source: August 2026.

IMPORTANT: This is a deliberately condensed, plain-language summary for a
first-pass triage tool. It is NOT a substitute for the authentic legal text.
A "Digital Omnibus on AI" simplification package reached provisional
political agreement in May 2026 but is not yet formally adopted; this
cheat-sheet reflects the currently binding text.
"""

ANNEX_III_CATEGORIES = """
ANNEX III - HIGH-RISK USE CASES (a system is high-risk if it falls into one
of these AND poses a significant risk of harm to health, safety, or
fundamental rights - Article 6(2)-(3)):

1. Biometrics: remote biometric identification (not for verification-only),
   biometric categorisation of sensitive traits, emotion recognition
   (outside the Article 5 outright bans in some contexts).
2. Critical infrastructure: AI used as a safety component in the management
   or operation of critical digital infrastructure, road traffic, or the
   supply of water, gas, heating, electricity.
3. Education & vocational training: AI determining access/admission,
   evaluating learning outcomes, assessing appropriate education level,
   monitoring/detecting prohibited student behaviour during tests.
4. Employment, worker management, self-employment access: AI for
   recruitment/candidate sourcing, screening or filtering applications,
   evaluating candidates, promotion/termination decisions, task allocation,
   monitoring or evaluating worker performance/behaviour.
5. Access to essential private/public services: creditworthiness/credit
   scoring, life/health insurance risk assessment and pricing, eligibility
   for public assistance benefits, emergency service dispatch prioritisation.
6. Law enforcement: AI assessing risk of offending/reoffending, evidence
   reliability assessment, profiling during detection/investigation.
7. Migration, asylum, border control: AI assessing security/irregular
   migration risk, examining asylum/visa applications, polygraph-like tools.
8. Administration of justice & democratic processes: AI assisting judicial
   research/interpretation/application of law to facts, AI influencing
   election or referendum outcomes or voting behaviour.
"""

ARTICLE_5_PROHIBITED = """
ARTICLE 5 - PROHIBITED PRACTICES (unacceptable risk, outright banned,
regardless of safeguards):

(a) Subliminal, manipulative, or deceptive techniques that materially
    distort behaviour and cause/are likely to cause significant harm.
(b) Exploiting vulnerabilities of a person/group due to age, disability, or
    a specific social/economic situation, distorting behaviour causing harm.
(c) Social scoring: evaluating/classifying people over time based on social
    behaviour or inferred/predicted personal traits, leading to detrimental
    treatment unrelated to the context in which the data was generated.
(d) Predicting an individual's risk of committing a criminal offence based
    solely on profiling or personality traits (no other supporting facts).
(e) Untargeted scraping of facial images from the internet or CCTV to build
    or expand facial recognition databases.
(f) Emotion recognition in the workplace or educational institutions
    (narrow medical/safety exceptions).
(g) Biometric categorisation to infer/deduce race, political opinions,
    trade union membership, religious/philosophical beliefs, sex life, or
    sexual orientation (narrow law-enforcement exceptions).
(h) Real-time remote biometric identification in publicly accessible spaces
    for law enforcement purposes (narrow, tightly-conditioned exceptions).
"""

ARTICLE_50_TRANSPARENCY = """
ARTICLE 50 - TRANSPARENCY OBLIGATIONS (limited-risk tier - disclosure
required, but not the full high-risk obligation set):

- Systems intended to interact directly with natural persons (e.g.
  chatbots) must inform the person they are interacting with an AI system,
  unless obvious from context.
- AI-generated or manipulated audio/image/video/text content ("deepfakes")
  must be disclosed as artificially generated/manipulated.
- Emotion recognition or biometric categorisation systems (where not
  otherwise prohibited) must inform exposed persons of the system's
  operation.
- AI-generated text published to inform the public on matters of public
  interest must be disclosed as AI-generated, unless human-reviewed with
  editorial responsibility.
"""

MINIMAL_RISK_NOTE = """
MINIMAL/NO RISK: Everything not captured above (e.g. spam filters,
AI-enabled video game NPCs, inventory-management recommenders, most
internal productivity tools) has no mandatory obligations under the Act,
though voluntary codes of conduct are encouraged (Article 95).
"""

FULL_CHEAT_SHEET = "\n".join(
    [ANNEX_III_CATEGORIES, ARTICLE_5_PROHIBITED, ARTICLE_50_TRANSPARENCY, MINIMAL_RISK_NOTE]
)
