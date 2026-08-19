"""
🧮 Circuit Analysis Learning Lab
An Interactive Beginner's Guide to Circuit Theorems & Analysis Methods

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
    page_title="Circuit Analysis Learning Lab",
    page_icon="🧮",
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
        background: linear-gradient(135deg, #1e3a8a, #3730a3);
        border: 1px solid #818cf8;
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
# CORE CIRCUIT ANALYSIS CALCULATIONS (pure functions, no widgets)
# ============================================================================

def practical_source_terminal_voltage(vs, r_internal, r_load):
    """Terminal voltage and current of a real (non-ideal) voltage source
    under load. Returns (v_terminal, current)."""
    total_r = r_internal + r_load
    if total_r <= 0:
        return None, None
    current = vs / total_r
    v_terminal = vs - current * r_internal
    return v_terminal, current


def loaded_voltage_divider(vs, r1, r2, r_load):
    """Output of a voltage divider once a load resistor is attached across
    R2. Returns (v_out_loaded, v_out_unloaded)."""
    if (r2 + r_load) <= 0:
        return None, None
    r_parallel = (r2 * r_load) / (r2 + r_load)
    if (r1 + r_parallel) <= 0:
        return None, None
    v_out_loaded = vs * r_parallel / (r1 + r_parallel)
    v_out_unloaded = vs * r2 / (r1 + r2) if (r1 + r2) > 0 else None
    return v_out_loaded, v_out_unloaded


def wheatstone_balance(r1, r2, r3):
    """Balance condition for a Wheatstone bridge: Rx = R2*R3/R1."""
    if r1 <= 0:
        return None
    return (r2 * r3) / r1


def thevenin_voltage_divider(vs, r1, r2):
    """Thevenin equivalent (as seen from across R2) of a simple source +
    two-resistor voltage-divider network. Returns (Vth, Rth)."""
    if (r1 + r2) <= 0:
        return None, None
    vth = vs * r2 / (r1 + r2)
    rth = (r1 * r2) / (r1 + r2)
    return vth, rth


def norton_from_thevenin(vth, rth):
    """Norton equivalent from a Thevenin equivalent: In = Vth/Rth, Rn = Rth."""
    if rth <= 0:
        return None, None
    return vth / rth, rth


def max_power_transfer(vth, rth):
    """Maximum Power Transfer Theorem: optimal load and the resulting max power."""
    if rth <= 0:
        return None, None
    rl_opt = rth
    p_max = (vth ** 2) / (4 * rth)
    return rl_opt, p_max


def power_delivered(vth, rth, rl):
    """Actual power delivered to an arbitrary load resistance."""
    total = rth + rl
    if total <= 0 or rl < 0:
        return None
    current = vth / total
    return (current ** 2) * rl


def source_transform_v_to_i(vs, rs):
    """Voltage source (Vs, series Rs) -> equivalent current source (Is, parallel Rp)."""
    if rs <= 0:
        return None, None
    return vs / rs, rs


def source_transform_i_to_v(is_, rp):
    """Current source (Is, parallel Rp) -> equivalent voltage source (Vs, series Rs)."""
    if rp <= 0:
        return None, None
    return is_ * rp, rp


def delta_to_wye(ra, rb, rc):
    """Delta (Ra,Rb,Rc) -> Wye (R1,R2,R3) transformation."""
    total = ra + rb + rc
    if total <= 0:
        return None, None, None
    r1 = (rb * rc) / total
    r2 = (ra * rc) / total
    r3 = (ra * rb) / total
    return r1, r2, r3


def wye_to_delta(r1, r2, r3):
    """Wye (R1,R2,R3) -> Delta (Ra,Rb,Rc) transformation."""
    if r1 <= 0 or r2 <= 0 or r3 <= 0:
        return None, None, None
    sum_prod = r1 * r2 + r2 * r3 + r3 * r1
    ra = sum_prod / r1
    rb = sum_prod / r2
    rc = sum_prod / r3
    return ra, rb, rc


def _divider_contribution(v_active, r_active, r_other, r_common):
    """Helper for superposition: voltage at the common node from ONE active
    source, with all other independent sources set to zero (shorted)."""
    r_parallel = (r_other * r_common) / (r_other + r_common) if (r_other + r_common) > 0 else 0
    if (r_active + r_parallel) <= 0:
        return 0.0
    return v_active * r_parallel / (r_active + r_parallel)


def superposition_two_sources(v1, v2, r1, r2, r_common):
    """Superposition theorem applied to two voltage sources feeding a shared
    node through their own series resistors. Returns (v_from_1, v_from_2, total)."""
    v_from_1 = _divider_contribution(v1, r1, r2, r_common)
    v_from_2 = _divider_contribution(v2, r2, r1, r_common)
    return v_from_1, v_from_2, v_from_1 + v_from_2


def millmans_theorem(sources):
    """Millman's Theorem: common node voltage for several (V, R) branches
    all referenced to the same ground, meeting at one node."""
    numerator = sum(v / r for v, r in sources if r > 0)
    denominator = sum(1.0 / r for v, r in sources if r > 0)
    if denominator == 0:
        return None
    return numerator / denominator


def nodal_2node_solve(g11, g12, g21, g22, i1, i2):
    """Solve a 2-node nodal analysis system:
    [g11 g12][V1]   [i1]
    [g21 g22][V2] = [i2]
    using Cramer's rule. Returns (V1, V2) or (None, None) if singular."""
    det = g11 * g22 - g12 * g21
    if det == 0:
        return None, None
    v1 = (i1 * g22 - i2 * g12) / det
    v2 = (g11 * i2 - g21 * i1) / det
    return v1, v2


