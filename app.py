import streamlit as st

st.set_page_config(
    page_title="Electronics for Beginners",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PROJECTS = [
    {
        "icon": "🔧",
        "title": "Electronic Components",
        "level": "LEVEL 1 • FOUNDATIONS",
        "description": "Learn resistors, capacitors, inductors, diodes, transistors, transformers, switches and other essential electronic components.",
        "url": "https://intro-to-electronic-components.streamlit.app/"
    },
    {
        "icon": "📏",
        "title": "Measurements & Instrumentation",
        "level": "LEVEL 1 • FOUNDATIONS",
        "description": "Explore electronic measurements, instruments, measurement techniques and practical laboratory concepts.",
        "url": "https://electronic-measurements-and-instrumentation.streamlit.app/"
    },
    {
        "icon": "⚡",
        "title": "Electrical Fundamentals",
        "level": "LEVEL 1 • FOUNDATIONS",
        "description": "Build a strong foundation in voltage, current, resistance, power, energy, Ohm's Law and basic electrical principles.",
        "url": "https://electrical-fundamentals.streamlit.app/"
    },
    {
        "icon": "🔌",
        "title": "Diodes & Rectifiers",
        "level": "LEVEL 2 • ANALOG ELECTRONICS",
        "description": "Understand diode operation, biasing, rectification, waveforms and practical diode applications.",
        "url": "https://diodes-rectifiers.streamlit.app/"
    },
    {
        "icon": "🔬",
        "title": "Transistors & Amplifiers",
        "level": "LEVEL 2 • ANALOG ELECTRONICS",
        "description": "Learn transistor fundamentals, transistor operation, amplification and analog electronic circuits.",
        "url": "https://transistors-and-amplifiers.streamlit.app/"
    },
    {
        "icon": "💡",
        "title": "Logic Gates",
        "level": "LEVEL 3 • DIGITAL ELECTRONICS",
        "description": "Explore AND, OR, NOT, NAND, NOR, XOR and XNOR gates, truth tables and Boolean logic.",
        "url": "https://logic-gates-lab.streamlit.app/"
    },
    {
        "icon": "🧮",
        "title": "Circuit Analysis",
        "level": "LEVEL 2 • CIRCUIT THEORY",
        "description": "Develop practical skills for understanding, calculating and analyzing electrical and electronic circuits.",
        "url": "https://circuit-analysis.streamlit.app/"
    },
    {
        "icon": "💻",
        "title": "Digital Electronics",
        "level": "LEVEL 3 • DIGITAL ELECTRONICS",
        "description": "Progress from logic gates into digital electronics, Boolean concepts and fundamental digital systems.",
        "url": "https://digital-electronics-for-beginners.streamlit.app/"
    }
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(37,99,235,.20), transparent 28%),
        radial-gradient(circle at 92% 12%, rgba(14,165,233,.14), transparent 25%),
        linear-gradient(135deg, #050d18 0%, #0a1b2f 48%, #06101d 100%);
    color: #fff;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

#MainMenu, footer { visibility: hidden; }

.hero {
    text-align: center;
    padding: 55px 15px 30px;
}

.hero-icon { font-size: 65px; line-height: 1; margin-bottom: 20px; }

.hero-title {
    font-size: clamp(2.4rem, 6vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.05;
    margin-bottom: 20px;
    background: linear-gradient(90deg, #fff, #93c5fd, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 780px;
    margin: auto;
    color: #cbd5e1;
    font-size: 1.12rem;
    line-height: 1.75;
}

.hero-tagline {
    margin-top: 22px;
    color: #38bdf8;
    font-weight: 800;
    letter-spacing: 1.2px;
    font-size: .9rem;
}

.stats {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
    margin: 25px 0 45px;
}

.stat {
    min-width: 155px;
    padding: 17px 24px;
    text-align: center;
    border-radius: 18px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.10);
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #38bdf8;
}

.stat-label {
    color: #94a3b8;
    font-size: .78rem;
    margin-top: 4px;
}

.section-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 15px;
    margin-bottom: 8px;
}

.section-description {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 35px;
}

.card {
    min-height: 375px;
    padding: 27px 22px 20px;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(255,255,255,.085), rgba(255,255,255,.035));
    border: 1px solid rgba(255,255,255,.12);
    box-shadow: 0 12px 30px rgba(0,0,0,.20);
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card:hover {
    transform: translateY(-8px);
    border-color: rgba(56,189,248,.55);
    box-shadow: 0 20px 45px rgba(0,0,0,.35), 0 0 25px rgba(56,189,248,.08);
}

.card-icon {
    text-align: center;
    font-size: 52px;
    margin-bottom: 15px;
}

.card-level {
    text-align: center;
    color: #38bdf8;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 9px;
}

.card-title {
    text-align: center;
    font-size: 1.28rem;
    font-weight: 800;
    margin-bottom: 12px;
}

.card-description {
    text-align: center;
    color: #cbd5e1;
    font-size: .88rem;
    line-height: 1.6;
}

div.stLinkButton > a {
    width: 100%;
    justify-content: center;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #2563eb, #0284c7) !important;
    border: 1px solid rgba(56,189,248,.35) !important;
    color: white !important;
    font-weight: 800 !important;
    margin-bottom: 22px;
}

div.stLinkButton > a:hover {
    background: linear-gradient(90deg, #1d4ed8, #0369a1) !important;
    border-color: #38bdf8 !important;
}

.path {
    margin-top: 50px;
    padding: 32px;
    border-radius: 25px;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.10);
}

.path-title {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 800;
    margin-bottom: 25px;
}

.path-item {
    padding: 15px 18px;
    margin-bottom: 10px;
    border-radius: 14px;
    background: rgba(255,255,255,.04);
    border-left: 4px solid #38bdf8;
    color: #cbd5e1;
}

.path-item strong { color: white; }

.info-box {
    margin-top: 35px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(37,99,235,.08);
    border: 1px solid rgba(56,189,248,.18);
    text-align: center;
}

.info-box strong { color: #38bdf8; }

.custom-footer {
    text-align: center;
    margin-top: 55px;
    padding: 30px 15px 10px;
    border-top: 1px solid rgba(255,255,255,.09);
    color: #94a3b8;
}

.custom-footer-title {
    color: white;
    font-weight: 800;
    font-size: 1.05rem;
    margin-bottom: 8px;
}

@media (max-width: 900px) {
    .card { min-height: 340px; }
}

@media (max-width: 600px) {
    .hero { padding-top: 30px; }
    .hero-icon { font-size: 50px; }
    .hero-title { letter-spacing: -1px; }
    .stats { gap: 8px; }
    .stat { min-width: 105px; padding: 13px 12px; }
    .stat-number { font-size: 1.45rem; }
    .card { min-height: 310px; }
    .path { padding: 22px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-icon">⚡</div>
    <div class="hero-title">Electronics for Beginners</div>
    <div class="hero-subtitle">
        Your central gateway to interactive electronics learning.
        Explore electrical fundamentals, components, measurements,
        analog electronics, circuit analysis, logic gates and digital
        electronics — all from one place.
    </div>
    <div class="hero-tagline">LEARN • EXPLORE • SIMULATE • PRACTICE • MASTER</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats">
    <div class="stat"><div class="stat-number">8</div><div class="stat-label">Learning Modules</div></div>
    <div class="stat"><div class="stat-number">8</div><div class="stat-label">Live Laboratories</div></div>
    <div class="stat"><div class="stat-number">3</div><div class="stat-label">Learning Levels</div></div>
    <div class="stat"><div class="stat-number">1</div><div class="stat-label">Learning Portal</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">Explore Electronics</div>
<div class="section-description">
    Select any topic to open its dedicated interactive learning laboratory.
</div>
""", unsafe_allow_html=True)

for start in range(0, len(PROJECTS), 4):
    row = PROJECTS[start:start + 4]
    columns = st.columns(4, gap="medium")

    for col, project in zip(columns, row):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div>
                        <div class="card-icon">{project["icon"]}</div>
                        <div class="card-level">{project["level"]}</div>
                        <div class="card-title">{project["title"]}</div>
                        <div class="card-description">{project["description"]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                "🚀 OPEN LEARNING LAB",
                project["url"],
                use_container_width=True
            )

st.markdown("""
<div class="path">
    <div class="path-title">🎓 Recommended Learning Path</div>
    <div class="path-item"><strong>01 → Electrical Fundamentals</strong><br>Start with voltage, current, resistance, power and basic electrical principles.</div>
    <div class="path-item"><strong>02 → Electronic Components</strong><br>Understand the components used to construct electronic circuits.</div>
    <div class="path-item"><strong>03 → Measurements & Instrumentation</strong><br>Learn how electrical and electronic quantities are measured.</div>
    <div class="path-item"><strong>04 → Circuit Analysis</strong><br>Learn to understand and analyze electrical and electronic circuits.</div>
    <div class="path-item"><strong>05 → Diodes & Rectifiers</strong><br>Explore semiconductor diodes and AC-to-DC rectification.</div>
    <div class="path-item"><strong>06 → Transistors & Amplifiers</strong><br>Learn transistor operation and the fundamentals of amplification.</div>
    <div class="path-item"><strong>07 → Logic Gates</strong><br>Enter digital logic through AND, OR, NOT, NAND, NOR, XOR and XNOR gates.</div>
    <div class="path-item"><strong>08 → Digital Electronics</strong><br>Progress from logic gates into broader digital electronic systems.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>⚡ One Portal. Eight Interactive Laboratories.</strong>
    <br><br>
    Electronics for Beginners serves as the central landing page.
    Each learning module remains an independent application,
    while this portal provides one simple entry point for students.
</div>
""", unsafe_allow_html=True)

with st.expander("🚀 Future Expansion"):
    st.markdown("""
    - 📚 Structured courses and lessons
    - 🧪 Virtual electronics laboratories
    - 🔌 Circuit simulation
    - 🧮 Electronics calculators
    - 🎯 Interactive quizzes
    - 📝 Practice examinations
    - 📊 Student progress tracking
    - 🏆 Achievements and certificates
    - 🤖 AI Electronics Tutor
    - 👨‍🏫 Lecturer dashboard
    - 👨‍🎓 Student dashboard
    - 📱 Mobile application
    - 🌐 Progressive Web App
    - 🔐 Student accounts
    """)

st.markdown("""
<div class="custom-footer">
    <div class="custom-footer-title">⚡ Electronics for Beginners</div>
    <div>Interactive Electronics Learning Laboratory</div>
    <div style="margin-top: 10px;">Learn • Explore • Simulate • Practice • Master</div>
</div>
""", unsafe_allow_html=True)
