"""
🔋 Electrical Fundamentals Learning Lab
An Interactive Beginner's Guide to Electrical Fundamentals

Built for first-year undergraduate Physics / Electronics students.
Single-file Streamlit application. No external APIs, databases, or internet
services are used — only streamlit, pandas, and matplotlib.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Electrical Fundamentals Learning Lab",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# NOTE: every HTML string below avoids blank lines inside a block — Streamlit's
# Markdown renderer treats a blank line inside an HTML block as the end of
# that block, and anything after gets shown as literal text instead of being
# rendered. The only exception is the <style> tag itself, which CommonMark
# treats as a raw block that isn't terminated by blank lines.
# ============================================================================
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}

    .concept-card {
        background: linear-gradient(135deg, #7c2d12, #9a3412);
        border: 1px solid #fb923c;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    }
    .concept-card, .concept-card h4, .concept-card p, .concept-card b, .concept-card li {
        color: #ffffff !important;
    }

    .app-card {
        background: linear-gradient(135deg, #164e2e, #14532d);
        border-left: 5px solid #4ade80;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .app-card, .app-card b, .app-card li { color: #ffffff !important; }

    .comp-banner {
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        color: #ffffff !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.35);
    }

    .symbol-box {
        background: #f9fafb;
        color: #111827;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #374151;
    }

    .status-good {
        background: #14532d;
        border-left: 5px solid #22c55e;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
    }
    .status-bad {
        background: #7f1d1d;
        border-left: 5px solid #ef4444;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
    }

    .bulb-wrap { text-align: center; padding: 0.6rem 0 0.3rem 0; }
    .bulb-on {
        width: 90px; height: 90px; border-radius: 50%; margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #fff9c4, #ffd60a 45%, #f59e0b 75%, #b45309 100%);
        box-shadow: 0 0 22px 9px rgba(255,214,10,0.85), 0 0 55px 26px rgba(255,176,10,0.45), inset 0 0 12px rgba(255,255,255,0.6);
    }
    .bulb-off {
        width: 90px; height: 90px; border-radius: 50%; margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #6b7280, #374151 60%, #111827 100%);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.7);
        opacity: 0.85;
    }

    .safety-note {
        background: #451a03;
        border-left: 5px solid #f59e0b;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.92rem;
    }

    h1, h2, h3 { color: #f9fafb; }
    </style>
    """,
    unsafe_allow_html=True,
)


def flat(html):
    """Collapse multi-line/indented HTML into one line with no blank lines,
    so Streamlit's Markdown renderer never mistakes it for a code block."""
    return "".join(line.strip() for line in html.strip().splitlines())


# ============================================================================
# CORE ELECTRICAL CALCULATIONS (pure functions, no widgets — reused everywhere)
# ============================================================================

def ohms_law_solve(v=None, i=None, r=None):
    """Given exactly two of (voltage, current, resistance), solve the third."""
    if v is None:
        if i in (None, 0) or r is None:
            return None, "Current must be non-zero to solve for voltage."
        return i * r, "Voltage (V)"
    if i is None:
        if r in (None, 0):
            return None, "Resistance must be non-zero to solve for current."
        return v / r, "Current (A)"
    if r is None:
        if i in (None, 0):
            return None, "Current must be non-zero to solve for resistance."
        return v / i, "Resistance (Ω)"
    return None, "Provide exactly two known values."


def power_solve(v=None, i=None, p=None):
    """Given exactly two of (voltage, current, power), solve the third using P = VI."""
    if p is None:
        if v is None or i is None:
            return None, "Need both voltage and current to find power."
        return v * i, "Power (W)"
    if v is None:
        if i in (None, 0):
            return None, "Current must be non-zero to solve for voltage."
        return p / i, "Voltage (V)"
    if i is None:
        if v in (None, 0):
            return None, "Voltage must be non-zero to solve for current."
        return p / v, "Current (A)"
    return None, "Provide exactly two known values."


def energy_kwh(power_w, hours):
    """Energy in kWh from power (Watts) used over a number of hours."""
    return (power_w * hours) / 1000.0


def series_resistance(values):
    """Total resistance of resistors in series: simple sum."""
    return sum(values)


def parallel_resistance(values):
    """Total resistance of resistors in parallel: 1/Rt = sum(1/R)."""
    values = [v for v in values if v > 0]
    if not values:
        return None
    return 1.0 / sum(1.0 / v for v in values)


def ac_peak_from_rms(v_rms):
    return v_rms * (2 ** 0.5)


def ac_rms_from_peak(v_peak):
    return v_peak / (2 ** 0.5)


def kcl_check(currents_in, currents_out):
    """Kirchhoff's Current Law: sum(in) should equal sum(out) at a node."""
    total_in = sum(currents_in)
    total_out = sum(currents_out)
    balanced = abs(total_in - total_out) < 1e-9
    return balanced, total_in, total_out


def kvl_check(source_voltage, drops):
    """Kirchhoff's Voltage Law: source voltage should equal the sum of drops
    around a single closed loop."""
    total_drops = sum(drops)
    balanced = abs(source_voltage - total_drops) < 1e-9
    return balanced, total_drops


