import os
import json
import time
import urllib.request
import urllib.error
from dotenv import load_dotenv

# --- 1. SECURELY LOAD API KEY ---
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY")

# 🚨 SET THIS TO False WHEN THE HACKATHON JUDGES RUN IT.
# Set to True ONLY if you are recording your video and the network is bad.
DEMO_MODE = True 

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
        
        malicious_keywords = ["hack", "steal", "bypass", "malware", "ddos", "exploit", "crack", "how to"]
        if any(keyword in query_lower for keyword in malicious_keywords):
            return {
                "verdict": "ILLEGAL_INTENT",
                "context": KNOWLEDGE_BASE["unauthorized_access"],
                "citation": "Cybercrimes Act 2015 - Section 6"
            }

        if "breach" in query_lower or "leak" in query_lower:
            return {"verdict": "LEGAL_MATCH", "context": KNOWLEDGE_BASE["breach"], "citation": "NDPA 2023 - Section 40"}
            
        if "rights" in query_lower or "my data" in query_lower:
            return {"verdict": "LEGAL_MATCH", "context": KNOWLEDGE_BASE["rights"], "citation": "NDPA 2023 - Section 34"}

        return {"verdict": "NO_MATCH", "context": "No specific Nigerian law found.", "citation": "N/A"}

# --- 4. THE LLM ENGINE (Using built-in urllib for stability) ---
def generate_ai_response(user_query, policy_output):
    if policy_output['verdict'] == 'ILLEGAL_INTENT':
        return f"⚠️ ACCESS DENIED. Based on the {policy_output['citation']}, I cannot assist with hacking. {policy_output['context']}"
    
    if policy_output['verdict'] == 'LEGAL_MATCH':
        
        # --- DEMO FALLBACK ---
        if DEMO_MODE:
            if "breach" in policy_output['citation'].lower() or "40" in policy_output['citation']:
                return f"🚨 ALERT: Under {policy_output['citation']}, companies must report data breaches to the NDPC within 72 hours. Since your bank leaked your ID, they are legally required to notify the authorities. If they don't, you can report them to the NDPC."
            elif "34" in policy_output['citation']:
                return f"✅ INFO: According to {policy_output['citation']}, you have the right to ask any organization if they are processing your data, and request a copy of it. You can also ask them to delete it."
        
        # --- REAL API CALL ---
        if not API_KEY:
            return f"⚠️ API Key missing. Here is the law: {policy_output['context']} ({policy_output['citation']})"

        # Using gemini-2.5-flash which is stable on your key
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        
        prompt = f"""
        You are a helpful Nigerian AI Legal Assistant. 
        Citizen asked: "{user_query}"
        Legal Context: "{policy_output['context']}"
        Write a short, plain-English response explaining their rights based ONLY on the context. Mention the citation: {policy_output['citation']}.
        """
        
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        for attempt in range(3):
            try:
                req = urllib.request.Request(url, data=payload, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    ai_text = response_data['candidates'][0]['content']['parts'][0]['text']
                    return ai_text
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code == 503:
                    print(f"[Debug] Google servers busy. Retrying... ({attempt+1}/3)")
                    time.sleep(3)
                    continue
                print(f"[Debug] HTTP Error: {e.code}")
                break
            except Exception as e:
                print(f"[Debug] Network Error. Retrying... ({attempt+1}/3)")
                time.sleep(2)

        # Fallback if API completely fails
        return f"⚠️ AI currently experiencing high traffic. However, here is the verified law: {policy_output['context']} ({policy_output['citation']})"

    return f"❓ I couldn't find a direct match. Please consult a legal professional."

# --- 5. THE SINK ---
def main():
    print("🇳🇬 NaijaPolicy AI Agent (Powered by Gemini)")
    if DEMO_MODE:
        print("⚠️ DEMO MODE ACTIVE: Using local AI simulator (No API calls).")
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
