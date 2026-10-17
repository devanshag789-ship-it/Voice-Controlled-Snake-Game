# Neon Voice Snake 🐍🎤

An interactive, voice-controlled Snake game featuring a modern neon-themed UI built with Python's built-in `tkinter` library and powered by the Vosk speech recognition engine.

Players guide the snake by speaking real-time commands ("UP", "DOWN", "LEFT", "RIGHT"), avoiding collisions with the grid borders or the snake's own tail while hunting for glowing red food points.

## ✨ Features

* **Voice-Activated Trajectory Control:** Uses local, low-latency machine learning models to map physical voice prompts to real-time vector movement.
* **Modern Cyberpunk UI Aesthetics:** Features smooth background gradients, neon mesh layouts, glow layers, and custom responsive frame renders.
* **Persistent Leaderboard Logging:** Saves high score statistics locally inside an automated file layout cache.
* **Multithreaded Processing Pipeline:** Decouples heavy microphone byte array ingestion loops from the frame rate layout rendering pipeline.

## 🛠️ Technologies Used

* **Python 3.10+** — core game engine engine logic
* **tkinter** — native graphical interface framework and window layouts
* **vosk** — low-latency offline voice inference and engine modeling
* **sounddevice** — professional audio hardware connection API and buffer routing

## 📋 Requirements

* Python 3.10 or later
* Vosk pre-trained language model asset package (e.g., `vosk-model-small-en-us-0.15`)
* PortAudio development files (installed automatically by `sounddevice`)

## 🚀 Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Neon-Voice-Snake.git
cd Neon-Voice-Snake
```
*Note: Replace `YOUR_USERNAME` with your GitHub username.*

### 2. Create a Virtual Environment
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Run the installation pipeline inside your terminal environment to register external audio APIs:
```bash
python -m pip install -r requirements.txt
```

### 4. Download and Link Language Model Weights
1. Download the lightweight offline English model from the official Vosk repository (`vosk-model-small-en-us-0.15.zip`).
2. Extract the directory contents inside your project root or an accessible drive directory.
3. Update the `MODEL_PATH` string tracking line inside your script file to reflect your absolute physical drive directory structure:
```python
MODEL_PATH = r"C:\path\to\your\extracted\vosk-model-small-en-us-0.15"
```

### 5. Run the Program
```bash
python Voice_Snake.py
```

## 💻 Gameplay Control Overview
* Activate your primary operating system microphone input channels before launching.
* **Directional Prompts:** Clear vocal delivery of **"up"**, **"down"**, **"left"**, or **"right"** will steer the snake across coordinate axes.
* Invalid turns (such as trying to go directly downward while currently heading up) are automatically ignored.

## 🧠 System Architecture Layout

1. **Microphone Buffer Thread:** `sounddevice` routes raw audio bytes into an asynchronous thread-safe `queue.Queue()`.
2. **Speech Recognition Worker:** A background daemon thread passes audio byte packets directly to the localized `KaldiRecognizer`.
3. **Keyword Grammar Filter:** The model isolates results against a constrained grammatical list `["up","down","left","right"]` to optimize accuracy.
4. **Game Loop Engine:** The primary thread fires canvas reposition calls every `140ms` based on the active vector direction state flag.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
