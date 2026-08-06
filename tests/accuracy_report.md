# Accuracy Report

**14/15 correct (93%)**

First-pass triage test against a hand-written test set spanning all four
EU AI Act risk tiers, including two deliberately ambiguous edge cases.

| ID | Expected | Got | Pass | Notes |
|----|----------|-----|------|-------|
| P1 | prohibited | prohibited | ✅ | Article 5(1)(f) - emotion recognition in the workplace. |
| P2 | prohibited | prohibited | ✅ | Article 5(1)(c) - social scoring leading to detrimental treatment unrelated to context. |
| P3 | prohibited | prohibited | ✅ | Article 5(1)(d) - individual criminal risk prediction based solely on profiling. |
| H1 | high-risk | ERROR | ❌ | Annex III(4) - employment/recruitment. |
| H2 | high-risk | high-risk | ✅ | Annex III(5) - creditworthiness assessment. |
| H3 | high-risk | high-risk | ✅ | Annex III(3) - education, access/admission decisions. |
| H4 | high-risk | high-risk | ✅ | Annex III(5) - eligibility for public assistance benefits. |
| H5 | high-risk | high-risk | ✅ | Annex III(6) - law enforcement, evidence reliability assessment. |
| L1 | limited-risk | limited-risk | ✅ | Article 50(1) - direct interaction disclosure. |
| L2 | limited-risk | limited-risk | ✅ | Article 50(4) - AI-generated/manipulated image content disclosure. |
| L3 | limited-risk | limited-risk | ✅ | Article 50(4) - AI-generated public-interest text disclosure (no human editorial responsibility). |
| M1 | minimal-risk | minimal-risk | ✅ | No Annex III/Article 5/Article 50 trigger. |
| M2 | minimal-risk | minimal-risk | ✅ | No Annex III/Article 5/Article 50 trigger. |
| M3 | minimal-risk | minimal-risk | ✅ | No Annex III/Article 5/Article 50 trigger (and typically exempt as R&D/entertainment context besides). |
| B1 | minimal-risk | minimal-risk | ✅ | Borderline: could look like Annex III(8) justice-adjacent, but internal contract summarization for staff (not assisting a court) is minimal-risk. Good test of over-triggering. |
| B2 | ambiguous | prohibited | ❌ | Deliberately ambiguous: emotion recognition on customers (not workplace/education) isn't Article 5(1)(f) prohibited, but it should trigger an Article 50(3) transparency obligation (limited-risk) at minimum, and the 'silently' framing raises a fairness/consent flag worth a human looking at. No single tier is clearly 'the' right answer - the pass condition is that the tool flags this as borderline rather than answering confidently. |

## Full descriptions and model reasoning

### P1 (PASS)
- **Description:** A system that monitors employees' facial expressions and tone of voice during work hours to flag 'disengagement' to managers.
- **Expected tier:** prohibited
- **Model tier:** prohibited
- **Model reasoning:** This system uses AI for emotion recognition in the workplace, which is explicitly prohibited under Article 5(1)(f) of the EU AI Act, unless very narrow exceptions for medical or safety purposes apply. As described, it does not meet these exceptions.

### P2 (PASS)
- **Description:** A mobile app for a retail chain that scores each customer's 'trustworthiness' based on unrelated social media activity, purchase history, and neighborhood, and uses that score to decide who gets refused service.
- **Expected tier:** prohibited
- **Model tier:** prohibited
- **Model reasoning:** The system creates a 'trustworthiness' score based on social media activity, purchase history, and neighborhood, and uses this score to refuse service. This constitutes social scoring as defined in Article 5(1)(c), which is an unacceptable risk and is outright banned.

### P3 (PASS)
- **Description:** A government pilot that predicts which individuals are likely to commit a crime in the next year based purely on their personality profile and demographic data, with no other supporting evidence.
- **Expected tier:** prohibited
- **Model tier:** prohibited
- **Model reasoning:** The system predicts an individual's risk of committing a criminal offence based solely on profiling and personality traits, with no other supporting facts. This practice is explicitly prohibited under Article 5(1)(d) of the EU AI Act.

### H1 (FAIL)
- **Description:** An AI tool that scans job applicants' CVs and ranks them for recruiters.
- **Expected tier:** high-risk
- **Model tier:** ERROR
- **Error:** 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}

### H2 (PASS)
- **Description:** An automated system used by a bank to decide whether to approve or deny personal loan applications.
- **Expected tier:** high-risk
- **Model tier:** high-risk
- **Model reasoning:** Credit scoring and creditworthiness assessment for individuals is explicitly listed under Annex III point 5 (access to essential private services). It directly determines access to a financial service, meeting the significant-risk bar.

