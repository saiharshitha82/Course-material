# Advanced Cybersecurity — Study Materials

**Audience:** First-semester Master's students (MSc Cybersecurity / Information Security / Computer Science)
**Prerequisites:** Undergraduate networking (TCP/IP, OSI), operating systems basics, introductory cryptography (symmetric vs. asymmetric, hashing), basic Linux command line.
**Format:** 14 teaching weeks, ~3 contact hours + ~6 self-study hours per week.

---

## How to use this pack

Each module is a self-contained study guide with the same layout:

1. **Learning outcomes** — what you should be able to do afterwards
2. **Core concepts** — the theory, with tables and diagrams
3. **Worked examples and case studies** — real incidents and how the concepts apply
4. **Lab / practical exercise** — hands-on work, runnable on a laptop or free cloud tier
5. **Discussion questions** — for seminars
6. **Self-check quiz** — with answers at the end of the module
7. **Further reading** — primary sources (standards, papers) you are expected to cite in assignments

Read the module **before** the lecture, attempt the quiz **after** it, and do the lab within the same week.

> Diagrams are written in Mermaid and render directly on GitHub. In other viewers, use a Mermaid-capable Markdown preview (e.g., VS Code with the Mermaid extension).

---

## Modules

| # | Module | Topics |
|---|--------|--------|
| 1 | [Advanced Threat Landscape & Emerging Technologies](modules/01-advanced-threat-landscape.md) | AI/ML as tool and threat · Quantum computing & post-quantum cryptography · IoT and embedded systems security |
| 2 | [Zero Trust Architecture & Cloud Security](modules/02-zero-trust-and-cloud-security.md) | Zero Trust principles & implementation · Multi-cloud / hybrid best practices · Secure configuration & access control |
| 3 | [Compliance & Security Frameworks](modules/03-compliance-and-frameworks.md) | GDPR · NIST Cybersecurity Framework 2.0 · ISO/IEC 27001:2022 ISMS |
| 4 | [Advanced Network & System Security](modules/04-network-and-system-security.md) | NGFW & IDS/IPS · Secure software development · Container & microservices security |
| 5 | [Cybersecurity Risk Management](modules/05-risk-management.md) | Advanced risk assessment · Threat modeling · Business continuity & disaster recovery |

Supporting material:

- [Glossary](glossary.md) — acronyms and key terms across all modules
- [Assessment guide](assessment-guide.md) — coursework briefs, exam format and marking rubrics

---

## Suggested 14-week schedule

| Week | Module | Topic | Lab |
|------|--------|-------|-----|
| 1 | 1 | Course intro; modern threat landscape; adversary economics | Map a recent incident to MITRE ATT&CK |
| 2 | 1 | AI/ML in cybersecurity — defensive and offensive | Train a simple anomaly detector; attempt evasion |
| 3 | 1 | Quantum threat & post-quantum cryptography; IoT/embedded security | PQC handshake with OpenSSL 3.5 / liboqs; firmware analysis with binwalk |
| 4 | 2 | Zero Trust principles (NIST SP 800-207, CISA ZTMM) | Design a ZTA for a case-study organisation |
| 5 | 2 | Cloud security: shared responsibility, multi/hybrid cloud | Cloud posture scan with Prowler / ScoutSuite |
| 6 | 2 | Secure cloud configuration, IAM and access control | Write and test least-privilege IAM policies |
| 7 | 3 | GDPR in practice | Draft a DPIA |
| 8 | 3 | NIST CSF 2.0 and ISO/IEC 27001:2022 | Build a CSF Current/Target Profile and gap analysis |
| 9 | — | **Mid-semester test** + coursework 1 due | — |
| 10 | 4 | NGFW, IDS/IPS, network detection | Write Suricata rules against a PCAP |
| 11 | 4 | Secure SDLC and software supply chain | SAST/SCA pipeline; generate an SBOM |
| 12 | 4 | Container & microservices security | Harden a Kubernetes deployment |
| 13 | 5 | Risk assessment (qualitative, quantitative, FAIR) & threat modeling | STRIDE threat model + FAIR Monte Carlo |
| 14 | 5 | BCP/DR; course review | Run a ransomware tabletop exercise; coursework 2 due |

---

## Lab environment

Most labs run on a laptop with 16 GB RAM:

- **VirtualBox / UTM** or **Docker Desktop / Podman**
- **Kali Linux** (or any Linux VM) — Wireshark, Suricata, Zeek, binwalk, nmap
- **Python 3.11+** with `scikit-learn`, `pandas`, `numpy`, `matplotlib`
- **kind** or **minikube** for local Kubernetes
- A free-tier account on **one** public cloud (AWS, Azure or GCP) — always set a billing alarm first, and tear down resources after each lab

> **Ethics and legality:** Only test systems you own or are explicitly authorised to test. All offensive techniques in this pack are taught so you can defend against them. Unauthorised access is a criminal offence in nearly every jurisdiction (e.g., UK Computer Misuse Act 1990, US CFAA, India IT Act 2000 s.43/66).
