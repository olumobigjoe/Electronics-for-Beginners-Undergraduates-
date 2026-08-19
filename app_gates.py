"""
Interactive Logic Gates Learning App
Built for undergraduate electronics students (first module: Logic Gates)
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Logic Gates 101",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}

    /* ---- Concept cards (Intro page) ---- */
    .gate-card {
        background: linear-gradient(135deg, #4c1d95, #1e3a8a);
        border: 1px solid #6366f1;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    }
    .gate-card, .gate-card h4, .gate-card p, .gate-card b {
        color: #ffffff !important;
    }

    /* ---- Application cards (Uses page) ---- */
    .app-card {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border-left: 5px solid #34d399;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .app-card, .app-card b {
        color: #ffffff !important;
    }

    /* ---- Output bulb (Simulator page) ---- */
    .bulb-wrap {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .bulb-on {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #fff9c4, #ffd60a 45%, #f59e0b 75%, #b45309 100%);
        box-shadow:
            0 0 25px 10px rgba(255, 214, 10, 0.85),
            0 0 60px 30px rgba(255, 176, 10, 0.45),
            inset 0 0 15px rgba(255,255,255,0.6);
        animation: pulse-glow 1.6s ease-in-out infinite;
    }
    .bulb-off {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #6b7280, #374151 60%, #111827 100%);
        box-shadow: inset 0 0 12px rgba(0,0,0,0.7);
        opacity: 0.85;
    }
    @keyframes pulse-glow {
        0%   { box-shadow: 0 0 20px 8px rgba(255,214,10,0.7), 0 0 50px 25px rgba(255,176,10,0.35), inset 0 0 15px rgba(255,255,255,0.6); }
        50%  { box-shadow: 0 0 32px 14px rgba(255,214,10,0.95), 0 0 75px 38px rgba(255,176,10,0.55), inset 0 0 18px rgba(255,255,255,0.75); }
        100% { box-shadow: 0 0 20px 8px rgba(255,214,10,0.7), 0 0 50px 25px rgba(255,176,10,0.35), inset 0 0 15px rgba(255,255,255,0.6); }
    }

    /* ---- Gate symbol image frame (Types of Gates page) ---- */
    .symbol-frame {
        background: #f9fafb;
        border-radius: 10px;
        padding: 0.6rem;
        text-align: center;
        border: 1px solid #374151;
    }

    /* ---- Simulator gate header banner ---- */
    .gate-banner {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        font-size: 1.05rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.35);
    }

    .big-symbol {
        font-family: monospace;
        font-size: 1.1rem;
        background: #0b0f17;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        color: #93c5fd;
        white-space: pre;
    }
    h1, h2, h3 {
        color: #f9fafb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# GATE DATA (7 basic gates)
# ----------------------------------------------------------------------
GATES = {
    "AND": {
        "expr": "Y = A · B",
        "desc": "Output is HIGH (1) only when ALL inputs are HIGH.",
        "symbol": "  A ──┐\n       )D──── Y\n  B ──┘\n  (AND shape)",
        "apps": "Used in safety interlock systems (e.g., a machine only runs if door is closed AND power is on).",
        "inputs": 2,
        "logic": lambda a, b: int(a and b),
    },
    "OR": {
        "expr": "Y = A + B",
        "desc": "Output is HIGH (1) if AT LEAST ONE input is HIGH.",
        "symbol": "  A ──╮\n       )>──── Y\n  B ──╯\n  (OR curved shape)",
        "apps": "Used in alarm systems (alarm triggers if smoke sensor OR door sensor activates).",
        "inputs": 2,
        "logic": lambda a, b: int(a or b),
    },
    "NOT": {
        "expr": "Y = A'",
        "desc": "Output is the OPPOSITE (inverse) of the input.",
        "symbol": "  A ──▷o──── Y\n  (Triangle + bubble)",
        "apps": "Used to invert signals, e.g., turning an 'active LOW' sensor signal into 'active HIGH'.",
        "inputs": 1,
        "logic": lambda a, b=None: int(not a),
    },
    "NAND": {
        "expr": "Y = (A · B)'",
        "desc": "Output is LOW (0) only when ALL inputs are HIGH; otherwise HIGH. (AND + NOT)",
        "symbol": "  A ──┐\n       )Do──── Y\n  B ──┘\n  (AND shape + bubble)",
        "apps": "Universal gate — used to build ALL other gates; common in memory (SRAM) cells.",
        "inputs": 2,
        "logic": lambda a, b: int(not (a and b)),
    },
    "NOR": {
        "expr": "Y = (A + B)'",
        "desc": "Output is HIGH (1) only when ALL inputs are LOW; otherwise LOW. (OR + NOT)",
        "symbol": "  A ──╮\n       )>o──── Y\n  B ──╯\n  (OR shape + bubble)",
        "apps": "Universal gate — used in rocket guidance systems (Apollo Guidance Computer used only NOR gates).",
        "inputs": 2,
        "logic": lambda a, b: int(not (a or b)),
    },
    "XOR": {
        "expr": "Y = A ⊕ B",
        "desc": "Output is HIGH (1) only when inputs are DIFFERENT.",
        "symbol": "  A ──╮\n      ))>──── Y\n  B ──╯\n  (OR shape, double curve)",
        "apps": "Used in binary adders (half-adder sum bit) and simple parity/error-checking circuits.",
        "inputs": 2,
        "logic": lambda a, b: int(a != b),
    },
    "XNOR": {
        "expr": "Y = (A ⊕ B)'",
        "desc": "Output is HIGH (1) only when inputs are the SAME.",
        "symbol": "  A ──╮\n      ))>o──── Y\n  B ──╯\n  (XOR shape + bubble)",
        "apps": "Used in equality comparators — checking if two binary numbers/bits match.",
        "inputs": 2,
        "logic": lambda a, b: int(a == b),
    },
}

GATE_ORDER = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]

# Distinct accent color per gate, used on symbol fill + simulator banner
GATE_COLORS = {
    "AND": "#3b82f6",
    "OR": "#8b5cf6",
    "NOT": "#ef4444",
    "NAND": "#f59e0b",
    "NOR": "#14b8a6",
    "XOR": "#ec4899",
    "XNOR": "#22c55e",
}


def _flat(html):
    """Collapse multi-line/indented HTML into one line with no blank lines.

    Streamlit's Markdown renderer treats a blank line inside an HTML block as
    the end of that block, so any indented lines that follow get shown as
    literal text instead of being rendered. Flattening avoids that entirely.
    """
    return "".join(line.strip() for line in html.strip().splitlines())


def _input_lines(two_inputs, fill):
    """Common A / B (or just A) input leads + labels."""
    if two_inputs:
        return f"""
        <line x1="5" y1="35" x2="60" y2="35" stroke="#111827" stroke-width="4"/>
        <line x1="5" y1="105" x2="60" y2="105" stroke="#111827" stroke-width="4"/>
        <text x="0" y="28" font-size="16" font-weight="bold" fill="#111827">A</text>
        <text x="0" y="98" font-size="16" font-weight="bold" fill="#111827">B</text>
        """
    return f"""
    <line x1="5" y1="70" x2="60" y2="70" stroke="#111827" stroke-width="4"/>
    <text x="0" y="63" font-size="16" font-weight="bold" fill="#111827">A</text>
    """


def draw_gate_svg(name):
    """Return a clean, standard (ANSI-style) SVG schematic symbol for the gate."""
    color = GATE_COLORS[name]
    svg_open = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    svg_close = "</svg>"
    out_label = '<text x="196" y="63" font-size="16" font-weight="bold" fill="#111827">Y</text>'

    if name == "AND":
        body = f"""
        <path d="M60,20 L110,20 A50,50 0 0 1 110,120 L60,120 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <line x1="160" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    elif name == "OR":
        body = f"""
        <path d="M60,20 Q95,70 60,120 Q135,110 170,70 Q135,30 60,20 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <line x1="170" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    elif name == "NOT":
        body = f"""
        <path d="M60,20 L60,120 L160,70 Z" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <circle cx="172" cy="70" r="12" fill="white" stroke="{color}" stroke-width="4"/>
        <line x1="184" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(False, color) + body + out_label + svg_close

    elif name == "NAND":
        body = f"""
        <path d="M60,20 L110,20 A50,50 0 0 1 110,120 L60,120 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <circle cx="172" cy="70" r="12" fill="white" stroke="{color}" stroke-width="4"/>
        <line x1="184" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    elif name == "NOR":
        body = f"""
        <path d="M60,20 Q95,70 60,120 Q135,110 170,70 Q135,30 60,20 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <circle cx="182" cy="70" r="12" fill="white" stroke="{color}" stroke-width="4"/>
        <line x1="194" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    elif name == "XOR":
        body = f"""
        <path d="M48,18 Q83,70 48,122" fill="none" stroke="{color}" stroke-width="4"/>
        <path d="M60,20 Q95,70 60,120 Q135,110 170,70 Q135,30 60,20 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <line x1="170" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    elif name == "XNOR":
        body = f"""
        <path d="M48,18 Q83,70 48,122" fill="none" stroke="{color}" stroke-width="4"/>
        <path d="M60,20 Q95,70 60,120 Q135,110 170,70 Q135,30 60,20 Z"
              fill="{color}22" stroke="{color}" stroke-width="4"/>
        <circle cx="182" cy="70" r="12" fill="white" stroke="{color}" stroke-width="4"/>
        <line x1="194" y1="70" x2="200" y2="70" stroke="#111827" stroke-width="4"/>
        """
        raw = svg_open + _input_lines(True, color) + body + out_label + svg_close

    else:
        raw = svg_open + svg_close

    return _flat(raw)


def truth_table(gate_name):
    g = GATES[gate_name]
    rows = []
    if g["inputs"] == 1:
        for a in [0, 1]:
            rows.append({"A": a, "Y": g["logic"](a)})
    else:
        for a in [0, 1]:
            for b in [0, 1]:
                rows.append({"A": a, "B": b, "Y": g["logic"](a, b)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------
# QUIZ DATA (5 questions, 3 options each)
# ----------------------------------------------------------------------
QUIZ = [
    {
        "q": "1. Which gate outputs HIGH only when ALL its inputs are HIGH?",
        "options": ["OR gate", "AND gate", "NOT gate"],
        "answer": "AND gate",
    },
    {
        "q": "2. What does the NOT gate do to its single input?",
        "options": ["Doubles it", "Inverts it", "Leaves it unchanged"],
        "answer": "Inverts it",
    },
    {
        "q": "3. Which gate is called a 'universal gate' because it can build all others?",
        "options": ["XOR gate", "NAND gate", "XNOR gate"],
        "answer": "NAND gate",
    },
    {
        "q": "4. An XOR gate outputs HIGH (1) when its two inputs are:",
        "options": ["The same", "Different", "Both zero"],
        "answer": "Different",
    },
    {
        "q": "5. Which of these is a real-world application of logic gates?",
        "options": ["Traffic light controllers", "Cooking pasta", "Painting a wall"],
        "answer": "Traffic light controllers",
    },
]

# ----------------------------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------------------------
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}

# ----------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
st.sidebar.title("🔌 Logic Gates")
st.sidebar.caption("Module 1 · Digital Electronics Fundamentals")
page = st.sidebar.radio(
    "Navigate",
    [
        "1️⃣ Introduction",
        "2️⃣ Types of Gates",
        "3️⃣ Uses & Applications",
        "4️⃣ Gate Simulator",
        "5️⃣ Quiz",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tip: Work through the sections in order. Use the **Simulator** to "
    "build intuition before attempting the **Quiz**."
)

# ----------------------------------------------------------------------
# 1. INTRODUCTION
# ----------------------------------------------------------------------
if page.startswith("1"):
    st.title("🔌 Introduction to Logic Gates")
    st.markdown(
        """
        ### What is a Logic Gate?
        A **logic gate** is a tiny electronic building block that makes a decision based on
        **binary inputs** — signals that are either **0 (LOW / OFF)** or **1 (HIGH / ON)**.

        Think of a logic gate like a **light switch with rules**:
        - A simple switch turns a light ON or OFF based on *one* action.
        - A logic gate turns its output ON or OFF based on the **combination** of one or more inputs,
          following a fixed rule (its "logic").

        ### Why Do Logic Gates Matter?
        Logic gates are the **fundamental building blocks of all digital electronics** — including
        calculators, smartphones, and the CPU inside your laptop. By combining thousands (or billions!)
        of simple gates, engineers build circuits that can add numbers, store memory, and run entire computers.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="gate-card">
            <h4>🔢 Binary Basics</h4>
            <p><b>1 (HIGH)</b> = ON, True, usually 5V or 3.3V<br>
            <b>0 (LOW)</b> = OFF, False, usually 0V</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="gate-card">
            <h4>🚦 Everyday Analogy</h4>
            <p>An AND gate is like needing a <b>key AND a PIN</b> to open a safe —
            both conditions must be true before you get access.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.success("👉 Head to **'Types of Gates'** in the sidebar to explore all 7 gates.")

