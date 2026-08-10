# E.V. AI - Tactical Brain & Vision System

E.V. is a locally running, open-source AI assistant designed for desktop automation, live tracking (OpenCV), and internet data learning. It operates **100% locally** and does not require any paid APIs or cloud keys.

## Features

1. **Local LLM Brain**: Powered by Hugging Face `transformers` and lightweight models (e.g., TinyLlama), enabling native chat and offline coding assistance.
2. **Tactical Vision & Tracking**: Uses OpenCV Haar Cascades to perform real-time tracking of living things (faces and bodies) through the webcam, complete with a tactical HUD.
3. **App & Device Control**: Integrated `pyautogui` and system subprocesses to open applications, control the mouse/keyboard, and execute raw Python code autonomously.
4. **Internet Learning Pipeline**: Includes a scraping script to fetch textual data from web URLs and a fine-tuning pipeline to update E.V.'s local knowledge base.

## Installation

Ensure you have Python 3.8+ installed.

1. **Clone the repository and set up a virtual environment**:
   ```bash
   python -m venv ev_env
   source ev_env/bin/activate  # On Windows, use `ev_env\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This project pins `numpy<2` to ensure compatibility with local OpenCV built binaries).*

## Usage Guide

### 1. Running the Core AI Brain (Chat & Control)
To launch E.V.'s interactive terminal:
```bash
python src/ev.py
```
**Commands you can try:**
- standard chat (e.g., `"Hello, who are you?"`)
- `open [app_name]` (e.g., `"open notepad"` or `"open calculator"`)
- `move mouse` (moves mouse to center of the screen)
- `type [text]` (e.g., `"type Hello World"`)
- `run code: [python code]` (e.g., `"run code: print('E.V. test successful!')"`)

### 2. Running Tactical Vision (Tracking)
To launch the webcam HUD and living things tracking:
```bash
python src/vision.py
```
*Press `q` on the video window to quit.*

### 3. Training E.V. on Internet Data
To scrape URLs and fine-tune the local AI model on the gathered data:
```bash
python src/train.py
```
*Modify the `test_urls` list in `src/train.py` to point to the data you wish E.V. to learn.*

## Running Tests
To ensure all modules are functioning correctly, you can run the test suite:
```bash
python -m unittest discover tests/
```
*(If running on a headless server, prefix with `xvfb-run -a` to support pyautogui/cv2 GUI tests).*
