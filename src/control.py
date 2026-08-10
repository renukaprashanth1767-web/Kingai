import os
import subprocess
import platform
import logging
import pyautogui
from typing import Optional

logger = logging.getLogger(__name__)

# Security measure for pyautogui
pyautogui.FAILSAFE = True

class EVControl:
    """
    E.V. Device and Application Control Module.
    Handles opening apps, moving the mouse, typing, and executing local code.
    """
    def __init__(self):
        self.os_name = platform.system()
        logger.info(f"EVControl initialized on {self.os_name} platform.")

    def open_application(self, app_name: str) -> str:
        """
        Attempts to open an application based on the OS.
        """
        try:
            if self.os_name == "Windows":
                # Very basic Windows opening
                os.startfile(app_name)
            elif self.os_name == "Darwin":
                # macOS opening
                subprocess.Popen(["open", "-a", app_name])
            else:
                # Linux opening (assuming app_name is an executable in PATH)
                subprocess.Popen([app_name])

            return f"Successfully launched {app_name}."
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return f"Failed to launch {app_name}. Error: {e}"

    def control_mouse(self, action: str, x: int = 0, y: int = 0) -> str:
        """
        Controls the mouse.
        action: 'move', 'click', 'center'
        """
        try:
            if action == 'center':
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=0.5)
                return "Moved mouse to the center of the screen."
            elif action == 'move':
                pyautogui.moveTo(x, y, duration=0.5)
                return f"Moved mouse to ({x}, {y})."
            elif action == 'click':
                pyautogui.click()
                return "Clicked mouse."
            else:
                return f"Unknown mouse action: {action}"
        except Exception as e:
            logger.error(f"Mouse control failed: {e}")
            return f"Failed to control mouse: {e}"

    def type_text(self, text: str) -> str:
        """
        Types the given text using the keyboard.
        """
        try:
            pyautogui.write(text, interval=0.05)
            return f"Typed: {text}"
        except Exception as e:
            logger.error(f"Keyboard control failed: {e}")
            return f"Failed to type text: {e}"

    def execute_python_code(self, code: str, filepath: str = "ev_temp_workspace.py") -> str:
        """
        Saves the provided Python code to a file and executes it.
        WARNING: This executes arbitrary code on the local machine.
        """
        try:
            with open(filepath, 'w') as f:
                f.write(code)

            logger.info(f"Executing code in {filepath}...")
            result = subprocess.run(["python", filepath], capture_output=True, text=True, timeout=30)

            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"

            return f"Execution completed. Output:\n{output.strip()}"
        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            logger.error(f"Failed to execute code: {e}")
            return f"Failed to execute code: {e}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ctrl = EVControl()
    # Simple test
    print(ctrl.execute_python_code("print('E.V. Coding test successful!')"))
