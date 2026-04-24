import os
import sys
import pyautogui
from openai import OpenAI
from dotenv import load_dotenv

class Ganesh:
    def __init__(self):
        print("Initializing Ganesh AI...")
        # Load environment variables
        load_dotenv()

        # Setup OpenAI client
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY environment variable not set. LLM features will not work.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

        # Security measure for pyautogui
        pyautogui.FAILSAFE = True

    def welcome(self):
        print("\n" + "="*50)
        print(" Welcome to Ganesh - Your Startup & Coding AI ")
        print("="*50)
        print("I am ready to help you build your startup, write code,")
        print("and control your desktop environment.")
        print("Type 'exit' to quit.\n")

    def ask_llm(self, prompt, system_prompt="You are Ganesh, an expert AI assistant that helps build startups, write high-quality code, and can automate desktop tasks. Provide concise and actionable advice."):
        if not self.client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY in your .env file."

        try:
            print("Thinking...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred while calling the LLM: {str(e)}"

    def control_desktop(self, command):
        """
        Executes basic desktop commands.
        Note: This is a simplified version. For full capability, the LLM should output structured
        commands (like JSON) that are parsed and executed here.
        """
        try:
            if "move mouse" in command.lower():
                # Just an example: move mouse to the center of the screen
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=1)
                return "Moved mouse to the center of the screen."
            elif "type" in command.lower():
                # Extract text to type (very basic extraction)
                text_to_type = command.lower().split("type")[1].strip().strip("'\"")
                pyautogui.write(text_to_type, interval=0.1)
                return f"Typed: {text_to_type}"
            else:
                return "Desktop command not recognized or supported yet."
        except Exception as e:
            return f"Failed to execute desktop command: {str(e)}"

if __name__ == "__main__":
    ganesh = Ganesh()
    ganesh.welcome()

    # Simple interactive loop
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if user_input.strip() == "":
                continue

            # Basic routing: if it looks like a desktop command, try that first
            if user_input.lower().startswith("move mouse") or user_input.lower().startswith("type"):
                response = ganesh.control_desktop(user_input)
            else:
                response = ganesh.ask_llm(user_input)

            print(f"\nGanesh: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
