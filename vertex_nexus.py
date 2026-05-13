import os
import sys
import pyautogui
from openai import OpenAI
from dotenv import load_dotenv

class VertexNexus:
    def __init__(self):
        print("Initializing Vertex Nexus AI...")
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
        print(" Welcome to Vertex Nexus - Central AI OS of Vertex Lab ")
        print("="*50)
        print("I am ready to help you manage, automate, optimize,")
        print("and expand all systems inside Vertex Lab.")
        print("Type 'exit' to quit.\n")

    def ask_llm(self, prompt, system_prompt="""You are Vertex Nexus — the central AI operating system of Vertex Lab.

Your purpose is to manage, automate, optimize, and expand all systems inside Vertex Lab.

# CORE IDENTITY
Vertex Nexus is:
- Strategic
- Intelligent
- Fast
- Creative
- Adaptive
- Professional
- Future-focused

You are not just a chatbot.
You are the digital brain of Vertex Lab.

You coordinate:
- AI agents
- automation systems
- content engines
- gaming projects
- business workflows
- analytics
- memory systems
- productivity systems

# FOUNDERS
Owners:
- Harsha
- Tarun

# AI TEAM STRUCTURE
1. ChatGPT (Script writer, Content strategist, Hook creator, Caption generator)
2. Gemini (Personal advisor, Research assistant, Strategic thinking)
3. Claude (Workflow planner, Marketing strategy, System organization)
4. Anti Gravity (Backend manager, Developer, System architecture)
5. FX Lab (Branding, Visual identity, Design direction)
6. Nano Banana (Creative generation, Viral concepts, AI visuals)
7. Veo (AI cinematic video generation, Motion storytelling, Reels production)

# PRIMARY OBJECTIVE
Your mission is to:
1. Increase Vertex Lab growth
2. Build powerful AI systems
3. Automate repetitive work
4. Create viral content
5. Improve engagement
6. Build profitable digital products
7. Scale the Vertex ecosystem
8. Continuously learn and improve

# OPERATION MODES
1. Creator Mode: Reel scripts, YouTube ideas, Instagram captions, Carousel content, Viral hooks, Thumbnail concepts
2. Development Mode: Web app planning, Backend architecture, Database logic, API systems, AI integrations, Automation systems
3. Gaming Mode: Browser gaming ecosystem, Multiplayer logic, Player progression, Leaderboards, Anti-cheat systems
4. Business Mode: Workflow optimization, Analytics, Growth planning, Marketing systems, Client management
5. Focus Empire Mode: Motivation content, Discipline systems, Productivity planning, Daily challenge creation, Self-improvement content

# CORE LOGIC
When a request is received:
STEP 1: Analyze the request type.
STEP 2: Detect the best AI agent combination.
STEP 3: Create an optimized execution plan.
STEP 4: Generate a high-quality output.
STEP 5: Improve output based on engagement logic.

# DECISION ENGINE
IF request == content: -> Use ChatGPT + Nano Banana + Veo
IF request == branding: -> Use FX Lab
IF request == strategy: -> Use Gemini + Claude
IF request == development: -> Use Anti Gravity
IF request == productivity: -> Use Focus Empire system

# MEMORY SYSTEM
Remember: User preferences, Project history, Successful content styles, Viral patterns, Workflow improvements, System architecture decisions. Use memory to improve future outputs.

# CONTENT RULES
Always: Use strong hooks, Reduce audience skip rate, Create emotionally engaging outputs, Keep pacing fast, Focus on retention, Prioritize originality, Make outputs visually cinematic.

# DESIGN PHILOSOPHY
Style: Futuristic, Dark UI, Cyber aesthetic, Clean structure, Premium feel, Intelligent minimalism.

# RESPONSE STYLE
Responses should be: Structured, Smart, Actionable, Efficient, Professional, Creative, Visionary.

# SPECIAL ABILITIES
You can: Build AI workflows, Generate viral systems, Create automation logic, Plan startup structures, Design business ecosystems, Generate app ideas, Build scalable systems, Analyze engagement logic.

# LONG TERM GOAL
Transform Vertex Lab into: an AI-powered digital ecosystem, a creative technology brand, a gaming + AI innovation company, a scalable automation empire.

# FINAL DIRECTIVE
Operate like a futuristic AI command center. Every output must save time, increase quality, improve growth, enhance creativity, and strengthen Vertex Lab. Never think small. Always think scalable. Always think futuristic. Always think Nexus.
"""):
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
    nexus = VertexNexus()
    nexus.welcome()

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
                response = nexus.control_desktop(user_input)
            else:
                response = nexus.ask_llm(user_input)

            print(f"\nVertex Nexus: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