# ============================================================================
# CORE CONCEPTS DATA
# 10 foundational electrical concepts, each with the fields the Explorer /
# Comparison pages need. "calc_key" links a concept to its interactive
# render function further down.
# ============================================================================
CONCEPTS = {
    "Voltage": {
        "desc": "The electrical 'push' or pressure that drives current through a circuit.",
        "unit": "Volt (V)",
        "formula": "V = I × R",
        "category": ["basic_quantity", "source"],
        "explanation": "Voltage is like water pressure in a pipe: the higher the pressure (voltage), the harder current is pushed through a circuit. Voltage is always measured *between two points* — it's a difference, not an absolute quantity.",
        "applications": "Battery ratings, mains supply (230V/120V), electronic device power rails.",
        "safety": "Higher voltages can drive dangerous currents through the human body. Always treat mains voltage (100V+) with extreme caution.",
        "calc_key": "ohms_law",
    },
    "Current": {
        "desc": "The rate of flow of electric charge through a conductor.",
        "unit": "Ampere (A)",
        "formula": "I = V / R",
        "category": ["basic_quantity"],
        "explanation": "Current is like the amount of water flowing past a point in a pipe each second. It's what actually does the work in a circuit — lighting a bulb, spinning a motor, or charging a battery.",
        "applications": "Fuse ratings, wire gauge selection, battery discharge ratings (mAh).",
        "safety": "It's current, not voltage alone, that is dangerous to the body — even a few tens of milliamps through the heart can be hazardous.",
        "calc_key": "ohms_law",
    },
    "Resistance": {
        "desc": "The opposition a material offers to the flow of electric current.",
        "unit": "Ohm (Ω)",
        "formula": "R = V / I",
        "category": ["basic_quantity"],
        "explanation": "Resistance is like a narrow section of pipe restricting water flow. Materials like copper have very low resistance (good conductors); materials like rubber have very high resistance (good insulators).",
        "applications": "Current limiting, heating elements, sensors (thermistors, LDRs).",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "ohms_law",
    },
    "Power": {
        "desc": "The rate at which electrical energy is transferred or converted (e.g. into heat, light, or motion).",
        "unit": "Watt (W)",
        "formula": "P = V × I",
        "category": ["basic_quantity", "energy_related"],
        "explanation": "Power tells you how fast energy is being used. A 100W bulb converts electrical energy into light and heat twice as fast as a 50W bulb.",
        "applications": "Appliance power ratings, power supply sizing, heating element design.",
        "safety": "High power in a small space means high heat — always check that components and wiring are rated for the power they must handle.",
        "calc_key": "power",
    },
    "Energy": {
        "desc": "The total amount of electrical work done over a period of time.",
        "unit": "Joule (J) — commonly billed in kilowatt-hours (kWh)",
        "formula": "Energy (kWh) = Power (kW) × Time (hours)",
        "category": ["energy_related"],
        "explanation": "If power is how *fast* you use electricity, energy is how *much* you used in total. Your electricity bill is based on energy (kWh), not power.",
        "applications": "Electricity billing, battery capacity planning, energy-efficiency comparisons.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "energy",
    },
    "Charge": {
        "desc": "A fundamental property of matter that causes it to experience a force in an electric field; the 'stuff' that current is a flow of.",
        "unit": "Coulomb (C)",
        "formula": "Q = I × t",
        "category": ["basic_quantity"],
        "explanation": "Charge is the total amount of 'electrical stuff' that has moved. One Coulomb is a lot of charge — a typical LED circuit moves only a tiny fraction of a Coulomb per second.",
        "applications": "Battery capacity (Amp-hours), capacitor charge storage, static electricity.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": None,
    },
    "Frequency (AC)": {
        "desc": "The number of times an alternating current or voltage completes a full cycle each second.",
        "unit": "Hertz (Hz)",
        "formula": "f = 1 / T",
        "category": ["ac_dc"],
        "explanation": "Mains electricity doesn't flow in one direction — it oscillates back and forth. Frequency tells you how many times per second it switches direction and returns. Most countries use 50 Hz or 60 Hz mains.",
        "applications": "Mains power systems, audio signals, radio transmission.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "ac",
    },
    "Conductors & Insulators": {
        "desc": "Materials classified by how easily they allow electric current to flow through them.",
        "unit": "N/A (described qualitatively, or by resistivity: Ω·m)",
        "formula": "N/A",
        "category": ["materials"],
        "explanation": "Conductors (like copper and aluminium) have electrons that move freely, allowing current to flow easily. Insulators (like rubber and plastic) hold their electrons tightly, blocking current flow — which is why wires are coated in plastic.",
        "applications": "Wiring (copper conductor, plastic insulation), circuit board traces, high-voltage insulators on power lines.",
        "safety": "Damaged insulation can expose a live conductor — a serious shock and fire hazard. Always inspect cables for cuts or wear.",
        "calc_key": None,
    },
    "AC vs DC": {
        "desc": "The two fundamental ways current can flow: Direct Current (one direction only) and Alternating Current (periodically reversing direction).",
        "unit": "N/A",
        "formula": "N/A",
        "category": ["ac_dc", "source"],
        "explanation": "DC flows steadily in one direction — like from a battery. AC periodically reverses direction — like mains power. AC is used for long-distance power transmission because its voltage can be easily changed with transformers.",
        "applications": "DC: batteries, USB power, electronics. AC: mains power, motors, transmission grids.",
        "safety": "⚠️ Mains AC is dangerous. Never experiment with household mains electricity without qualified supervision.",
        "calc_key": None,
    },
    "Series & Parallel Circuits": {
        "desc": "The two basic ways to connect multiple components: one after another (series) or side-by-side across the same two points (parallel).",
        "unit": "N/A",
        "formula": "Series: Rt = R1+R2+…  |  Parallel: 1/Rt = 1/R1+1/R2+…",
        "category": ["circuit_configuration"],
        "explanation": "In series, the same current flows through every component, but voltage is shared between them. In parallel, every component sees the same voltage, but current is shared between them.",
        "applications": "Household wiring (outlets in parallel so each works independently), string lights (older sets used series wiring), battery packs (series for higher voltage, parallel for higher capacity).",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "series_parallel",
    },
}

