# agent.py
# AI Policy Agent for Nigerian Cybersecurity Law (HTTP Version)
# Built for ITU AI for Good Hackathon 2026
# Author: Ikehi Isaac

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# --- 1. THE KNOWLEDGE BASE (Simulated for Demo) ---
KNOWLEDGE_BASE = {
    "data_breach": """
    [NDPA 2023]: The Nigeria Data Protection Act mandates that data controllers must notify the Nigeria Data Protection Commission (NDPC) within 72 hours of becoming aware of a data breach. 
    [National Cybersecurity Policy 2014]: Critical National Information Infrastructure (CNII) operators must report incidents to ngCERT.
    """,
    "ai_policy": """
    [National AI Strategy 2024]: Nigeria aims to be a global leader in AI. It emphasizes responsible and ethical AI development, transparency, and human-centric design. It establishes the need for a National AI Ethics Expert Group.
    """,
    "cyber_threat": """
    [National Security Strategy 2019]: Cybercrime, cyber-espionage, and fake news are identified as critical threats to national stability. The strategy calls for proactive measures and inter-agency collaboration to secure cyberspace.
    """,
    "default": """
    [System]: The user's question does not perfectly match the available Nigerian policy documents. Please provide a general answer based on national security and AI ethics principles.
    """
}

# --- 2. SETUP API URL ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# --- 3. THE RAG LOGIC ---
def retrieve_policy_context(question):
    """Simple keyword matching to retrieve the right policy."""
    question = question.lower()
    if "breach" in question or "data" in question or "privacy" in question:
        return KNOWLEDGE_BASE["data_breach"]
    elif "ai" in question or "strategy" in question or "ethic" in question:
        return KNOWLEDGE_BASE["ai_policy"]
    elif "threat" in question or "security" in question or "cybercrime" in question:
        return KNOWLEDGE_BASE["cyber_threat"]
    else:
        return KNOWLEDGE_BASE["default"]

def ask_agent(question):
    """Sends the question + policy context to the AI via HTTP."""
    context = retrieve_policy_context(question)
    
    prompt = f"""
    You are the Nigerian Cybersecurity Policy Agent. 
    Answer the user's question using ONLY the policy context provided below. 
    Always cite the specific law or document (e.g., NDPA 2023, National AI Strategy).
    If the context does not contain the answer, say "I do not have that specific policy information."
    
    POLICY CONTEXT:
    {context}
    
    USER QUESTION: 
    {question}
    """
    
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(API_URL, json=body, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"Error connecting to AI: {e}"

# --- 4. MAIN LOOP (For the Demo Video) ---
if __name__ == "__main__":
    print("===================================================")
    print("🇳🇬 NIGERIAN CYBERSECURITY POLICY AGENT (ITU 2026)")
    print("===================================================")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Agent: Goodbye.")
            break
        
        if not user_input.strip():
            continue
            
        print("\n[Agent is thinking...]\n")
        answer = ask_agent(user_input)
        print(f"Agent: {answer}\n")
        print("-" * 50)