# ============================================================================
# CIRCUIT ELEMENTS & SOURCES DATA
# 8 fundamental building blocks used in circuit analysis, each with the
# fields the Explorer page needs. "calc_key" links an entry to its
# interactive render function further down.
# ============================================================================
CIRCUIT_ELEMENTS = {
    "Ideal Voltage Source": {
        "desc": "A theoretical source that maintains a fixed voltage across its terminals, no matter how much current is drawn.",
        "symbol_desc": "Circle with + and − terminals",
        "key_property": "Zero internal resistance — terminal voltage never sags under load",
        "category": ["source", "ideal"],
        "explanation": "In the real world no source is perfect, but the 'ideal voltage source' model is a hugely useful simplification for analysis — assume it, solve the circuit, and only worry about internal resistance if the problem specifically asks you to.",
        "applications": "The starting assumption for most introductory circuit analysis problems; a reasonable approximation for a well-regulated power supply.",
        "calc_key": None,
    },
    "Ideal Current Source": {
        "desc": "A theoretical source that pushes a fixed current through a circuit, no matter what voltage that requires.",
        "symbol_desc": "Circle with an arrow showing current direction",
        "key_property": "Infinite internal resistance — current never changes regardless of the load",
        "category": ["source", "ideal"],
        "explanation": "Less intuitive than a voltage source, but just as useful in analysis — an ideal current source will develop whatever voltage is necessary across its terminals to force exactly its rated current through the circuit.",
        "applications": "Modelling transistor current sources, current-mode circuit analysis, biasing circuits.",
        "calc_key": None,
    },
    "Practical Voltage Source": {
        "desc": "A more realistic model: an ideal voltage source with a small internal (series) resistance.",
        "symbol_desc": "Ideal voltage source in series with a resistor, inside a dashed boundary",
        "key_property": "Terminal voltage SAGS as load current increases, due to the internal resistance",
        "category": ["source", "practical"],
        "explanation": "Every real battery or power supply has some internal resistance — this is why a battery's voltage appears to drop when you connect a demanding load, even though the source itself hasn't changed.",
        "applications": "Modelling real batteries, power supplies, and generators for more accurate circuit analysis.",
        "calc_key": "practical_source_calc",
    },
    "Practical Current Source": {
        "desc": "A more realistic model: an ideal current source with a (large but finite) internal resistance in parallel.",
        "symbol_desc": "Ideal current source with a resistor in parallel, inside a dashed boundary",
        "key_property": "Some current 'leaks' through the internal parallel resistance instead of reaching the load",
        "category": ["source", "practical"],
        "explanation": "A real current source (like many transistor circuits) can't maintain infinite output resistance — some of its current inevitably leaks through an internal parallel resistance rather than all of it reaching the intended load.",
        "applications": "Modelling transistor current sources and current mirrors more accurately.",
        "calc_key": None,
    },
    "Dependent (Controlled) Source": {
        "desc": "A source whose output is NOT fixed, but instead depends on a voltage or current somewhere else in the circuit.",
        "symbol_desc": "Diamond shape (instead of a circle) — this shape is the universal symbol for 'dependent source'",
        "key_property": "Four types: VCVS, CCVS, VCCS, CCCS — named by what controls them (Voltage/Current) and what they output (Voltage/Current)",
        "category": ["source", "dependent"],
        "explanation": "Unlike an independent source (which has a fixed value you choose), a dependent source's value is an equation involving another part of the circuit — this is exactly how transistors and op-amps are modelled for analysis purposes.",
        "applications": "Modelling transistor amplification (a BJT's collector current source depends on its base current), op-amp models, feedback systems.",
        "calc_key": None,
    },
    "Ground / Reference Node": {
        "desc": "The chosen reference point in a circuit against which every other voltage is measured — defined as exactly 0V.",
        "symbol_desc": "Three descending horizontal lines (or a single hatched line)",
        "key_property": "Not a physical component — just a bookkeeping choice that makes every other node voltage meaningful",
        "category": ["reference"],
        "explanation": "Voltage is always a difference between two points — 'ground' is simply the point we all agree to call zero, so that when someone says 'this node is at 5V', everyone knows what that means relative to.",
        "applications": "Essential in nodal analysis, and in every real circuit diagram to establish a common reference.",
        "calc_key": None,
    },
    "Wheatstone Bridge": {
        "desc": "A diamond-shaped network of four resistors used to precisely measure an unknown resistance by balancing the bridge.",
        "symbol_desc": "Four resistors in a diamond, with a galvanometer bridging the two midpoints",
        "key_property": "At BALANCE, no current flows through the galvanometer: R1×R3 = R2×Rx",
        "category": ["circuit", "measurement"],
        "explanation": "By adjusting one resistor until the galvanometer reads exactly zero, the bridge is 'balanced' — at that exact point, simple algebra (no need to solve the whole circuit) reveals the unknown resistance.",
        "applications": "Precision resistance measurement, strain gauge sensors, temperature sensor signal conditioning.",
        "calc_key": "wheatstone_calc",
    },
    "Loaded Voltage Divider": {
        "desc": "A simple two-resistor voltage divider, but with a load resistor attached — revealing why 'ideal' divider formulas can mislead in practice.",
        "symbol_desc": "Two series resistors from source to ground, with a third (load) resistor tapped at the midpoint",
        "key_property": "Attaching a load always PULLS the output voltage down compared to the unloaded (open-circuit) prediction",
        "category": ["circuit"],
        "explanation": "The simple voltage divider formula (Vout = Vs × R2/(R1+R2)) only holds if nothing is drawing current from the output. The moment you connect a real load, it forms a parallel combination with R2, and the actual output voltage will always be lower than the naive formula predicts.",
        "applications": "A classic 'gotcha' in circuit design — always check how much current your load will draw before trusting a simple divider formula.",
        "calc_key": "loaded_divider_calc",
    },
}

CIRCUIT_ELEMENT_ORDER = list(CIRCUIT_ELEMENTS.keys())

