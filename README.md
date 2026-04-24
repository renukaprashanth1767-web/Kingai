# Ganesh AI - Your Personal Startup & Coding Assistant

Ganesh is an AI assistant designed to help you create a startup, write code, build applications, and even control your computer's desktop to perform automated tasks.

## Step-by-Step Setup Guide

Follow these steps to get Ganesh up and running on your machine.

### 1. Prerequisites
- **Python 3.8+**: Ensure you have Python installed. You can check your version by running `python --version` or `python3 --version`.
- **OpenAI API Key**: Ganesh uses OpenAI to power its intelligence. You'll need an API key from [platform.openai.com](https://platform.openai.com/).

### 2. Setting Up the Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

Open your terminal or command prompt and navigate to your project directory.

Create the virtual environment using `python -m venv`:
```bash
python -m venv ganesh_env
```

Activate the virtual environment:
- On **Windows**:
  ```bash
  ganesh_env\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source ganesh_env/bin/activate
  ```

### 3. Installing Dependencies
With your virtual environment activated, install the required packages using `python -m pip`.

```bash
python -m pip install -r requirements.txt
```

*(If you don't have a `requirements.txt` yet, Ganesh relies on libraries like `openai`, `pyautogui`, and `python-dotenv`. You can install them manually: `python -m pip install openai pyautogui python-dotenv`)*

### 4. Configuration
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Running Ganesh
You can now run the Ganesh AI assistant:
```bash
python ganesh.py
```

## Features

- **Startup Advisor**: Ask Ganesh for business strategies, market analysis, and product ideas.
- **Coding Assistant**: Ganesh can write, debug, and explain code for you.
- **Desktop Control**: Using `pyautogui`, Ganesh can perform tasks on your computer, such as moving the mouse, clicking, and typing. *Use this feature with caution!*

## Example Usage

When you run `ganesh.py`, you will enter an interactive shell. Here are some things you can ask:
- *"Help me come up with a name for a new AI startup."*
- *"Write a Python script to scrape a website."*
- *"Move my mouse to the center of the screen."*
