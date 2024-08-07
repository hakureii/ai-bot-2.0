import os
import shutil
from groq import Groq

class Ai:
    def __init__(self):
        self.model = "llama-3.1-70b-versatile"
        # self.model = "llama3-70b-8192"
        self.client = Groq(api_key=os.getenv("GROQ"))
        with open("system.json") as file:
            import json
            self.history = [json.load(file)]

    def response(self, message: str = ""):
        self.update_history(role="user",message=message)
        ai_response = self.client.chat.completions.create(
                model = self.model,
                max_tokens = 512,
                messages=self.history
        )
        self.update_history(message=ai_response.choices[0].message.content)
        return ai_response.choices[0].message.content

    def update_history(self, role: str = "assistant", message: str = ""):
        self.history.append(
            {
                "role": role,
                "content": message
            }
        )

ai = Ai()

def main():
    os.system("clear")
    print("Welcome to the AI Chat! Type 'q' to quit.")
    while True:
        print("_" * shutil.get_terminal_size().columns)
        prompt = input("\nYour Input: ")

        if prompt.lower() == "q":
            print("Goodbye!")
            break

        response = ai.response(prompt)
        print(f"\n\033[0;34m{response}\033[0m\n")

if __name__ == "__main__":
    main()