# ============================================================================
# CIRCUIT THEOREMS & ANALYSIS METHODS DATA
# (used on the "Theorems & Analysis Methods" reference page)
# ============================================================================
ANALYSIS_METHODS = {
    "Kirchhoff's Current Law (KCL)": {
        "formula": "ΣI(in) = ΣI(out) at any node",
        "explanation": "The total current flowing into a junction must equal the total current flowing out — charge cannot pile up or vanish at a node. The foundation of nodal analysis.",
        "use": "Analysing circuits with multiple branches meeting at a point.",
    },
    "Kirchhoff's Voltage Law (KVL)": {
        "formula": "Σ V(source) = Σ V(drops) around any closed loop",
        "explanation": "Going all the way around any closed loop in a circuit, the total supplied voltage must equal the total of all voltage drops — the foundation of mesh analysis.",
        "use": "Analysing circuits with multiple components in a loop.",
    },
    "Nodal Analysis": {
        "formula": "Write a KCL equation at every node (except the reference/ground node), solve for node voltages",
        "explanation": "Chooses one node as the 0V reference, then writes one current-balance equation for every other node, using each node's unknown voltage — solving the resulting system of equations gives every node voltage in the circuit.",
        "use": "Circuits with many parallel branches — often the most efficient method when there are more loops than nodes.",
    },
    "Mesh Analysis": {
        "formula": "Write a KVL equation for every independent loop, solve for loop (mesh) currents",
        "explanation": "Assigns an unknown circulating current to each independent loop ('mesh') in a planar circuit, then writes one voltage-balance equation per loop — solving the resulting system gives every branch current.",
        "use": "Circuits with many series loops — often the most efficient method when there are more nodes than loops. Only works directly on planar circuits.",
    },
    "Thevenin's Theorem": {
        "formula": "Any two-terminal linear network can be replaced by a single voltage source (Vth) in series with a single resistance (Rth)",
        "explanation": "No matter how complicated the rest of a circuit is, everything connected to a pair of terminals can be boiled down to just one voltage source and one resistor, AS SEEN from those two terminals — massively simplifying repeated 'what if I change the load' analysis.",
        "use": "Analysing how a circuit's output changes for different load values, without re-solving the whole circuit each time.",
    },
    "Norton's Theorem": {
        "formula": "Any two-terminal linear network can be replaced by a single current source (In) in parallel with a single resistance (Rn)",
        "explanation": "The current-source counterpart to Thevenin's Theorem — the same two-terminal network can equally be represented as a current source with a parallel resistance, and In = Vth/Rth, Rn = Rth.",
        "use": "Whichever form (Thevenin or Norton) is more convenient for the next step of an analysis — they're always interchangeable.",
    },
    "Superposition Theorem": {
        "formula": "In a linear circuit with multiple independent sources, the total response = the SUM of the responses to each source acting ALONE (all other independent sources set to zero)",
        "explanation": "Turn off all independent sources except one (voltage sources become short circuits, current sources become open circuits), solve the simpler circuit, repeat for each source, then add up all the individual results.",
        "use": "Circuits with multiple independent sources, where analysing one source at a time is easier than solving everything at once. Only valid for LINEAR circuits.",
    },
    "Maximum Power Transfer Theorem": {
        "formula": "Maximum power is delivered to a load when RL = Rth (the load resistance equals the Thevenin resistance of the source network)",
        "explanation": "If you're free to choose the load resistance, the load will receive the most possible power exactly when it matches the source network's own Thevenin resistance — not when it's very large or very small.",
        "use": "Audio amplifier/speaker impedance matching, antenna and transmission line matching, sensor interface design.",
    },
    "Source Transformation": {
        "formula": "A voltage source Vs with series Rs ⟷ a current source Is = Vs/Rs with the SAME resistance Rs in parallel",
        "explanation": "Any practical voltage source can be converted into an equivalent practical current source (and vice versa) — they behave identically from the perspective of everything else connected to them.",
        "use": "Simplifying circuit analysis by converting sources into whichever form makes the rest of the circuit easier to combine (series-friendly voltage sources vs. parallel-friendly current sources).",
    },
    "Delta-Wye (Δ-Y) Transformation": {
        "formula": "Converts a triangle ('Delta', Δ) network of 3 resistors into an equivalent 'Wye' (Y) star network, or vice versa",
        "explanation": "Some resistor networks are neither purely series nor purely parallel — they're connected in a triangle or star shape that resists simplification. Delta-Wye transformation converts between the two forms, unlocking further series/parallel simplification.",
        "use": "Three-phase power system analysis, resistor networks that can't otherwise be reduced with simple series/parallel rules.",
    },
    "Millman's Theorem": {
        "formula": "V(node) = [ΣVi/Ri] / [Σ1/Ri]  for several (voltage, resistance) branches all meeting at one common node",
        "explanation": "A shortcut for finding the voltage at a single node where several voltage-source-plus-resistor branches all converge — without needing to set up and solve a full system of equations.",
        "use": "Quickly analysing parallel-branch circuits (like multiple batteries in parallel through different internal resistances) that all share one output node.",
    },
}

ANALYSIS_METHOD_ORDER = list(ANALYSIS_METHODS.keys())

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each circuit element. Every
# returned string is flattened to one line with flat() so Streamlit's
# Markdown renderer never mis-parses an embedded blank line as the end of
# the block.
# ============================================================================
CIRCUIT_ELEMENT_COLORS = {
    "Ideal Voltage Source": "#3b82f6",
    "Ideal Current Source": "#f59e0b",
    "Practical Voltage Source": "#8b5cf6",
    "Practical Current Source": "#ec4899",
    "Dependent (Controlled) Source": "#14b8a6",
    "Ground / Reference Node": "#6b7280",
    "Wheatstone Bridge": "#0ea5e9",
    "Loaded Voltage Divider": "#22c55e",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def _zigzag(x, y, color, width=60, height=24):
    """Small horizontal resistor zigzag centred at (x,y)."""
    h = height / 2
    x0 = x - width / 2
    step = width / 6
    pts = [(x0, y)]
    for i in range(1, 6):
        pts.append((x0 + i * step, y + (h if i % 2 else -h)))
    pts.append((x0 + width, y))
    path = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'


def _vzigzag(x, y, color, height=60, width=24):
    """Small vertical resistor zigzag centred at (x,y)."""
    w = width / 2
    y0 = y - height / 2
    step = height / 6
    pts = [(x, y0)]
    for i in range(1, 6):
        pts.append((x + (w if i % 2 else -w), y0 + i * step))
    pts.append((x, y0 + height))
    path = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'


def _ground_symbol(x, y, color="#111827"):
    return (
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+12}" stroke="{color}" stroke-width="3"/>'
        f'<line x1="{x-16}" y1="{y+12}" x2="{x+16}" y2="{y+12}" stroke="{color}" stroke-width="3"/>'
        f'<line x1="{x-10}" y1="{y+19}" x2="{x+10}" y2="{y+19}" stroke="{color}" stroke-width="3"/>'
        f'<line x1="{x-4}" y1="{y+26}" x2="{x+4}" y2="{y+26}" stroke="{color}" stroke-width="3"/>'
    )


