# Vertex Nexus - Central AI Operating System of Vertex Lab

Vertex Nexus is an AI assistant designed to help you manage, automate, optimize, and expand all systems inside Vertex Lab, and even control your computer's desktop to perform automated tasks.

## Step-by-Step Setup Guide

Follow these steps to get Vertex Nexus up and running on your machine.

### 1. Prerequisites
- **Python 3.8+**: Ensure you have Python installed. You can check your version by running `python --version` or `python3 --version`.
- **OpenAI API Key**: Vertex Nexus uses OpenAI to power its intelligence. You'll need an API key from [platform.openai.com](https://platform.openai.com/).

### 2. Setting Up the Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

Open your terminal or command prompt and navigate to your project directory.

Create the virtual environment using `python -m venv`:
```bash
python -m venv nexus_env
```

Activate the virtual environment:
- On **Windows**:
  ```bash
  nexus_env\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source nexus_env/bin/activate
  ```

### 3. Installing Dependencies
With your virtual environment activated, install the required packages using `python -m pip`.

```bash
python -m pip install -r requirements.txt
```

*(If you don't have a `requirements.txt` yet, Vertex Nexus relies on libraries like `openai`, `pyautogui`, and `python-dotenv`. You can install them manually: `python -m pip install openai pyautogui python-dotenv`)*

### 4. Configuration
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Running Vertex Nexus
You can now run the Vertex Nexus AI assistant:
```bash
python vertex_nexus.py
```

## Features

- **Creator Mode**: Reel scripts, YouTube ideas, Instagram captions, Carousel content, Viral hooks, Thumbnail concepts.
- **Development Mode**: Web app planning, Backend architecture, Database logic, API systems, AI integrations, Automation systems.
- **Gaming Mode**: Browser gaming ecosystem, Multiplayer logic, Player progression, Leaderboards, Anti-cheat systems.
- **Business Mode**: Workflow optimization, Analytics, Growth planning, Marketing systems, Client management.
- **Focus Empire Mode**: Motivation content, Discipline systems, Productivity planning, Daily challenge creation, Self-improvement content.
- **Desktop Control**: Using `pyautogui`, Vertex Nexus can perform tasks on your computer, such as moving the mouse, clicking, and typing. *Use this feature with caution!*

## Example Usage

When you run `vertex_nexus.py`, you will enter an interactive shell. Here are some things you can ask:
- *"Create a reel script using Creator Mode."*
- *"Plan backend architecture using Development Mode."*
- *"Move my mouse to the center of the screen."*
