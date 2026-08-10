import unittest
from unittest.mock import patch
from src.control import EVControl

class TestEVControl(unittest.TestCase):
    def setUp(self):
        self.control = EVControl()

    @patch('src.control.pyautogui.moveTo')
    @patch('src.control.pyautogui.size', return_value=(1920, 1080))
    def test_mouse_center(self, mock_size, mock_moveTo):
        response = self.control.control_mouse('center')
        mock_moveTo.assert_called_once_with(960.0, 540.0, duration=0.5)
        self.assertEqual(response, "Moved mouse to the center of the screen.")

    @patch('src.control.pyautogui.write')
    def test_type_text(self, mock_write):
        response = self.control.type_text("Hello World")
        mock_write.assert_called_once_with("Hello World", interval=0.05)
        self.assertEqual(response, "Typed: Hello World")

    @patch('src.control.subprocess.run')
    def test_execute_python_code(self, mock_subprocess):
        # Mock successful code execution
        mock_subprocess.return_value.stdout = "Code execution success"
        mock_subprocess.return_value.stderr = ""

        response = self.control.execute_python_code("print('test')")

        mock_subprocess.assert_called_once()
        self.assertIn("Code execution success", response)

if __name__ == '__main__':
    unittest.main()