def draw_circuit_element_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the circuit element."""
    color = CIRCUIT_ELEMENT_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Ideal Voltage Source":
        body = f"""
        {_lead(110, 5, 110, 35)}
        <circle cx="110" cy="70" r="35" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="103" y="55" font-size="18" font-weight="bold" fill="{color}">+</text>
        <text x="103" y="92" font-size="18" font-weight="bold" fill="{color}">−</text>
        {_lead(110, 105, 110, 135)}
        """

    elif name == "Ideal Current Source":
        body = f"""
        {_lead(110, 5, 110, 35)}
        <circle cx="110" cy="70" r="35" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <line x1="110" y1="88" x2="110" y2="52" stroke="{color}" stroke-width="4"/>
        <polygon points="110,45 102,60 118,60" fill="{color}"/>
        {_lead(110, 105, 110, 135)}
        """

    elif name == "Practical Voltage Source":
        body = f"""
        <rect x="45" y="10" width="130" height="120" rx="8" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="5,4"/>
        {_lead(110, 10, 110, 32)}
        <circle cx="110" cy="55" r="24" fill="{color}22" stroke="{color}" stroke-width="3"/>
        <text x="104" y="45" font-size="14" font-weight="bold" fill="{color}">+</text>
        <text x="104" y="68" font-size="14" font-weight="bold" fill="{color}">−</text>
        {_lead(110, 79, 110, 92)}
        {_vzigzag(110, 105, color, height=30, width=20)}
        {_lead(110, 120, 110, 130)}
        """

    elif name == "Practical Current Source":
        body = f"""
        <rect x="30" y="10" width="160" height="120" rx="8" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="5,4"/>
        {_lead(80, 10, 80, 32)}
        {_lead(140, 10, 140, 32)}
        <circle cx="80" cy="60" r="24" fill="{color}22" stroke="{color}" stroke-width="3"/>
        <line x1="80" y1="76" x2="80" y2="46" stroke="{color}" stroke-width="3"/>
        <polygon points="80,40 74,52 86,52" fill="{color}"/>
        {_lead(80, 84, 80, 105)}
        {_vzigzag(140, 65, color, height=46, width=18)}
        {_lead(80, 105, 140, 105)}
        {_lead(140, 88, 140, 105)}
        {_lead(80, 105, 80, 130)}
        {_lead(140, 105, 140, 130)}
        """

    elif name == "Dependent (Controlled) Source":
        body = f"""
        {_lead(110, 5, 110, 35)}
        <polygon points="110,35 145,70 110,105 75,70" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <text x="100" y="65" font-size="16" font-weight="bold" fill="{color}">+</text>
        <text x="100" y="88" font-size="16" font-weight="bold" fill="{color}">−</text>
        {_lead(110, 105, 110, 135)}
        """

    elif name == "Ground / Reference Node":
        body = f"""
        {_lead(110, 15, 110, 60)}
        {_ground_symbol(110, 60, color)}
        <text x="80" y="12" font-size="12" font-weight="bold" fill="#111827">0 V reference</text>
        """

    elif name == "Wheatstone Bridge":
        d = color
        body = f"""
        {_lead(0, 70, 35, 70, d, 3)}
        {_lead(185, 70, 220, 70, d, 3)}
        {_lead(35, 70, 105, 25, d, 2)}
        {_lead(185, 70, 115, 25, d, 2)}
        {_lead(35, 70, 105, 115, d, 2)}
        {_lead(185, 70, 115, 115, d, 2)}
        {_lead(110, 40, 110, 100, d, 2)}
        <circle cx="110" cy="70" r="12" fill="{d}22" stroke="{d}" stroke-width="3"/>
        <text x="103" y="75" font-size="12" font-weight="bold" fill="{d}">G</text>
        <g transform="translate(68,42) rotate(-33)">{_zigzag(0, 0, d, width=44, height=16)}</g>
        <g transform="translate(152,42) rotate(33)">{_zigzag(0, 0, d, width=44, height=16)}</g>
        <g transform="translate(68,98) rotate(33)">{_zigzag(0, 0, d, width=44, height=16)}</g>
        <g transform="translate(152,98) rotate(-33)">{_zigzag(0, 0, d, width=44, height=16)}</g>
        """

    elif name == "Loaded Voltage Divider":
        d = color
        body = f"""
        {_lead(60, 5, 60, 20)}
        {_vzigzag(60, 40, d, height=36, width=18)}
        {_lead(60, 58, 60, 70)}
        {_vzigzag(60, 90, d, height=36, width=18)}
        {_lead(60, 108, 60, 130)}
        {_ground_symbol(60, 130, "#111827")}
        {_lead(60, 70, 150, 70, d, 2)}
        {_lead(150, 70, 150, 90, "#9ca3af", 2)}
        {_vzigzag(150, 105, "#9ca3af", height=30, width=16)}
        {_lead(150, 120, 150, 130, "#9ca3af", 2)}
        {_ground_symbol(150, 130, "#9ca3af")}
        <text x="160" y="72" font-size="11" font-weight="bold" fill="#9ca3af">load</text>
        <text x="10" y="15" font-size="11" font-weight="bold" fill="#111827">Vs</text>
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same item is rendered on more than one page.
# ============================================================================

def render_practical_source_calc(key_prefix):
    st.markdown("**⚙️ Practical Voltage Source Calculator**")
    c1, c2, c3 = st.columns(3)
    vs = c1.number_input("Ideal Source Voltage (V)", min_value=0.0, value=9.0, step=0.5, key=f"{key_prefix}_ps_vs")
    r_int = c2.number_input("Internal Resistance (Ω)", min_value=0.0, value=1.0, step=0.1, key=f"{key_prefix}_ps_rint")
    r_load = c3.number_input("Load Resistance (Ω)", min_value=0.01, value=10.0, step=1.0, key=f"{key_prefix}_ps_rload")
    v_term, current = practical_source_terminal_voltage(vs, r_int, r_load)
    if v_term is None:
        st.warning("⚠️ Check that resistances are valid.")
    else:
        st.markdown(f'<div class="status-good">✅ Terminal Voltage = {v_term:.3f} V &nbsp;|&nbsp; Current = {current*1000:.2f} mA</div>', unsafe_allow_html=True)
        sag_pct = ((vs - v_term) / vs * 100) if vs > 0 else 0
        st.caption(f"Voltage sag due to internal resistance: {sag_pct:.2f}% below the ideal {vs} V — try increasing internal resistance or decreasing load resistance to see it worsen.")


