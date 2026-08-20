from pathlib import Path

import streamlit as st


# ============================================================
# ELECT4BEGINNERS
# Main application / navigation
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Elect4Beginners | Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

st.html(
    """
    <style>

    /* =========================================
       APP BACKGROUND
       ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 0%,
                rgba(6, 182, 212, 0.07),
                transparent 28%
            ),
            radial-gradient(
                circle at 5% 30%,
                rgba(37, 99, 235, 0.07),
                transparent 30%
            ),
            #07111f;
    }


    .block-container {
        max-width: 1400px;

        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #091525 100%
            );

        border-right:
            1px solid
            rgba(148, 163, 184, 0.10);
    }


    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }


    /* =========================================
       SIDEBAR HEADER
       ========================================= */

    .sidebar-brand {
        padding: 8px 4px 18px 4px;

        border-bottom:
            1px solid
            rgba(148, 163, 184, 0.10);

        margin-bottom: 14px;
    }


    .sidebar-brand-title {
        color: #f8fafc;

        font-size: 1.05rem;

        font-weight: 850;

        letter-spacing: -0.025em;
    }


    .sidebar-brand-subtitle {
        color: #64748b;

        font-size: 0.72rem;

        margin-top: 3px;
    }


    .sidebar-label {
        color: #60a5fa;

        font-size: 0.66rem;

        font-weight: 800;

        letter-spacing: 0.12em;

        text-transform: uppercase;

        margin: 8px 4px;
    }


    /* =========================================
       NAVIGATION
       ========================================= */

    section[data-testid="stSidebar"]
    [data-testid="stPageLink"] {
        border-radius: 9px;

        margin: 3px 0;

        transition:
            background 0.15s ease;
    }


    section[data-testid="stSidebar"]
    [data-testid="stPageLink"]:hover {
        background:
            rgba(37, 99, 235, 0.10);
    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {
        min-height: 44px;

        border-radius: 10px;

        font-weight: 700;

        color: white;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        border:
            1px solid
            rgba(96, 165, 250, 0.20);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }


    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 30px
            rgba(37, 99, 235, 0.22);
    }


    /* =========================================
       MOBILE
       ========================================= */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

    }

    </style>
    """
)


# ============================================================
# SIDEBAR BRAND
#
# IMPORTANT:
# This uses st.html() rather than st.markdown()
# so the HTML cannot appear as a white code box.
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                ⚡ Elect4Beginners
            </div>

            <div class="sidebar-brand-subtitle">
                Electronics made simple
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-label">
            Learning Hub
        </div>
        """
    )


# ============================================================
# NAVIGATION PAGES
# ============================================================

pages = [

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "home.py"),
        title="Home",
        icon="🏠",
        url_path="home",
        default=True,
    ),


    # --------------------------------------------------------
    # ELECTRICAL FUNDAMENTALS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_fundamentals.py"),
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),


    # --------------------------------------------------------
    # ELECTRONIC COMPONENTS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_components.py"),
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),


    # --------------------------------------------------------
    # LOGIC GATES
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_gates.py"),
        title="Logic Gates",
        icon="🔌",
        url_path="logic-gates",
    ),


    # --------------------------------------------------------
    # DIGITAL ELECTRONICS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_digital_electronics.py"),
        title="Digital Electronics",
        icon="💾",
        url_path="digital-electronics",
    ),


    # --------------------------------------------------------
    # CIRCUIT ANALYSIS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_circuit_analysis.py"),
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit-analysis",
    ),


    # --------------------------------------------------------
    # DIODES & RECTIFIERS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_rectifiers.py"),
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),


    # --------------------------------------------------------
    # TRANSISTORS & AMPLIFIERS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_amplifiers.py"),
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),


    # --------------------------------------------------------
    # MEASUREMENTS
    # --------------------------------------------------------

    st.Page(
        str(BASE_DIR / "app_measurements.py"),
        title="Measurements & Instruments",
        icon="📏",
        url_path="measurements",
    ),
]


# ============================================================
# CREATE NAVIGATION
# ============================================================

nav = st.navigation(
    pages,
    position="sidebar",
)


# ============================================================
# RUN SELECTED PAGE
# ============================================================

nav.run()
