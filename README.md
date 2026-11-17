# CodeAlpha — AI Internship Projects

Two projects completed during my **Artificial Intelligence internship at CodeAlpha**: real-time object detection with tracking, and a multilingual text translation tool.

## Projects at a Glance

| # | Project | What it does | Tech |
|---|---------|--------------|------|
| 1 | [Object Detection & Tracking](#task-1-object-detection--tracking) | Detects objects in real time and gives each one a persistent tracking ID | YOLOv8, Deep SORT, OpenCV |
| 2 | [Language Translation Tool](#task-2-language-translation-tool) | Translates text between 20+ languages with text-to-speech | Streamlit, deep-translator, gTTS |

## Repository Structure

```text
├── CodeAlpha_ObjectDetectionTracking/
│   ├── detect_track.py
│   └── requirements.txt
├── CodeAlpha_LanguageTranslationTool/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Each project has its own `requirements.txt`, so install dependencies from inside the project folder you want to run.

---

## Task 1: Object Detection & Tracking

Real-time object detection with **YOLOv8** and multi-object tracking with **Deep SORT**. Each detected object gets a label and a persistent tracking ID that stays with it across frames.

### Run

```bash
cd CodeAlpha_ObjectDetectionTracking
pip install -r requirements.txt

# Webcam
python detect_track.py

# Video file, saving the annotated output
python detect_track.py --source video.mp4 --save output.mp4
```

Press `q` to quit.

---

## Task 2: Language Translation Tool

A web app that translates text between **20+ languages** (including Kannada and Hindi) using the Google Translate engine via `deep-translator`.

### Features

- Source and target language selection
- Auto-detect source language
- Copy-to-clipboard button
- Text-to-speech playback (gTTS)

### Run

```bash
cd CodeAlpha_LanguageTranslationTool
pip install -r requirements.txt
streamlit run app.py
```

---

## Tech Stack

- **Language:** Python
- **Computer Vision:** YOLOv8, Deep SORT
- **Web App:** Streamlit
- **Translation and Speech:** deep-translator (Google Translate), gTTS

## Author

**Dhanya B K**
B.E. in Artificial Intelligence and Machine Learning, Vivekananda College of Engineering and Technology, Puttur
