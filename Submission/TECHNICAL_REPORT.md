# AI for Good Sandbox Hackathon -- Cyberterians -- NaijaPolicy AI Agent

**Team leader:** Ikehi Isaac
**Github link:** https://github.com/IsaacDevX/ITU-AI-Readiness-Solo

## 1. Introduction
Nigeria is rapidly digitizing, yet its legal frameworks governing cyberspace (NDPA 2023, Cybercrimes Act 2015, National AI Strategy) remain highly technical and inaccessible to the average citizen or small business owner. This submission proposes the **NaijaPolicy AI Agent**, a specialized conversational agent designed for the Government Services domain. By utilizing Retrieval-Augmented Generation (RAG) combined with a strict **Deterministic Policy Node**, the agent translates complex legal text into actionable, plain-English advice. This solution maps directly to the ITU AI Readiness framework, prioritizing human-centric design, data privacy, and trustworthy AI.

## 2. Description of the Use Case
**The Problem:** If a citizen suspects their data was leaked by a company, they are unlikely to know the 72-hour reporting rule mandated by the Nigeria Data Protection Commission (NDPC). Existing global AI models hallucinate or give US/EU-centric legal advice, which is dangerous.
**The Solution:** The NaijaPolicy Agent uses a localized Knowledge Base (KB). A user asks a question (e.g., "My bank leaked my ID"). The system retrieves the exact NDPA section and the AI explains the user's rights.
**Gaps Solved:** It eliminates language barriers, drastically reduces the cost of legal consultation, and prevents AI hallucinations by restricting the AI's knowledge to verified government PDFs.

## 3. Use Case Requirements
*   **Data Node:** Ingestion of legal PDFs. **Requirement:** Strict data sanitization to prevent prompt injection attacks. 
*   **Model Node:** A localized LLM (via API). **Requirement:** The AI must only format the output; it cannot make the legal decision.
*   **Policy Node:** Deterministic Rule Engine. **Requirement:** Hard-coded logic to ensure compliance with Nigerian law.
*   **Privacy:** **Requirement:** Zero data retention. User queries are processed and immediately discarded to comply with NDPA (Section 24).

## 4. Mapping with ITU-T Y.3172 Readiness 2.0 Report

| Node | Use Case (Government Services) | Readiness 2.0 Report | Documents (Nigerian Policies) |
| :--- | :--- | :--- | :--- |
| **SRC** | Raw Sources | Data & Model Marketplace. | NDPA 2023, Cybercrimes Act 2015, NAIS. |
| **C** | Collection | Secure HTTP API queries from the user. | NDPA 2023: Consent & Purpose Limitation rules. |
| **PP** | Preprocessing | Text chunking, embedding, and PII stripping. | NDPA 2023: Data Minimization principles. |
M | Model / RAG | Retrieval over the verified legal corpus; Google Gemini LLM (gemini-2.5-flash) drafts the explanation based on the retrieved context. | NAIS Pillar 4: Responsible AI. |
| **P** | Policy Node | **Deterministic rule engine.** No AI model in the decision path. Four rules (e.g., "If breach, check 72-hour rule"). Returns: `VIOLATION`, `COMPLIANT`, `ILLEGAL_INTENT`. | Cybercrimes Act 2015 (Prohibits unauthorized access). |
| **D** | Distribution | Attaches citations with the specific Act, Section, and URL; logs the audit entry. | NSS 2019: Data-driven governance. |
| **SINK** | Application | User-facing chat interface; returns a 403-equivalent refusal if the query asks for illegal actions. | NAIS: Human-centric AI. |

## 5. Error Scenarios
**Scenario 1 (Malicious Intent):** A user tries to trick the AI into providing malware code to attack a government website.
*   **Handling:** The Policy Node intercepts the query. It detects malicious intent via keyword analysis and hard-coded rules. It outputs: *"According to the Cybercrimes Act 2015, unauthorized access is illegal. I can only provide information on how to report cyber threats to ngCERT."*

**Scenario 2 (The Hallucination/Controversy):** A user asks a highly specific legal question about a new state law not in the database.
*   **Handling:** If the RAG model cannot find a direct citation in the KB, the Policy Node triggers `INSUFFICIENT_EVIDENCE`. The AI is strictly instructed not to guess. It outputs: *"I do not have enough verified information on this. Please consult the Nigerian Bar Association."*

## 6. Policy Gaps and Standards Gaps
Through this mapping exercise, we identified a critical gap: The NDPA 2023 does not explicitly define liability for AI-generated advice. If our agent gives a wrong legal interpretation, who is liable? The developer? The user? The algorithm? This project highlights the urgent need for the upcoming National AI Policy to define algorithmic accountability and AI liability frameworks, as outlined in Pillar 5 of the NAIS.
