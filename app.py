from pathlib import Path

import streamlit as st


# ============================================================
# ELECT4BEGINNERS
# MASTER APPLICATION THEME + NAVIGATION
# ============================================================

# BASE_DIR = Path(__file__).resolve().parent


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
# MASTER THEME
#
# This CSS is intentionally global so that the eight existing
# learning modules inherit one consistent visual system.
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       COLOUR SYSTEM
       ======================================================== */

    :root {
        --e4b-bg: #07111f;
        --e4b-bg-2: #0b1729;
        --e4b-panel: #0f1d31;
        --e4b-panel-2: #12243b;

        --e4b-border: rgba(148, 163, 184, 0.14);

        --e4b-text: #f8fafc;
        --e4b-text-soft: #dbeafe;
        --e4b-muted: #a8b8cc;
        --e4b-muted-2: #7f91a8;

        --e4b-blue: #3b82f6;
        --e4b-blue-light: #60a5fa;
        --e4b-cyan: #22d3ee;
    }


    /* ========================================================
       MAIN APPLICATION BACKGROUND
       ======================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 90% 0%,
                rgba(6, 182, 212, 0.075),
                transparent 28%
            ),
            radial-gradient(
                circle at 5% 35%,
                rgba(37, 99, 235, 0.075),
                transparent 30%
            ),
            var(--e4b-bg) !important;

        color: var(--e4b-text) !important;
    }


    /* Main content area */

    [data-testid="stAppViewContainer"]
    [data-testid="stMain"] {

        background:
            transparent !important;
    }


    /* Streamlit's older .main selector */

    .main {
        background:
            transparent !important;
    }


    .block-container {

        max-width: 1400px;

        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       GLOBAL TEXT
       ======================================================== */

    .stApp p,
    .stApp li,
    .stApp span,
    .stApp label {

        color: var(--e4b-text-soft);
    }


    .stApp p {

        line-height: 1.65;
    }


    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {

        color: var(--e4b-text) !important;
    }


    h1 {
        letter-spacing: -0.035em;
    }


    h2 {
        letter-spacing: -0.025em;
    }


    h3 {
        letter-spacing: -0.02em;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #081321 0%,
                #0a1728 55%,
                #091525 100%
            ) !important;

        border-right:
            1px solid
            rgba(148, 163, 184, 0.12) !important;
    }


    section[data-testid="stSidebar"] > div {

        background:
            transparent !important;

        padding-top: 1rem;
    }


    /* Sidebar text */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {

        color: #dbeafe !important;
    }


    /* Navigation links */

    section[data-testid="stSidebar"]
    [data-testid="stPageLink"] {

        border-radius: 9px !important;

        margin: 3px 0 !important;

        color: #dbeafe !important;

        transition:
            background 0.15s ease,
            color 0.15s ease;
    }


    section[data-testid="stSidebar"]
    [data-testid="stPageLink"]:hover {

        background:
            rgba(59, 130, 246, 0.13) !important;

        color: #ffffff !important;
    }


    section[data-testid="stSidebar"]
    [data-testid="stPageLink"]
    a {

        color: #dbeafe !important;
    }


    section[data-testid="stSidebar"]
    [data-testid="stPageLink"]
    a:hover {

        color: #ffffff !important;
    }


    /* Selected navigation item */

    section[data-testid="stSidebar"]
    [data-testid="stPageLink"][aria-current="page"] {

        background:
            linear-gradient(
                90deg,
                rgba(59, 130, 246, 0.22),
                rgba(37, 99, 235, 0.12)
            ) !important;

        border-left:
            3px solid
            #60a5fa !important;
    }


    section[data-testid="stSidebar"]
    [data-testid="stPageLink"][aria-current="page"]
    a {

        color: #ffffff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

    .sidebar-brand {

        padding:
            8px 4px 18px 4px;

        margin-bottom: 14px;

        border-bottom:
            1px solid
            rgba(148, 163, 184, 0.10);
    }


    .sidebar-brand-title {

        color: #f8fafc !important;

        font-size: 1.05rem;

        font-weight: 850;

        letter-spacing: -0.025em;
    }


    .sidebar-brand-subtitle {

        color: #91a4bc !important;

        font-size: 0.72rem;

        margin-top: 3px;
    }


    .sidebar-label {

        color: #60a5fa !important;

        font-size: 0.66rem;

        font-weight: 800;

        letter-spacing: 0.12em;

        text-transform: uppercase;

        margin: 8px 4px;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        min-height: 44px;

        border-radius: 10px;

        font-weight: 700;

        color: #ffffff !important;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            ) !important;

        border:
            1px solid
            rgba(96, 165, 250, 0.22) !important;

        box-shadow:
            0 5px 18px
            rgba(37, 99, 235, 0.10);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 12px 30px
            rgba(37, 99, 235, 0.25);
    }


    .stButton > button p {

        color: #ffffff !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stSlider label,
    .stRadio label,
    .stCheckbox label {

        color: #dbeafe !important;

        font-weight: 600 !important;
    }


    /* Text / number input */

    .stTextInput input,
    .stNumberInput input {

        background:
            #0d1b2e !important;

        color:
            #f8fafc !important;

        border:
            1px solid
            rgba(148, 163, 184, 0.20) !important;

        border-radius:
            9px !important;
    }


    .stTextInput input:focus,
    .stNumberInput input:focus {

        border-color:
            #60a5fa !important;

        box-shadow:
            0 0 0 1px
            rgba(96, 165, 250, 0.35) !important;
    }


    /* Selectbox */

    div[data-baseweb="select"] > div {

        background:
            #0d1b2e !important;

        color:
            #f8fafc !important;

        border-color:
            rgba(148, 163, 184, 0.20) !important;
    }


    div[data-baseweb="select"] span {

        color:
            #f8fafc !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(15, 29, 49, 0.82) !important;

        border:
            1px solid
            rgba(148, 163, 184, 0.14) !important;

        border-radius:
            12px !important;
    }


    [data-testid="stExpander"] summary {

        color:
            #f8fafc !important;
    }


    [data-testid="stExpander"] summary p {

        color:
            #e2e8f0 !important;

        font-weight:
            650 !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {

        color:
            #a8b8cc !important;

        font-weight:
            650 !important;
    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            #60a5fa !important;
    }


    div[data-baseweb="tab-highlight"] {

        background:
            #3b82f6 !important;
    }


    /* ========================================================
       DATAFRAMES / TABLES
       ======================================================== */

    [data-testid="stDataFrame"] {

        border-radius:
            10px !important;

        border:
            1px solid
            rgba(148, 163, 184, 0.14) !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(15, 29, 49, 0.82);

        border:
            1px solid
            rgba(148, 163, 184, 0.12);

        border-radius:
            12px;

        padding:
            12px 14px;
    }


    [data-testid="stMetricLabel"] {

        color:
            #94a3b8 !important;
    }


    [data-testid="stMetricValue"] {

        color:
            #f8fafc !important;
    }


    /* ========================================================
       ALERTS / INFO
       ======================================================== */

    [data-testid="stAlert"] {

        border-radius:
            10px !important;
    }


    /* ========================================================
       LINKS
       ======================================================== */

    .stApp a {

        color:
            #60a5fa !important;
    }


    .stApp a:hover {

        color:
            #93c5fd !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border-color:
            rgba(148, 163, 184, 0.12) !important;
    }


    /* ========================================================
       CODE
       ======================================================== */

    code {

        color:
            #7dd3fc !important;

        background:
            rgba(15, 23, 42, 0.75) !important;
    }


    pre {

        background:
            #0b1729 !important;

        border:
            1px solid
            rgba(148, 163, 184, 0.12) !important;

        border-radius:
            10px !important;
    }


    /* ========================================================
       CAPTIONS
       ======================================================== */

    .stCaption,
    [data-testid="stCaptionContainer"] {

        color:
            #91a4bc !important;
    }


    /* ========================================================
       SLIDERS
       ======================================================== */

    [data-testid="stSlider"] [role="slider"] {

        background:
            #60a5fa !important;

        border-color:
            #60a5fa !important;
    }


    /* ========================================================
       CHECKBOX / RADIO
       ======================================================== */

    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {

        color:
            #dbeafe !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {

            padding-left:
                1rem;

            padding-right:
                1rem;
        }

    }

    </style>
    """
)





# ============================================================
# NAVIGATION
# ============================================================

pages = [

    st.Page(
        str("home.py"),
        title="Home",
        icon="🏠",
        url_path="home",
        default=True,
    ),

    st.Page(
        str("app_fundamentals.py"),
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),

    st.Page(
        str("app_components.py"),
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),

    st.Page(
        str("app_gates.py"),
        title="Logic Gates",
        icon="🔌",
        url_path="logic-gates",
    ),

    st.Page(
        str("app_digital_electronics.py"),
        title="Digital Electronics",
        icon="💾",
        url_path="digital-electronics",
    ),

    st.Page(
        str("app_circuit_analysis.py"),
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit-analysis",
    ),

    st.Page(
        str("app_rectifiers.py"),
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),

    st.Page(
        str("app_amplifiers.py"),
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),

    st.Page(
        str("app_measurements.py"),
        title="Measurements & Instruments",
        icon="📏",
        url_path="measurements",
    ),
]


# ============================================================
# RUN NAVIGATION
# ============================================================

nav = st.navigation(
    pages,
    position="sidebar",
)

nav.run()
# ============================================================
# RUN NAVIGATION
# ============================================================

nav = st.navigation(
    pages,
    position="sidebar",
)

nav.run()
