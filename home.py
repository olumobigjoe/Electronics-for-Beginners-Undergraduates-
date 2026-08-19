"""
Home / Hub landing page for the Electronics Learning Hub.

Renders a card-grid entry point (icon + level badge + title + blurb +
"Start Learning" button per topic) instead of relying on Streamlit's
default sidebar page list. Clicking a card's button jumps straight into
that topic via st.switch_page(), using the Page objects app.py stashed
in st.session_state before navigation started.

NOTE: every HTML string below avoids blank lines inside a block —
Streamlit's Markdown renderer treats a blank line inside an HTML block
as the end of that block, and anything after gets shown as literal
text instead of being rendered. The only exception is the <style> tag
itself, which CommonMark treats as a raw block not terminated by blank
lines.
"""

import streamlit as st

st.set_page_config(
    page_title="Electronics for Beginners",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}

    .hub-hero {
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }
    .hub-hero h1 {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }
    .hub-hero p.subtitle {
        color: #93c5fd;
        font-size: 1.05rem;
        max-width: 700px;
        margin: 0 auto 0.6rem auto;
        line-height: 1.5;
    }
    .hub-hero p.tagline {
        color: #60a5fa;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .stat-box {
        background: #131b2e;
        border: 1px solid #1f2a44;
        border-radius: 12px;
        text-align: center;
        padding: 0.9rem 0.5rem;
    }
    .stat-box .stat-num {
        color: #60a5fa;
        font-size: 1.6rem;
        font-weight: 800;
    }
    .stat-box .stat-label {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.15rem;
    }

    .explore-heading {
        text-align: center;
        margin-top: 1.6rem;
    }
    .explore-heading h2 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 800;
    }
    .explore-heading p {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: -0.3rem;
    }

    .topic-card {
        background: #131b2e;
        border: 1px solid #1f2a44;
        border-radius: 14px;
        padding: 1.1rem 1.2rem 0.4rem 1.2rem;
        margin-bottom: 0.7rem;
        min-height: 235px;
    }
    .topic-card .badge {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .topic-card .badge.tier-1 {color: #60a5fa;}
    .topic-card .badge.tier-2 {color: #f472b6;}
    .topic-card .badge.tier-3 {color: #34d399;}
    .topic-card .icon {
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    }
    .topic-card h4 {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .topic-card p {
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.45;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        background: transparent;
        color: #e5e7eb;
        border: 1px solid #3b4863;
        border-radius: 999px;
        padding: 0.4rem 0.8rem;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1.1rem;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #60a5fa;
        color: #60a5fa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# HERO
# ============================================================================
st.markdown(
    """
    <div class="hub-hero">
        <h1>Electronics for Beginners</h1>
        <p class="subtitle">An interactive electronics learning laboratory designed to take you
        from electrical fundamentals to digital electronics through practical,
        beginner-friendly learning.</p>
        <p class="tagline">Learn • Explore • Simulate • Practice • Master</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        '<div class="stat-box"><div class="stat-num">8</div>'
        '<div class="stat-label">Learning Modules</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="stat-box"><div class="stat-num">3</div>'
        '<div class="stat-label">Learning Levels</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="stat-box"><div class="stat-num">∞</div>'
        '<div class="stat-label">Practice Opportunities</div></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="explore-heading">
        <h2>Explore the Learning Laboratory</h2>
        <p>Select a topic below to begin learning.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ============================================================================
# TOPIC CARDS
# key   -> matches the key used in app.py's PAGES_BY_KEY registry
# tier  -> 1, 2, or 3, controls the badge color / label
# ============================================================================
TOPICS = [
    {
        "key": "components",
        "icon": "🔧",
        "tier": 1,
        "tier_label": "Level 1 · Foundations",
        "title": "Electronic Components",
        "blurb": "Learn resistors, capacitors, inductors, diodes, transistors and "
                 "other fundamental electronic components.",
    },
    {
        "key": "measurements",
        "icon": "📏",
        "tier": 1,
        "tier_label": "Level 1 · Foundations",
        "title": "Measurements & Instrumentation",
        "blurb": "Understand electronic measurements, instruments, measurement "
                 "techniques and practical laboratory concepts.",
    },
    {
        "key": "fundamentals",
        "icon": "⚡",
        "tier": 1,
        "tier_label": "Level 1 · Foundations",
        "title": "Electrical Fundamentals",
        "blurb": "Build a strong foundation in voltage, current, resistance, "
                 "power, energy and basic electrical principles.",
    },
    {
        "key": "rectifiers",
        "icon": "🔺",
        "tier": 2,
        "tier_label": "Level 2 · Analog Electronics",
        "title": "Diodes & Rectifiers",
        "blurb": "Explore diode operation, rectification, waveforms and "
                 "practical applications of diode circuits.",
    },
    {
        "key": "amplifiers",
        "icon": "🔀",
        "tier": 2,
        "tier_label": "Level 2 · Analog Electronics",
        "title": "Transistors & Amplifiers",
        "blurb": "Understand transistor fundamentals, amplification and the "
                 "building blocks of analog circuits.",
    },
    {
        "key": "logic_gates",
        "icon": "🔌",
        "tier": 3,
        "tier_label": "Level 3 · Digital Electronics",
        "title": "Logic Gates",
        "blurb": "Explore AND, OR, NOT, NAND, NOR, XOR and XNOR gates through "
                 "interactive digital logic learning.",
    },
    {
        "key": "circuit_analysis",
        "icon": "🧮",
        "tier": 3,
        "tier_label": "Level 3 · Circuit Theory",
        "title": "Circuit Analysis",
        "blurb": "Develop practical skills for analyzing electrical and "
                 "electronic circuits and understanding circuit behavior.",
    },
    {
        "key": "digital_electronics",
        "icon": "💾",
        "tier": 3,
        "tier_label": "Level 3 · Digital Electronics",
        "title": "Digital Electronics",
        "blurb": "Move from basic logic gates into digital electronics and "
                 "computer hardware concepts.",
    },
]


def render_card(topic: dict) -> None:
    st.markdown(
        f"""
        <div class="topic-card">
            <div class="badge tier-{topic['tier']}">{topic['tier_label']}</div>
            <div class="icon">{topic['icon']}</div>
            <h4>{topic['title']}</h4>
            <p>{topic['blurb']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🖊️ Start Learning", key=f"start_{topic['key']}"):
        pages_by_key = st.session_state.get("_pages_by_key", {})
        target = pages_by_key.get(topic["key"])
        if target is not None:
            st.switch_page(target)
        else:
            st.error("Navigation isn't ready yet — please reload the page.")


row1 = st.columns(4)
for col, topic in zip(row1, TOPICS[:4]):
    with col:
        render_card(topic)

row2 = st.columns(4)
for col, topic in zip(row2, TOPICS[4:]):
    with col:
        render_card(topic)
