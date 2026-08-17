import streamlit as st

# ============================================================
# ELECTRONICS FOR BEGINNERS
# Master Learning Portal
# Updated with live Streamlit application links
# ============================================================

st.set_page_config(
    page_title="Electronics for Beginners",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.18), transparent 30%),
        radial-gradient(circle at top right, rgba(14,165,233,0.12), transparent 25%),
        linear-gradient(135deg, #06111f 0%, #0b1d32 50%, #071426 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero {
    text-align: center;
    padding: 55px 20px 40px;
}

.hero-icon {
    font-size: 65px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 15px;
    background: linear-gradient(90deg, #ffffff, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.15rem;
    line-height: 1.7;
    max-width: 760px;
    margin: auto;
    color: #cbd5e1;
}

.hero-tagline {
    margin-top: 20px;
    color: #60a5fa;
    font-size: 1rem;
    font-weight: 700;
}

.stats {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 10px auto 45px;
    flex-wrap: wrap;
}

.stat {
    min-width: 150px;
    padding: 18px 25px;
    border-radius: 15px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    text-align: center;
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #38bdf8;
}

.stat-label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 4px;
}

.section-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 8px;
}

.section-description {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 35px;
}

.course-card {
    min-height: 350px;
    padding: 30px 25px;
    border-radius: 24px;
    background: rgba(255,255,255,0.065);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 10px;
}

.course-card:hover {
    transform: translateY(-7px);
    border-color: rgba(56,189,248,0.6);
    box-shadow:
        0 15px 45px rgba(0,0,0,0.35),
        0 0 25px rgba(14,165,233,0.12);
}

.course-icon {
    font-size: 50px;
    text-align: center;
    margin-bottom: 15px;
}

.course-level {
    text-align: center;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #38bdf8;
    font-weight: 700;
    margin-bottom: 8px;
}

.course-title {
    text-align: center;
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 12px;
}

.course-description {
    color: #cbd5e1;
    font-size: 0.92rem;
    line-height: 1.6;
    text-align: center;
    min-height: 85px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(56,189,248,0.35);
    background: rgba(37,99,235,0.85);
    color: white;
    font-weight: 700;
    padding: 0.65rem;
}

div.stButton > button:hover {
    background: #0284c7;
    border-color: #38bdf8;
    color: white;
}

.path-box {
    margin-top: 45px;
    padding: 35px;
    border-radius: 25px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}

.path-title {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 800;
    margin-bottom: 25px;
}

.path-step {
    padding: 18px;
    margin-bottom: 12px;
    border-radius: 15px;
    background: rgba(255,255,255,0.045);
    border-left: 4px solid #38bdf8;
}

.path-step strong {
    color: #ffffff;
}

.path-step span {
    color: #94a3b8;
}

.footer {
    text-align: center;
    margin-top: 60px;
    padding: 30px 15px;
    border-top: 1px solid rgba(255,255,255,0.1);
    color: #94a3b8;
}

.footer-title {
    color: white;
    font-weight: 800;
    font-size: 1.05rem;
    margin-bottom: 8px;
}

@media (max-width: 1000px) {
    .course-card {
        min-height: 330px;
    }
}

