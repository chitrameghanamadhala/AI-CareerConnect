# 🚀 AI Career Connect — Beginner's Guide & Documentation

Welcome to **AI Career Connect**! This project is an intelligent career guidance web application. It acts like a personal career advisor powered by Artificial Intelligence (AI). You can talk to it using text or your voice, and it gives you personalized career recommendations, salary details, and live visual charts.

---

## 💡 What Does This Project Do? (In Simple Words)

Imagine having an AI career counselor in your browser:
1. **User Sign Up & Login**: You create an account and log in safely.
2. **Talk to AI (Text or Voice)**: You can type questions like *"What jobs can I get with Python skills?"* or click the microphone button to **speak out loud**.
3. **Listen to Responses**: The AI can **read its answer out loud** to you using a speech synthesizer.
4. **Smart Recommendations**: The system remembers your conversation, analyzes your skills, and suggests matching career paths with average salaries and growth rates.
5. **Dynamic Dashboard**: A modern visual dashboard showing interactive bar charts of your activity and quick stat cards.

---

## 🛠️ The 6 Core Features Explained Simply

| Feature | What It Is | How It Works |
|---|---|---|
| **1. Flask Backend** | The engine of the web app | Built with Python's Flask framework. It controls web pages, routes requests, and connects everything together. |
| **2. SQLite Database** | The memory/storage | A simple, built-in database file (`instance/app.db`) that saves user accounts, career options, and chat history. |
| **3. Mistral AI Integration** | The smart AI counselor | Connects to Mistral AI (a powerful AI model) to answer your career questions intelligently. |
| **4. Speech-to-Text (STT)** | Voice input (Microphone) | Converts what you say into text so you don't have to type. |
| **5. Text-to-Speech (TTS)** | Audio output (Speaker) | Converts the AI's text replies into MP3 audio so you can listen to them. |
| **6. Dynamic Dashboard** | Visual control center | Displays real-time charts (using Chart.js) and summary boxes (total chats, career paths, messages). |

---

## 📁 Project Folder Structure — Why Each Folder Exists

Here is the map of all files in this project and what each one does:

```
AIcareerconnect/
│
├── app/                          # Main Application Folder (All app code lives here)
│   ├── __init__.py               # The App Factory — builds and starts the Flask app cleanly
│   ├── config.py                 # Configuration settings (database URLs, secret keys)
│   ├── extensions.py             # Plugin instances (Database, Login Manager) to avoid code conflicts
│   │
│   ├── models/                   # Database Models (Defines how data is saved in SQLite)
│   │   ├── __init__.py           # Registers all database tables
│   │   ├── user.py               # Saves user accounts & password hashes
│   │   ├── career.py             # Saves career job titles, salaries, and skills
│   │   └── conversation.py       # Saves chat history & messages
│   │
│   ├── routes/                   # Web Page Handlers (Blueprints)
│   │   ├── __init__.py           # Blueprint package loader
│   │   ├── auth.py               # Manages Login, Register, and Logout pages
│   │   ├── dashboard.py          # Manages Dashboard page & chart data (/stats)
│   │   ├── career.py             # Manages Career Recommendations & Search pages
│   │   └── api.py                # REST API for background AJAX calls (AI Chat, STT, TTS)
│   │
│   ├── services/                 # Business Logic Layer (The Heavy Lifting)
│   │   ├── __init__.py           # Services package loader
│   │   ├── mistral_service.py    # Connects to Mistral AI API to generate career advice
│   │   ├── speech_to_text.py     # Transcribes recorded microphone audio into text
│   │   ├── text_to_speech.py     # Converts AI text answers into audio MP3 files
│   │   └── career_analyzer.py    # Analyzes user chat keywords to recommend matching jobs
│   │
│   ├── templates/                # HTML Page Layouts (What you see in the browser)
│   │   ├── base.html             # The master layout (Navigation bar, header, footer)
│   │   ├── auth/                 # Login & Register HTML forms
│   │   ├── dashboard/            # Dashboard layout & widget components (chart, chat, stats)
│   │   └── career/               # Career list & detail view HTML templates
│   │
│   ├── static/                   # CSS Stylesheets, JavaScript Files & Media
│   │   ├── css/                  # Dark-themed modern styles (main.css, dashboard.css)
│   │   ├── js/                   # Interactive scripts (chat.js, speech.js, dashboard.js)
│   │   ├── audio/                # Cache directory where generated MP3 audio files are saved
│   │   └── img/                  # Images and icons
│   │
│   └── utils/                    # Shared Helper Tools
│       ├── decorators.py         # Custom protections (e.g., @login_required)
│       ├── helpers.py            # Text formatting & date/time helpers (e.g., "2 hours ago")
│       └── validators.py         # Form input checkers (checks if emails and passwords are valid)
│
├── migrations/                   # Database version history tracker (Flask-Migrate)
├── tests/                        # Automated unit tests to make sure code works correctly
├── instance/                     # Local storage folder holding your app.db file (Git-ignored)
├── .env                          # Secret key file (holds your MISTRAL_API_KEY)
├── .env.example                  # Template showing which secret variables are required
├── .gitignore                    # Tells Git which secret or temporary files NOT to upload
├── requirements.txt              # List of all Python libraries needed for this project
├── run.py                        # The main file you run to start the application!
├── explaination.txt              # In-depth architectural explanation document
└── README.md                     # This documentation file
```

---

## ⚡ How to Set Up & Run the Project (Step-by-Step)

Follow these easy steps to get the project running on your computer:

### Step 1: Open Terminal in Project Directory
Open your terminal (PowerShell or Command Prompt) and navigate to the project folder:
```bash
cd c:\Users\maggie\Desktop\AIcareerconnect
```

### Step 2: Activate Virtual Environment
```bash
# On Windows:
.\env\Scripts\activate
```

### Step 3: Set Your Mistral AI Key in `.env`
Open the `.env` file in your text editor and add your free Mistral API Key:
```env
MISTRAL_API_KEY=your_actual_mistral_api_key_here
```

### Step 4: Run the Application
```bash
python run.py
```

### Step 5: Open in Browser
Open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 How to Run Tests

To verify that all features, databases, and routes are working properly:

```bash
.\env\Scripts\python.exe -m pytest tests/ -v
```
*(You will see 25/25 tests passing successfully!)*

---

## 🎯 Summary of Key Design Rules Used
- **App Factory Pattern**: Keeps the codebase clean, modular, and easy to test.
- **Thin Routes, Fat Services**: Web routes only handle requests and responses; all complex logic (AI, STT, TTS) lives inside `app/services/`.
- **Security First**: Passwords are never stored in plain text (they use Werkzeug secure hashes), and secrets live safely inside `.env`.
