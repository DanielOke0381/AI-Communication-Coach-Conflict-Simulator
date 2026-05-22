import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

class AIAgent:
    def __init__(self, model_id="gemini-3.1-flash-lite"):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = model_id
        self.system_instruction = ""

    def safe_send(self, message_history, user_input):
        try:
            full_context = f"SYSTEM INSTRUCTION: {self.system_instruction}\n\n"
            formatted_history = []
            for msg in message_history:
                role = "model" if msg["role"] == "assistant" else "user"
                formatted_history.append({"role": role, "parts": [{"text": msg["content"]}]})

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=formatted_history + [{"role": "user", "parts": [{"text": full_context + user_input}]}]
            )
            return response.text
        except Exception as e:
            return f" Gemini Error: {str(e)}"

class AgentFactory:
    @staticmethod
    def get_agent(mode, persona="", situation=""):
        agent = AIAgent()
        
        # UNIVERSAL PROTOCOL (Applied to all agents)
        language_protocol = (
            "\n\n[CRITICAL: Detect the user's language and respond entirely in that language. "
            "Maintain the assigned persona and tone while translating the intent perfectly.]"
        )

        if mode == "Communication Coach":
            agent.system_instruction = (
                "You are a calm, supportive Communication Coach. "
                "Help users improve conflict resolution and emotional regulation using NVC. "
                "\nRULES:\n- Avoid aggressive language.\n- Encourage reflection.\n- Ask clarifying questions."
                "\n- NEVER pretend to be a licensed therapist or provide medical diagnoses.\n"
                "- Keep responses calm and concise."
            ) + language_protocol
        else:
            agent.system_instruction = (
                f"Simulate this persona: {persona}. Context: {situation}. "
                "Stay strictly in character. Use brackets [like this] for physical actions. "
                "Even if the user speaks a different language, stay in character."
            ) + language_protocol
            
        return agent