import streamlit as st


st.set_page_config(
    page_title="Elect4Beginners — Electronics Made Simple",
    page_icon="⚡",
    layout="wide",
)


# ============================================================
# PAGE STYLES
# ============================================================

st.markdown(
    """
    <style>

    .hero {
        position: relative;
        overflow: hidden;
        padding: 4.5rem 3.5rem;
        border-radius: 28px;
        margin-bottom: 2.5rem;

        background:
            radial-gradient(
                circle at 85% 20%,
                rgba(6,182,212,.22),
                transparent 25%
            ),
            radial-gradient(
                circle at 20% 80%,
                rgba(37,99,235,.22),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #0b1729,
                #07111f
            );

        border: 1px solid
            rgba(96,165,250,.16);

        box-shadow:
            0 25px 70px
            rgba(0,0,0,.25);
    }

    .eyebrow {
        display: inline-block;
        padding: .35rem .7rem;
        border-radius: 999px;

        background: rgba(37,99,235,.12);
        border: 1px solid rgba(96,165,250,.18);

        color: #60a5fa;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;

        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(2.8rem, 6vw, 5.5rem);
        line-height: .98;
        letter-spacing: -.055em;
        font-weight: 900;

        color: #f8fafc;

        max-width: 850px;
        margin: 0;
    }

    .hero-title span {
        background:
            linear-gradient(
                90deg,
                #60a5fa,
                #22d3ee
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        line-height: 1.7;

        max-width: 700px;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }


    /* =============================
       CIRCUIT VISUAL
       ============================= */

    .circuit {
        position: absolute;
        right: 4%;
        top: 15%;
        width: 260px;
        height: 260px;

        border-radius: 50%;

        border:
            1px solid
            rgba(96,165,250,.14);

        box-shadow:
            0 0 70px
            rgba(37,99,235,.10);
    }

    .circuit::before {
        content: "V = I × R";

        position: absolute;
        inset: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #60a5fa;
        font-size: 1.3rem;
        font-weight: 800;
    }

    .circuit::after {
        content: "";

        position: absolute;

        width: 12px;
        height: 12px;

        background: #22d3ee;
        border-radius: 50%;

        top: 30px;
        right: 35px;

        box-shadow:
            0 0 25px
            rgba(34,211,238,.9);
    }


    /* =============================
       SECTION HEADERS
       ============================= */

    .section-label {
        color: #60a5fa;
        font-size: .75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .12em;

        margin-bottom: .4rem;
    }

    .section-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -.035em;

        margin-bottom: .5rem;
    }

    .section-description {
        color: #94a3b8;
        max-width: 650px;
        line-height: 1.65;
    }


    /* =============================
       COURSE CARDS
       ============================= */

    .course-card {
        height: 100%;
        min-height: 205px;

        padding: 1.5rem;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,.96),
                rgba(11,23,41,.92)
            );

        border:
            1px solid
            rgba(148,163,184,.12);

        transition:
            transform .2s ease,
            border-color .2s ease,
            box-shadow .2s ease;
    }

    .course-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(96,165,250,.35);

        box-shadow:
            0 18px 45px
            rgba(0,0,0,.22);
    }

    .course-icon {
        width: 48px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background:
            rgba(37,99,235,.12);

        font-size: 1.45rem;

        margin-bottom: 1.1rem;
    }

    .course-title {
        color: #f8fafc;
        font-weight: 750;
        font-size: 1.05rem;
        margin-bottom: .45rem;
    }

    .course-description {
        color: #94a3b8;
        font-size: .88rem;
        line-height: 1.55;
    }


    /* =============================
       FEATURE CARDS
       ============================= */

    .feature-card {
        padding: 1.6rem;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(37,99,235,.09),
                rgba(6,182,212,.04)
            );

        border:
            1px solid
            rgba(96,165,250,.13);

        height: 100%;
    }

    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: .8rem;
    }

    .feature-title {
        color: #f8fafc;
        font-weight: 750;
        margin-bottom: .45rem;
    }

    .feature-text {
        color: #94a3b8;
        line-height: 1.55;
        font-size: .9rem;
    }


    /* =============================
       LEARNING PATH
       ============================= */

    .path {
        margin-top: 1.5rem;
        padding: 1.5rem;

        border-radius: 18px;

        background:
            rgba(15,23,42,.75);

        border:
            1px solid
            rgba(148,163,184,.12);
    }

    .path-step {
        display: flex;
        align-items: center;
        gap: 1rem;

        padding: .8rem 0;
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
        font-size: .8rem;
        font-weight: 800;
    }

    .path-title {
        color: #e2e8f0;
        font-weight: 650;
    }

    .path-description {
        color: #64748b;
        font-size: .8rem;
    }


    /* =============================
       FINAL CTA
       ============================= */

    .cta {
        text-align: center;

        padding: 3.5rem 2rem;

        margin-top: 3rem;

        border-radius: 24px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(37,99,235,.20),
                transparent 55%
            ),
            #0b1729;

        border:
            1px solid
            rgba(96,165,250,.16);
    }

    .cta-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 850;
        letter-spacing: -.03em;
    }

    .cta-text {
        color: #94a3b8;
        max-width: 600px;
        margin: .8rem auto 1.5rem;
        line-height: 1.6;
    }


    @media (max-width: 800px) {

        .hero {
            padding: 2.5rem 1.5rem;
        }

        .circuit {
            display: none;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="circuit"></div>

        <div class="eyebrow">
            ⚡ Interactive Electronics Learning
        </div>

        <h1 class="hero-title">
            Electronics
            <br>
            <span>made simple.</span>
        </h1>

        <p class="hero-subtitle">
            Learn electronics from the ground up through
            clear explanations, interactive experiments,
            circuit analysis and practical challenges.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


hero_col1, hero_col2 = st.columns([1, 1])

with hero_col1:

    if st.button(
        "🚀 Start Learning",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("app_fundamentals.py")


with hero_col2:

    if st.button(
        "🧪 Explore the Labs",
        use_container_width=True,
    ):
        st.switch_page("app_circuit_analysis.py")


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# WHY ELECT4BEGINNERS
# ============================================================

st.markdown(
    """
    <div class="section-label">
        WHY ELECT4BEGINNERS
    </div>

    <div class="section-title">
        Learn by understanding, not memorising.
    </div>

    <div class="section-description">
        Electronics becomes much easier when you can see
        how the concepts connect. Elect4Beginners combines
        explanations, calculations, diagrams and interactive
        learning into one place.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

feature_cols = st.columns(4)

features = [
    (
        "📚",
        "Clear lessons",
        "Complex electronics concepts explained in beginner-friendly language.",
    ),
    (
        "🧪",
        "Interactive labs",
        "Experiment with circuits and see how electrical principles behave.",
    ),
    (
        "🧮",
        "Practical calculations",
        "Use real electronics formulas instead of learning them in isolation.",
    ),
    (
        "🧠",
        "Build confidence",
        "Test your understanding with examples, challenges and quizzes.",
    ),
]

for col, (icon, title, description) in zip(feature_cols, features):

    with col:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# COURSES
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-label">
        THE CURRICULUM
    </div>

    <div class="section-title">
        Everything you need to get started.
    </div>

    <div class="section-description">
        Follow the learning path from basic electrical
        principles to circuits, semiconductors, digital
        electronics and practical measurements.
    </div>
    """,
    unsafe_allow_html=True,
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
        "Understand resistors, capacitors, inductors, LEDs and other essential components.",
        "app_components.py",
    ),
    (
        "🔌",
        "Logic Gates",
        "Explore AND, OR, NOT, NAND, NOR, XOR and the foundations of digital logic.",
        "app_gates.py",
    ),
    (
        "💾",
        "Digital Electronics",
        "Learn binary logic, digital systems and the building blocks of modern electronics.",
        "app_digital_electronics.py",
    ),
    (
        "🧮",
        "Circuit Analysis",
        "Apply Ohm's law, Kirchhoff's laws and circuit analysis techniques.",
        "app_circuit_analysis.py",
    ),
    (
        "🔺",
        "Diodes & Rectifiers",
        "Understand diode behaviour, rectification and practical applications.",
        "app_rectifiers.py",
    ),
    (
        "🔀",
        "Transistors & Amplifiers",
        "Discover transistor operation, amplification and electronic switching.",
        "app_amplifiers.py",
    ),
    (
        "📏",
        "Measurements & Instruments",
        "Learn how to measure voltage, current, resistance and other electrical quantities.",
        "app_measurements.py",
    ),
]


for row_start in range(0, len(courses), 4):

    row = courses[row_start:row_start + 4]

    cols = st.columns(4)

    for col, course in zip(cols, row):

        icon, title, description, page = course

        with col:

            st.markdown(
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
                """,
                unsafe_allow_html=True,
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

st.markdown("<br><br>", unsafe_allow_html=True)

path_col1, path_col2 = st.columns([1.2, 1])

with path_col1:

    st.markdown(
        """
        <div class="section-label">
            YOUR LEARNING PATH
        </div>

        <div class="section-title">
            Go from beginner to confident.
        </div>

        <div class="section-description">
            A simple progression helps you understand
            why each new concept matters before moving
            on to the next one.
        </div>

        <div class="path">

            <div class="path-step">
                <div class="path-number">1</div>
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
                <div class="path-number">2</div>
                <div>
                    <div class="path-title">
                        Components
                    </div>
                    <div class="path-description">
                        Meet the building blocks of circuits.
                    </div>
                </div>
            </div>

            <div class="path-step">
                <div class="path-number">3</div>
                <div>
                    <div class="path-title">
                        Circuit Analysis
                    </div>
                    <div class="path-description">
                        Learn how components work together.
                    </div>
                </div>
            </div>

            <div class="path-step">
                <div class="path-number">4</div>
                <div>
                    <div class="path-title">
                        Semiconductors & Digital
                    </div>
                    <div class="path-description">
                        Move into modern electronic systems.
                    </div>
                </div>
            </div>

            <div class="path-step">
                <div class="path-number">5</div>
                <div>
                    <div class="path-title">
                        Measurement & Practice
                    </div>
                    <div class="path-description">
                        Apply what you've learned.
                    </div>
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with path_col2:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                🧠
            </div>

            <div class="course-title">
                The Elect4Beginners philosophy
            </div>

            <div class="feature-text">

                Don't just memorise that
                <strong>V = IR</strong>.

                Understand what voltage means,
                see how resistance changes current,
                calculate the result and then
                apply it to a real circuit.

                <br><br>

                <strong style="color:#60a5fa;">
                    Understand → Experiment → Apply
                </strong>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CTA
# ============================================================

st.markdown(
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
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "⚡ Begin with Electrical Fundamentals",
    use_container_width=True,
    type="primary",
):
    st.switch_page("app_fundamentals.py")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br><br>

    <div style="
        border-top:1px solid rgba(148,163,184,.10);
        padding-top:1.5rem;
        text-align:center;
        color:#475569;
        font-size:.78rem;
    ">

        <strong style="color:#64748b;">
            ⚡ Elect4Beginners
        </strong>

        &nbsp; • &nbsp;

        Electronics made simple.

    </div>
    """,
    unsafe_allow_html=True,
)
