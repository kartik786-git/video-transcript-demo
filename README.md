## 📺 Watch It in Action

> See this app being built and used step-by-step on **Real World Devs**!

<div align="center">

### ▶️ Complete Build Video

[![Build Video](https://img.youtube.com/vi/Jg0rT_fRvTg/0.jpg)](https://www.youtube.com/watch?v=Jg0rT_fRvTg)

*Click to watch the full video of building this app from scratch.*

### 🎬 Real World Devs — YouTube Channel

[![YouTube](https://img.shields.io/badge/Subscribe-RealWorldDevs-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@realworlddevs)

</div>

### 📊 Live Output Example

Here's what the app produces — a clean, timestamped transcript ready to download:

<img width="1917" height="838" alt="App output example" src="https://github.com/user-attachments/assets/c68afef4-791d-4b73-a524-5e17c0e14973" />

---


# 🎬 Video Transcript Extractor

> Extract timestamped transcripts from local video files or YouTube URLs using **Whisper AI** — no API keys, no accounts, fully offline-capable.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-faster--whisper-9C27B0?style=for-the-badge&logo=openai&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-%230078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🧭 Table of Contents

- [Architecture](#-architecture)
- [Working Flow](#-working-flow)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Features](#-features)
- [Project Structure](#-project-structure)

---

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph Input["🎯 INPUT"]
        direction LR
        A1["🖥️ Local Video / Audio"]
        A2["▶️ YouTube URL"]
    end

    subgraph Front["🚀 FRONT-END"]
        direction LR
        C1["🖥️ CLI app.py"]
        C2["🌐 Streamlit Web UI"]
    end

    subgraph Engine["⚙️ TRANSCRIPTION ENGINE"]
        direction LR
        D1["🔄 engine.transcribe"]
        D2["🎙️ faster-whisper"]
        D3["📥 yt-dlp / API"]
    end

    subgraph Model["🧠 MODEL STORE"]
        direction LR
        M1["📦 download_model.py"]
        M2["📁 models/"]
    end

    subgraph Output["📤 OUTPUT"]
        direction LR
        O1["📝 SRT"]
        O2["💬 VTT"]
        O3["📄 TXT"]
        O4["🧾 JSON"]
    end

    A1 --> C1
    A2 --> C1
    A1 --> C2
    A2 --> C2
    C1 --> D1
    C2 --> D1
    D1 --> D2
    D1 --> D3
    M1 --> M2
    M2 -.-> D2
    D2 --> O1
    D2 --> O2
    D2 --> O3
    D2 --> O4

    style A1 fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    style A2 fill:#FFEBEE,stroke:#D32F2F,stroke-width:2px
    style C1 fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    style C2 fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    style D1 fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
    style D2 fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
    style D3 fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
    style M1 fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    style M2 fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    style O1 fill:#FFFDE7,stroke:#F9A825,stroke-width:2px
    style O2 fill:#FFFDE7,stroke:#F9A825,stroke-width:2px
    style O3 fill:#FFFDE7,stroke:#F9A825,stroke-width:2px
    style O4 fill:#FFFDE7,stroke:#F9A825,stroke-width:2px
```

---

## 🔄 Working Flow

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant F as 🖥️ Front-end (CLI / Streamlit)
    participant E as ⚙️ Engine
    participant W as 🎙️ Whisper (faster-whisper)
    participant M as 📦 Model Store
    participant O as 📤 Output Files

    U->>F: Provide video file or YouTube URL
    F->>E: Call engine.transcribe()
    alt YouTube URL
        E->>E: Fetch via yt-dlp / YouTube API
    else Local file
        E->>E: Read audio stream
    end
    E->>M: Check / load Whisper model
    M-->>E: Model available (offline-ready)
    E->>W: Run speech-to-text
    W-->>E: Return timed segments
    E-->>F: Return transcript segments
    F->>O: Save SRT / VTT / TXT / JSON
    O-->>U: Ready to download 🎉
```

---

## 👶 No Tech Skills? No Problem!

> If you are **not a developer** — just follow these 4 simple steps. No commands, no typing, no coding.

### ✅ One-time Setup (takes ~5 minutes)

1. **Install Python** (free, one time only)
   - Go to 👉 [python.org/downloads](https://www.python.org/downloads/)
   - Click the big **"Download Python"** button and install it.
   - ⚠️ **Important:** during install, tick the box that says **"Add Python to PATH"**.

2. **Double-click `setup.bat`**
   - It lives in the same folder as this file.
   - Let it run — it will install everything and download the AI models automatically.
   - Just wait and watch. You don't need to press anything until the end.

3. **When it asks "Launch the web app now? [Y/N]"** → press **Y** and press **Enter**.
   - Your browser will open the app automatically. 🎉

### 🖱️ How to Use the App (every day)

1. A page opens in your browser called **"Video Transcript Extractor"**.
2. Choose what you have:
   - **YouTube URL** → paste a video link, *or*
   - **Upload file** → click "Browse files" and pick your video.
3. Click the big **Transcribe** button. ⏳
4. Wait a little (first run can take a few minutes — be patient). ☕
5. Your transcript appears on screen.
6. Click **Download .srt / .txt / .json** to save it to your computer. 📥

> **Trouble?** Make sure you did **Step 1** (Python with "Add to PATH"), then run `setup.bat` again.

---

## 🚀 Quick Start

> **Prerequisites:** [Python 3.10+](https://python.org) with *Add to PATH* enabled.

### 🪟 Windows (Recommended)

```batch
setup.bat
```

This script creates a virtual environment, installs dependencies, downloads Whisper models, and optionally launches the web app.

### 🐍 Manual Setup (Any OS)

```powershell
# 1. Create & activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # macOS / Linux

# 2. Install dependencies (web + CLI)
pip install -r requirements-web.txt

# 3. Download Whisper models (one-time)
python download_model.py --size small medium

# 4. Launch the web app
streamlit run webapp.py
```

Open **http://localhost:8501** in your browser. 🎉

---

## 📖 Usage

### 🌐 Web App

1. Run `streamlit run webapp.py`
2. Choose input type: **YouTube URL** or **Upload file**
3. Pick a Whisper model (`tiny`, `base`, `small`, `medium`, `large-v3`)
4. Click **Transcribe**
5. Download the transcript in your preferred format

### 💻 CLI

```powershell
# Local file
python app.py my_video.mp4

# YouTube URL
python app.py https://www.youtube.com/watch?v=XXXX --model base

# Custom formats & output directory
python app.py clip.webm --format srt vtt --output-dir ./out

# Use GPU with better precision
python app.py video.mp4 --device cuda --compute-type float16

# Offline mode (fail fast if model missing)
python app.py video.mp4 --offline
```

#### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | Whisper model size | `small` |
| `--language` | Audio language code (e.g. `en`) | auto-detect |
| `--format` | Output formats (srt/vtt/txt/json) | `srt txt json` |
| `--output-dir` | Output directory | `./output` |
| `--device` | Compute device (`cpu`/`cuda`) | `cpu` |
| `--compute-type` | CTranslate2 compute type | `int8` |
| `--offline` | Never download anything | off |

---

## ✨ Features

- 🎙️ **Whisper AI** speech-to-text (faster-whisper)
- 📹 **Local & YouTube** video support
- 🧠 **Multiple models** — tiny, base, small, medium, large-v3
- 📦 **Multiple formats** — SRT, VTT, TXT, JSON
- 🔌 **CLI + Web UI** — Streamlit dashboard included
- 📴 **Offline mode** — models cached locally, no tokens needed
- ⚡ **GPU support** — CUDA with `float16` compute

---

## 📂 Project Structure

```
.
├── app.py                  # 🖥️ CLI entry point
├── webapp.py               # 🌐 Streamlit web UI
├── download_model.py       # 📦 Whisper model downloader
├── setup.bat               # 🪟 One-time Windows setup
├── requirements.txt        # ⚙️ Core deps (faster-whisper, yt-dlp)
├── requirements-web.txt    # 🌐 Web UI deps (streamlit, pandas)
├── models/                 # 🧠 Downloaded Whisper models
├── output/                 # 📤 Generated transcripts
├── transcript_video/       # 📚 Core package (engine, models, outputs)
└── README.md               # 📖 This file
```

---



<div align="center">

**Made with ❤️ — No API keys. No accounts. Just transcripts.**

</div>
