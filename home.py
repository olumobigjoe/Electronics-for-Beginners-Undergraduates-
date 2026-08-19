import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Elect4Beginners | Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
)


# ============================================================
# GLOBAL HOME PAGE CSS
# ============================================================

st.html("""
<style>

html, body {
    background: #07111f !important;
}

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(6, 182, 212, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 35%,
            rgba(37, 99, 235, 0.10),
            transparent 30%
        ),
        #07111f !important;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ==========================================
   HERO
   ========================================== */

.hero {
    position: relative;
    overflow: hidden;

    padding: 4rem 3.5rem;

    border-radius: 28px;

    background:
        radial-gradient(
            circle at 85% 35%,
            rgba(34, 211, 238, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 100%,
            rgba(37, 99, 235, 0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0d1b30,
            #07111f
        );

    border: 1px solid rgba(96, 165, 250, 0.16);

    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.25);
}


.hero-content {
    position: relative;
    z-index: 2;

    max-width: 720px;
}


.eyebrow {
    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(37, 99, 235, 0.12);

    border: 1px solid rgba(96, 165, 250, 0.18);

    color: #60a5fa;

    font-size: 0.72rem;

    font-weight: 800;

    letter-spacing: 0.08em;

    text-transform: uppercase;
}


.hero-title {
    margin: 1.2rem 0 0 0;

    color: #f8fafc;

    font-size: clamp(3rem, 6vw, 5.2rem);

    line-height: 0.98;

    letter-spacing: -0.055em;

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
    margin-top: 1.5rem;

    max-width: 650px;

    color: #94a3b8;

    font-size: 1.08rem;

    line-height: 1.75;
}


/* ==========================================
   CIRCUIT GRAPHIC
   ========================================== */

.circuit {
    position: absolute;

    right: 7%;
    top: 50%;

    transform: translateY(-50%);

    width: 260px;
    height: 260px;

    border-radius: 50%;

    border: 1px solid rgba(96, 165, 250, 0.14);

    box-shadow:
        0 0 90px rgba(37, 99, 235, 0.10);
}


.circuit-line {
    position: absolute;

    left: 10%;
    right: 10%;

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

    box-shadow:
        0 0 15px rgba(34, 211, 238, 0.5);
}


.circuit-text {
    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    color: #60a5fa;

    font-size: 1.35rem;

    font-weight: 800;
}


.dot {
    position: absolute;

    width: 11px;
    height: 11px;

    border-radius: 50%;

    background: #22d3ee;

    box-shadow:
        0 0 20px rgba(34, 211, 238, 0.9);
}


.dot-one {
    top: 35px;
    right: 45px;
}


.dot-two {
    bottom: 35px;
    left: 45px;
}


/* ==========================================
   SECTION HEADINGS
   ========================================== */

.section {
    margin-top: 3rem;
}


.section-label {
    color: #60a5fa;

    font-size: 0.7rem;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.12em;
}


.section-title {
    margin-top: 0.45rem;

    color: #f8fafc;

    font-size: 2rem;

    font-weight: 850;

    letter-spacing: -0.04em;
}


.section-description {
    margin-top: 0.5rem;

    max-width: 700px;

    color: #94a3b8;

    font-size: 0.95rem;

    line-height: 1.7;
}


/* ==========================================
   CARDS
   ========================================== */

.card {
    min-height: 190px;

    padding: 1.5rem;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.96),
            rgba(11, 23, 41, 0.92)
        );

    border:
        1px solid rgba(148, 163, 184, 0.11);
}


.card-icon {
    font-size: 1.7rem;

    margin-bottom: 1rem;
}


.card-title {
    color: #f8fafc;

    font-size: 1rem;

    font-weight: 750;

    margin-bottom: 0.5rem;
}


.card-text {
    color: #94a3b8;

    font-size: 0.84rem;

    line-height: 1.65;
}


/* ==========================================
   COURSE CARD
   ========================================== */

.course {
    min-height: 205px;

    padding: 1.35rem;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.96),
            rgba(11, 23, 41, 0.92)
        );

    border:
        1px solid rgba(148, 163, 184, 0.11);
}


.course-icon {
    width: 46px;
    height: 46px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 13px;

    background:
        rgba(37, 99, 235, 0.11);

    font-size: 1.4rem;

    margin-bottom: 1rem;
}


.course-title {
    color: #f8fafc;

    font-size: 0.98rem;

    font-weight: 750;

    margin-bottom: 0.5rem;
}


.course-text {
    color: #94a3b8;

    font-size: 0.81rem;

    line-height: 1.6;
}


/* ==========================================
   LEARNING PATH
   ========================================== */

.path {
    padding: 1.5rem;

    border-radius: 18px;

    background:
        rgba(15, 23, 42, 0.8);

    border:
        1px solid rgba(148, 163, 184, 0.11);
}


.path-item {
    display: flex;

    align-items: center;

    gap: 12px;

    padding: 10px 0;
}


.path-number {
    width: 36px;
    height: 36px;

    flex: 0 0 36px;

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

    font-weight: 800;

    font-size: 0.78rem;
}


.path-name {
    color: #e2e8f0;

    font-size: 0.88rem;

    font-weight: 700;
}


.path-small {
    color: #64748b;

    font-size: 0.73rem;

    margin-top: 2px;
}


/* ==========================================
   CTA
   ========================================== */

.cta {
    margin-top: 3rem;

    padding: 3.5rem 2rem;

    text-align: center;

    border-radius: 24px;

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(37, 99, 235, 0.22),
            transparent 55%
        ),
        #0b1729;

    border:
        1px solid rgba(96, 165, 250, 0.14);
}


.cta-title {
    color: #f8fafc;

    font-size: 2rem;

    font-weight: 850;

    letter-spacing: -0.04em;
}


.cta-text {
    max-width: 600px;

    margin: 0.7rem auto 0;

    color: #94a3b8;

    line-height: 1.65;
}


.footer {
    margin-top: 3rem;

    padding-top: 1.5rem;

    border-top:
        1px solid rgba(148, 163, 184, 0.10);

    text-align: center;

    color: #475569;

    font-size: 0.75rem;
}


/* ==========================================
   MOBILE
   ========================================== */

@media (max-width: 850px) {

    .hero {
        padding: 2.5rem 1.5rem;
    }

    .circuit {
        display: none;
    }

    .hero-title {
        font-size: 3rem;
    }

}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="circuit">

        <div class="circuit-line"></div>

        <div class="circuit-text">
            V = I × R
        </div>

        <div class="dot dot-one"></div>

        <div class="dot dot-two"></div>

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


        <div class="hero-description">
            Learn electronics from the ground up through
            clear explanations, interactive experiments,
            circuit analysis and practical challenges.
        </div>

    </div>

</div>
""")