CONCEPT_ORDER = list(CONCEPTS.keys())

# ============================================================================
# LAWS DATA (used on the Laws & Relationships page)
# ============================================================================
LAWS = {
    "Ohm's Law": {
        "formula": "V = I × R",
        "explanation": "The voltage across a resistor equals the current flowing through it multiplied by its resistance. This is the single most important relationship in basic circuit analysis.",
        "use": "Solving for any one of voltage, current, or resistance when the other two are known.",
    },
    "Power Law": {
        "formula": "P = V × I  (also P = I²R  or  P = V²/R)",
        "explanation": "Electrical power equals voltage multiplied by current. Combined with Ohm's Law, power can also be expressed purely in terms of current and resistance, or voltage and resistance.",
        "use": "Sizing power supplies, calculating heat dissipation, choosing component power ratings.",
    },
    "Kirchhoff's Current Law (KCL)": {
        "formula": "ΣI(in) = ΣI(out)",
        "explanation": "At any junction (node) in a circuit, the total current flowing in must equal the total current flowing out. Charge cannot pile up or disappear at a junction.",
        "use": "Analysing circuits with multiple branches meeting at a point.",
    },
    "Kirchhoff's Voltage Law (KVL)": {
        "formula": "Σ V(source) = Σ V(drops)",
        "explanation": "Around any closed loop in a circuit, the total supplied voltage must equal the total of all the voltage drops across components in that loop.",
        "use": "Analysing circuits with multiple components in a single loop or multiple loops.",
    },
    "Series Resistance": {
        "formula": "Rt = R1 + R2 + R3 + …",
        "explanation": "When resistors are connected end-to-end (series), their resistances simply add together — the total is always larger than the largest individual resistor.",
        "use": "Calculating total resistance in a single-path circuit.",
    },
    "Parallel Resistance": {
        "formula": "1/Rt = 1/R1 + 1/R2 + 1/R3 + …",
        "explanation": "When resistors are connected side-by-side across the same two points (parallel), the total resistance is always smaller than the smallest individual resistor.",
        "use": "Calculating total resistance when current has multiple paths to choose from.",
    },
}

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each concept. Every returned
# string is flattened to one line with flat() so Streamlit's Markdown
# renderer never mis-parses an embedded blank line as the end of the block.
# ============================================================================
CONCEPT_COLORS = {
    "Voltage": "#f97316",
    "Current": "#3b82f6",
    "Resistance": "#8b5cf6",
    "Power": "#eab308",
    "Energy": "#22c55e",
    "Charge": "#ec4899",
    "Frequency (AC)": "#06b6d4",
    "Conductors & Insulators": "#84cc16",
    "AC vs DC": "#f43f5e",
    "Series & Parallel Circuits": "#0ea5e9",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def draw_concept_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the concept."""
    color = CONCEPT_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Voltage":
        # Battery symbol: long thin plate (+) and short thick plate (-), repeated
        body = f"""
        {_lead(0, 70, 70, 70)}
        <line x1="70" y1="30" x2="70" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="85" y1="45" x2="85" y2="95" stroke="{color}" stroke-width="9"/>
        <line x1="100" y1="30" x2="100" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="115" y1="45" x2="115" y2="95" stroke="{color}" stroke-width="9"/>
        {_lead(115, 70, 220, 70)}
        <text x="60" y="20" font-size="18" font-weight="bold" fill="#111827">+</text>
        <text x="108" y="128" font-size="18" font-weight="bold" fill="#111827">−</text>
        """

    elif name == "Current":
        # Wire with a directional current arrow
        body = f"""
        {_lead(15, 70, 205, 70, color, 5)}
        <polygon points="180,70 160,58 160,82" fill="{color}"/>
        <text x="90" y="45" font-size="15" font-weight="bold" fill="#111827">I</text>
        <circle cx="30" cy="70" r="4" fill="{color}"/>
        <circle cx="60" cy="70" r="4" fill="{color}"/>
        <circle cx="90" cy="70" r="4" fill="{color}"/>
        """

    elif name == "Resistance":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 L72,45 L88,95 L104,45 L120,95 L136,45 L150,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        """

    elif name == "Power":
        # Lightning bolt inside a circle
        body = f"""
        <circle cx="110" cy="70" r="55" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <polygon points="120,20 80,80 105,80 95,120 140,60 112,60" fill="{color}"/>
        """

    elif name == "Energy":
        # Battery + clock combined
        body = f"""
        <rect x="45" y="45" width="60" height="50" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <rect x="103" y="60" width="8" height="20" fill="{color}"/>
        <circle cx="150" cy="70" r="40" fill="none" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="70" x2="150" y2="45" stroke="{color}" stroke-width="3"/>
        <line x1="150" y1="70" x2="168" y2="80" stroke="{color}" stroke-width="3"/>
        """

    elif name == "Charge":
        # Plus and minus charge circles with field lines
        body = f"""
        <circle cx="65" cy="70" r="28" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="55" y="80" font-size="26" font-weight="bold" fill="{color}">+</text>
        <circle cx="155" cy="70" r="28" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="147" y="80" font-size="30" font-weight="bold" fill="{color}">−</text>
        <line x1="93" y1="70" x2="127" y2="70" stroke="{color}" stroke-width="2" stroke-dasharray="4,4"/>
        """

    elif name == "Frequency (AC)":
        # Sine wave
        body = f"""
        {_lead(0, 70, 25, 70)}
        <path d="M25,70 C40,20 55,20 70,70 C85,120 100,120 115,70 C130,20 145,20 160,70 C175,120 190,120 205,70"
              fill="none" stroke="{color}" stroke-width="4"/>
        {_lead(205, 70, 220, 70)}
        """

    elif name == "Conductors & Insulators":
        # Bare wire (conductor) vs insulated wire cross-section
        body = f"""
        <circle cx="60" cy="70" r="22" fill="{color}" stroke="{color}" stroke-width="2"/>
        <text x="30" y="115" font-size="12" font-weight="bold" fill="#111827">Conductor</text>
        <circle cx="160" cy="70" r="30" fill="none" stroke="#9ca3af" stroke-width="10"/>
        <circle cx="160" cy="70" r="16" fill="{color}"/>
        <text x="122" y="115" font-size="12" font-weight="bold" fill="#111827">Insulated wire</text>
        """

    elif name == "AC vs DC":
        # DC steady line vs AC sine wave, side by side
        body = f"""
        <line x1="15" y1="70" x2="95" y2="70" stroke="{color}" stroke-width="4"/>
        <text x="35" y="115" font-size="13" font-weight="bold" fill="#111827">DC</text>
        <path d="M115,70 C127,35 138,35 150,70 C162,105 173,105 185,70 C197,35 205,35 210,55"
              fill="none" stroke="{color}" stroke-width="4"/>
        <text x="150" y="115" font-size="13" font-weight="bold" fill="#111827">AC</text>
        <line x1="105" y1="20" x2="105" y2="120" stroke="#9ca3af" stroke-width="2" stroke-dasharray="3,3"/>
        """

    elif name == "Series & Parallel Circuits":
        # Two small diagrams: series resistors on top, parallel on bottom
        body = f"""
        {_lead(5, 35, 40, 35, color, 3)}
        <path d="M40,35 L48,22 L58,48 L68,22 L78,48 L86,35" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(86, 35, 105, 35, color, 3)}
        <path d="M105,35 L113,22 L123,48 L133,22 L143,48 L151,35" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(151, 35, 215, 35, color, 3)}
        <text x="0" y="20" font-size="11" font-weight="bold" fill="#111827">Series</text>
        {_lead(5, 100, 5, 130, color, 3)}
        {_lead(215, 100, 215, 130, color, 3)}
        {_lead(5, 100, 60, 100, color, 3)}
        <path d="M60,100 L68,90 L78,112 L88,90 L96,100" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(96, 100, 215, 100)}
        {_lead(5, 130, 60, 130, color, 3)}
        <path d="M60,130 L68,120 L78,140 L88,120 L96,130" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(96, 130, 215, 130, color, 3)}
        <text x="0" y="95" font-size="11" font-weight="bold" fill="#111827">Parallel</text>
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same concept is rendered on more than one page.
# ============================================================================

def render_ohms_law_calc(key_prefix):
    st.markdown("**⚙️ Ohm's Law Calculator** — `V = I × R`")
    solve_for = st.radio(
        "Solve for:", ["Voltage (V)", "Current (I)", "Resistance (R)"],
        horizontal=True, key=f"{key_prefix}_ohm_solve",
    )
    c1, c2 = st.columns(2)
    if solve_for == "Voltage (V)":
        i = c1.number_input("Current (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_ohm_i")
        r = c2.number_input("Resistance (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_ohm_r")
        result, label = ohms_law_solve(i=i, r=r)
        r_plot = r
    elif solve_for == "Current (I)":
        v = c1.number_input("Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_ohm_v")
        r = c2.number_input("Resistance (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_ohm_r2")
        result, label = ohms_law_solve(v=v, r=r)
        r_plot = r
    else:
        v = c1.number_input("Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_ohm_v2")
        i = c2.number_input("Current (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_ohm_i2")
        result, label = ohms_law_solve(v=v, i=i)
        r_plot = result if result else 100

    if result is None:
        st.warning(f"⚠️ {label}")
    else:
        st.markdown(f'<div class="status-good">✅ {label} = {result:.3f}</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        currents = [x * 0.05 for x in range(21)]
        voltages = [i_val * r_plot for i_val in currents]
        ax.plot(currents, voltages, color="#f97316", linewidth=2)
        ax.set_xlabel("Current (A)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title(f"V vs I  (R = {r_plot:.1f} Ω)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


def render_power_calc(key_prefix):
    st.markdown("**⚙️ Power Calculator** — `P = V × I`")
    solve_for = st.radio(
        "Solve for:", ["Power (P)", "Voltage (V)", "Current (I)"],
        horizontal=True, key=f"{key_prefix}_pow_solve",
    )
    c1, c2 = st.columns(2)
    if solve_for == "Power (P)":
        v = c1.number_input("Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_pow_v")
        i = c2.number_input("Current (A)", min_value=0.0, value=2.0, step=0.1, key=f"{key_prefix}_pow_i")
        result, label = power_solve(v=v, i=i)
    elif solve_for == "Voltage (V)":
        p = c1.number_input("Power (W)", min_value=0.0, value=24.0, step=1.0, key=f"{key_prefix}_pow_p")
        i = c2.number_input("Current (A)", min_value=0.0, value=2.0, step=0.1, key=f"{key_prefix}_pow_i2")
        result, label = power_solve(p=p, i=i)
    else:
        p = c1.number_input("Power (W)", min_value=0.0, value=24.0, step=1.0, key=f"{key_prefix}_pow_p2")
        v = c2.number_input("Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_pow_v2")
        result, label = power_solve(p=p, v=v)

    if result is None:
        st.warning(f"⚠️ {label}")
    else:
        st.markdown(f'<div class="status-good">✅ {label} = {result:.3f}</div>', unsafe_allow_html=True)


def render_energy_calc(key_prefix):
    st.markdown("**⚙️ Energy Consumption Calculator** — `Energy (kWh) = Power (kW) × Time (h)`")
    c1, c2 = st.columns(2)
    power_w = c1.number_input("Appliance Power (W)", min_value=0.0, value=1000.0, step=50.0, key=f"{key_prefix}_energy_p")
    hours = c2.number_input("Hours used", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_energy_h")
    kwh = energy_kwh(power_w, hours)
    st.markdown(f'<div class="status-good">✅ Energy used ≈ {kwh:.3f} kWh</div>', unsafe_allow_html=True)
    st.caption("This is what your electricity meter and bill are based on — not power alone, but power × time.")


def render_series_parallel_calc(key_prefix):
    st.markdown("**⚙️ Series / Parallel Resistance Calculator**")
    mode = st.radio("Configuration:", ["Series", "Parallel"], horizontal=True, key=f"{key_prefix}_sp_mode")
    n = st.slider("Number of resistors", 2, 5, 2, key=f"{key_prefix}_sp_n")
    values = []
    cols = st.columns(n)
    for idx in range(n):
        v = cols[idx].number_input(f"R{idx+1} (Ω)", min_value=0.1, value=100.0, step=10.0, key=f"{key_prefix}_sp_r{idx}")
        values.append(v)
    if mode == "Series":
        total = series_resistance(values)
        st.markdown(f'<div class="status-good">✅ Total Resistance (Series) = {total:.2f} Ω</div>', unsafe_allow_html=True)
        st.caption("Series total is always larger than the largest single resistor.")
    else:
        total = parallel_resistance(values)
        st.markdown(f'<div class="status-good">✅ Total Resistance (Parallel) = {total:.2f} Ω</div>', unsafe_allow_html=True)
        st.caption("Parallel total is always smaller than the smallest single resistor.")


def render_ac_calc(key_prefix):
    st.markdown("**⚙️ AC Peak ↔ RMS Calculator**")
    direction = st.radio("Convert:", ["RMS → Peak", "Peak → RMS"], horizontal=True, key=f"{key_prefix}_ac_dir")
    if direction == "RMS → Peak":
        vrms = st.number_input("RMS Voltage (V)", min_value=0.0, value=230.0, step=1.0, key=f"{key_prefix}_ac_rms")
        vpeak = ac_peak_from_rms(vrms)
        st.markdown(f'<div class="status-good">✅ Peak Voltage ≈ {vpeak:.2f} V</div>', unsafe_allow_html=True)
    else:
        vpeak = st.number_input("Peak Voltage (V)", min_value=0.0, value=325.0, step=1.0, key=f"{key_prefix}_ac_peak")
        vrms = ac_rms_from_peak(vpeak)
        st.markdown(f'<div class="status-good">✅ RMS Voltage ≈ {vrms:.2f} V</div>', unsafe_allow_html=True)
    st.caption("RMS (Root Mean Square) voltage is the 'effective' steady value that delivers the same power as an equivalent DC voltage.")
    fig, ax = plt.subplots(figsize=(4.5, 3))
    import math
    t = [x * 0.02 for x in range(101)]
    wave = [vpeak * math.sin(2 * math.pi * x) for x in t]
    ax.plot(t, wave, color="#06b6d4", linewidth=2)
    ax.axhline(vrms, color="#f97316", linestyle="--", linewidth=1.5, label="RMS level")
    ax.axhline(-vrms, color="#f97316", linestyle="--", linewidth=1.5)
    ax.set_xlabel("Time (cycles)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("AC Waveform: Peak vs RMS")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


CALC_RENDERERS = {
    "ohms_law": render_ohms_law_calc,
    "power": render_power_calc,
    "energy": render_energy_calc,
    "series_parallel": render_series_parallel_calc,
    "ac": render_ac_calc,
}

def render_kcl_kvl_sim(key_prefix):
    st.markdown("**⚙️ Kirchhoff's Laws Checker**")
    law = st.radio("Which law?", ["Current Law (KCL)", "Voltage Law (KVL)"], horizontal=True, key=f"{key_prefix}_kirch_law")
    if law == "Current Law (KCL)":
        st.caption("Enter the currents flowing into and out of a single junction (node).")
        c1, c2 = st.columns(2)
        in1 = c1.number_input("Current in 1 (A)", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_kcl_in1")
        in2 = c1.number_input("Current in 2 (A)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_kcl_in2")
        out1 = c2.number_input("Current out 1 (A)", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_kcl_out1")
        out2 = c2.number_input("Current out 2 (A)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_kcl_out2")
        balanced, total_in, total_out = kcl_check([in1, in2], [out1, out2])
        if balanced:
            st.markdown(f'<div class="status-good">✅ Balanced! Total in = {total_in:.2f} A = Total out = {total_out:.2f} A</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-bad">⛔ Not balanced — Total in = {total_in:.2f} A but Total out = {total_out:.2f} A. In a real circuit these must always match.</div>', unsafe_allow_html=True)
    else:
        st.caption("Enter a source voltage and the voltage drops around a single closed loop.")
        c1, c2 = st.columns(2)
        source = c1.number_input("Source Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_kvl_src")
        d1 = c2.number_input("Drop across R1 (V)", min_value=0.0, value=7.0, step=0.5, key=f"{key_prefix}_kvl_d1")
        d2 = c2.number_input("Drop across R2 (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_kvl_d2")
        balanced, total_drops = kvl_check(source, [d1, d2])
        if balanced:
            st.markdown(f'<div class="status-good">✅ Balanced! Source = {source:.2f} V = Total drops = {total_drops:.2f} V</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-bad">⛔ Not balanced — Source = {source:.2f} V but Total drops = {total_drops:.2f} V. Around any closed loop these must always match.</div>', unsafe_allow_html=True)


CALC_RENDERERS["kirchhoff"] = render_kcl_kvl_sim


# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. What does voltage represent in a circuit?", "options": ["The rate of current flow", "The electrical 'push' or pressure", "The opposition to current"], "answer": "The electrical 'push' or pressure"},
    {"q": "2. What is the unit of electric current?", "options": ["Volt", "Ohm", "Ampere"], "answer": "Ampere"},
    {"q": "3. According to Ohm's Law, if voltage increases and resistance stays the same, current will:", "options": ["Increase", "Decrease", "Stay the same"], "answer": "Increase"},
    {"q": "4. What formula gives electrical power?", "options": ["P = V × I", "P = V / I", "P = I / V"], "answer": "P = V × I"},
    {"q": "5. What is measured in kilowatt-hours (kWh)?", "options": ["Power", "Resistance", "Energy"], "answer": "Energy"},
    {"q": "6. In a series circuit, what stays the same through every component?", "options": ["Voltage", "Current", "Resistance"], "answer": "Current"},
    {"q": "7. In a parallel circuit, what stays the same across every branch?", "options": ["Voltage", "Current", "Power"], "answer": "Voltage"},
    {"q": "8. What does Kirchhoff's Current Law state?", "options": ["Current in equals current out at a junction", "Voltage is always constant", "Resistance never changes"], "answer": "Current in equals current out at a junction"},
    {"q": "9. Which best describes AC (alternating current)?", "options": ["Flows in one direction only", "Periodically reverses direction", "Only exists in batteries"], "answer": "Periodically reverses direction"},
    {"q": "10. A material that allows current to flow easily is called a:", "options": ["Insulator", "Conductor", "Resistor"], "answer": "Conductor"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "You measure 0 V across a component that should be powered, even though the supply is on.",
        "question": "What is the most likely issue?",
        "options": ["There is a break (open circuit) somewhere in the path", "The component has too little resistance", "The frequency is too high"],
        "answer": "There is a break (open circuit) somewhere in the path",
        "explanation": "An open circuit stops current everywhere along that path, so no voltage is developed across components downstream of the break.",
    },
    {
        "scenario": "A fuse keeps blowing shortly after you turn a circuit on.",
        "question": "What does this suggest?",
        "options": ["The circuit is drawing more current than the fuse rating allows", "The voltage source is too stable", "The resistance is too high"],
        "answer": "The circuit is drawing more current than the fuse rating allows",
        "explanation": "A repeatedly blowing fuse is a strong sign of excess current — often from a short circuit or an overloaded/faulty component.",
    },
    {
        "scenario": "Two resistors are wired in parallel, and you calculate the total resistance to be higher than either resistor alone.",
        "question": "What went wrong?",
        "options": ["The calculation is wrong — parallel resistance is always LESS than the smallest resistor", "This is correct behaviour for parallel circuits", "Parallel resistors always equal the sum of both values"],
        "answer": "The calculation is wrong — parallel resistance is always LESS than the smallest resistor",
        "explanation": "Adding a parallel path always gives current an easier route overall, so total resistance always drops below the smallest individual resistor.",
    },
    {
        "scenario": "At a circuit junction, 5 A flows in but your measurements show only 3 A flowing out through the visible branches.",
        "question": "According to Kirchhoff's Current Law, what should you do?",
        "options": ["Look for a missing or unmeasured branch carrying the other 2 A", "Assume the law doesn't apply here", "Ignore the discrepancy"],
        "answer": "Look for a missing or unmeasured branch carrying the other 2 A",
        "explanation": "KCL says current in must equal current out — a mismatch almost always means a branch was missed, not that the law failed.",
    },
    {
        "scenario": "An appliance rated 2000 W is run for 3 hours, and someone claims it used 2000 kWh of energy.",
        "question": "What is wrong with this claim?",
        "options": ["2000 W for 3 hours is only 6 kWh, not 2000 kWh", "Power and energy are the same thing", "The claim is correct"],
        "answer": "2000 W for 3 hours is only 6 kWh, not 2000 kWh",
        "explanation": "Energy (kWh) = Power (kW) × Time (h) = 2 kW × 3 h = 6 kWh. Confusing power (rate) with energy (total) is a very common mistake.",
    },
]

# ============================================================================
# SESSION STATE INITIALISATION
# ============================================================================
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("🔋 ELECTRICAL FUNDAMENTALS")
st.sidebar.subheader("LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore the core concepts\n"
    "3. Study the key laws\n"
    "4. Experiment with the simulator\n"
    "5. Study applications\n"
    "6. Complete troubleshooting\n"
    "7. Take the quiz"
)
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Introduction",
        "🔎 Core Concepts Explorer",
        "📐 Laws & Relationships",
        "🎛️ Interactive Simulator",
        "🔬 Practical Applications",
        "🧪 Troubleshooting Lab",
        "📝 Quiz",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Work through the sections in order for the smoothest learning experience.")

# ============================================================================
# TOP DASHBOARD (visible on every page)
# ============================================================================
st.title("🔋 Electrical Fundamentals Learning Lab")
st.caption("An Interactive Beginner's Guide to Electrical Fundamentals")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Concepts Covered", len(CONCEPTS))
d2.metric("📐 Key Laws", len(LAWS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Electrical Fundamentals")

    st.markdown(
        """
        ### What is Electricity?
        Electricity is the flow of tiny charged particles called **electrons** through
        a material. When electrons are pushed to move through a conductor (like a copper
        wire), we call that movement **electric current** — and it's what powers almost
        every device you use.

        Every circuit, no matter how complex, is built from a handful of fundamental
        ideas: voltage, current, resistance, power, and energy. Understanding these
        deeply is the foundation for everything else in electronics.
        """
    )

    st.subheader("💧 The Water-Pipe Analogy")
    st.write("A simple (though imperfect) way to picture electricity is to imagine water flowing through pipes:")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>💧 Voltage → Pressure</h4>'
            '<p>The push that drives water (current) through the pipe. More pressure = more push.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>🌊 Current → Flow Rate</h4>'
            '<p>The amount of water passing a point each second — the thing that actually does the work.</p></div>',
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            '<div class="concept-card"><h4>🚧 Resistance → Narrowing</h4>'
            '<p>A restriction in the pipe that limits how much water can flow for a given pressure.</p></div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "⚠️ Note: this water analogy is a simplified teaching tool — real electrical behaviour "
        "involves electric and magnetic fields, not literal fluid flow."
    )

    st.subheader("⚡ Why These Fundamentals Matter")
    st.markdown(
        '<div class="app-card">Every electronic component you will ever study — resistors, capacitors, '
        'transistors, ICs — behaves according to these same basic rules of voltage, current, resistance, '
        'power, and energy. Master these fundamentals first, and every other electronics topic becomes '
        'far easier to understand.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Head to **'Core Concepts Explorer'** in the sidebar to study each fundamental in detail.")

# ============================================================================
# 2. CORE CONCEPTS EXPLORER
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Core Concepts Explorer")
    st.caption("Expand each concept to see its symbol/diagram, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in CONCEPT_ORDER:
        c = CONCEPTS[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_concept_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Unit:** {c['unit']}")
                st.markdown(f"**Formula:** `{c['formula']}`")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")
                if c["safety"]:
                    st.markdown(f'<div class="safety-note">⚠️ {c["safety"]}</div>', unsafe_allow_html=True)

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. LAWS & RELATIONSHIPS
# ============================================================================
elif page.startswith("📐"):
    st.header("📐 Laws & Relationships")
    st.caption("The key mathematical laws that govern every electrical circuit.")

    filter_tags = st.multiselect(
        "Filter concepts by category",
        ["basic_quantity", "energy_related", "ac_dc", "materials", "source", "circuit_configuration"],
        default=[],
    )
    if filter_tags:
        filtered_names = [n for n in CONCEPT_ORDER if any(t in CONCEPTS[n]["category"] for t in filter_tags)]
    else:
        filtered_names = CONCEPT_ORDER

    st.subheader("🧮 Concept Reference Table")
    rows = []
    for name in filtered_names:
        c = CONCEPTS[name]
        rows.append({
            "Concept": name,
            "Unit": c["unit"],
            "Formula": c["formula"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Key Laws")
    for law_name, law in LAWS.items():
        with st.expander(f"**{law_name}** — `{law['formula']}`"):
            st.markdown(f"**Explanation:** {law['explanation']}")
            st.markdown(f"**Used for:** {law['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any concept with an interactive model and experiment with its behaviour.")

    simulatable = [n for n in CONCEPT_ORDER if CONCEPTS[n]["calc_key"] is not None]
    options = simulatable + ["Kirchhoff's Laws"]
    sel = st.selectbox("Select a concept or law", options)

    if sel == "Kirchhoff's Laws":
        st.markdown(
            flat('<div class="comp-banner" style="background: linear-gradient(90deg, #7c3aed, #4c1d95);">'
                 '⚡ <b>Kirchhoff\'s Laws</b> &nbsp;|&nbsp; Governing rules for current at junctions and voltage around loops</div>'),
            unsafe_allow_html=True,
        )
        render_kcl_kvl_sim(key_prefix="sim_kirchhoff")
    else:
        c = CONCEPTS[sel]
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #ea580c, #9a3412);">'
                 f'⚡ <b>{sel}</b> &nbsp;|&nbsp; {c["desc"]}</div>'),
            unsafe_allow_html=True,
        )
        col_symbol, col_calc = st.columns([1, 1.6])
        with col_symbol:
            st.markdown("##### 🔷 Symbol / Diagram")
            st.markdown(f'<div class="symbol-box">{draw_concept_svg(sel)}</div>', unsafe_allow_html=True)
            st.markdown(f"**Unit:** {c['unit']}")
        with col_calc:
            CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how these fundamentals show up in everyday electrical systems.")

    APPLICATIONS = [
        ("🏠 Home Wiring", "Household outlets are wired in parallel so each one works independently at the same voltage; circuit breakers act like resettable fuses, tripping on excess current (Ohm's Law and KCL in action)."),
        ("🔋 Batteries & Power Banks", "Cells connected in series increase total voltage; cells connected in parallel increase total current capacity (Amp-hours) — a direct application of series/parallel principles."),
        ("💡 Lighting Circuits", "LED bulbs use far less power than incandescent bulbs for the same brightness — a direct application of the Power Law (P = VI) and energy efficiency."),
        ("⚡ Power Transmission Grids", "Electricity is transmitted at very high AC voltages to minimise current (and therefore energy lost as heat, P = I²R) over long distances, then stepped down for safe home use."),
        ("📱 Electronic Devices", "Internal voltage regulators and resistor networks precisely control voltage and current to protect sensitive components — all governed by Ohm's Law and the Power Law."),
        ("🚗 Electric Vehicles", "EV battery packs combine many cells in series and parallel to reach the voltage and capacity needed, and energy (kWh) is exactly how EV range and charging are measured."),
    ]
    for title, body in APPLICATIONS:
        with st.expander(title):
            st.markdown(f'<div class="app-card">{body}</div>', unsafe_allow_html=True)

# ============================================================================
# 6. TROUBLESHOOTING LAB
# ============================================================================
elif page.startswith("🧪"):
    st.header("🧪 Troubleshooting Lab")
    st.caption("Work through each scenario, choose your answer, and get immediate feedback.")

    for idx, item in enumerate(TROUBLESHOOTING):
        st.markdown(f"##### Scenario {idx + 1}")
        st.markdown(f'<div class="concept-card">{item["scenario"]}</div>', unsafe_allow_html=True)
        choice = st.radio(item["question"], item["options"], index=None, key=f"trouble_{idx}")
        if choice is not None:
            if choice == item["answer"]:
                st.markdown(f'<div class="status-good">✅ Correct! {item["explanation"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="status-bad">❌ Not quite. Correct answer: <b>{item["answer"]}</b>. {item["explanation"]}</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("---")

# ============================================================================
# 7. QUIZ
# ============================================================================
elif page.startswith("📝"):
    st.header("📝 Electrical Fundamentals Quiz")
    st.caption("10 questions · 3 options each · Scored out of 100%")

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
            st.warning("⚠️ Please answer all 10 questions before submitting.")
        else:
            correct_count = sum(1 for i, item in enumerate(QUIZ) if answers[i] == item["answer"])
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
                st.info(f"👍 Good effort! You scored {score_pct}%. Review the questions you missed below.")
            else:
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Core Concepts Explorer' section and try again!")

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