@media (max-width: 768px) {
    .hero {
        padding-top: 30px;
    }

    .hero-icon {
        font-size: 50px;
    }

    .course-card {
        min-height: 310px;
    }

    .stats {
        gap: 10px;
    }

    .stat {
        min-width: 120px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# LIVE LEARNING LABS
# ============================================================

courses = [
    {
        "icon": "🔧",
        "level": "Level 1 • Foundations",
        "title": "Electronic Components",
        "description": (
            "Learn resistors, capacitors, inductors, diodes, "
            "transistors and other fundamental electronic components."
        ),
        "url": "https://intro-to-electronic-components.streamlit.app/"
    },
    {
        "icon": "📏",
        "level": "Level 1 • Foundations",
        "title": "Measurements & Instrumentation",
        "description": (
            "Understand electronic measurements, instruments, "
            "measurement techniques and practical laboratory concepts."
        ),
        "url": "https://electronic-measurements-and-instrumentation.streamlit.app/"
    },
    {
        "icon": "⚡",
        "level": "Level 1 • Foundations",
        "title": "Electrical Fundamentals",
        "description": (
            "Build a strong foundation in voltage, current, "
            "resistance, power, energy and basic electrical principles."
        ),
        "url": "https://electrical-fundamentals.streamlit.app/"
    },
    {
        "icon": "🔌",
        "level": "Level 2 • Analog Electronics",
        "title": "Diodes & Rectifiers",
        "description": (
            "Explore diode operation, rectification, waveforms "
            "and practical applications of diode circuits."
        ),
        "url": "https://diodes-rectifiers.streamlit.app/"
    },
    {
        "icon": "🔬",
        "level": "Level 2 • Analog Electronics",
        "title": "Transistors & Amplifiers",
        "description": (
            "Understand transistor fundamentals, amplification "
            "and the building blocks of analog electronic circuits."
        ),
        "url": "https://transistors-and-amplifiers.streamlit.app/"
    },
    {
        "icon": "💡",
        "level": "Level 3 • Digital Electronics",
        "title": "Logic Gates",
        "description": (
            "Explore AND, OR, NOT, NAND, NOR, XOR and XNOR "
            "gates through interactive digital logic learning."
        ),
        "url": "https://logic-gates-lab.streamlit.app/"
    },
    {
        "icon": "🧮",
        "level": "Level 2 • Circuit Theory",
        "title": "Circuit Analysis",
        "description": (
            "Develop practical skills for analyzing electrical "
            "and electronic circuits and understanding circuit behavior."
        ),
        "url": "https://circuit-analysis.streamlit.app/"
    },
    {
        "icon": "💻",
        "level": "Level 3 • Digital Electronics",
        "title": "Digital Electronics",
        "description": (
            "Move from basic logic gates into digital electronics "
            "and computer hardware concepts."
        ),
        "url": "https://digital-electronics-for-beginners.streamlit.app/"
    }
]


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-icon">⚡</div>

    <div class="hero-title">
        Electronics for Beginners
    </div>

    <div class="hero-subtitle">
        An interactive electronics learning laboratory designed
        to take you from electrical fundamentals to digital
        electronics through practical, beginner-friendly learning.
    </div>

    <div class="hero-tagline">
        LEARN • EXPLORE • SIMULATE • PRACTICE • MASTER
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# STATS
# ============================================================

st.markdown("""
<div class="stats">

    <div class="stat">
        <div class="stat-number">8</div>
        <div class="stat-label">Learning Modules</div>
    </div>

    <div class="stat">
        <div class="stat-number">3</div>
        <div class="stat-label">Learning Levels</div>
    </div>

    <div class="stat">
        <div class="stat-number">8</div>
        <div class="stat-label">Live Learning Labs</div>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# COURSE SECTION
# ============================================================

st.markdown("""
<div class="section-title">
    Explore the Learning Laboratory
</div>

<div class="section-description">
    Choose a topic below to open its interactive learning laboratory.
</div>
""", unsafe_allow_html=True)


# ============================================================
# COURSE CARDS
# ============================================================

for row_start in range(0, len(courses), 4):

    row_courses = courses[row_start:row_start + 4]

    columns = st.columns(4)

    for column, course in zip(columns, row_courses):

        with column:

            st.markdown(
                f"""
                <div class="course-card">

                    <div>

                        <div class="course-icon">
                            {course["icon"]}
                        </div>

                        <div class="course-level">
                            {course["level"]}
                        </div>

                        <div class="course-title">
                            {course["title"]}
                        </div>

                        <div class="course-description">
                            {course["description"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                "🚀 OPEN LEARNING LAB",
                course["url"],
                use_container_width=True
            )


# ============================================================
# LEARNING PATH
# ============================================================

st.markdown("""
<div class="path-box">

    <div class="path-title">
        🎓 Recommended Learning Path
    </div>

    <div class="path-step">
        <strong>01 → Electrical Fundamentals</strong><br>
        <span>
            Understand voltage, current, resistance, power and
            basic electrical principles.
        </span>
    </div>

    <div class="path-step">
        <strong>02 → Electronic Components</strong><br>
        <span>
            Learn the components that make electronic circuits work.
        </span>
    </div>

    <div class="path-step">
        <strong>03 → Measurements & Instrumentation</strong><br>
        <span>
            Learn how electrical quantities are measured and tested.
        </span>
    </div>

    <div class="path-step">
        <strong>04 → Circuit Analysis</strong><br>
        <span>
            Learn how to understand and analyze complete circuits.
        </span>
    </div>

    <div class="path-step">
        <strong>05 → Diodes & Rectifiers</strong><br>
        <span>
            Explore semiconductor devices and AC-to-DC conversion.
        </span>
    </div>

    <div class="path-step">
        <strong>06 → Transistors & Amplifiers</strong><br>
        <span>
            Understand transistor operation and signal amplification.
        </span>
    </div>

    <div class="path-step">
        <strong>07 → Logic Gates</strong><br>
        <span>
            Enter the world of digital logic and Boolean operations.
        </span>
    </div>

    <div class="path-step">
        <strong>08 → Digital Electronics</strong><br>
        <span>
            Build upon logic gates and explore digital systems.
        </span>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FUTURE PLATFORM FEATURES
# ============================================================

with st.expander("🚀 Future Platform Features"):

    st.markdown("""
    ### Planned expansion of the Electronics for Beginners platform

    - 📚 Structured courses
    - 🧪 Interactive virtual laboratories
    - 🧮 Electronics calculators
    - 🎯 Topic-based quizzes
    - 📝 Practice examinations
    - 🏆 Student achievement system
    - 📊 Learning progress dashboard
    - 🤖 AI Electronics Tutor
    - 🔌 Virtual circuit simulator
    - 📈 Interactive graphs and waveforms
    - 🎓 Certificates
    - 👨‍🏫 Lecturer/instructor dashboard
    - 📱 Mobile application
    - 🌐 Progressive Web App (PWA)
    - 🔐 Student accounts
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <div class="footer-title">
        ⚡ Electronics for Beginners
    </div>

    <div>
        Interactive Electronics Learning Laboratory
    </div>

    <div style="margin-top:10px;">
        Learn • Explore • Simulate • Practice • Master
    </div>

</div>
""", unsafe_allow_html=True)