# ============================================================
# HERO BUTTONS
# ============================================================

left, right = st.columns(2)

with left:

    if st.button(
        "🚀  Start Learning",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("app_fundamentals.py")


with right:

    if st.button(
        "🧪  Explore Circuit Analysis",
        use_container_width=True,
    ):
        st.switch_page("app_circuit_analysis.py")


# ============================================================
# WHY ELECT4BEGINNERS
# ============================================================

st.html("""
<div class="section">

    <div class="section-label">
        WHY ELECT4BEGINNERS
    </div>

    <div class="section-title">
        Learn by understanding, not memorising.
    </div>

    <div class="section-description">
        Electronics becomes easier when you can connect
        theory to what actually happens inside a circuit.
        Learn the concept, experiment with it, then apply it.
    </div>

</div>
""")


st.write("")


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


columns = st.columns(4)

for column, item in zip(columns, features):

    icon, title, text = item

    with column:

        st.html(
            f"""
            <div class="card">

                <div class="card-icon">
                    {icon}
                </div>

                <div class="card-title">
                    {title}
                </div>

                <div class="card-text">
                    {text}
                </div>

            </div>
            """
        )


# ============================================================
# CURRICULUM
# ============================================================

st.html("""
<div class="section">

    <div class="section-label">
        THE CURRICULUM
    </div>

    <div class="section-title">
        Everything you need to build a foundation.
    </div>

    <div class="section-description">
        Progress from basic electrical principles to
        components, circuits, digital electronics,
        semiconductors and measurement.
    </div>

</div>
""")


st.write("")


courses = [
    (
        "🔋",
        "Electrical Fundamentals",
        "Voltage, current, resistance, power, energy and basic circuits.",
        "app_fundamentals.py",
    ),
    (
        "⚡",
        "Electronic Components",
        "Understand the components that make electronic circuits work.",
        "app_components.py",
    ),
    (
        "🔌",
        "Logic Gates",
        "Explore AND, OR, NOT, NAND, NOR and XOR logic.",
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

    cols = st.columns(4)

    for col, course in zip(cols, row):

        icon, title, text, page = course

        with col:

            st.html(
                f"""
                <div class="course">

                    <div class="course-icon">
                        {icon}
                    </div>

                    <div class="course-title">
                        {title}
                    </div>

                    <div class="course-text">
                        {text}
                    </div>

                </div>
                """
            )

            if st.button(
                "Explore →",
                key=f"course_{page}",
                use_container_width=True,
            ):
                st.switch_page(page)


# ============================================================
# LEARNING PATH
# ============================================================

st.html("""
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
""")


st.write("")


path_col, philosophy_col = st.columns([1.2, 1])


with path_col:

    st.html("""
    <div class="path">

        <div class="path-item">

            <div class="path-number">1</div>

            <div>
                <div class="path-name">
                    Electrical Fundamentals
                </div>

                <div class="path-small">
                    Learn the language of electricity.
                </div>
            </div>

        </div>


        <div class="path-item">

            <div class="path-number">2</div>

            <div>
                <div class="path-name">
                    Electronic Components
                </div>

                <div class="path-small">
                    Meet the building blocks of circuits.
                </div>
            </div>

        </div>


        <div class="path-item">

            <div class="path-number">3</div>

            <div>
                <div class="path-name">
                    Circuit Analysis
                </div>

                <div class="path-small">
                    Understand how components work together.
                </div>
            </div>

        </div>


        <div class="path-item">

            <div class="path-number">4</div>

            <div>
                <div class="path-name">
                    Digital Electronics
                </div>

                <div class="path-small">
                    Move into modern electronic systems.
                </div>
            </div>

        </div>


        <div class="path-item">

            <div class="path-number">5</div>

            <div>
                <div class="path-name">
                    Measurements & Practice
                </div>

                <div class="path-small">
                    Apply what you have learned.
                </div>
            </div>

        </div>

    </div>
    """)


with philosophy_col:

    st.html("""
    <div class="card">

        <div class="card-icon">
            🧠
        </div>

        <div class="card-title">
            The Elect4Beginners approach
        </div>

        <div class="card-text">

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

            <br><br>

            <strong style="color:#60a5fa;">
                Understand → Experiment → Apply
            </strong>

        </div>

    </div>
    """)


# ============================================================
# CTA
# ============================================================

st.html("""
<div class="cta">

    <div class="cta-title">
        Ready to understand electronics?
    </div>

    <div class="cta-text">
        Start with the fundamentals and build your
        knowledge one concept at a time.
    </div>

</div>
""")


st.write("")


if st.button(
    "⚡  Begin with Electrical Fundamentals",
    use_container_width=True,
    type="primary",
):
    st.switch_page("app_fundamentals.py")


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    <strong style="color:#64748b;">
        ⚡ Elect4Beginners
    </strong>

    &nbsp; • &nbsp;

    Electronics made simple.

</div>
""")