def render_wheatstone_calc(key_prefix):
    st.markdown("**⚙️ Wheatstone Bridge Balance Calculator** — `Rx = R2×R3 / R1`")
    c1, c2, c3 = st.columns(3)
    r1 = c1.number_input("R1 (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_wb_r1")
    r2 = c2.number_input("R2 (Ω)", min_value=0.0, value=220.0, step=10.0, key=f"{key_prefix}_wb_r2")
    r3 = c3.number_input("R3 (Ω)", min_value=0.0, value=150.0, step=10.0, key=f"{key_prefix}_wb_r3")
    rx = wheatstone_balance(r1, r2, r3)
    if rx is None:
        st.warning("⚠️ R1 must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Unknown Resistance Rx = {rx:.2f} Ω (at balance — galvanometer reads zero)</div>', unsafe_allow_html=True)
        st.caption("This is the resistance Rx would need to be for the bridge to be perfectly balanced with the R1, R2, R3 values above.")


def render_loaded_divider_calc(key_prefix):
    st.markdown("**⚙️ Loaded Voltage Divider Calculator**")
    c1, c2, c3, c4 = st.columns(4)
    vs = c1.number_input("Supply Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_ld_vs")
    r1 = c2.number_input("R1 (Ω)", min_value=0.01, value=1000.0, step=100.0, key=f"{key_prefix}_ld_r1")
    r2 = c3.number_input("R2 (Ω)", min_value=0.01, value=1000.0, step=100.0, key=f"{key_prefix}_ld_r2")
    r_load = c4.number_input("Load Resistance (Ω)", min_value=0.01, value=1000.0, step=100.0, key=f"{key_prefix}_ld_rload")
    v_loaded, v_unloaded = loaded_voltage_divider(vs, r1, r2, r_load)
    if v_loaded is None:
        st.warning("⚠️ Check that resistances are valid.")
    else:
        st.markdown(f'<div class="status-good">✅ Loaded Output = {v_loaded:.3f} V &nbsp;|&nbsp; Unloaded (ideal) Output = {v_unloaded:.3f} V</div>', unsafe_allow_html=True)
        drop_pct = ((v_unloaded - v_loaded) / v_unloaded * 100) if v_unloaded else 0
        st.caption(f"The load pulled the output down by {drop_pct:.2f}% from the naive prediction — try lowering the load resistance to see this effect grow.")


CALC_RENDERERS = {
    "practical_source_calc": render_practical_source_calc,
    "wheatstone_calc": render_wheatstone_calc,
    "loaded_divider_calc": render_loaded_divider_calc,
}


def render_thevenin_norton_sim(key_prefix):
    st.markdown("**⚙️ Thevenin & Norton Equivalent Calculator**")
    st.caption("Example network: a source Vs feeding a two-resistor voltage divider — Thevenin/Norton found as seen across R2.")
    c1, c2, c3 = st.columns(3)
    vs = c1.number_input("Source Voltage Vs (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_th_vs")
    r1 = c2.number_input("R1 (Ω)", min_value=0.01, value=1000.0, step=100.0, key=f"{key_prefix}_th_r1")
    r2 = c3.number_input("R2 (Ω)", min_value=0.01, value=2000.0, step=100.0, key=f"{key_prefix}_th_r2")
    vth, rth = thevenin_voltage_divider(vs, r1, r2)
    if vth is None:
        st.warning("⚠️ Check that resistances are valid.")
    else:
        in_, rn = norton_from_thevenin(vth, rth)
        st.markdown(f'<div class="status-good">✅ Thevenin: Vth = {vth:.3f} V, Rth = {rth:.2f} Ω &nbsp;|&nbsp; Norton: In = {in_*1000:.3f} mA, Rn = {rn:.2f} Ω</div>', unsafe_allow_html=True)


def render_max_power_sim(key_prefix):
    st.markdown("**⚙️ Maximum Power Transfer Calculator**")
    c1, c2 = st.columns(2)
    vth = c1.number_input("Thevenin Voltage Vth (V)", min_value=0.0, value=10.0, step=0.5, key=f"{key_prefix}_mp_vth")
    rth = c2.number_input("Thevenin Resistance Rth (Ω)", min_value=0.01, value=50.0, step=5.0, key=f"{key_prefix}_mp_rth")
    rl_opt, p_max = max_power_transfer(vth, rth)
    if rl_opt is None:
        st.warning("⚠️ Rth must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Optimal Load RL = {rl_opt:.2f} Ω &nbsp;|&nbsp; Maximum Power = {p_max*1000:.2f} mW</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        rl_vals = [max(rth * 0.05, 0.01) + x * (rth * 4 / 100) for x in range(101)]
        p_vals = [power_delivered(vth, rth, rl) for rl in rl_vals]
        ax.plot(rl_vals, [p * 1000 for p in p_vals], color="#3b82f6", linewidth=2)
        ax.axvline(rl_opt, color="#ef4444", linestyle="--", linewidth=1.5, label="RL = Rth (optimal)")
        ax.set_xlabel("Load Resistance RL (Ω)")
        ax.set_ylabel("Power Delivered (mW)")
        ax.set_title("Power Delivered vs Load Resistance")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Notice power peaks exactly at RL = Rth, and falls off on both sides — matching the theorem.")


def render_source_transform_sim(key_prefix):
    st.markdown("**⚙️ Source Transformation Calculator**")
    direction = st.radio("Convert:", ["Voltage Source → Current Source", "Current Source → Voltage Source"], horizontal=True, key=f"{key_prefix}_st_dir")
    if direction == "Voltage Source → Current Source":
        c1, c2 = st.columns(2)
        vs = c1.number_input("Voltage Source Vs (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_st_vs")
        rs = c2.number_input("Series Resistance Rs (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_st_rs")
        is_, rp = source_transform_v_to_i(vs, rs)
        if is_ is None:
            st.warning("⚠️ Rs must be greater than 0.")
        else:
            st.markdown(f'<div class="status-good">✅ Equivalent Current Source: Is = {is_*1000:.2f} mA, in parallel with Rp = {rp:.2f} Ω</div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        is_ma = c1.number_input("Current Source Is (mA)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_st_is")
        rp = c2.number_input("Parallel Resistance Rp (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_st_rp")
        vs, rs = source_transform_i_to_v(is_ma / 1000.0, rp)
        st.markdown(f'<div class="status-good">✅ Equivalent Voltage Source: Vs = {vs:.2f} V, in series with Rs = {rs:.2f} Ω</div>', unsafe_allow_html=True)


def render_delta_wye_sim(key_prefix):
    st.markdown("**⚙️ Delta-Wye (Δ-Y) Transformation Calculator**")
    direction = st.radio("Convert:", ["Delta → Wye", "Wye → Delta"], horizontal=True, key=f"{key_prefix}_dw_dir")
    if direction == "Delta → Wye":
        c1, c2, c3 = st.columns(3)
        ra = c1.number_input("Ra (Ω)", min_value=0.01, value=30.0, step=5.0, key=f"{key_prefix}_dw_ra")
        rb = c2.number_input("Rb (Ω)", min_value=0.01, value=30.0, step=5.0, key=f"{key_prefix}_dw_rb")
        rc = c3.number_input("Rc (Ω)", min_value=0.01, value=30.0, step=5.0, key=f"{key_prefix}_dw_rc")
        r1, r2, r3 = delta_to_wye(ra, rb, rc)
        if r1 is None:
            st.warning("⚠️ Check that resistances are valid.")
        else:
            st.markdown(f'<div class="status-good">✅ Wye equivalent: R1 = {r1:.2f} Ω, R2 = {r2:.2f} Ω, R3 = {r3:.2f} Ω</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        r1 = c1.number_input("R1 (Ω)", min_value=0.01, value=10.0, step=5.0, key=f"{key_prefix}_dw_r1")
        r2 = c2.number_input("R2 (Ω)", min_value=0.01, value=10.0, step=5.0, key=f"{key_prefix}_dw_r2")
        r3 = c3.number_input("R3 (Ω)", min_value=0.01, value=10.0, step=5.0, key=f"{key_prefix}_dw_r3")
        ra, rb, rc = wye_to_delta(r1, r2, r3)
        if ra is None:
            st.warning("⚠️ Check that resistances are valid.")
        else:
            st.markdown(f'<div class="status-good">✅ Delta equivalent: Ra = {ra:.2f} Ω, Rb = {rb:.2f} Ω, Rc = {rc:.2f} Ω</div>', unsafe_allow_html=True)


def render_superposition_sim(key_prefix):
    st.markdown("**⚙️ Superposition Theorem Calculator**")
    st.caption("Two voltage sources (each with their own series resistor) feeding a shared node through a common resistor.")
    c1, c2, c3 = st.columns(3)
    v1 = c1.number_input("Source V1 (V)", value=10.0, step=1.0, key=f"{key_prefix}_sp_v1")
    v2 = c1.number_input("Source V2 (V)", value=5.0, step=1.0, key=f"{key_prefix}_sp_v2")
    r1 = c2.number_input("Series R1 (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_sp_r1")
    r2 = c2.number_input("Series R2 (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_sp_r2")
    r_common = c3.number_input("Common Resistor (Ω)", min_value=0.01, value=200.0, step=10.0, key=f"{key_prefix}_sp_rc")
    v_from_1, v_from_2, total = superposition_two_sources(v1, v2, r1, r2, r_common)
    st.markdown(
        f'<div class="status-good">✅ Contribution from V1 alone = {v_from_1:.3f} V &nbsp;|&nbsp; '
        f'Contribution from V2 alone = {v_from_2:.3f} V &nbsp;|&nbsp; '
        f'Total (superposed) = {total:.3f} V</div>',
        unsafe_allow_html=True,
    )
    st.caption("Each contribution is found with the OTHER source shorted (set to 0V) — then the results are simply added together.")


def render_millman_sim(key_prefix):
    st.markdown("**⚙️ Millman's Theorem Calculator**")
    st.caption("Three voltage-source branches (each with its own series resistance) meeting at a common node.")
    cols = st.columns(3)
    sources = []
    for i in range(3):
        with cols[i]:
            v = st.number_input(f"V{i+1} (V)", value=float(5 * (i + 1)), step=1.0, key=f"{key_prefix}_mm_v{i}")
            r = st.number_input(f"R{i+1} (Ω)", min_value=0.01, value=100.0, step=10.0, key=f"{key_prefix}_mm_r{i}")
            sources.append((v, r))
    v_node = millmans_theorem(sources)
    if v_node is None:
        st.warning("⚠️ Check that resistances are valid.")
    else:
        st.markdown(f'<div class="status-good">✅ Common Node Voltage = {v_node:.3f} V</div>', unsafe_allow_html=True)


def render_nodal_sim(key_prefix):
    st.markdown("**⚙️ 2-Node Nodal Analysis Solver**")
    st.caption("Solves the linear system [G][V] = [I] for a 2-node circuit using Cramer's rule.")
    st.markdown("**Conductance Matrix (G, in Siemens) and Current Vector (I, in Amps):**")
    c1, c2 = st.columns(2)
    g11 = c1.number_input("G11", value=0.03, step=0.005, format="%.4f", key=f"{key_prefix}_nd_g11")
    g12 = c1.number_input("G12", value=-0.01, step=0.005, format="%.4f", key=f"{key_prefix}_nd_g12")
    g21 = c2.number_input("G21", value=-0.01, step=0.005, format="%.4f", key=f"{key_prefix}_nd_g21")
    g22 = c2.number_input("G22", value=0.02, step=0.005, format="%.4f", key=f"{key_prefix}_nd_g22")
    i1 = st.number_input("I1 (A)", value=0.1, step=0.01, key=f"{key_prefix}_nd_i1")
    i2 = st.number_input("I2 (A)", value=0.0, step=0.01, key=f"{key_prefix}_nd_i2")
    v1, v2 = nodal_2node_solve(g11, g12, g21, g22, i1, i2)
    if v1 is None:
        st.warning("⚠️ This system is singular (no unique solution) — adjust the conductance values.")
    else:
        st.markdown(f'<div class="status-good">✅ V1 = {v1:.3f} V &nbsp;|&nbsp; V2 = {v2:.3f} V</div>', unsafe_allow_html=True)
    st.caption("In a real circuit, G11 and G22 are the sum of conductances (1/R) connected to each node, and G12=G21 is the negative conductance of the resistor shared between them.")


EXTRA_SIMULATORS = {
    "Thevenin & Norton Equivalents": render_thevenin_norton_sim,
    "Maximum Power Transfer": render_max_power_sim,
    "Source Transformation": render_source_transform_sim,
    "Delta-Wye Transformation": render_delta_wye_sim,
    "Superposition Theorem": render_superposition_sim,
    "Millman's Theorem": render_millman_sim,
    "Nodal Analysis (2-Node Solver)": render_nodal_sim,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. What does Thevenin's Theorem let you replace a complex network with?", "options": ["A single resistor only", "A single voltage source in series with a single resistance", "A single current source only"], "answer": "A single voltage source in series with a single resistance"},
    {"q": "2. In the Norton equivalent, how is In related to the Thevenin equivalent?", "options": ["In = Vth × Rth", "In = Vth / Rth", "In = Rth / Vth"], "answer": "In = Vth / Rth"},
    {"q": "3. According to the Maximum Power Transfer Theorem, when is power to the load maximised?", "options": ["When RL is as large as possible", "When RL is as small as possible", "When RL equals Rth"], "answer": "When RL equals Rth"},
    {"q": "4. When applying Superposition, what do you do to every OTHER independent voltage source while analysing one source?", "options": ["Double its value", "Replace it with a short circuit (0V)", "Remove it and leave an open circuit"], "answer": "Replace it with a short circuit (0V)"},
    {"q": "5. What condition indicates a Wheatstone bridge is balanced?", "options": ["The galvanometer reads maximum current", "The galvanometer reads zero current", "All four resistors are equal"], "answer": "The galvanometer reads zero current"},
    {"q": "6. What happens to a loaded voltage divider's output compared to the unloaded (ideal) prediction?", "options": ["It stays exactly the same", "It is always pulled LOWER by the load", "It is always pushed HIGHER by the load"], "answer": "It is always pulled LOWER by the load"},
    {"q": "7. What is the main use of Delta-Wye transformation?", "options": ["Converting AC to DC", "Simplifying resistor networks that aren't purely series or parallel", "Measuring capacitance"], "answer": "Simplifying resistor networks that aren't purely series or parallel"},
    {"q": "8. Which analysis method is based on writing KCL equations at each node?", "options": ["Mesh Analysis", "Nodal Analysis", "Superposition"], "answer": "Nodal Analysis"},
    {"q": "9. What is the practical cause of 'voltage sag' in a real battery under load?", "options": ["The battery's internal resistance", "The load's colour", "The circuit's frequency"], "answer": "The battery's internal resistance"},
    {"q": "10. What makes a source 'dependent' rather than 'independent'?", "options": ["It has no fixed value — it depends on a voltage or current elsewhere in the circuit", "It only works with AC", "It cannot be used in analysis"], "answer": "It has no fixed value — it depends on a voltage or current elsewhere in the circuit"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A student calculates a circuit's Thevenin equivalent, then connects a load resistor equal to Rth, expecting to see the source's full open-circuit voltage across it — but measures only half.",
        "question": "What is the likely misunderstanding?",
        "options": ["Connecting RL = Rth creates a voltage divider between Rth and RL, so the load only sees HALF the Thevenin voltage, not all of it", "The Thevenin calculation must be wrong", "Rth should always be zero"],
        "answer": "Connecting RL = Rth creates a voltage divider between Rth and RL, so the load only sees HALF the Thevenin voltage, not all of it",
        "explanation": "RL = Rth is the condition for MAXIMUM POWER transfer, not maximum voltage — since Rth and RL form a simple series voltage divider, the load will always see exactly half of Vth when they're equal.",
    },
    {
        "scenario": "While applying superposition, a student leaves a second voltage source connected at full value instead of shorting it, while calculating the first source's contribution.",
        "question": "What will happen to their result?",
        "options": ["The calculation will still be correct", "The individual contribution will be wrong, and the sum of all contributions won't match the true circuit response", "Superposition doesn't require sources to be turned off"],
        "answer": "The individual contribution will be wrong, and the sum of all contributions won't match the true circuit response",
        "explanation": "Superposition specifically requires isolating the effect of ONE source at a time — leaving other independent sources active breaks the method's core assumption and produces an incorrect (double-counted) result.",
    },
    {
        "scenario": "A voltage divider was designed assuming no load, but once the real load resistor is connected, the measured output voltage is noticeably lower than the calculated value.",
        "question": "What is the most likely explanation?",
        "options": ["The load resistor forms a parallel combination with the lower divider resistor, pulling the output down — exactly as expected for a loaded divider", "The resistors must be faulty", "Voltage dividers cannot be loaded at all"],
        "answer": "The load resistor forms a parallel combination with the lower divider resistor, pulling the output down — exactly as expected for a loaded divider",
        "explanation": "This is completely normal, predictable behaviour — the simple unloaded-divider formula only applies when nothing else draws current from the output node.",
    },
    {
        "scenario": "A student building a Wheatstone bridge circuit adjusts one resistor but the galvanometer never reads exactly zero, no matter what value they try.",
        "question": "What is a sensible thing to check?",
        "options": ["Whether the other three resistor values actually allow a balance point to exist for the range of the adjustable resistor", "Whether the galvanometer needs more power", "Whether Wheatstone bridges can ever be balanced at all"],
        "answer": "Whether the other three resistor values actually allow a balance point to exist for the range of the adjustable resistor",
        "explanation": "The balance condition R1×R3 = R2×Rx has a specific required value for Rx — if the adjustable resistor's range doesn't include that value, true balance can never be reached no matter how it's adjusted.",
    },
    {
        "scenario": "A student sets up nodal analysis equations for a circuit, but their conductance matrix is singular (determinant = 0), and the solver gives no unique answer.",
        "question": "What does a singular system typically indicate?",
        "options": ["The circuit is drawing too much current", "The equations are not independent — often from a mistake in setting up the node equations, or a genuinely underdetermined circuit", "The resistors are too large"],
        "answer": "The equations are not independent — often from a mistake in setting up the node equations, or a genuinely underdetermined circuit",
        "explanation": "A singular (non-invertible) system means the equations don't provide enough independent information to pin down a unique solution — usually worth double-checking that every node and every KCL equation was set up correctly.",
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
st.sidebar.title("🧮 CIRCUIT ANALYSIS")
st.sidebar.subheader("LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore circuit elements & sources\n"
    "3. Study theorems & analysis methods\n"
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
        "🔎 Circuit Elements & Sources",
        "📐 Theorems & Analysis Methods",
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
st.title("🧮 Circuit Analysis Learning Lab")
st.caption("An Interactive Beginner's Guide to Circuit Theorems & Analysis Methods")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Circuit Elements", len(CIRCUIT_ELEMENTS))
d2.metric("📐 Theorems & Methods", len(ANALYSIS_METHODS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Circuit Analysis")

    st.markdown(
        """
        ### Why Do We Need Special Analysis Methods?
        For simple series and parallel resistor circuits, Ohm's Law is all you need.
        But real circuits often have multiple sources, multiple loops, and resistor
        networks that are neither purely series nor purely parallel — and for those,
        we need more powerful, systematic tools.

        This module covers the essential theorems and methods every electronics
        student needs to analyse arbitrarily complex LINEAR circuits — often without
        needing to solve the whole thing at once.
        """
    )

    st.subheader("🧰 Two Broad Strategies")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>🔢 Systematic Equation Methods</h4>'
            '<p><b>Nodal Analysis</b> and <b>Mesh Analysis</b> — write a full system of '
            'equations describing the whole circuit at once, then solve them together.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>✂️ Simplification Theorems</h4>'
            '<p><b>Thevenin</b>, <b>Norton</b>, <b>Superposition</b>, and <b>Source Transformation</b> — '
            'reduce part of a circuit to something much simpler before solving.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("⚠️ The Golden Rule: Linearity")
    st.markdown(
        '<div class="app-card">Every theorem in this module — Superposition, Thevenin, Norton, Millman\'s — '
        'relies on the circuit being <b>LINEAR</b>: made only of resistors, linear dependent sources, and '
        'independent sources (no diodes, transistors driven into nonlinear regions, or other nonlinear '
        'elements). Applying these theorems to a nonlinear circuit will give wrong answers.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Head to **'Circuit Elements & Sources'** in the sidebar to explore the building blocks these methods work with.")

# ============================================================================
# 2. CIRCUIT ELEMENTS & SOURCES
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Circuit Elements & Sources Explorer")
    st.caption("Expand each entry to see its symbol, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in CIRCUIT_ELEMENT_ORDER:
        c = CIRCUIT_ELEMENTS[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_circuit_element_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Symbol:** {c['symbol_desc']}")
                st.markdown(f"**Key Property:** {c['key_property']}")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. THEOREMS & ANALYSIS METHODS
# ============================================================================
elif page.startswith("📐"):
    st.header("📐 Theorems & Analysis Methods")
    st.caption("The key theorems and systematic methods for analysing linear circuits.")

    filter_tags = st.multiselect(
        "Filter circuit elements by category",
        ["source", "ideal", "practical", "dependent", "reference", "circuit", "measurement"],
        default=[],
    )
    if filter_tags:
        filtered = [n for n in CIRCUIT_ELEMENT_ORDER if any(t in CIRCUIT_ELEMENTS[n]["category"] for t in filter_tags)]
    else:
        filtered = CIRCUIT_ELEMENT_ORDER

    st.subheader("🧮 Circuit Element Reference Table")
    rows = []
    for name in filtered:
        c = CIRCUIT_ELEMENTS[name]
        rows.append({
            "Element": name,
            "Symbol": c["symbol_desc"],
            "Key Property": c["key_property"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Circuit Theorems & Methods")
    for method_name in ANALYSIS_METHOD_ORDER:
        m = ANALYSIS_METHODS[method_name]
        with st.expander(f"**{method_name}**"):
            st.markdown(f"**Key facts:** {m['formula']}")
            st.markdown(f"**Explanation:** {m['explanation']}")
            st.markdown(f"**Used for:** {m['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any theorem or analysis method and work through a live example.")

    sel = st.selectbox("Select a theorem or method", list(EXTRA_SIMULATORS.keys()))
    st.markdown(
        flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #4338ca, #312e81);">'
             f'🧮 <b>{sel}</b></div>'),
        unsafe_allow_html=True,
    )
    EXTRA_SIMULATORS[sel](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how circuit analysis theorems solve real engineering problems.")

    APPLICATIONS = [
        ("🔊 Audio Amplifier Design", "Maximum Power Transfer guides speaker/amplifier impedance matching so the amplifier delivers as much power as possible to the speaker without excessive distortion or wasted heat."),
        ("🔋 Battery & Power Supply Design", "Thevenin equivalents let engineers characterise a power source's behaviour with just two numbers (Vth, Rth), predicting how it will perform under any load without re-analysing the internal circuitry each time."),
        ("📡 Antenna & Transmission Line Matching", "Matching a transmission line's impedance to an antenna's impedance (a direct application of Maximum Power Transfer) minimises signal reflections and maximises transmitted power."),
        ("⚖️ Precision Measurement", "Wheatstone bridges, balanced using precision reference resistors, remain one of the most accurate ways to measure an unknown resistance, strain, or temperature."),
        ("🖥️ Circuit Simulation Software (SPICE)", "Software tools like SPICE solve circuits internally using large-scale nodal analysis, systematically applying KCL at every node in even enormously complex circuits."),
        ("⚡ Three-Phase Power Systems", "Delta-Wye transformation is fundamental to analysing three-phase power distribution, letting engineers convert between the two common wiring configurations used in power grids."),
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
    st.header("📝 Circuit Analysis Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Circuit Elements & Sources' section and try again!")

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
