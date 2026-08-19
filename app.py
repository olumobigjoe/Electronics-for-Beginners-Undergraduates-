from pathlib import Path

import streamlit as st


# ============================================================
# ELECT4BEGINNERS
# Main application
# ============================================================

# BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Elect4Beginners — Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLES
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --navy: #07111f;
        --navy-light: #0b1729;
        --blue: #2563eb;
        --blue-light: #60a5fa;
        --cyan: #06b6d4;
        --text: #f8fafc;
        --muted: #94a3b8;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(6, 182, 212, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 30%,
                rgba(37, 99, 235, 0.08),
                transparent 30%
            ),
            #07111f;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p {
        color: #cbd5e1;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #091526 100%
            );

        border-right:
            1px solid
            rgba(148, 163, 184, 0.12);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink"] {
        border-radius: 9px;
        margin: 3px 0;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink"]:hover {
        background:
            rgba(37, 99, 235, 0.12);
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 10px;
        min-height: 44px;

        font-weight: 700;

        border:
            1px solid
            rgba(96, 165, 250, 0.22);

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        color: white;

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color:
            rgba(96, 165, 250, 0.6);

        box-shadow:
            0 12px 30px
            rgba(37, 99, 235, 0.25);
    }

    hr {
        border-color:
            rgba(148, 163, 184, 0.1);
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PAGES
# ============================================================

pages = [
    st.Page(
        "home.py",
        title="Home",
        icon="🏠",
        url_path="home",
        default=True,
    ),

    st.Page(
        "app_fundamentals.py",
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),

    st.Page(
        "app_components.py",
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),

    st.Page(
        "app_gates.py",
        title="Logic Gates",
        icon="🔌",
        url_path="logic-gates",
    ),

    st.Page(
        "app_digital_electronics.py",
        title="Digital Electronics",
        icon="💾",
        url_path="digital-electronics",
    ),

    st.Page(
        "app_circuit_analysis.py",
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit-analysis",
    ),

    st.Page(
        "app_rectifiers.py",
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),

    st.Page(
        "app_amplifiers.py",
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),

    st.Page(
        "app_measurements.py",
        title="Measurements & Instruments",
        icon="📏",
        url_path="measurements",
    ),
]


# ============================================================
# SIDEBAR BRAND
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 0.4rem 0.2rem 1rem 0.2rem;
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

                    font-size:22px;

                    box-shadow:
                        0 8px 24px
                        rgba(37,99,235,.25);
                ">
                    ⚡
                </div>

                <div>

                    <div style="
                        color:#f8fafc;
                        font-size:1.02rem;
                        font-weight:800;
                        letter-spacing:-.02em;
                    ">
                        Elect4Beginners
                    </div>

                    <div style="
                        color:#64748b;
                        font-size:.7rem;
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

    st.caption("LEARN")

    st.markdown(
        """
        <div style="
            padding:12px;
            margin-top:8px;
            margin-bottom:14px;
            border-radius:12px;

            background:
                rgba(37,99,235,.07);

            border:
                1px solid
                rgba(96,165,250,.10);
        ">

            <div style="
                color:#60a5fa;
                font-size:.68rem;
                font-weight:800;
                text-transform:uppercase;
                letter-spacing:.08em;
            ">
                Learning journey
            </div>

            <div style="
                color:#e2e8f0;
                font-size:.88rem;
                font-weight:700;
                margin-top:5px;
            ">
                Start with the fundamentals
            </div>

            <div style="
                color:#64748b;
                font-size:.73rem;
                line-height:1.4;
                margin-top:4px;
            ">
                Build your electronics knowledge
                one concept at a time.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("ELECT4BEGINNERS")

    st.markdown(
        """
        <div style="
            color:#475569;
            font-size:.72rem;
            line-height:1.6;
        ">
            Learn<br>
            Experiment<br>
            Understand
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RUN NAVIGATION
# ============================================================

nav = st.navigation(
    pages,
    position="sidebar",
)

nav.run()
