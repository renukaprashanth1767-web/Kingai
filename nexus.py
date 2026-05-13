import os
import sys
import json
import pyautogui
import urllib.request
import platform
import datetime
from openai import OpenAI
from dotenv import load_dotenv

class Nexus:
    def __init__(self):
        print("Initializing Nexus AI (Jarvis Protocol)...")
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

        # Memory setup
        self.memory_file = "nexus_memory.json"
        self.memory = self.load_memory()

    def load_memory(self):
        """Loads conversation history from a JSON file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
        return []

    def save_memory(self):
        """Saves current conversation history to a JSON file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def fetch_online_data(self, url):
        """Fetches basic text content from a URL."""
        try:
            print(f"Fetching data from {url}...")
            # Set a user-agent to avoid being blocked by simple checks
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                # Return first 1000 characters to avoid huge contexts
                return content[:1000] + "\n...[truncated]"
        except Exception as e:
            return f"Error fetching {url}: {e}"

    def get_system_status(self):
        """Returns string containing system info like OS, time, etc."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os_info = platform.system() + " " + platform.release()
        return f"Current Time: {now}\nOS: {os_info}"

    def ask_llm(self, user_input):
        if not self.client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY."

        # Add current input to memory
        self.memory.append({"role": "user", "content": user_input})

        # Build context from memory (limiting to last 10 exchanges to save tokens)
        context_messages = self.memory[-10:]

        system_prompt = (
            "You are Nexus, an advanced, auto-learning AI similar to Jarvis. "
            "You learn from user data (context provided) and can process online data. "
            "You have access to desktop controls. Provide concise, smart responses. "
            "If the user asks for online information, you can ask them to provide a URL starting with 'fetch <url>'."
        )

        messages = [{"role": "system", "content": system_prompt}] + context_messages

        try:
            print("Nexus is thinking...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response.choices[0].message.content

            # Save assistant reply to memory
            self.memory.append({"role": "assistant", "content": reply})
            self.save_memory()

            return reply
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def control_desktop(self, command):
        """Jarvis-like desktop automation."""
        try:
            if "move mouse" in command.lower():
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=1)
                return "Moved mouse to the center of the screen."
            elif "type" in command.lower():
                text = command.lower().split("type")[1].strip().strip("'\"")
                pyautogui.write(text, interval=0.1)
                return f"Typed: {text}"
            else:
                return "Unknown desktop command."
        except Exception as e:
            return f"Failed desktop action: {e}"

    def welcome(self):
        print("\n" + "="*50)
        print(" Welcome to Nexus - Auto-learning Jarvis AI ")
        print("="*50)
        print("I am Nexus. I learn from your data and online sources.")
        print("Type 'exit' to quit.")
        print("Commands: 'fetch <url>', 'status', 'move mouse', 'type <text>'\n")

if __name__ == "__main__":
    nexus = Nexus()
    nexus.welcome()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("Nexus: Shutting down systems. Goodbye.")
                break

            # Handle specific Jarvis commands
            if user_input.lower() == "status":
                response = nexus.get_system_status()
            elif user_input.lower().startswith("fetch "):
                url = user_input.split(" ", 1)[1]
                content = nexus.fetch_online_data(url)
                # Feed this fetched content to the LLM to learn/summarize
                response = nexus.ask_llm(f"I fetched this data from {url}:\n{content}\nSummarize or answer based on this.")
            elif user_input.lower().startswith("move mouse") or user_input.lower().startswith("type"):
                response = nexus.control_desktop(user_input)
            else:
                response = nexus.ask_llm(user_input)

            print(f"\nNexus: {response}\n")

        except KeyboardInterrupt:
            print("\nNexus: Shutting down systems. Goodbye.")
            break
