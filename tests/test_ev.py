import unittest
from unittest.mock import patch, MagicMock
from src.ev import EVBrain

class TestEVBrain(unittest.TestCase):
    @patch('src.ev.pipeline')
    @patch('src.ev.AutoModelForCausalLM.from_pretrained')
    @patch('src.ev.AutoTokenizer.from_pretrained')
    def test_ev_brain_initialization(self, mock_tokenizer, mock_model, mock_pipeline):
        # Mocking the pipeline generation to return a dummy response
        mock_pipeline.return_value = MagicMock(return_value=[{"generated_text": "I am E.V."}])

        brain = EVBrain(model_name="mock-model")

        self.assertIsNotNone(brain.generator)
        response = brain.generate_response("Who are you?")
        self.assertIn("I am E.V.", response)

    @patch('src.ev.AutoTokenizer.from_pretrained', side_effect=Exception("Model loading failed"))
    def test_ev_brain_initialization_failure(self, mock_tokenizer):
        brain = EVBrain(model_name="bad-model")

        self.assertIsNone(brain.generator)
        response = brain.generate_response("Test")
        self.assertEqual(response, "E.V. Brain is offline. Model failed to load.")

if __name__ == '__main__':
    unittest.main()
