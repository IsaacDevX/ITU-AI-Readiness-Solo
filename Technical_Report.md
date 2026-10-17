# Technical Report: The Nigerian Cybersecurity Policy Agent

**Hackathon:** ITU AI for Good Sandbox Hackathon 2026
**Domain:** Government Services
**Team Name:** Cyberterians (Solo)
**Author:** Ikehi Isaac

---

## 1. Introduction

Artificial Intelligence is increasingly used by governments to analyze anomalies, deliver public services, and manage national security. However, in Nigeria, there is a critical gap between the enactment of complex cybersecurity laws and the ability of citizens and businesses to understand them. 

In the context of government services, we propose an **AI Policy Agent**: an intelligent, retrieval-augmented generation (RAG) system designed to interpret Nigerian cybersecurity and AI policies. This solution matters because many citizens, small businesses, and even local government officials struggle to navigate the dense legal frameworks of the Nigeria Data Protection Act (NDPA) 2023, the National Cybersecurity Policy, and the National AI Strategy. Timely, accurate interpretation of these laws is critical for data protection, national security, and building trust in the digital economy.

Bringing an accessible, AI-driven policy interpretation tool to the public turns a scarce specialist service (legal and cybersecurity consultation) into something that can reach every citizen. This submission maps the technical solution of the AI Agent with the policy/strategies for AI integration, mapping directly to the ITU AI Readiness framework dimensions, including data governance, model validation, and human-in-the-loop deployment support. Grounding this solution in the ITU Readiness requirements contributes directly to Nigeria's effort towards a secure, digital, and intelligent future.

---

## 2. Description of the Use Case

The problem is the lack of accessible, localized knowledge regarding cybersecurity law and AI governance. Currently, at-risk citizens and small businesses are often left in the dark until it is too late—resulting in data breaches, severe financial penalties, or national security vulnerabilities. Existing solutions rely on manual legal consultation, which is resource-intensive, expensive, and often intimidating for the average Nigerian.

Our solution is an **AI Agent powered by a localized Knowledge Base (KB)**. The AI agent captures natural language questions from users (e.g., "What are my obligations as a hospital if patient data is leaked?") and generates a response based strictly on the uploaded Nigerian policy documents. It provides an early, objective, and non-intrusive indication of legal obligations and data protection rights, ensuring that the user understands the national policies without needing a legal degree.

**NOTE:** This solution solves the gap identified in existing solutions by combining the speed of Large Language Models (LLMs) with the strict accuracy of a curated, domain-specific Knowledge Base. By using a Retrieval-Augmented Generation (RAG) approach, the AI Agent ensures it does not "hallucinate" fake laws, but rather quotes directly from the National AI Strategy, NDPA, and National Security Strategy.

---
## 3. Use Case Requirements

Each node of the AI Agent pipeline is associated with specific requirements to ensure it operates securely and effectively within the government services domain:

- **Data Node:** It is required that a minimum of 50MB of text data (Policies, Acts, and Strategies) be collected for a valid, grounded inference. It is required that the data be pre-processed (chunked and embedded) and hosted locally or via a secure cloud environment. It is required that strict data deidentification policies be applied to ensure no personally identifiable information (PII) of citizens is stored in the Knowledge Base.
- **Model Node:** It is required that the AI Agent utilizes a Retrieval-Augmented Generation (RAG) model. The model must be prompted with strict system instructions to only answer based on the provided Knowledge Base and to refuse answering if the information is not present.
- **Compute Node:** An edge compute platform (or secure cloud infrastructure) is deployed to handle the vector database and API calls to the LLM. 
- **Sink Node:** A user-friendly interface (such as a web chat or Telegram bot) is hosted to allow citizens and government officials to query the system.

---

## 4. Mapping with ITU-T Y.3172 Readiness 2.0 Report, and domain-specific policies

The following table maps our AI Agent use case to the ITU Readiness framework and the relevant Nigerian policy documents.

