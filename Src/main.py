import os
import json
import time
import requests
from dotenv import load_dotenv

# --- 1. SECURELY LOAD API KEY ---
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY")

# --- 2. MOCK KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "breach": "NDPA 2023 Section 40: A data controller shall, within 72 hours of becoming aware of a breach... notify the Commission.",
    "rights": "NDPA 2023 Section 34: A data subject has the right to obtain confirmation as to whether their data is being processed.",
    "unauthorized_access": "Cybercrimes Act 2015 Section 6: Any person who intentionally accesses a computer system without authorization is guilty of an offence."
}

# --- 3. THE DETERMINISTIC POLICY NODE (The Guardrail) ---
class DeterministicPolicyNode:
    @staticmethod
    def evaluate(query):
        query_lower = query.lower()
        
        # SECURITY GUARDRAIL (Zero AI used here. 100% Deterministic)
        malicious_keywords = ["hack", "steal", "bypass", "malware", "ddos", "exploit", "crack", "how to"]
        if any(keyword in query_lower for keyword in malicious_keywords):
            return {
                "verdict": "ILLEGAL_INTENT",
                "context": KNOWLEDGE_BASE["unauthorized_access"],
                "citation": "Cybercrimes Act 2015 - Section 6"
            }

        # LEGAL CONTEXT RETRIEVAL
        if "breach" in query_lower or "leak" in query_lower:
            return {"verdict": "LEGAL_MATCH", "context": KNOWLEDGE_BASE["breach"], "citation": "NDPA 2023 - Section 40"}
            
        if "rights" in query_lower or "my data" in query_lower:
            return {"verdict": "LEGAL_MATCH", "context": KNOWLEDGE_BASE["rights"], "citation": "NDPA 2023 - Section 34"}

        return {"verdict": "NO_MATCH", "context": "No specific Nigerian law found in the database.", "citation": "N/A"}

# --- 4. THE LLM ENGINE (With Auto-Retry & Fallback) ---
def generate_ai_response(user_query, policy_output):
    # 1. Guardrail Block
    if policy_output['verdict'] == 'ILLEGAL_INTENT':
        return f"⚠️ ACCESS DENIED. Based on the {policy_output['citation']}, I cannot assist with hacking. {policy_output['context']}"
    
    # 2. LLM Generation
    if policy_output['verdict'] == 'LEGAL_MATCH':
        if not API_KEY:
            return "System Error: API Key is missing. Please check your .env file."

        # Using the latest stable model: gemini-3.8-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
        
        prompt = f"""
        You are a helpful Nigerian AI Legal Assistant. 
        A citizen asked: "{user_query}"
        Here is the verified legal context from Nigerian Law: "{policy_output['context']}"
        Write a short, plain-English response explaining their rights based ONLY on the context provided. 
        Mention the citation: {policy_output['citation']}.
        Do not make up any laws.
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        
        # --- AUTO-RETRY LOOP ---
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                response_data = response.json()
                
                if 'error' in response_data:
                    error_msg = response_data['error']['message']
                    # Catch temporary overload errors
                    if "high demand" in error_msg or "overloaded" in error_msg or "temporary" in error_msg:
                        print(f"[Debug] Google servers busy. Retrying in 3 seconds (Attempt {attempt+1}/{max_retries})...")
                        time.sleep(3)
                        continue # Try again
                    else:
                        print(f"[Debug] API Error: {error_msg}")
                        break
                        
                # Success! Return the AI text
                ai_text = response_data['candidates'][0]['content']['parts'][0]['text']
                return ai_text
                
            except Exception as e:
                print(f"[Debug] Connection Error: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(3) 
                
        # Fallback if all retries fail
        return f"⚠️ AI currently experiencing high traffic. However, here is the verified law: {policy_output['context']} ({policy_output['citation']})"

    # 3. No Match
    return f"❓ I couldn't find a direct match in the Nigerian Cybersecurity Policy for your question. Please consult a legal professional."

# --- 5. THE SINK (Terminal Interface) ---
def main():
    if not API_KEY:
        print("❌ WARNING: API Key not found. LLM features will be disabled.")

    print("🇳🇬 NaijaPolicy AI Agent (Powered by Gemini 3.8 Flash)")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_query = input("Ask a question about Nigerian Cybersecurity Law: ")
        if user_query.lower() == 'exit':
            break
            
        policy_output = DeterministicPolicyNode.evaluate(user_query)
        
        print("\nThinking...\n")
        final_response = generate_ai_response(user_query, policy_output)
        
        print(f"Agent:\n{final_response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
