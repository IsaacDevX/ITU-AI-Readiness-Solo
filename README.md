# NaijaPolicy AI Agent (ITU AI for Good Hackathon)

## 🎯 The Problem
Nigerian citizens and SMEs lack accessible, plain-English knowledge of their rights under complex cybersecurity laws like the NDPA 2023 and the Cybercrimes Act 2015. 

## 💡 The Solution
An AI-powered Policy Agent that uses Retrieval-Augmented Generation (RAG) combined with a **Deterministic Policy Node** to answer questions based *strictly* on Nigerian law, while guaranteeing safety and preventing AI hallucinations.

## 🏗️ Architecture (ITU-T Y.3172 Mapping)
*   **SRC:** NDPA 2023, National Cybersecurity Policy, NAIS.
*   **C:** Secure user queries.
*   **PP:** PII stripping (NDPA Section 24).
*   **M:** LLM (Gemini/OpenAI) RAG pipeline.
*   **P (Policy Node):** Rule engine (No AI in the decision path). 
*   **D:** Citations linked to specific Act sections.
*   **SINK:** User chat interface.

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add your API key to `.env` (e.g., `GEMINI_API_KEY=your_key`).
3. Run: `python src/main.py`
