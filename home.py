from textwrap import dedent

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Elect4Beginners — Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.markdown(
        dedent(content),
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE CSS
# ============================================================

html(
    """
    <style>

    /* ==========================================
       HERO
       ========================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 3.6rem 3.2rem;

        border-radius: 26px;

        margin-bottom: 1.2rem;

        background:
            radial-gradient(
                circle at 85% 25%,
                rgba(6,182,212,.15),
                transparent 25%
            ),
            radial-gradient(
                circle at 15% 90%,
                rgba(37,99,235,.18),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #0b1729,
                #07111f
            );

        border:
            1px solid
            rgba(96,165,250,.16);

        box-shadow:
            0 25px 70px
            rgba(0,0,0,.22);
    }


    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 720px;
    }


    .eyebrow {
        display: inline-flex;
        align-items: center;

        padding: 7px 12px;

        border-radius: 999px;

        background:
            rgba(37,99,235,.10);

        border:
            1px solid
            rgba(96,165,250,.16);

        color: #60a5fa;

        font-size: .72rem;
        font-weight: 800;

        text-transform: uppercase;
        letter-spacing: .08em;

        margin-bottom: 1.1rem;
    }


    .hero-title {
        margin: 0;

        color: #f8fafc;

        font-size:
            clamp(2.8rem, 6vw, 5rem);

        line-height: .98;

        letter-spacing: -.055em;

        font-weight: 900;
    }


    .hero-highlight {
        background:
            linear-gradient(
                90deg,
                #60a5fa,
                #22d3ee
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-description {
        color: #94a3b8;

        font-size: 1.08rem;

        line-height: 1.7;

        max-width: 650px;

        margin-top: 1.35rem;
    }


    /* ==========================================
       CIRCUIT DECORATION
       ========================================== */

    .circuit-art {
        position: absolute;

        right: 5%;
        top: 50%;

        transform: translateY(-50%);

        width: 250px;
        height: 250px;

        border-radius: 50%;

        border:
            1px solid
            rgba(96,165,250,.14);

        box-shadow:
            0 0 80px
            rgba(37,99,235,.10);
    }


    .circuit-art::before {
        content: "";

        position: absolute;

        left: 15%;
        right: 15%;

        top: 50%;

        height: 2px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #2563eb,
                #22d3ee,
                transparent
            );
    }


    .circuit-art::after {
        content: "V = I × R";

        position: absolute;

        inset: 0;

        display: flex;

        align-items: center;
        justify-content: center;

        color: #60a5fa;

        font-size: 1.35rem;

        font-weight: 800;
    }


    .circuit-dot {
        position: absolute;

        width: 10px;
        height: 10px;

        border-radius: 50%;

        background: #22d3ee;

        box-shadow:
            0 0 20px
            rgba(34,211,238,.9);
    }


    .dot-one {
        top: 28px;
        right: 45px;
    }


    .dot-two {
        bottom: 42px;
        left: 38px;
    }


    /* ==========================================
       SECTIONS
       ========================================== */

    .section {
        margin-top: 2.8rem;
    }


    .section-label {
        color: #60a5fa;

        font-size: .7rem;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: .12em;

        margin-bottom: .4rem;
    }


    .section-title {
        color: #f8fafc;

        font-size: 1.9rem;

        font-weight: 850;

        letter-spacing: -.035em;

        margin-bottom: .4rem;
    }


    .section-description {
        color: #94a3b8;

        max-width: 680px;

        line-height: 1.65;

        font-size: .95rem;
    }


    /* ==========================================
       FEATURE CARDS
       ========================================== */

    .feature-card {
        height: 100%;
        min-height: 190px;

        padding: 1.45rem;

        border-radius: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,.95),
                rgba(11,23,41,.90)
            );

        border:
            1px solid
            rgba(148,163,184,.11);
    }


    .feature-icon {
        font-size: 1.65rem;
        margin-bottom: .85rem;
    }


    .feature-title {
        color: #f8fafc;

        font-size: 1rem;

        font-weight: 750;

        margin-bottom: .45rem;
    }


    .feature-text {
        color: #94a3b8;

        font-size: .84rem;

        line-height: 1.6;
    }


    /* ==========================================
       COURSE CARDS
       ========================================== */

    .course-card {
        min-height: 205px;

        padding: 1.35rem;

        border-radius: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,.96),
                rgba(11,23,41,.92)
            );

        border:
            1px solid
            rgba(148,163,184,.11);

        transition:
            transform .2s ease,
            border-color .2s ease,
            box-shadow .2s ease;
    }


    .course-card:hover {
        transform: translateY(-3px);

        border-color:
            rgba(96,165,250,.28);

        box-shadow:
            0 15px 40px
            rgba(0,0,0,.18);
    }


    .course-icon {
        width: 44px;
        height: 44px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            rgba(37,99,235,.10);

        font-size: 1.35rem;

        margin-bottom: 1rem;
    }


    .course-title {
        color: #f8fafc;

        font-size: .98rem;

        font-weight: 750;

        margin-bottom: .45rem;
    }


    .course-description {
        color: #94a3b8;

        font-size: .81rem;

        line-height: 1.55;
    }


    /* ==========================================
       LEARNING PATH
       ========================================== */

    .path-card {
        padding: 1.35rem;

        border-radius: 17px;

        background:
            rgba(15,23,42,.78);

        border:
            1px solid
            rgba(148,163,184,.11);
    }


    .path-step {
        display: flex;

        align-items: center;

        gap: 12px;

        padding: 10px 0;
    }


    .path-number {
        width: 34px;
        height: 34px;

        flex: 0 0 34px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #06b6d4
            );

        color: white;

        font-size: .78rem;

        font-weight: 800;
    }


    .path-title {
        color: #e2e8f0;

        font-size: .87rem;

        font-weight: 700;
    }


    .path-description {
        color: #64748b;

        font-size: .73rem;

        margin-top: 2px;
    }


    /* ==========================================
       PHILOSOPHY
       ========================================== */

    .philosophy {
        height: 100%;

        padding: 1.7rem;

        border-radius: 17px;

        background:
            radial-gradient(
                circle at 90% 0%,
                rgba(6,182,212,.10),
                transparent 35%
            ),
            rgba(15,23,42,.78);

        border:
            1px solid
            rgba(96,165,250,.12);
    }


    .philosophy-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }


    .philosophy-title {
        color: #f8fafc;

        font-size: 1.05rem;

        font-weight: 800;

        margin-bottom: .75rem;
    }


    .philosophy-text {
        color: #94a3b8;

        font-size: .87rem;

        line-height: 1.7;
    }


    .philosophy-highlight {
        display: inline-block;

        margin-top: 1rem;

        color: #60a5fa;

        font-size: .85rem;

        font-weight: 800;
    }


    /* ==========================================
       CTA
       ========================================== */

    .cta {
        text-align: center;

        padding: 3rem 1.5rem;

        margin-top: 3rem;

        border-radius: 22px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(37,99,235,.20),
                transparent 55%
            ),
            #0b1729;

        border:
            1px solid
            rgba(96,165,250,.14);
    }


    .cta-title {
        color: #f8fafc;

        font-size: 1.85rem;

        font-weight: 850;

        letter-spacing: -.035em;
    }


    .cta-text {
        color: #94a3b8;

        max-width: 600px;

        margin: .7rem auto 0;

        line-height: 1.6;

        font-size: .92rem;
    }


    /* ==========================================
       MOBILE
       ========================================== */

    @media (max-width: 850px) {

        .hero {
            padding: 2.6rem 1.5rem;
        }

        .circuit-art {
            display: none;
        }

        .hero-title {
            font-size: 3rem;
        }

    }

    </style>
    """
)


# ============================================================
# HERO
# ============================================================

html(
    """
    <div class="hero">

        <div class="circuit-art">
            <div class="circuit-dot dot-one"></div>
            <div class="circuit-dot dot-two"></div>
        </div>

        <div class="hero-content">

            <div class="eyebrow">
                ⚡ Interactive Electronics Learning
            </div>

            <h1 class="hero-title">
                Electronics
                <br>
                <span class="hero-highlight">
                    made simple.
                </span>
            </h1>

            <p class="hero-description">
                Learn electronics from the ground up through
                clear explanations, interactive experiments,
                circuit analysis and practical challenges.
            </p>

        </div>

    </div>
    """
)


# ============================================================
# HERO BUTTONS
# ============================================================

button_one, button_two = st.columns(2)


with button_one:

    if st.button(
        "🚀  Start Learning",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("app_fundamentals.py")


with button_two:

    if st.button(
        "🧪  Explore Circuit Analysis",
        use_container_width=True,
    ):
        st.switch_page("app_circuit_analysis.py")


# ============================================================
# WHY ELECT4BEGINNERS
# ============================================================

html(
    """
    <div class="section">

        <div class="section-label">
            WHY ELECT4BEGINNERS
        </div>

        <div class="section-title">
            Learn by understanding, not memorising.
        </div>

        <div class="section-description">
            Electronics becomes easier when you can connect
            the theory to what actually happens inside a
            circuit. Learn the concept, experiment with it,
            then apply it.
        </div>

    </div>
    """
)


st.markdown("<br>", unsafe_allow_html=True)


features = [
    (
        "📚",
        "Clear lessons",
        "Complex electronics concepts explained in simple, "
        "beginner-friendly language.",
    ),
    (
        "🧪",
        "Interactive learning",
        "Explore circuits, calculations and electrical "
        "principles instead of only reading about them.",
    ),
    (
        "🧮",
        "Practical calculations",
        "Apply Ohm's law, power, energy and circuit analysis "
        "to real electrical problems.",
    ),
    (
        "🧠",
        "Build confidence",
        "Move from understanding the basics to solving "
        "practical electronics problems.",
    ),
]


feature_columns = st.columns(4)


for column, feature in zip(feature_columns, features):

    icon, title, description = feature

    with column:

        html(
            f"""
            <div class="feature-card">

                <div class="feature-icon">
                    {icon}
                </div>

                <div class="feature-title">
                    {title}
                </div>

                <div class="feature-text">
                    {description}
                </div>

            </div>
            """
        )


# ============================================================
# CURRICULUM
# ============================================================

html(
    """
    <div class="section">

        <div class="section-label">
            THE CURRICULUM
        </div>

        <div class="section-title">
            Start with the fundamentals.
        </div>

        <div class="section-description">
            Work through the core areas of electronics,
            from basic electrical principles to
            semiconductors, digital systems and measurement.
        </div>

    </div>
    """
)


st.markdown("<br>", unsafe_allow_html=True)


courses = [
    (
        "🔋",
        "Electrical Fundamentals",
        "Voltage, current, resistance, power, energy, AC/DC and basic circuits.",
        "app_fundamentals.py",
    ),
    (
        "⚡",
        "Electronic Components",
        "Understand the components that make modern circuits work.",
        "app_components.py",
    ),
    (
        "🔌",
        "Logic Gates",
        "Explore AND, OR, NOT, NAND, NOR, XOR and digital logic.",
        "app_gates.py",
    ),
    (
        "💾",
        "Digital Electronics",
        "Learn binary logic and the foundations of digital systems.",
        "app_digital_electronics.py",
    ),
    (
        "🧮",
        "Circuit Analysis",
        "Apply Ohm's law, Kirchhoff's laws and circuit analysis.",
        "app_circuit_analysis.py",
    ),
    (
        "🔺",
        "Diodes & Rectifiers",
        "Understand diode behaviour, rectification and applications.",
        "app_rectifiers.py",
    ),
    (
        "🔀",
        "Transistors & Amplifiers",
        "Learn transistor operation, switching and amplification.",
        "app_amplifiers.py",
    ),
    (
        "📏",
        "Measurements & Instruments",
        "Learn how to measure and interpret electrical quantities.",
        "app_measurements.py",
    ),
]


for start in range(0, len(courses), 4):

    row = courses[start:start + 4]

    columns = st.columns(4)

    for column, course in zip(columns, row):

        icon, title, description, page = course

        with column:

            html(
                f"""
                <div class="course-card">

                    <div class="course-icon">
                        {icon}
                    </div>

                    <div class="course-title">
                        {title}
                    </div>

                    <div class="course-description">
                        {description}
                    </div>

                </div>
                """
            )

            if st.button(
                "Explore →",
                key=f"explore_{page}",
                use_container_width=True,
            ):
                st.switch_page(page)


# ============================================================
# LEARNING PATH
# ============================================================

html(
    """
    <div class="section">

        <div class="section-label">
            LEARNING PATH
        </div>

        <div class="section-title">
            Build your knowledge step by step.
        </div>

        <div class="section-description">
            Start with the language of electricity, understand
            the components, then learn how complete circuits
            and electronic systems work.
        </div>

    </div>
    """
)


st.markdown("<br>", unsafe_allow_html=True)


path_column, philosophy_column = st.columns([1.2, 1])


with path_column:

    html(
        """
        <div class="path-card">

            <div class="path-step">

                <div class="path-number">
                    1
                </div>

                <div>
                    <div class="path-title">
                        Electrical Fundamentals
                    </div>

                    <div class="path-description">
                        Learn the language of electricity.
                    </div>
                </div>

            </div>

            <div class="path-step">

                <div class="path-number">
                    2
                </div>

                <div>
                    <div class="path-title">
                        Electronic Components
                    </div>

                    <div class="path-description">
                        Meet the building blocks of circuits.
                    </div>
                </div>

            </div>

            <div class="path-step">

                <div class="path-number">
                    3
                </div>

                <div>
                    <div class="path-title">
                        Circuit Analysis
                    </div>

                    <div class="path-description">
                        Understand how components work together.
                    </div>
                </div>

            </div>

            <div class="path-step">

                <div class="path-number">
                    4
                </div>

                <div>
                    <div class="path-title">
                        Semiconductors & Digital Electronics
                    </div>

                    <div class="path-description">
                        Move into modern electronic systems.
                    </div>
                </div>

            </div>

            <div class="path-step">

                <div class="path-number">
                    5
                </div>

                <div>
                    <div class="path-title">
                        Measurements & Practice
                    </div>

                    <div class="path-description">
                        Apply what you have learned.
                    </div>
                </div>

            </div>

        </div>
        """
    )


with philosophy_column:

    html(
        """
        <div class="philosophy">

            <div class="philosophy-icon">
                🧠
            </div>

            <div class="philosophy-title">
                The Elect4Beginners approach
            </div>

            <div class="philosophy-text">

                Don't just memorise that
                <strong style="color:#e2e8f0;">
                    V = I × R
                </strong>.

                Understand what voltage means,
                see how resistance changes current,
                calculate the result and then apply
                it to an actual circuit.

                <br><br>

                The goal isn't simply to finish lessons.

                The goal is to understand electronics
                well enough to use it.

            </div>

            <div class="philosophy-highlight">
                Understand → Experiment → Apply
            </div>

        </div>
        """
    )


# ============================================================
# CTA
# ============================================================

html(
    """
    <div class="cta">

        <div class="cta-title">
            Ready to understand electronics?
        </div>

        <div class="cta-text">
            Start with the fundamentals and build your
            knowledge one concept at a time.
        </div>

    </div>
    """
)


st.markdown("<br>", unsafe_allow_html=True)


if st.button(
    "⚡  Begin with Electrical Fundamentals",
    use_container_width=True,
    type="primary",
):
    st.switch_page("app_fundamentals.py")


# ============================================================
# FOOTER
# ============================================================

html(
    """
    <div style="
        margin-top:3rem;
        padding-top:1.4rem;
        border-top:1px solid rgba(148,163,184,.10);
        text-align:center;
        color:#475569;
        font-size:.75rem;
    ">

        <strong style="color:#64748b;">
            ⚡ Elect4Beginners
        </strong>

        <span style="margin:0 8px;">
            •
        </span>

        Electronics made simple.

    </div>
    """
)
