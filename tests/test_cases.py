"""
Manually curated test set spanning all four EU AI Act risk tiers, including
a few deliberately ambiguous/borderline cases.

expected_tier is the author's own reading of the Act (see README for the
"evaluation & testing" methodology section) - not a legal determination.
"""

TEST_CASES = [
    # --- Prohibited ---
    {
        "id": "P1",
        "description": "A system that monitors employees' facial expressions and tone of voice during work hours to flag 'disengagement' to managers.",
        "expected_tier": "prohibited",
        "notes": "Article 5(1)(f) - emotion recognition in the workplace.",
    },
    {
        "id": "P2",
        "description": "A mobile app for a retail chain that scores each customer's 'trustworthiness' based on unrelated social media activity, purchase history, and neighborhood, and uses that score to decide who gets refused service.",
        "expected_tier": "prohibited",
        "notes": "Article 5(1)(c) - social scoring leading to detrimental treatment unrelated to context.",
    },
    {
        "id": "P3",
        "description": "A government pilot that predicts which individuals are likely to commit a crime in the next year based purely on their personality profile and demographic data, with no other supporting evidence.",
        "expected_tier": "prohibited",
        "notes": "Article 5(1)(d) - individual criminal risk prediction based solely on profiling.",
    },
    # --- High-risk ---
    {
        "id": "H1",
        "description": "An AI tool that scans job applicants' CVs and ranks them for recruiters.",
        "expected_tier": "high-risk",
        "notes": "Annex III(4) - employment/recruitment.",
    },
    {
        "id": "H2",
        "description": "An automated system used by a bank to decide whether to approve or deny personal loan applications.",
        "expected_tier": "high-risk",
        "notes": "Annex III(5) - creditworthiness assessment.",
    },
    {
        "id": "H3",
        "description": "Software used by a university admissions office to automatically score and rank applicants for a limited number of spots.",
        "expected_tier": "high-risk",
        "notes": "Annex III(3) - education, access/admission decisions.",
    },
    {
        "id": "H4",
        "description": "A tool used by a national employment agency to determine which unemployed citizens are eligible for continued benefit payments.",
        "expected_tier": "high-risk",
        "notes": "Annex III(5) - eligibility for public assistance benefits.",
    },
    {
        "id": "H5",
        "description": "An AI system used by police to assess the reliability of evidence gathered during a criminal investigation.",
        "expected_tier": "high-risk",
        "notes": "Annex III(6) - law enforcement, evidence reliability assessment.",
    },
    # --- Limited-risk ---
    {
        "id": "L1",
        "description": "A chatbot on our e-commerce website that answers customer questions about order status and returns.",
        "expected_tier": "limited-risk",
        "notes": "Article 50(1) - direct interaction disclosure.",
    },
    {
        "id": "L2",
        "description": "A marketing tool that generates realistic AI images of people using our products for social media ads.",
        "expected_tier": "limited-risk",
        "notes": "Article 50(4) - AI-generated/manipulated image content disclosure.",
    },
    {
        "id": "L3",
        "description": "A news aggregator that uses AI to auto-generate short article summaries for a public-interest news site, without any human editorial review before publishing.",
        "expected_tier": "limited-risk",
        "notes": "Article 50(4) - AI-generated public-interest text disclosure (no human editorial responsibility).",
    },
    # --- Minimal-risk ---
    {
        "id": "M1",
        "description": "An internal tool that uses AI to forecast which warehouse items will run low on stock next month.",
        "expected_tier": "minimal-risk",
        "notes": "No Annex III/Article 5/Article 50 trigger.",
    },
    {
        "id": "M2",
        "description": "An AI-powered spam filter for our company email inboxes.",
        "expected_tier": "minimal-risk",
        "notes": "No Annex III/Article 5/Article 50 trigger.",
    },
    {
        "id": "M3",
        "description": "A video game NPC that uses AI to generate dynamic dialogue responses to the player.",
        "expected_tier": "minimal-risk",
        "notes": "No Annex III/Article 5/Article 50 trigger (and typically exempt as R&D/entertainment context besides).",
    },
    # --- Deliberately ambiguous / borderline ---
    {
        "id": "B1",
        "description": "A tool that uses AI to summarize long legal contracts into plain-language bullet points for internal staff.",
        "expected_tier": "minimal-risk",
        "notes": "Borderline: could look like Annex III(8) justice-adjacent, but internal contract summarization for staff (not assisting a court) is minimal-risk. Good test of over-triggering.",
    },
    {
        "id": "B2",
        "description": "A customer support voice assistant that also silently analyzes callers' vocal tone to estimate their emotional state and logs it for quality-assurance review.",
        "expected_tier": "ambiguous",
        "notes": (
            "Deliberately ambiguous: emotion recognition on customers (not "
            "workplace/education) isn't Article 5(1)(f) prohibited, but it "
            "should trigger an Article 50(3) transparency obligation "
            "(limited-risk) at minimum, and the 'silently' framing raises a "
            "fairness/consent flag worth a human looking at. No single tier "
            "is clearly 'the' right answer - the pass condition is that the "
            "tool flags this as borderline rather than answering confidently."
        ),
    },
]
