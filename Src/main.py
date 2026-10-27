import os
import google.generativeai as genai

# --- 1. SETUP API KEY ---
# The judges will need to put their own API key here to test it, 
# or you can hardcode yours for the demo (but explain it's normally stored in an env variable for security).
API_KEY = "PASTE_YOUR_API_KEY_HERE" 
genai.configure(api_key=API_KEY)

# Initialize the LLM (Gemini 1.5 Flash is fast and perfect for this)
llm_model = genai.GenerativeModel('gemini-1.5-flash')

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
        malicious_keywords = ["hack", "steal", "bypass", "malware", "ddos", "exploit", "crack"]
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

# --- 4. THE LLM ENGINE (Powering the Response) ---
def generate_ai_response(user_query, policy_output):
    # If the guardrail blocked it, we don't even call the LLM. We just print the hardcoded block.
    if policy_output['verdict'] == 'ILLEGAL_INTENT':
        return f"⚠️ ACCESS DENIED. Based on the {policy_output['citation']}, I cannot assist with hacking. {policy_output['context']}"
    
    # If it's a safe legal question, we ask Gemini to write the answer.
    if policy_output['verdict'] == 'LEGAL_MATCH':
        prompt = f"""
        You are a helpful Nigerian AI Legal Assistant. 
        A citizen asked: "{user_query}"
        
        Here is the verified legal context from Nigerian Law: "{policy_output['context']}"
        
        Write a short, plain-English response explaining their rights or what they should do based ONLY on the context provided. 
        Mention the citation: {policy_output['citation']}.
        Do not make up any laws.
        """
        try:
            response = llm_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}"

    # Fallback
    return f"❓ I couldn't find a direct match in the Nigerian Cybersecurity Policy for your question. Please consult a legal professional."

# --- 5. THE SINK (Terminal Interface) ---
def main():
    print("🇳🇬 NaijaPolicy AI Agent (Powered by Gemini LLM)")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_query = input("Ask a question about Nigerian Cybersecurity Law: ")
        if user_query.lower() == 'exit':
            break
            
        # Step 1: Check Guardrails (Deterministic)
        policy_output = DeterministicPolicyNode.evaluate(user_query)
        
        # Step 2: Generate Response (LLM)
        print("\nThinking...\n")
        final_response = generate_ai_response(user_query, policy_output)
        
        print(f"Agent:\n{final_response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
