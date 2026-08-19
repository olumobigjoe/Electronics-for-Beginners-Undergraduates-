from pathlib import Path
import streamlit as st


# ============================================================
# ELECT4BEGINNERS — MAIN APPLICATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Elect4Beginners — Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# Global theme
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL
       ============================== */

    :root {
        --navy: #07111f;
        --navy-2: #0b1729;
        --blue: #2563eb;
        --cyan: #06b6d4;
        --yellow: #fbbf24;
        --green: #22c55e;
        --text: #f8fafc;
        --muted: #94a3b8;
        --border: rgba(148, 163, 184, 0.16);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 80% 5%,
                rgba(37, 99, 235, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 30%,
                rgba(6, 182, 212, 0.06),
                transparent 25%
            ),
            #07111f;
        color: var(--text);
    }

    .main {
        background: transparent;
    }

    /* Remove excessive top padding */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #0a1627 100%
            );
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text);
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink"] {
        border-radius: 10px;
        margin: 3px 0;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
        background: rgba(37, 99, 235, 0.14);
    }


    /* ==============================
       BUTTONS
       ============================== */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        background: linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );
        color: white;
        font-weight: 700;
        padding: 0.65rem 1.2rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.25);
        border-color: #60a5fa;
    }


    /* ==============================
       LINKS
       ============================== */

    a {
        color: #60a5fa !important;
    }


    /* ==============================
       HEADINGS
       ============================== */

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p {
        color: #cbd5e1;
    }


    /* ==============================
       METRICS
       ============================== */

    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem;
    }


    /* ==============================
       DIVIDERS
       ============================== */

    hr {
        border-color: rgba(148, 163, 184, 0.12);
    }


    /* ==============================
       MOBILE
       ============================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 2rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------

pages = [
    st.Page(
        str(BASE_DIR / "home.py"),
        title="Home",
        icon="🏠",
        url_path="home",
        default=True,
    ),

    st.Page(
        str(BASE_DIR / "app_fundamentals.py"),
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),

    st.Page(
        str(BASE_DIR / "app_components.py"),
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),

    st.Page(
        str(BASE_DIR / "app_gates.py"),
        title="Logic Gates",
        icon="🔌",
        url_path="logic-gates",
    ),

    st.Page(
        str(BASE_DIR / "app_digital_electronics.py"),
        title="Digital Electronics",
        icon="💾",
        url_path="digital-electronics",
    ),

    st.Page(
        str(BASE_DIR / "app_circuit_analysis.py"),
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit-analysis",
    ),

    st.Page(
        str(BASE_DIR / "app_rectifiers.py"),
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),

    st.Page(
        str(BASE_DIR / "app_amplifiers.py"),
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),

    st.Page(
        str(BASE_DIR / "app_measurements.py"),
        title="Measurements & Instruments",
        icon="📏",
        url_path="measurements",
    ),
]


# ------------------------------------------------------------
# Sidebar branding
# ------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 0.5rem 0.3rem 1.2rem 0.3rem;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:10px;
            ">

                <div style="
                    width:42px;
                    height:42px;
                    border-radius:12px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:
                        linear-gradient(
                            135deg,
                            #2563eb,
                            #06b6d4
                        );
                    font-size:23px;
                    box-shadow:
                        0 8px 25px
                        rgba(37,99,235,.25);
                ">
                    ⚡
                </div>

                <div>
                    <div style="
                        color:#f8fafc;
                        font-size:1.05rem;
                        font-weight:800;
                        letter-spacing:-.02em;
                    ">
                        Elect4Beginners
                    </div>

                    <div style="
                        color:#64748b;
                        font-size:.72rem;
                        margin-top:2px;
                    ">
                        Electronics made simple
                    </div>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("LEARNING")

    st.markdown(
        """
        <div style="
            margin-top:1.5rem;
            padding:1rem;
            border-radius:12px;
            background:rgba(37,99,235,.08);
            border:1px solid rgba(96,165,250,.12);
        ">
            <div style="
                color:#94a3b8;
                font-size:.72rem;
                text-transform:uppercase;
                letter-spacing:.08em;
                margin-bottom:.35rem;
            ">
                Your journey
            </div>

            <div style="
                color:#f8fafc;
                font-size:.95rem;
                font-weight:700;
            ">
                Start with the fundamentals
            </div>

            <div style="
                color:#64748b;
                font-size:.78rem;
                margin-top:.35rem;
            ">
                Build your electronics knowledge step by step.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.caption("ELECT4BEGINNERS")
    st.caption("Learn • Experiment • Understand")


# ------------------------------------------------------------
# Run application
# ------------------------------------------------------------

nav = st.navigation(pages, position="sidebar")
nav.run()