# ----------------------------------------------------------------------
# 2. TYPES OF GATES
# ----------------------------------------------------------------------
elif page.startswith("2"):
    st.title("2️⃣ Types of Logic Gates")
    st.caption("There are 7 basic logic gates every electronics student should know.")

    for name in GATE_ORDER:
        g = GATES[name]
        with st.expander(f"**{name} Gate** — {g['expr']}", expanded=False):
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(
                    f'<div class="symbol-frame">{draw_gate_svg(name)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Boolean Expression:** `{g['expr']}`")
                st.write(g["desc"])
            with c2:
                st.markdown("**Truth Table**")
                st.dataframe(truth_table(name), use_container_width=True, hide_index=True)

# ----------------------------------------------------------------------
# 3. USES AND APPLICATIONS
# ----------------------------------------------------------------------
elif page.startswith("3"):
    st.title("3️⃣ Uses and Areas of Application")
    st.write(
        "Logic gates aren't just theory — they're at work inside devices you use every day. "
        "Expand each gate below to see a real-world application."
    )
    for name in GATE_ORDER:
        g = GATES[name]
        st.markdown(
            f"""
            <div class="app-card">
            <b>{name} Gate</b> — {g['apps']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🌍 Broader Application Areas")
    apps = [
        "🖩 **Calculators** — arithmetic circuits (adders/subtractors) built from XOR & AND gates",
        "🚦 **Traffic Light Controllers** — sequencing logic to switch lights safely",
        "🚨 **Alarm & Security Systems** — combining sensor inputs (motion, door, smoke)",
        "💾 **Computer Memory (RAM)** — NAND/NOR gates form the basis of memory cells",
        "🧠 **Microprocessors/CPUs** — billions of gates combined to execute instructions",
        "🔐 **Access Control Systems** — multi-condition unlocking (badge AND PIN)",
    ]
    for a in apps:
        st.markdown(f"- {a}")

# ----------------------------------------------------------------------
# 4. GATE SIMULATOR
# ----------------------------------------------------------------------
elif page.startswith("4"):
    st.title("4️⃣ Interactive Gate Simulator")
    st.caption("Choose a gate, toggle the inputs, and watch the output LED respond live.")

    sel = st.selectbox("Select a Logic Gate", GATE_ORDER)
    g = GATES[sel]
    color = GATE_COLORS[sel]

    st.markdown(
        f"""
        <div class="gate-banner" style="background: linear-gradient(90deg, {color}, {color}aa);">
        ⚡ <b>{sel} Gate</b> &nbsp;|&nbsp; Boolean Expression: <code>{g['expr']}</code> &nbsp;|&nbsp; {g['desc']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_symbol, col_inputs, col_output = st.columns([1.2, 1, 1])

    with col_symbol:
        st.markdown("##### 🔷 Gate Symbol")
        st.markdown(f'<div class="symbol-frame">{draw_gate_svg(sel)}</div>', unsafe_allow_html=True)

    with col_inputs:
        st.markdown("##### 🎛️ Inputs")
        a = st.toggle("Input A", value=False, key="input_a")
        a = int(a)
        if g["inputs"] == 2:
            b = st.toggle("Input B", value=False, key="input_b")
            b = int(b)
            output = g["logic"](a, b)
        else:
            b = None
            output = g["logic"](a)

    with col_output:
        st.markdown("##### 💡 Output Bulb")
        bulb_class = "bulb-on" if output == 1 else "bulb-off"
        st.markdown(f'<div class="bulb-wrap"><div class="{bulb_class}"></div></div>', unsafe_allow_html=True)
        label_color = "#facc15" if output == 1 else "#9ca3af"
        state_word = "HIGH" if output == 1 else "LOW"
        st.markdown(
            f"<h3 style='text-align:center;color:{label_color};'>Y = {output} ({state_word})</h3>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("📋 Truth Table (current row highlighted)")
    tt = truth_table(sel)
    if g["inputs"] == 2:
        mask = (tt["A"] == a) & (tt["B"] == b)
    else:
        mask = tt["A"] == a

    def highlight_row(row):
        is_current = (row["A"] == a) and (g["inputs"] == 1 or row["B"] == b)
        return ["background-color: #16a34a; color: white" if is_current else "" for _ in row]

    st.dataframe(tt.style.apply(highlight_row, axis=1), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown(
        """
        <div class="gate-banner" style="background: linear-gradient(90deg, #f59e0b, #ef4444);">
        🔗 <b>Bonus: Cascaded Circuit</b> — AND ➜ NOT (this combination behaves exactly like a NAND gate!)
        </div>
        """,
        unsafe_allow_html=True,
    )
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown("##### 🎛️ Inputs")
        ca = st.toggle("Input A ", value=False, key="cascade_a")
        cb = st.toggle("Input B ", value=False, key="cascade_b")
    and_out = int(ca and cb)
    not_out = int(not and_out)
    with cc2:
        st.markdown("##### ⚙️ Stage Outputs")
        st.markdown(f"AND stage output: **{and_out}**")
        st.markdown(f"NOT stage (final) output: **{not_out}**")
    with cc3:
        st.markdown("##### 💡 Final Bulb")
        bulb_class = "bulb-on" if not_out == 1 else "bulb-off"
        st.markdown(f'<div class="bulb-wrap"><div class="{bulb_class}"></div></div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 5. QUIZ
# ----------------------------------------------------------------------
elif page.startswith("5"):
    st.title("5️⃣ Logic Gates Quiz")
    st.caption("5 questions · 3 options each · Scored out of 100%")

    with st.form("quiz_form"):
        for i, item in enumerate(QUIZ):
            st.markdown(f"**{item['q']}**")
            choice = st.radio(
                label=f"q{i}",
                options=item["options"],
                index=None,
                key=f"quiz_radio_{i}",
                label_visibility="collapsed",
            )
            st.session_state.quiz_answers[i] = choice
            st.markdown("")
        submitted = st.form_submit_button("✅ Submit Quiz")

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        answers = st.session_state.quiz_answers
        if any(v is None for v in answers.values()):
            st.warning("⚠️ Please answer all 5 questions before submitting.")
        else:
            correct_count = sum(
                1 for i, item in enumerate(QUIZ) if answers[i] == item["answer"]
            )
            score_pct = round((correct_count / len(QUIZ)) * 100)

            st.markdown("## 📊 Your Results")
            m1, m2 = st.columns(2)
            m1.metric("Score", f"{correct_count}/{len(QUIZ)}")
            m2.metric("Percentage", f"{score_pct}%")
            st.progress(score_pct / 100)

            if score_pct >= 80:
                st.success(f"🎉 Excellent work! You scored {score_pct}%.")
                st.balloons()
            elif score_pct >= 50:
                st.info(f"👍 Good effort! You scored {score_pct}%. Review the gates you missed below.")
            else:
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Types of Gates' section and try again!")

            st.markdown("### Review")
            for i, item in enumerate(QUIZ):
                user_ans = answers[i]
                is_correct = user_ans == item["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"{icon} **{item['q']}**")
                st.write(f"Your answer: {user_ans}")
                if not is_correct:
                    st.write(f"Correct answer: **{item['answer']}**")
                st.markdown("---")

            if st.button("🔄 Retake Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}
                for i in range(len(QUIZ)):
                    st.session_state.pop(f"quiz_radio_{i}", None)
                st.rerun()
