# Assessment Guide

| Component | Weight | Timing | Learning outcomes |
|-----------|:------:|--------|-------------------|
| Lab portfolio (best 8 of 12 lab reports) | 20% | Weekly, 1 week after each lab | All modules |
| Coursework 1 — Zero Trust & Cloud Security Design | 20% | Week 9 | Modules 1–2 |
| Coursework 2 — Integrated Risk & Compliance Report | 25% | Week 14 | Modules 3–5 |
| Mid-semester test (MCQ + short answer, 60 min) | 10% | Week 9 | Modules 1–3 |
| Final written exam (2 hours) | 25% | Exam period | All modules |

---

## Coursework 1 — Zero Trust & Cloud Security Design (≈3,000 words)

**Scenario:** *FinNova*, a fintech start-up (400 staff) running on two public clouds plus a legacy on-premises core-banking system, has suffered a credential-phishing incident. The board wants a Zero Trust roadmap.

**Deliverables**
1. Threat landscape summary relevant to FinNova, including AI-enabled social engineering and a short PQC readiness statement (Module 1).
2. Current-state maturity assessment against the CISA ZTMM pillars.
3. Target architecture diagram showing PE/PA/PEP, identity, device posture, ZTNA, segmentation, logging.
4. Secure cloud baseline: landing-zone structure, guardrails, IAM approach, logging, three example policies (IAM or policy-as-code).
5. Phased 18-month roadmap with costs/effort estimates, dependencies and KPIs.

**Marking rubric**

| Criterion | Weight | Excellent (70%+) | Satisfactory (50–69%) | Fail (<50%) |
|-----------|:------:|------------------|----------------------|-------------|
| Understanding of ZT & cloud principles | 25% | Accurate, cites SP 800-207/ZTMM precisely, critical insight | Mostly accurate, descriptive | Misconceptions, ZT treated as a product |
| Architecture quality | 25% | Coherent, justified, handles legacy and OT edge cases | Reasonable but generic | Incomplete or incoherent |
| Practical configuration | 20% | Correct least-privilege policies, tested | Minor errors | Over-permissive or wrong |
| Roadmap & business alignment | 20% | Prioritised, realistic, measurable KPIs | Some prioritisation | Wish list |
| Presentation & referencing | 10% | Professional, primary sources | Adequate | Poor or unreferenced |

---

## Coursework 2 — Integrated Risk & Compliance Report (≈4,000 words)

**Scenario:** *HealthLink*, an EU-based telehealth provider using containerised microservices on Kubernetes, processing patient health data.

**Deliverables**
1. STRIDE (+ LINDDUN) threat model of the patient-consultation service with DFD.
2. Quantitative risk analysis (FAIR Monte Carlo) of the top two scenarios, with loss exceedance curves.
3. GDPR analysis: lawful basis and Art. 9 condition, DPIA summary, breach notification plan (GDPR + NIS2).
4. Control framework: mapping of proposed controls to NIST CSF 2.0 subcategories and ISO 27001 Annex A; draft SoA extract.
5. Secure SDLC and Kubernetes hardening recommendations.
6. BIA for three services with RTO/RPO/MTD, and a ransomware-resilient DR strategy.
7. Executive summary (1 page) for the board.

**Marking rubric**

| Criterion | Weight |
|-----------|:------:|
| Threat model completeness and accuracy | 15% |
| Risk quantification — method, justification of estimates, interpretation | 20% |
| Regulatory analysis (GDPR/NIS2) correctness | 15% |
| Framework mapping and SoA | 15% |
| Technical recommendations (SSDLC, containers) | 15% |
| BC/DR design | 10% |
| Executive communication | 10% |

---

## Final exam — format and sample questions

**Section A (40%)** — 8 short-answer questions (answer all)
**Section B (60%)** — 3 essay/scenario questions out of 5

### Sample Section A questions
1. Explain why Grover's algorithm does not require replacing AES, while Shor's algorithm requires replacing RSA. *(5 marks)*
2. List four tenets of NIST SP 800-207. *(4 marks)*
3. A controller discovers a breach on Friday at 17:00. By when must the supervisory authority be notified, and what must the notification contain? *(5 marks)*
4. Compute SLE and ALE for AV = €1.2M, EF = 0.25, ARO = 0.2, and evaluate a control costing €30k/year that halves ARO. *(5 marks)*
5. Write a Suricata rule that alerts on HTTP requests to the URI `/wp-login.php` from external networks. *(5 marks)*
6. Explain two Kubernetes controls that would have prevented the 2018 Tesla cryptojacking incident. *(4 marks)*

### Sample Section B questions
1. "Machine learning will make signature-based intrusion detection obsolete." Critically evaluate with reference to base rates, adversarial ML and operational experience. *(20 marks)*
2. You are the new CISO of a manufacturer with ISO 27001 certification that was nonetheless crippled by ransomware. Explain how this could happen and how you would use NIST CSF 2.0 and FAIR to rebuild the programme. *(20 marks)*
3. Design a post-quantum migration programme for a national bank, including inventory, prioritisation via Mosca's inequality, hybrid deployment and governance. *(20 marks)*
4. Compare STRIDE, PASTA and attack trees. Which would you recommend for an agile team building an LLM-powered customer service agent, and why? *(20 marks)*
5. Evaluate the security implications of migrating a monolithic application to microservices on Kubernetes. *(20 marks)*

---

## Academic integrity and use of AI tools

You may use AI assistants for brainstorming, explanation and proofreading, **but you must**: disclose their use in an appendix; verify every technical claim and reference against primary sources (AI tools frequently invent standards clauses and citations); and submit work that reflects your own analysis. Undisclosed AI-generated content is treated as academic misconduct.
