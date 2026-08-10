import os
import sys
import logging
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from src.control import EVControl

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EVBrain:
    """
    E.V. Local AI Brain
    Uses Hugging Face Transformers to run a local language model for conversation and coding.
    Requires no API keys.
    """
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        logger.info(f"Initializing E.V. AI Brain with model: {model_name}")
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            logger.info("E.V. Brain initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize local model: {e}")
            self.generator = None

        self.control = EVControl()

    def handle_command(self, user_input: str) -> str:
        """
        Parses the user input and routes it to the appropriate control module
        or generates a text response.
        """
        user_input_lower = user_input.lower()

        # Simple rule-based routing for hardware/app control
        if user_input_lower.startswith("open "):
            app_name = user_input.split(" ", 1)[1]
            return self.control.open_application(app_name)

        elif user_input_lower.startswith("move mouse"):
            return self.control.control_mouse('center')

        elif user_input_lower.startswith("type "):
            text = user_input.split(" ", 1)[1]
            return self.control.type_text(text)

        elif user_input_lower.startswith("run code:"):
            code = user_input.split("run code:", 1)[1].strip()
            return self.control.execute_python_code(code)

        else:
            return self.generate_response(user_input)

    def generate_response(self, prompt: str, max_length: int = 200) -> str:
        """
        Generates a text response using the local model.
        """
        if not self.generator:
            return "E.V. Brain is offline. Model failed to load."

        try:
            # Simple prompt formatting for instruction models
            formatted_prompt = f"<|system|>\nYou are E.V., a highly advanced local AI assistant. You can write code, control devices, and analyze camera feeds.\n<|user|>\n{prompt}\n<|assistant|>\n"

            response = self.generator(
                formatted_prompt,
                max_new_tokens=max_length,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                return_full_text=False
            )
            return response[0]["generated_text"].strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error processing query: {e}"

if __name__ == "__main__":
    brain = EVBrain()
    print("\nE.V. Online. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("E.V. shutting down...")
                break
            if not user_input.strip():
                continue

            print("E.V. is processing...")
            response = brain.handle_command(user_input)
            print(f"E.V.: {response}\n")
        except KeyboardInterrupt:
            print("\nE.V. shutting down...")
            break
