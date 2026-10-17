# 🎓 NPTEL PrepMaster AI - PDF to Exam Prep & Quiz Simulator

An AI-powered web platform tailored specifically for **NPTEL (SWAYAM - IIT/IISc)** examination preparation. Simply upload any NPTEL lecture slides, textbook PDF, or assignment sheet, and the platform instantly transforms it into a complete, interactive exam preparation kit.

---

## 🌟 Core Features

### 1. 📄 Instant PDF Parsing & Extraction
- **Drag & Drop Upload:** Upload weekly lecture slide decks, course notes, or assignment problem sheets (up to 25MB).
- **Intelligent Text Extraction:** Extracts clean text, calculates word count, detects titles, and estimates revision time.
- **Preloaded NPTEL Modules Included:** Test immediately with 1-click on preloaded courses:
  - *Cloud Computing & Virtualization (Week 3)*
  - *Data Structures & Algorithms - Graphs & Shortest Paths (Week 4)*
  - *Deep Learning & Convolutional Neural Networks (Week 6)*
  - *Or load the bundled `sample_nptel_lecture.pdf`*

### 2. 📝 Authentic NPTEL / TCS iON Exam Simulator
- **True-to-Life Exam Interface:** Simulated interface modeled directly after the official NPTEL/TCS iON proctored examination.
- **Question Palette Navigation:**
  - 🟢 **Answered**
  - 🟣 **Marked for Review**
  - 🟣🟢 **Answered & Marked for Review**
  - 🔴 **Not Answered**
  - ⚪ **Not Visited**
- **Countdown Timer:** Timed simulation with auto-submission when the clock runs out.
- **Exam Question Formats:** Supports both Single Choice (MCQ) and Multiple Correct (MSQ) questions.
- **Scorecard & NPTEL Certification Tiers:**
  - 🥇 **Elite + Gold** ($\ge 90\%$)
  - 🥈 **Elite + Silver** ($75\% - 89\%$)
  - 🎖️ **Elite** ($60\% - 74\%$)
  - 📜 **Successfully Qualified** ($40\% - 59\%$)
  - ⚠️ **Needs Revision** ($< 40\%$)
- **Celebration & Detailed Review Mode:** Confetti burst on high scores, side-by-side solution explanations, and filter to review only mistakes.

### 3. 📌 High-Yield Key Points & Formulas Cheat Sheet
- Core definitions, formulas, and theorems rendered beautifully with **KaTeX math typography**.
- Common **NPTEL Exam Traps** highlighting frequent student misconceptions.
- Interactive checkboxes so students can check off points as they master them.
- One-click copy to clipboard.

### 4. 📖 Deep Conceptual Explanations & Analogies
- Topic-by-topic breakdowns.
- Real-world intuitive analogies making complex engineering topics easy to grasp.
- Step-by-step mathematical and algorithmic derivations.

### 5. 🗂️ Interactive 3D Flashcards
- Smooth 3D card flips (click or press `Space`).
- Spaced-repetition revision with Next, Previous, and Shuffle controls.

### 6. 💬 NPTEL AI Doubt Solver (Teaching Assistant)
- Ask any doubt grounded in the uploaded PDF.
- Pre-made quick-prompt chips for common doubts.
- Step-by-step professor-style markdown answers with LaTeX equations.

### 7. 📥 Export & Study Offline
- Download complete question bank as **Structured JSON**.
- Download formatted notes as **Markdown (`.md`)**.
- Clean **Print-Ready** layout to print hardcopy revision sheets.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Python 3.13 tested and supported)
- Modern web browser (Chrome, Edge, Firefox, Brave)

### 1-Click Launch (Windows)
Double-click `run.bat` in the project folder. It will start the server and open your browser automatically at:
```
http://127.0.0.1:8000
```

### Manual Command Line Launch
1. Open PowerShell or Command Prompt in this folder:
```powershell
pip install -r requirements.txt
```
2. Start the web application:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
3. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🔑 Google Gemini API Key (Optional but Recommended)

The application features a **Smart Offline / Demo Engine** that works immediately without any key.

To unlock **live, custom AI analysis** powered by Google's latest **Gemini 2.5 Flash**:
1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey) (Takes ~30 seconds, 100% free, no credit card required).
2. Click **"Gemini API Key"** in the top navigation bar of the website and paste your key.
3. Alternatively, save it in a `.env` file:
   ```env
   GEMINI_API_KEY=AIzaSyYourKeyHere...
   ```

---

## 📁 Project Structure

```
├── app.py                     # FastAPI backend & REST API endpoints
├── pdf_processor.py           # PDF text extractor, page mapper & metadata analyzer
├── ai_generator.py            # Gemini 2.5 Flash integration + offline fallback synthesis
├── sample_data.py             # Preloaded NPTEL courses (Cloud, DSA, Deep Learning)
├── generate_sample_pdf.py     # Script to generate authentic sample NPTEL lecture PDF
├── requirements.txt           # Python backend dependencies
├── run.bat                    # One-click Windows starter script
├── .env.example               # Environment variables template
├── sample_nptel_lecture.pdf   # Pre-generated sample PDF for instant testing
└── static/
    ├── index.html             # Single Page Application UI
    ├── css/
    │   └── custom.css         # 3D flashcards, TCS iON palette, print styling
    └── js/
        └── app.js             # Reactive quiz engine, timer, tabs & API communication
```

---

## 🎯 Technologies Used
- **Backend:** Python 3.13, FastAPI, Uvicorn, PyPDF, ReportLab, Python-Multipart
- **AI / LLM:** Google GenAI SDK (`google-genai`), Gemini 2.5 Flash / Gemini 1.5 Flash
- **Frontend:** HTML5, Tailwind CSS, KaTeX (LaTeX math rendering), Marked.js, Canvas-Confetti, FontAwesome Icons
