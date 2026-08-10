import unittest
from unittest.mock import patch, MagicMock
from src.train import EVTrainer
from datasets import Dataset

class TestEVTrainer(unittest.TestCase):
    def setUp(self):
        self.trainer = EVTrainer(model_name="mock-model")

    @patch('src.train.requests.get')
    def test_fetch_internet_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>This is test data.</p><p>More test data.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        text = self.trainer.fetch_internet_data("http://mockurl.com")

        self.assertIn("This is test data.", text)
        self.assertIn("More test data.", text)

    @patch('src.train.requests.get')
    def test_fetch_internet_data_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        text = self.trainer.fetch_internet_data("http://mockurl.com")
        self.assertIsNone(text)

if __name__ == '__main__':
    unittest.main()
