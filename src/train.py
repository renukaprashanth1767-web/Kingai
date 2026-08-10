import os
import json
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

# Disable wandb logging for training to avoid requiring API keys
os.environ["WANDB_DISABLED"] = "true"

from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import Dataset

logger = logging.getLogger(__name__)

class EVTrainer:
    """
    E.V. Training Module.
    Scrapes data from the internet and fine-tunes the local AI model.
    """
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_name = model_name
        self.data_file = "ev_training_data.jsonl"
        logger.info(f"EVTrainer initialized. Target model: {self.model_name}")

    def fetch_internet_data(self, url: str) -> Optional[str]:
        """
        Scrapes paragraph text from a given URL.
        """
        try:
            logger.info(f"Fetching data from {url}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')

            text_data = " ".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            return text_data
        except Exception as e:
            logger.error(f"Failed to fetch data from {url}: {e}")
            return None

    def build_dataset(self, urls: List[str]) -> bool:
        """
        Fetches data from multiple URLs and saves them into a JSONL file for training.
        Format: {"text": "..."}
        """
        logger.info(f"Building dataset from {len(urls)} URLs...")
        scraped_count = 0

        with open(self.data_file, 'w', encoding='utf-8') as f:
            for url in urls:
                content = self.fetch_internet_data(url)
                if content and len(content) > 100:
                    # Break into smaller chunks to act as training documents
                    chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
                    for chunk in chunks:
                        json.dump({"text": chunk}, f)
                        f.write('\n')
                        scraped_count += 1

        logger.info(f"Dataset built. Total training samples: {scraped_count}")
        return scraped_count > 0

    def load_dataset_from_jsonl(self) -> Dataset:
        """Loads the JSONL dataset into a Hugging Face Dataset object."""
        data = []
        with open(self.data_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return Dataset.from_list(data)

    def train_model(self, output_dir: str = "./ev_brain_custom", epochs: int = 1):
        """
        Fine-tunes the local model using the scraped dataset.
        WARNING: This requires significant memory (RAM/VRAM) depending on the model size.
        """
        if not os.path.exists(self.data_file):
            logger.error("Training data file not found. Run build_dataset first.")
            return

        try:
            logger.info(f"Loading tokenizer and model ({self.model_name}) for training...")
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # Ensure padding token is set
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            model = AutoModelForCausalLM.from_pretrained(self.model_name)

            dataset = self.load_dataset_from_jsonl()

            def tokenize_function(examples):
                return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

            logger.info("Tokenizing dataset...")
            tokenized_datasets = dataset.map(tokenize_function, batched=True)

            # Define training arguments for a fast, local fine-tune
            training_args = TrainingArguments(
                output_dir=output_dir,
                evaluation_strategy="no",
                learning_rate=2e-5,
                weight_decay=0.01,
                per_device_train_batch_size=2,
                num_train_epochs=epochs,
                save_strategy="epoch",
                logging_dir='./logs',
                logging_steps=10,
                report_to="none" # Disable wandb reporting
            )

            # Use Trainer class from transformers
            from transformers import DataCollatorForLanguageModeling
            data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_datasets,
                data_collator=data_collator,
            )

            logger.info("Starting training loop...")
            trainer.train()

            logger.info(f"Training complete. Saving custom E.V. Brain to {output_dir}")
            trainer.save_model(output_dir)
            tokenizer.save_pretrained(output_dir)

        except Exception as e:
            logger.error(f"Training failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trainer = EVTrainer()

    # Test scraping a simple Wikipedia page
    test_urls = ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
    if trainer.build_dataset(test_urls):
        print("Dataset built successfully. Ready for training.")
        # Note: We do not call trainer.train_model() here by default to prevent
        # heavy resource usage during basic execution. User can trigger it manually.