| Use Case (Government Services / AI Policy Agent) | Readiness 2.0 Report | Documents (Policies, Strategies, AI Regulations) |
| :--- | :--- | :--- |
| **SRC** (Source): Textual data from Nigerian Cybersecurity laws, National AI Strategy, and Data Protection Acts. | Data and model marketplace | **Usability guidelines:** Copyright and Open Access policies for government documents. |
| **C** (Communication): Users query the AI Agent via a web interface (HTTPS) or API. | Edge AI usage | **Reliability and availability guidelines:** National Cybersecurity Policy (2014) mandates secure communication channels and protection of Critical National Information Infrastructure (CNII). |
| **A** (Analytics): The AI Agent processes the query using a vector database (semantic search) and LLM reasoning. | Data harmonization standardized representation format | **Source of data input:** NDPA 2023 (Data minimization and purpose limitation). |
| **P** (Platform): The LLM API (e.g., Gemini) and the vector database (e.g., ChromaDB). | Source of model, metadata | **Benchmarking standards, privacy guidelines:** National AI Strategy (2024) emphasizes ethical AI and algorithmic transparency. |
| **M** (Model): The AI Agent (RAG architecture). | Trustworthiness of the model | **Human-in-loop:** NDPA 2023 mandates the right to explanation and human review for automated decisions. |
| **D** (Data): The Knowledge Base (NDPA, NSS, NAIS, Cybercrimes Act). | Energy considerations | **Data governance:** National Cybersecurity Policy guidelines on data protection and privacy rights. |
| **SINK**: The final response to the user, presented with citations to the specific law. | Collaboration with AI, human in the loop | **Strategy alignment:** Aligns with the National AI Strategy (NAIS) goal of using AI for social development and inclusion. |

---
## 5. Scenarios and Controversies

To test the robustness of the AI Policy Agent, we must evaluate how it handles real-world scenarios, including situations where the solution might face controversy.

### Scenario 1: The Data Breach (Normal Operation)
- **The Situation:** A small business owner asks the AI Agent: *"A hacker stole my customer database. What does Nigerian law require me to do?"*
- **The AI Response:** The Agent queries the Knowledge Base, finds the NDPA 2023 and the National Cybersecurity Policy, and responds: *"Under the NDPA 2023, you must notify the Nigeria Data Protection Commission (NDPC) within 72 hours of becoming aware of the breach. You must also alert the ngCERT as per the National Cybersecurity Policy."*
- **Outcome:** The solution works perfectly, providing actionable, legally grounded advice.

### Scenario 2: The Controversy (Algorithmic Bias and Misuse)
- **The Situation:** A user attempts to use the AI Agent to bypass privacy laws, asking: *"How can I track an employee's location without their consent and avoid getting caught?"*
- **The Controversy:** If the AI answers this, it violates the ethical guidelines of the National AI Strategy (NAIS) 2024 and the privacy rights under the NDPA 2023. This escalates the case from a simple query to a data-privacy and ethics breach.
- **How the AI Agent Addresses the Controversy:** The Knowledge Base policies must trigger **stronger guardrails**. 
  1. **Refusal:** The Agent is programmed to refuse queries that seek to violate the law.
  2. **Policy Trigger:** It cites Section 5.2.1 of the National Cybersecurity Policy regarding the right to privacy and the NAIS principle of "Responsible and Ethical Conduct."
  3. **Human-in-the-loop:** For complex or controversial queries, the Agent provides the legal framework but advises the user to consult a certified Data Protection Officer (DPO) or the NDPC directly, adhering to the ITU's "human-in-the-loop" requirement.

---

## 6. Policy Gaps and Standards Gaps Derived from the Mapping Exercise

By mapping our AI Agent to the ITU Readiness framework and Nigerian laws, we identified several critical policy and standards gaps:

### 1. The Absence of a Dedicated AI Law
As highlighted in the SSRN academic analysis, Nigeria currently lacks a standalone AI Governance Law. While we have the NDPA and the National AI Strategy, there is no statutory definition of AI or enforceable standards for algorithmic transparency. Our AI Agent currently relies on the NAIS guidelines, but a national AI Act is urgently needed.

### 2. Lack of AI-Specific Data Protection Provisions
The NDPA 2023 is largely silent on automated decision-making and algorithmic profiling. Unlike the EU's GDPR (Article 22), Nigeria's NDPA lacks equivalent safeguards, including the right to human intervention or explanation. Our AI Agent is designed to cite the law, but the law itself needs updating to address modern AI risks.

### 3. Infrastructure and Compute Gaps
As noted in the National AI Strategy, Nigeria faces a significant deficit in High-Performance Computing (HPC) and reliable digital infrastructure. Deploying AI Agents for government services requires robust cloud infrastructure, which is currently limited, making local hosting difficult.

### 4. Data Quality and Localized Datasets
The NAIS notes that Nigeria lacks high-quality, localized datasets. A Knowledge Base is only as good as its data. There is a national need for standardized, machine-readable datasets of Nigerian laws and policies to power future AI agents.

