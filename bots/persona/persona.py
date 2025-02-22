import os
from openai import OpenAI


class Persona:
    def __init__(self, config: dict, bot_token: str):
        self.intro = config.get("intro", "You are a helpful assistant.")
        self.llm_provider = config.get("llm_provider", "gpt")
        self.bot_token = bot_token
        self.history = []  # List of {"role": str, "content": str}

    def add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def generate_response(self) -> str:
        if not self.history:
            self.add_to_history("system", self.intro)
        try:
            if self.llm_provider == "gpt":
                client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                chat_completion = client.chat.completions.create(
                    messages=self.history,
                    model="gpt-4o",
                )
                response = chat_completion.choices[0].message.content
            elif self.llm_provider == "deepseek":
                client = OpenAI(
                    api_key=os.environ.get("DEEPSEEK_API_KEY"),
                    base_url="https://api.deepseek.com",
                )
                chat_completion = client.chat.completions.create(
                    messages=self.history,
                    model="deepseek-chat",
                )
                response = chat_completion.choices[0].message.content
            else:
                response = "LLM not supported"
            self.add_to_history("assistant", response)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Something went wrong, please try again later."

    def process_message_text(self, message: str) -> str:
        self.add_to_history("user", message)
        return self.generate_response()
