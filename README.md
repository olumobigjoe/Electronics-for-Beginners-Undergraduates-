# ⚡ Electronics for Beginners

## Master Portal for Interactive Electronics Learning

**Electronics for Beginners** is a central Streamlit landing page that brings eight independent live electronics learning laboratories together under **one master URL**.

The individual projects remain separate applications. This portal provides students with one starting point and clickable topic cards that open each live laboratory.

## 🌐 Live Learning Laboratories

| Module | Live Application |
|---|---|
| 🔧 Electronic Components | https://intro-to-electronic-components.streamlit.app/ |
| 📏 Measurements & Instrumentation | https://electronic-measurements-and-instrumentation.streamlit.app/ |
| ⚡ Electrical Fundamentals | https://electrical-fundamentals.streamlit.app/ |
| 🔌 Diodes & Rectifiers | https://diodes-rectifiers.streamlit.app/ |
| 🔬 Transistors & Amplifiers | https://transistors-and-amplifiers.streamlit.app/ |
| 💡 Logic Gates | https://logic-gates-lab.streamlit.app/ |
| 🧮 Circuit Analysis | https://circuit-analysis.streamlit.app/ |
| 💻 Digital Electronics | https://digital-electronics-for-beginners.streamlit.app/ |

## 🎓 Recommended Learning Path

1. Electrical Fundamentals
2. Electronic Components
3. Measurements & Instrumentation
4. Circuit Analysis
5. Diodes & Rectifiers
6. Transistors & Amplifiers
7. Logic Gates
8. Digital Electronics

## ✨ Features

- One central landing page
- Eight learning modules
- Eight live Streamlit applications
- Clickable square learning cards
- Direct access to each laboratory
- Recommended learning path
- Modern electronics-themed interface
- Responsive desktop, tablet and mobile layout

## 🛠️ Technology

- Python
- Streamlit
- HTML
- CSS

## 📁 Project Structure

```text
Electronics-for-Beginners/
├── app.py
├── requirements.txt
└── README.md
```

## 💻 Run Locally

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploying the Master Portal

1. Create a GitHub repository named `Electronics-for-Beginners`.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Connect the repository to Streamlit Community Cloud.
4. Select `app.py` as the main file.
5. Deploy.

Streamlit will generate the master portal URL. For example:

```text
https://electronics-for-beginners.streamlit.app/
```

The exact URL depends on the deployment name you select.

## 🔗 How It Works

The master application does **not** merge the source code of the eight projects.

Instead:

```text
MASTER PORTAL
    │
    ├── Electronic Components
    │       └── Live Components App
    ├── Measurements & Instrumentation
    │       └── Live Measurements App
    ├── Electrical Fundamentals
    │       └── Live Fundamentals App
    ├── Diodes & Rectifiers
    │       └── Live Diodes App
    ├── Transistors & Amplifiers
    │       └── Live Transistors App
    ├── Logic Gates
    │       └── Live Logic Gates App
    ├── Circuit Analysis
    │       └── Live Circuit Analysis App
    └── Digital Electronics
            └── Live Digital Electronics App
```

Each project can therefore continue to be developed independently.

## 🔮 Future Development

The portal can later become a complete electronics education platform with:

- Structured courses
- Interactive lessons
- Virtual electronics laboratories
- Circuit simulation
- Electronics calculators
- Quizzes
- Practice examinations
- AI Electronics Tutor
- Student progress tracking
- Student dashboard
- Lecturer dashboard
- Achievements
- Certificates
- Mobile application
- Progressive Web App

## 🎯 Vision

The long-term goal is to combine:

**COURSES + INTERACTIVE LABS + CIRCUIT SIMULATION + QUIZZES + AI TUTOR + PROGRESS TRACKING + CERTIFICATES**

into one complete electronics learning ecosystem.

## ⚡ Electronics for Beginners

### Learn • Explore • Simulate • Practice • Master
