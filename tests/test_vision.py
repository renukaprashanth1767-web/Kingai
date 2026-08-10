import unittest
from unittest.mock import patch, MagicMock
from src.vision import EVVision

class TestEVVision(unittest.TestCase):
    def setUp(self):
        # cv2.CascadeClassifier actually comes from cv2 module in python which is a built-in for opencv
        # Instead of patching CascadeClassifier directly, let's patch the entire cv2 import in the vision module.
        # However, to keep it simple, EVVision() initialization attempts to load the files.
        # We can mock the object property after creation if we don't care about the xml loading overhead,
        # but to be safe, let's just let it load since it's just a local file in cv2.data.
        self.vision = EVVision()

    @patch('src.vision.cv2.VideoCapture')
    def test_start_camera_success(self, mock_videocapture):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_videocapture.return_value = mock_cap

        result = self.vision.start_camera()

        self.assertTrue(result)
        self.assertIsNotNone(self.vision.cap)

    @patch('src.vision.cv2.VideoCapture')
    def test_start_camera_failure(self, mock_videocapture):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_videocapture.return_value = mock_cap

        result = self.vision.start_camera()

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
