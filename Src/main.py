import os
import re

# --- MOCK KNOWLEDGE BASE (In production, this uses a Vector DB) ---
KNOWLEDGE_BASE = {
    "breach": "NDPA 2023 Section 40: A data controller shall, within 72 hours of becoming aware of a breach... notify the Commission.",
    "rights": "NDPA 2023 Section 34: A data subject has the right to obtain confirmation as to whether their data is being processed.",
    "unauthorized_access": "Cybercrimes Act 2015 Section 6: Any person who intentionally accesses a computer system without authorization is guilty of an offence."
}

# --- THE SECRET WEAPON: DETERMINISTIC POLICY NODE ---
# We do NOT let the LLM make the final decision. We use hard-coded logic.
class DeterministicPolicyNode:
    @staticmethod
    def evaluate(query, retrieved_context):
        query_lower = query.lower()
        
        # 🚨 RULE 0: SECURITY GUARDRAIL (MUST BE CHECKED FIRST) 🚨
        # We check for malicious intent before anything else.
        malicious_keywords = ["how to hack", "steal password", "hack a bank", "bypass security", "malware", "ddos"]
        if any(keyword in query_lower for keyword in malicious_keywords):
            return {
                "verdict": "ILLEGAL_INTENT",
                "context": KNOWLEDGE_BASE["unauthorized_access"],
                "citation": "Cybercrimes Act 2015 - Section 6",
                "action": "Request DENIED. Unauthorized access is a criminal offense."
            }

        # Rule 1: Check for Data Breach queries
        if "breach" in query_lower or "leak" in query_lower:
            return {
                "verdict": "VIOLATION_CHECK",
                "context": KNOWLEDGE_BASE["breach"],
                "citation": "NDPA 2023 - Section 40",
                "action": "Ensure the Data Controller notified NDPC within 72 hours."
            }
            
        # Rule 2: Check for Citizen Rights
        if "rights" in query_lower or "my data" in query_lower:
            return {
                "verdict": "COMPLIANT_INFO",
                "context": KNOWLEDGE_BASE["rights"],
                "citation": "NDPA 2023 - Section 34",
                "action": "You have the right to request a copy of your data."
            }

        # Default Fallback (If no rules match)
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "context": "I do not have enough context to answer this based on Nigerian law.",
            "citation": "N/A",
            "action": "Please contact a legal professional."
        }

# --- MOCK RAG MODEL (Simulating the AI part) ---
class RAGModel:
    @staticmethod
    def generate_response(query, policy_node_output):
        # In a real app, this calls Gemini/OpenAI API to make the text sound human.
        # Example Prompt to LLM: "Rewrite this legal verdict for a Nigerian citizen: {policy_node_output}"
        
        if policy_node_output['verdict'] == 'ILLEGAL_INTENT':
            return f"⚠️ ACCESS DENIED. Based on the {policy_node_output['citation']}, I cannot assist with hacking. {policy_node_output['context']}"
            
        if policy_node_output['verdict'] == 'VIOLATION_CHECK':
            return f"🚨 ALERT: According to the {policy_node_output['citation']}, {policy_node_output['context']} \n\nAction to take: {policy_node_output['action']}"
            
        if policy_node_output['verdict'] == 'COMPLIANT_INFO':
            return f"✅ INFO: According to the {policy_node_output['citation']}, {policy_node_output['context']} \n\nNext steps: {policy_node_output['action']}"
            
        return f"❓ I couldn't find a direct match in the Nigerian Cybersecurity Policy for your question. {policy_node_output['action']}"

# --- THE SINK (Application Interface) ---
def main():
    print("🇳🇬 NaijaPolicy AI Agent (ITU AI for Good Hackathon)")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_query = input("Ask a question about Nigerian Cybersecurity Law: ")
        if user_query.lower() == 'exit':
            break
            
        # 1. Retrieve context (Mocked)
        retrieved_context = "Mock retrieved text from NDPA/Cybercrimes Act"
        
        # 2. Pass through Deterministic Policy Node (No LLM allowed to decide)
        policy_output = DeterministicPolicyNode.evaluate(user_query, retrieved_context)
        
        # 3. LLM generates the final friendly response based ONLY on the policy output
        final_response = RAGModel.generate_response(user_query, policy_output)
        
        print(f"\nAgent: {final_response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