### H3 (PASS)
- **Description:** Software used by a university admissions office to automatically score and rank applicants for a limited number of spots.
- **Expected tier:** high-risk
- **Model tier:** high-risk
- **Model reasoning:** The system is used by a university admissions office to score and rank applicants, which falls under Annex III point 3. This category includes AI systems determining access to educational institutions and evaluating learning outcomes or admission criteria. Such a system poses a significant risk to fundamental rights (access to education).

### H4 (PASS)
- **Description:** A tool used by a national employment agency to determine which unemployed citizens are eligible for continued benefit payments.
- **Expected tier:** high-risk
- **Model tier:** high-risk
- **Model reasoning:** The system determines eligibility for public assistance benefits, which is explicitly listed as a high-risk use case under Annex III point 5. This decision directly impacts individuals' access to essential services and fundamental rights.

### H5 (PASS)
- **Description:** An AI system used by police to assess the reliability of evidence gathered during a criminal investigation.
- **Expected tier:** high-risk
- **Model tier:** high-risk
- **Model reasoning:** The AI system is used by law enforcement to assess the reliability of evidence, which is explicitly listed as a high-risk use case under Annex III point 6. This directly impacts the administration of justice and fundamental rights.

### L1 (PASS)
- **Description:** A chatbot on our e-commerce website that answers customer questions about order status and returns.
- **Expected tier:** limited-risk
- **Model tier:** limited-risk
- **Model reasoning:** The system interacts directly with natural persons and does not fall into any Annex III category or Article 5 prohibition. It only triggers the Article 50 obligation to disclose that users are interacting with an AI system.

### L2 (PASS)
- **Description:** A marketing tool that generates realistic AI images of people using our products for social media ads.
- **Expected tier:** limited-risk
- **Model tier:** limited-risk
- **Model reasoning:** The system generates realistic AI images ('deepfakes') for marketing purposes. While not explicitly listed as high-risk or prohibited, Article 50(2) mandates disclosure for AI-generated or manipulated audio, image, video, or text content. This system falls under that transparency obligation.

### L3 (PASS)
- **Description:** A news aggregator that uses AI to auto-generate short article summaries for a public-interest news site, without any human editorial review before publishing.
- **Expected tier:** limited-risk
- **Model tier:** limited-risk
- **Model reasoning:** The system generates AI content (summaries) for a public-interest news site. Article 50(2) requires disclosure that such content is artificially generated when published, unless it has been human-reviewed with editorial responsibility. As there is no human review mentioned, this transparency obligation is triggered.

### M1 (PASS)
- **Description:** An internal tool that uses AI to forecast which warehouse items will run low on stock next month.
- **Expected tier:** minimal-risk
- **Model tier:** minimal-risk
- **Model reasoning:** Inventory forecasting does not affect any individual's fundamental rights, safety, or access to services, and does not fall into any Annex III category or trigger a transparency obligation. No mandatory obligations apply.

### M2 (PASS)
- **Description:** An AI-powered spam filter for our company email inboxes.
- **Expected tier:** minimal-risk
- **Model tier:** minimal-risk
- **Model reasoning:** An AI-powered spam filter for internal company email inboxes does not fall under any of the prohibited practices in Article 5, nor does it fit any of the high-risk use cases described in Annex III. It also does not trigger any transparency obligations under Article 50 as it does not interact directly with natural persons in a way that requires disclosure, nor does it generate deepfakes or perform prohibited biometric categorisation.

### M3 (PASS)
- **Description:** A video game NPC that uses AI to generate dynamic dialogue responses to the player.
- **Expected tier:** minimal-risk
- **Model tier:** minimal-risk
- **Model reasoning:** AI-generated dialogue for video game NPCs does not fall under any prohibited practices in Article 5, nor does it fit any of the high-risk categories in Annex III. It also does not trigger any transparency obligations under Article 50 as it is not intended to interact directly with natural persons in a way that requires disclosure, nor is it generating deepfakes or public interest content.

### B1 (PASS)
- **Description:** A tool that uses AI to summarize long legal contracts into plain-language bullet points for internal staff.
- **Expected tier:** minimal-risk
- **Model tier:** minimal-risk
- **Model reasoning:** Contract summarization for internal use does not fall into an Annex III category (it does not itself administer justice or apply law to facts on behalf of a court) and doesn't interact directly with external end-users in a way that triggers Article 50.

### B2 (FAIL)
- **Description:** A customer support voice assistant that also silently analyzes callers' vocal tone to estimate their emotional state and logs it for quality-assurance review.
- **Expected tier:** ambiguous
- **Model tier:** prohibited
- **Model reasoning:** The system performs emotion recognition (analyzing vocal tone to estimate emotional state) and logs this data for quality assurance, which implies a workplace context. Article 5(1)(f) explicitly prohibits emotion recognition in the workplace, with very narrow exceptions not applicable here.