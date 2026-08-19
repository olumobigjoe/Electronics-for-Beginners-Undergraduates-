"""
🔀 Transistors & Amplifiers Learning Lab
An Interactive Beginner's Guide to Transistors & Amplifier Circuits

Built for first-year undergraduate Physics / Electronics students.
Single-file Streamlit application. No external APIs, databases, or internet
services are used — only streamlit, pandas, and matplotlib.

Run with:
    streamlit run app.py
"""

import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Transistors & Amplifiers Learning Lab",
    page_icon="🔀",
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
        background: linear-gradient(135deg, #164e63, #0e7490);
        border: 1px solid #22d3ee;
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
# CORE TRANSISTOR / AMPLIFIER CALCULATIONS (pure functions, no widgets)
# ============================================================================

def bjt_operating_point(vcc, rb, rc, vbe=0.7, beta=100):
    """Simple fixed-bias BJT DC analysis. Returns (Ib, Ic, Vce, saturated)."""
    if rb <= 0:
        return None, None, None, False
    ib = (vcc - vbe) / rb
    if ib <= 0:
        return ib, 0.0, vcc, False
    ic = beta * ib
    vce = vcc - ic * rc
    saturated = vce <= 0.2
    if saturated:
        vce = 0.2
        ic = (vcc - vce) / rc if rc > 0 else ic
    return ib, ic, vce, saturated


def ce_gain_with_re(rc, re):
    """Common-emitter voltage gain with an UNBYPASSED emitter resistor: Av ≈ -Rc/Re."""
    if re <= 0:
        return None
    return -rc / re


def ce_gain_bypassed(rc, ic_ma, vt=0.02585):
    """Common-emitter voltage gain with a BYPASSED emitter resistor: Av ≈ -gm*Rc."""
    if ic_ma <= 0:
        return None
    ic_a = ic_ma / 1000.0
    gm = ic_a / vt  # transconductance in Siemens
    return -gm * rc


def emitter_follower_gain(re, r_source=0.0):
    """Emitter follower (common collector) voltage gain — close to, but just under, 1."""
    total = re + r_source
    if total <= 0:
        return None
    return re / total


def mosfet_drain_current_ma(vgs, vth, k_ma_per_v2=1.0):
    """Simplified square-law MOSFET model (saturation region): Id = k(Vgs-Vth)^2."""
    if vgs <= vth:
        return 0.0
    return k_ma_per_v2 * (vgs - vth) ** 2


def darlington_beta(beta1, beta2):
    """Combined current gain of a Darlington pair: β ≈ β1×β2 + β1 + β2."""
    return beta1 * beta2 + beta1 + beta2


def phototransistor_current_ma(light_pct, beta=100, base_light_current_ua=0.5):
    """Simplified, illustrative model: light generates a small base-equivalent
    current, amplified by the transistor's beta."""
    ib_a = (light_pct / 100.0) * base_light_current_ua * 1e-6
    ic_a = beta * ib_a
    return ic_a * 1000.0


def ujt_oscillator_freq(r_ohm, c_uf, eta=0.6):
    """Classic UJT relaxation oscillator frequency:
    f = 1 / (R * C * ln(1 / (1 - eta)))."""
    c_f = c_uf * 1e-6
    if r_ohm <= 0 or c_f <= 0 or not (0 < eta < 1):
        return None
    try:
        return 1.0 / (r_ohm * c_f * math.log(1.0 / (1.0 - eta)))
    except (ValueError, ZeroDivisionError):
        return None


# ============================================================================
# TRANSISTOR TYPES DATA
# 9 transistor types, each with the fields the Explorer page needs.
# "calc_key" links a transistor to its interactive render function further down.
# ============================================================================
TRANSISTOR_TYPES = {
    "NPN BJT": {
        "desc": "The most common Bipolar Junction Transistor — a small base current controls a much larger collector current.",
        "terminals": "Base (B), Collector (C), Emitter (E)",
        "control": "Current-controlled: base current (Ib) sets collector current (Ic ≈ β × Ib)",
        "category": ["bjt", "amplifying", "switching"],
        "explanation": "Think of an NPN transistor as a valve controlled by a trickle of water: a small current into the Base lets a much larger current flow from Collector to Emitter — this current-controlled amplification is the essence of a BJT.",
        "applications": "Amplifier stages, digital switching, current sources, the building block of countless analogue circuits.",
        "safety": "Exceeding maximum collector current, collector-emitter voltage, or power dissipation will destroy the transistor — always check the datasheet limits.",
        "calc_key": "bjt_bias",
    },
    "PNP BJT": {
        "desc": "The 'mirror image' of an NPN transistor — all currents and voltages are reversed in polarity.",
        "terminals": "Base (B), Collector (C), Emitter (E)",
        "control": "Current-controlled, but current flows OUT of the base to turn it on (opposite to NPN)",
        "category": ["bjt", "amplifying", "switching"],
        "explanation": "A PNP transistor works exactly like an NPN transistor, but 'upside down' electrically — the Emitter is normally at a HIGHER voltage than the Collector, and turning it on means pulling current OUT of the base rather than pushing it in.",
        "applications": "High-side switching (switching the positive supply rail), complementary pairs with NPN transistors in push-pull amplifier stages.",
        "safety": "Easy to confuse with NPN wiring — connecting a PNP transistor with NPN-style biasing will simply not work (and may damage it).",
        "calc_key": None,
    },
    "N-Channel MOSFET": {
        "desc": "A voltage-controlled transistor: the voltage on an insulated Gate controls current flow between Drain and Source.",
        "terminals": "Gate (G), Drain (D), Source (S)",
        "control": "Voltage-controlled: Gate-Source voltage (Vgs) controls Drain current (Id)",
        "category": ["fet", "amplifying", "switching", "power"],
        "explanation": "Unlike a BJT, a MOSFET's Gate is electrically insulated from the channel — almost no current flows into the gate at all. Instead, the Gate voltage creates an electric field that controls how much current can flow through the channel.",
        "applications": "Power switching (motor drivers, PWM circuits), digital logic (the basis of virtually all modern ICs), high-efficiency power supplies.",
        "safety": "⚠️ MOSFET gates are extremely sensitive to static electricity (ESD) and can be damaged just by touching the pins. Never leave a MOSFET gate floating (unconnected) in a circuit — it can pick up stray charge and switch on unpredictably.",
        "calc_key": "mosfet_calc",
    },
    "P-Channel MOSFET": {
        "desc": "The complementary counterpart to an N-channel MOSFET — conducts when the Gate is made NEGATIVE relative to the Source.",
        "terminals": "Gate (G), Drain (D), Source (S)",
        "control": "Voltage-controlled, but turns ON when Vgs is negative (opposite to N-channel)",
        "category": ["fet", "amplifying", "switching", "power"],
        "explanation": "A P-channel MOSFET behaves like an N-channel MOSFET with all voltage polarities reversed — it's commonly used for high-side switching, where the Source connects to the positive supply rail.",
        "applications": "High-side power switching, complementary CMOS logic circuits (paired with N-channel MOSFETs), reverse-polarity protection circuits.",
        "safety": "Same ESD sensitivity as N-channel MOSFETs — handle gate pins with care.",
        "calc_key": None,
    },
    "JFET": {
        "desc": "Junction Field-Effect Transistor — a voltage-controlled transistor that is normally ON, and is turned OFF by an increasing reverse gate voltage.",
        "terminals": "Gate (G), Drain (D), Source (S)",
        "control": "Voltage-controlled: increasing reverse Gate-Source voltage PINCHES OFF the channel, reducing current",
        "category": ["fet", "amplifying"],
        "explanation": "Unlike a MOSFET (normally off until you turn it on), a JFET is normally ON — applying a reverse voltage to its Gate progressively 'pinches off' the conducting channel, reducing current the more reverse voltage you apply.",
        "applications": "Low-noise amplifier input stages, analogue switches, voltage-controlled resistors.",
        "safety": "The Gate-Source junction is essentially a diode — forward-biasing it (rather than reverse-biasing, as intended) can damage the device.",
        "calc_key": None,
    },
    "IGBT": {
        "desc": "Insulated Gate Bipolar Transistor — combines a MOSFET's easy voltage-controlled Gate with a BJT's ability to handle high current and voltage.",
        "terminals": "Gate (G), Collector (C), Emitter (E)",
        "control": "Voltage-controlled Gate (like a MOSFET), but current flows like a BJT's Collector-Emitter path",
        "category": ["hybrid", "power", "switching"],
        "explanation": "An IGBT is essentially a MOSFET driving a BJT internally — giving you the simple, low-power Gate drive of a MOSFET combined with the high voltage and current handling of a BJT, ideal for heavy-duty power switching.",
        "applications": "Motor drives, electric vehicle inverters, industrial power supplies, renewable energy inverters (solar/wind).",
        "safety": "⚠️ IGBTs are used in high-power circuits, often at dangerous voltages — always follow proper high-power safety procedures and never work on live power electronics without training.",
        "calc_key": None,
    },
    "Darlington Pair": {
        "desc": "Two BJT transistors connected so the first amplifies the base current for the second, multiplying the overall current gain.",
        "terminals": "Base (B), Collector (C), Emitter (E) — behaves as a single transistor with much higher gain",
        "control": "Current-controlled, like a single BJT, but with dramatically higher effective β",
        "category": ["bjt", "amplifying", "switching"],
        "explanation": "By feeding the Emitter current of one transistor into the Base of a second, a Darlington pair multiplies their individual current gains together — a pair of transistors with β=100 each can combine for an effective gain of over 10,000.",
        "applications": "Driving high-current loads (motors, relays, solenoids) from a very small control current — common in Darlington driver ICs (e.g. ULN2003).",
        "safety": "Has a higher base-emitter turn-on voltage (≈1.2–1.4V, since it's two junctions) than a single transistor — account for this in bias calculations.",
        "calc_key": "darlington_calc",
    },
    "Phototransistor": {
        "desc": "A transistor whose base current is generated by light striking its junction instead of an external electrical connection.",
        "terminals": "Collector (C), Emitter (E) — often no separate Base lead is brought out",
        "control": "Light-controlled: more light striking the junction generates a larger effective base current, which is then amplified",
        "category": ["optical", "sensing"],
        "explanation": "A phototransistor is like a photodiode combined with a transistor amplifier stage built into a single device — the small photocurrent that light generates gets multiplied by the transistor's current gain, making it far more sensitive than a plain photodiode.",
        "applications": "Light sensors, optical isolators (optocouplers), IR remote-control receivers, object/proximity detection.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "phototransistor_calc",
    },
    "UJT (Unijunction Transistor)": {
        "desc": "A three-terminal device that isn't really a transistor in the amplifying sense — it's a specialised switch that triggers sharply once its Emitter voltage crosses a threshold set by the two Base terminals.",
        "terminals": "Emitter (E), Base 1 (B1), Base 2 (B2)",
        "control": "Triggers when Emitter voltage exceeds a threshold set by the 'intrinsic standoff ratio' (η) and the B1-B2 voltage",
        "category": ["special_purpose", "oscillator"],
        "explanation": "A UJT doesn't amplify signals like a BJT or FET — instead, it acts as a voltage-triggered switch, making it perfect for building simple relaxation oscillators: a capacitor charges up slowly through a resistor until it hits the UJT's trigger point, then discharges rapidly, and the cycle repeats.",
        "applications": "Simple sawtooth/relaxation oscillators, timing circuits, triggering circuits for SCRs (thyristors) in power control.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "ujt_calc",
    },
}

TRANSISTOR_ORDER = list(TRANSISTOR_TYPES.keys())

# ============================================================================
# AMPLIFIER CONFIGURATIONS & CLASSES DATA
# (used on the "Amplifier Configurations & Classes" page)
# ============================================================================
AMPLIFIER_CONFIGS = {
    "Common Emitter (CE)": {
        "formula": "Av ≈ -Rc/Re (unbypassed) or -gm×Rc (bypassed)  |  High voltage & current gain  |  Inverts the signal (180° phase shift)",
        "explanation": "The most widely used BJT amplifier configuration — the input is applied to the Base, the output is taken from the Collector, and the Emitter is common to both. Offers strong voltage AND current gain, but inverts the signal.",
        "use": "General-purpose voltage amplification — the default choice for a single BJT amplifier stage.",
    },
    "Common Base (CB)": {
        "formula": "Av can be high, but current gain ≈ 1  |  Does NOT invert the signal  |  Low input impedance, high output impedance",
        "explanation": "The input is applied to the Emitter and the output taken from the Collector, with the Base held at a fixed (common) voltage. Excellent high-frequency performance, but its very low input impedance makes it less common for general use.",
        "use": "High-frequency / RF amplifier stages, current buffers.",
    },
    "Common Collector (CC) / Emitter Follower": {
        "formula": "Av ≈ 1 (slightly less than 1)  |  High current gain  |  Does NOT invert the signal  |  High input impedance, low output impedance",
        "explanation": "The input is applied to the Base and the output taken from the Emitter, with the Collector common (tied to the supply). Voltage gain is close to 1 — its real value is impedance matching, not voltage amplification.",
        "use": "Buffer stages — isolating a high-impedance source from a low-impedance load without loading it down.",
    },
    "Common Source (CS)": {
        "formula": "Av ≈ -gm×Rd  |  High voltage gain  |  Inverts the signal  |  The FET equivalent of a Common Emitter stage",
        "explanation": "The FET counterpart to the BJT's Common Emitter configuration — input at the Gate, output at the Drain, Source common to both. Provides strong voltage gain with very high input impedance (since the Gate draws almost no current).",
        "use": "General-purpose FET voltage amplification, especially where very high input impedance matters.",
    },
    "Common Drain (CD) / Source Follower": {
        "formula": "Av ≈ 1 (slightly less than 1)  |  Does NOT invert the signal  |  Very high input impedance, low output impedance",
        "explanation": "The FET counterpart to the BJT's Emitter Follower — input at the Gate, output at the Source. Used for buffering, just like the emitter follower, but with even higher input impedance.",
        "use": "Buffer stages for very high-impedance sources (e.g. following a sensitive sensor or a Common Source stage).",
    },
    "Common Gate (CG)": {
        "formula": "Av can be high, current gain ≈ 1  |  Does NOT invert the signal  |  Low input impedance, good high-frequency response",
        "explanation": "The FET counterpart to Common Base — input at the Source, output at the Drain, Gate held at a fixed (common) voltage. Like Common Base, it excels at high frequencies.",
        "use": "High-frequency / RF amplifier stages.",
    },
    "Class A Amplifier": {
        "formula": "Conduction angle = 360° (transistor conducts for the ENTIRE input cycle)  |  Typical efficiency ≈ 20–30%",
        "explanation": "The transistor is biased to conduct throughout the entire input signal cycle, giving the lowest distortion of any class — but also the lowest efficiency, since the transistor is always dissipating power even with no signal.",
        "use": "High-fidelity audio amplifiers where sound quality matters more than efficiency.",
    },
    "Class B Amplifier": {
        "formula": "Conduction angle = 180° (each transistor conducts for HALF the input cycle)  |  Typical efficiency ≈ 65–78.5%",
        "explanation": "Two transistors share the work, each handling one half of the signal (push-pull) — much more efficient than Class A, but with 'crossover distortion' where the two halves meet near zero volts.",
        "use": "Higher-efficiency audio power amplifiers where some crossover distortion is acceptable or later corrected.",
    },
    "Class AB Amplifier": {
        "formula": "Conduction angle between 180° and 360°  |  Typical efficiency ≈ 50–70%",
        "explanation": "A practical compromise between Class A and Class B — a small bias current keeps both transistors slightly conducting near the crossover point, greatly reducing crossover distortion while keeping reasonably good efficiency.",
        "use": "The most common choice for real-world audio power amplifiers — a balance of good sound quality and reasonable efficiency.",
    },
    "Class C Amplifier": {
        "formula": "Conduction angle less than 180° (conducts for only a SMALL portion of the cycle)  |  Typical efficiency > 80%",
        "explanation": "The transistor conducts for only a small slice of each cycle, driving a resonant (tuned) circuit that 'rings' to reconstruct the rest of the waveform — extremely efficient, but only works for a narrow range of frequencies and introduces significant distortion.",
        "use": "RF transmitter power amplifiers at a single fixed frequency, where a tuned output circuit can restore the waveform.",
    },
}

AMPLIFIER_ORDER = list(AMPLIFIER_CONFIGS.keys())

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each transistor type. Every
# returned string is flattened to one line with flat() so Streamlit's
# Markdown renderer never mis-parses an embedded blank line as the end of
# the block.
# ============================================================================
TRANSISTOR_COLORS = {
    "NPN BJT": "#3b82f6",
    "PNP BJT": "#f97316",
    "N-Channel MOSFET": "#8b5cf6",
    "P-Channel MOSFET": "#ec4899",
    "JFET": "#14b8a6",
    "IGBT": "#eab308",
    "Darlington Pair": "#22c55e",
    "Phototransistor": "#06b6d4",
    "UJT (Unijunction Transistor)": "#ef4444",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def draw_transistor_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the transistor type."""
    color = TRANSISTOR_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "NPN BJT":
        body = f"""
        <circle cx="115" cy="70" r="48" fill="none" stroke="{color}" stroke-width="3"/>
        {_lead(0, 70, 95, 70)}
        <line x1="95" y1="42" x2="95" y2="98" stroke="{color}" stroke-width="5"/>
        <line x1="95" y1="55" x2="145" y2="30" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="30" x2="145" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="95" y1="85" x2="145" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="110" x2="145" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="145,110 127,100 131,114" fill="{color}"/>
        <text x="150" y="14" font-size="13" font-weight="bold" fill="#111827">C</text>
        <text x="98" y="63" font-size="13" font-weight="bold" fill="#111827">B</text>
        <text x="150" y="134" font-size="13" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "PNP BJT":
        body = f"""
        <circle cx="115" cy="70" r="48" fill="none" stroke="{color}" stroke-width="3"/>
        {_lead(0, 70, 95, 70)}
        <line x1="95" y1="42" x2="95" y2="98" stroke="{color}" stroke-width="5"/>
        <line x1="95" y1="55" x2="145" y2="30" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="30" x2="145" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="95" y1="85" x2="145" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="110" x2="145" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="95,85 113,89 108,76" fill="{color}"/>
        <text x="150" y="14" font-size="13" font-weight="bold" fill="#111827">C</text>
        <text x="98" y="63" font-size="13" font-weight="bold" fill="#111827">B</text>
        <text x="150" y="134" font-size="13" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "N-Channel MOSFET":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <line x1="60" y1="35" x2="60" y2="105" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="30" x2="72" y2="55" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="60" x2="72" y2="80" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="85" x2="72" y2="110" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="32" x2="150" y2="32" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="32" x2="150" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="70" x2="100" y2="70" stroke="{color}" stroke-width="4"/>
        <line x1="100" y1="70" x2="100" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="100,110 92,96 108,96" fill="{color}"/>
        <line x1="72" y1="108" x2="150" y2="108" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="108" x2="150" y2="130" stroke="{color}" stroke-width="4"/>
        <text x="155" y="14" font-size="12" font-weight="bold" fill="#111827">D</text>
        <text x="30" y="63" font-size="12" font-weight="bold" fill="#111827">G</text>
        <text x="155" y="134" font-size="12" font-weight="bold" fill="#111827">S</text>
        """

    elif name == "P-Channel MOSFET":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <line x1="60" y1="35" x2="60" y2="105" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="30" x2="72" y2="55" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="60" x2="72" y2="80" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="85" x2="72" y2="110" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="32" x2="150" y2="32" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="32" x2="150" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="70" x2="100" y2="70" stroke="{color}" stroke-width="4"/>
        <line x1="100" y1="70" x2="100" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="72,70 88,78 88,62" fill="{color}"/>
        <line x1="72" y1="108" x2="150" y2="108" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="108" x2="150" y2="130" stroke="{color}" stroke-width="4"/>
        <text x="155" y="14" font-size="12" font-weight="bold" fill="#111827">D</text>
        <text x="30" y="63" font-size="12" font-weight="bold" fill="#111827">G</text>
        <text x="155" y="134" font-size="12" font-weight="bold" fill="#111827">S</text>
        """

    elif name == "JFET":
        body = f"""
        {_lead(0, 70, 55, 70)}
        <line x1="55" y1="40" x2="55" y2="100" stroke="{color}" stroke-width="5"/>
        <line x1="55" y1="45" x2="30" y2="45" stroke="{color}" stroke-width="3"/>
        <polygon points="30,45 44,39 44,51" fill="{color}"/>
        {_lead(0, 45, 30, 45, color, 3)}
        <line x1="55" y1="50" x2="120" y2="30" stroke="{color}" stroke-width="4"/>
        <line x1="120" y1="30" x2="120" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="55" y1="90" x2="120" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="120" y1="110" x2="120" y2="130" stroke="{color}" stroke-width="4"/>
        <text x="125" y="14" font-size="12" font-weight="bold" fill="#111827">D</text>
        <text x="0" y="38" font-size="12" font-weight="bold" fill="#111827">G</text>
        <text x="125" y="134" font-size="12" font-weight="bold" fill="#111827">S</text>
        """

    elif name == "IGBT":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <line x1="60" y1="35" x2="60" y2="105" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="30" x2="72" y2="110" stroke="{color}" stroke-width="5"/>
        <line x1="72" y1="32" x2="150" y2="32" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="32" x2="150" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="72" y1="70" x2="150" y2="108" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="108" x2="150" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="150,108 132,102 136,116" fill="{color}"/>
        <text x="155" y="14" font-size="12" font-weight="bold" fill="#111827">C</text>
        <text x="30" y="63" font-size="12" font-weight="bold" fill="#111827">G</text>
        <text x="155" y="134" font-size="12" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "Darlington Pair":
        body = f"""
        <rect x="20" y="10" width="180" height="120" rx="8" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="4,3"/>
        <circle cx="80" cy="55" r="28" fill="none" stroke="{color}" stroke-width="2.5"/>
        {_lead(0, 55, 55, 55, color, 3)}
        <line x1="55" y1="40" x2="55" y2="70" stroke="{color}" stroke-width="4"/>
        <line x1="55" y1="45" x2="90" y2="30" stroke="{color}" stroke-width="3"/>
        <line x1="55" y1="65" x2="90" y2="80" stroke="{color}" stroke-width="3"/>
        <polygon points="55,65 70,68 66,56" fill="{color}"/>
        <circle cx="145" cy="90" r="28" fill="none" stroke="{color}" stroke-width="2.5"/>
        <line x1="120" y1="75" x2="120" y2="105" stroke="{color}" stroke-width="4"/>
        <line x1="90" y1="80" x2="120" y2="90" stroke="{color}" stroke-width="3"/>
        <line x1="120" y1="80" x2="160" y2="65" stroke="{color}" stroke-width="3"/>
        <line x1="160" y1="65" x2="160" y2="45" stroke="{color}" stroke-width="3"/>
        <line x1="120" y1="100" x2="160" y2="115" stroke="{color}" stroke-width="3"/>
        <line x1="160" y1="115" x2="160" y2="132" stroke="{color}" stroke-width="3"/>
        <polygon points="120,100 138,103 134,90" fill="{color}"/>
        <text x="163" y="42" font-size="11" font-weight="bold" fill="#111827">C</text>
        <text x="163" y="132" font-size="11" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "Phototransistor":
        body = f"""
        <circle cx="115" cy="70" r="48" fill="none" stroke="{color}" stroke-width="3"/>
        <line x1="95" y1="42" x2="95" y2="98" stroke="{color}" stroke-width="5"/>
        <line x1="95" y1="55" x2="145" y2="30" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="30" x2="145" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="95" y1="85" x2="145" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="145" y1="110" x2="145" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="145,110 127,100 131,114" fill="{color}"/>
        <line x1="60" y1="10" x2="80" y2="30" stroke="{color}" stroke-width="3"/>
        <polygon points="80,30 71,28 78,21" fill="{color}"/>
        <line x1="45" y1="30" x2="65" y2="50" stroke="{color}" stroke-width="3"/>
        <polygon points="65,50 56,48 63,41" fill="{color}"/>
        <text x="150" y="14" font-size="13" font-weight="bold" fill="#111827">C</text>
        <text x="150" y="134" font-size="13" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "UJT (Unijunction Transistor)":
        body = f"""
        <line x1="90" y1="20" x2="90" y2="120" stroke="{color}" stroke-width="6"/>
        {_lead(90, 20, 130, 5, color, 3)}
        {_lead(130, 5, 175, 5)}
        {_lead(90, 120, 130, 135, color, 3)}
        {_lead(130, 135, 175, 135)}
        <line x1="20" y1="70" x2="60" y2="70" stroke="{color}" stroke-width="3"/>
        <polygon points="60,70 48,64 48,76" fill="{color}"/>
        {_lead(0, 70, 20, 70, color, 3)}
        <text x="135" y="2" font-size="11" font-weight="bold" fill="#111827">B2</text>
        <text x="135" y="145" font-size="11" font-weight="bold" fill="#111827">B1</text>
        <text x="5" y="60" font-size="11" font-weight="bold" fill="#111827">E</text>
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same item is rendered on more than one page.
# ============================================================================

def render_bjt_bias(key_prefix):
    st.markdown("**⚙️ BJT DC Bias / Operating Point Calculator** (simple fixed-bias)")
    c1, c2 = st.columns(2)
    vcc = c1.number_input("Supply Voltage Vcc (V)", min_value=0.0, value=9.0, step=0.5, key=f"{key_prefix}_bjt_vcc")
    rb = c1.number_input("Base Resistor Rb (kΩ)", min_value=0.1, value=100.0, step=10.0, key=f"{key_prefix}_bjt_rb")
    rc = c2.number_input("Collector Resistor Rc (kΩ)", min_value=0.1, value=1.0, step=0.1, key=f"{key_prefix}_bjt_rc")
    beta = c2.number_input("Current Gain (β)", min_value=1.0, value=100.0, step=10.0, key=f"{key_prefix}_bjt_beta")
    ib, ic, vce, saturated = bjt_operating_point(vcc, rb * 1000, rc * 1000, beta=beta)
    if ib is None:
        st.warning("⚠️ Base resistor must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Ib = {ib*1e6:.2f} µA &nbsp;|&nbsp; Ic = {ic*1000:.2f} mA &nbsp;|&nbsp; Vce = {vce:.2f} V</div>', unsafe_allow_html=True)
        if saturated:
            st.markdown('<div class="status-bad">⚠️ This bias point drives the transistor into SATURATION (Vce near 0) — it is acting as a closed switch, not a linear amplifier.</div>', unsafe_allow_html=True)
        elif vce >= vcc - 0.2:
            st.markdown('<div class="status-bad">⚠️ Ib is very small — the transistor is close to CUTOFF (barely conducting).</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-good">✅ Operating in the ACTIVE (linear) region — suitable for amplification.</div>', unsafe_allow_html=True)


def render_mosfet_calc(key_prefix):
    st.markdown("**⚙️ MOSFET Drain Current Calculator** (simplified square-law model)")
    c1, c2, c3 = st.columns(3)
    vgs = c1.number_input("Gate-Source Voltage Vgs (V)", value=3.0, step=0.1, key=f"{key_prefix}_mos_vgs")
    vth = c2.number_input("Threshold Voltage Vth (V)", min_value=0.1, value=2.0, step=0.1, key=f"{key_prefix}_mos_vth")
    k = c3.number_input("Transconductance Parameter k (mA/V²)", min_value=0.01, value=2.0, step=0.5, key=f"{key_prefix}_mos_k")
    id_ma = mosfet_drain_current_ma(vgs, vth, k)
    if id_ma <= 0:
        st.markdown('<div class="status-bad">⛔ Vgs is below threshold — MOSFET is OFF, no drain current flows.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-good">✅ MOSFET is ON — Drain Current Id ≈ {id_ma:.2f} mA</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    vgs_range = [vth - 1 + x * 0.05 for x in range(int((4) / 0.05) + 1)]
    curve = [mosfet_drain_current_ma(v, vth, k) for v in vgs_range]
    ax.plot(vgs_range, curve, color="#8b5cf6", linewidth=2)
    ax.scatter([vgs], [id_ma], color="#ef4444", zorder=5)
    ax.axvline(vth, color="#9ca3af", linestyle="--", linewidth=1, label="Vth")
    ax.set_xlabel("Vgs (V)")
    ax.set_ylabel("Id (mA)")
    ax.set_title("MOSFET Transfer Characteristic")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_darlington_calc(key_prefix):
    st.markdown("**⚙️ Darlington Pair Combined Gain Calculator** — `β ≈ β1×β2 + β1 + β2`")
    c1, c2 = st.columns(2)
    beta1 = c1.number_input("Transistor 1 Gain (β1)", min_value=1.0, value=100.0, step=10.0, key=f"{key_prefix}_dar_b1")
    beta2 = c2.number_input("Transistor 2 Gain (β2)", min_value=1.0, value=100.0, step=10.0, key=f"{key_prefix}_dar_b2")
    combined = darlington_beta(beta1, beta2)
    st.markdown(f'<div class="status-good">✅ Combined Darlington Gain β ≈ {combined:,.0f}</div>', unsafe_allow_html=True)
    st.caption("A tiny base current can now control a dramatically larger collector current than either transistor could alone.")


def render_phototransistor_calc(key_prefix):
    st.markdown("**⚙️ Phototransistor Light Response Simulator** (simplified educational model)")
    c1, c2 = st.columns(2)
    light = c1.slider("Light level: Dark ← → Bright", 0, 100, 50, key=f"{key_prefix}_pt_light")
    beta = c2.number_input("Current Gain (β)", min_value=1.0, value=100.0, step=10.0, key=f"{key_prefix}_pt_beta")
    ic_ma = phototransistor_current_ma(light, beta)
    st.markdown(f'<div class="status-good">✅ Approximate Collector Current ≈ {ic_ma:.3f} mA</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    levels = list(range(0, 101, 5))
    curve = [phototransistor_current_ma(x, beta) for x in levels]
    ax.plot(levels, curve, color="#06b6d4", linewidth=2)
    ax.scatter([light], [ic_ma], color="#ef4444", zorder=5)
    ax.set_xlabel("Light Level (%)")
    ax.set_ylabel("Collector Current (mA)")
    ax.set_title("Phototransistor Response (conceptual)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_ujt_calc(key_prefix):
    st.markdown("**⚙️ UJT Relaxation Oscillator Frequency Calculator**")
    st.caption("Classic formula: f = 1 / (R × C × ln(1 / (1 − η)))")
    c1, c2, c3 = st.columns(3)
    r_kohm = c1.number_input("Timing Resistor R (kΩ)", min_value=0.1, value=47.0, step=1.0, key=f"{key_prefix}_ujt_r")
    c_uf = c2.number_input("Timing Capacitor C (µF)", min_value=0.001, value=0.1, step=0.01, key=f"{key_prefix}_ujt_c")
    eta = c3.slider("Intrinsic Standoff Ratio (η)", 0.3, 0.9, 0.6, step=0.01, key=f"{key_prefix}_ujt_eta")
    freq = ujt_oscillator_freq(r_kohm * 1000, c_uf, eta)
    if freq is None:
        st.warning("⚠️ Check that R, C, and η are all valid (0 < η < 1).")
    else:
        st.markdown(f'<div class="status-good">✅ Oscillation Frequency ≈ {freq:.2f} Hz &nbsp;|&nbsp; Period ≈ {1000.0/freq:.3f} ms</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        period = 1.0 / freq
        t = [x * period / 200 for x in range(400)]
        wave = [(x % period) / period for x in t]
        ax.plot(t, wave, color="#ef4444", linewidth=1.5)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Capacitor Voltage (normalised)")
        ax.set_title("Approximate Sawtooth Output")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


CALC_RENDERERS = {
    "bjt_bias": render_bjt_bias,
    "mosfet_calc": render_mosfet_calc,
    "darlington_calc": render_darlington_calc,
    "phototransistor_calc": render_phototransistor_calc,
    "ujt_calc": render_ujt_calc,
}


def render_ce_gain_sim(key_prefix):
    st.markdown("**⚙️ Common Emitter Amplifier Gain Calculator**")
    mode = st.radio("Emitter configuration:", ["Unbypassed (with Re)", "Bypassed (Re shorted for AC)"], horizontal=True, key=f"{key_prefix}_ce_mode")
    rc_kohm = st.number_input("Collector Resistor Rc (kΩ)", min_value=0.1, value=4.7, step=0.5, key=f"{key_prefix}_ce_rc")
    if mode == "Unbypassed (with Re)":
        re_kohm = st.number_input("Emitter Resistor Re (kΩ)", min_value=0.01, value=1.0, step=0.1, key=f"{key_prefix}_ce_re")
        av = ce_gain_with_re(rc_kohm, re_kohm)
        st.markdown(f'<div class="status-good">✅ Voltage Gain Av ≈ {av:.2f} (inverting)</div>', unsafe_allow_html=True)
        st.caption("An unbypassed emitter resistor trades away some gain for much better stability and linearity.")
    else:
        ic_ma = st.number_input("DC Collector Current Ic (mA)", min_value=0.01, value=1.0, step=0.1, key=f"{key_prefix}_ce_ic")
        av = ce_gain_bypassed(rc_kohm * 1000, ic_ma)
        st.markdown(f'<div class="status-good">✅ Voltage Gain Av ≈ {av:.1f} (inverting)</div>', unsafe_allow_html=True)
        st.caption("Bypassing the emitter resistor (with a capacitor) maximises AC gain, using the transistor's transconductance (gm).")


def render_follower_gain_sim(key_prefix):
    st.markdown("**⚙️ Emitter / Source Follower Gain Calculator**")
    re_ohm = st.number_input("Emitter/Source Resistance (Ω)", min_value=1.0, value=1000.0, step=100.0, key=f"{key_prefix}_ef_re")
    r_source_ohm = st.number_input("Internal/Source Resistance (Ω)", min_value=0.0, value=50.0, step=10.0, key=f"{key_prefix}_ef_rs")
    av = emitter_follower_gain(re_ohm, r_source_ohm)
    st.markdown(f'<div class="status-good">✅ Voltage Gain Av ≈ {av:.4f} (non-inverting, close to but always less than 1)</div>', unsafe_allow_html=True)
    st.caption("A follower's real value is impedance transformation, not voltage gain — it lets a weak source drive a low-impedance load.")


def render_class_efficiency_sim(key_prefix):
    st.markdown("**⚙️ Amplifier Class Efficiency Comparison**")
    st.caption("Typical theoretical maximum efficiencies for each amplifier class.")
    classes = ["Class A", "Class B", "Class AB", "Class C"]
    efficiencies = [30, 78.5, 60, 85]
    fig, ax = plt.subplots(figsize=(5, 3))
    colors = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"]
    ax.bar(classes, efficiencies, color=colors)
    ax.set_ylabel("Typical Max Efficiency (%)")
    ax.set_title("Amplifier Class Efficiency Comparison")
    ax.set_ylim(0, 100)
    for i, v in enumerate(efficiencies):
        ax.text(i, v + 2, f"{v}%", ha="center", fontweight="bold")
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Higher efficiency generally trades off against signal fidelity (distortion) — Class A sounds best but wastes the most power as heat; Class C is extremely efficient but only usable with a tuned RF load.")


EXTRA_SIMULATORS = {
    "Common Emitter Amplifier Gain": render_ce_gain_sim,
    "Emitter/Source Follower Gain": render_follower_gain_sim,
    "Amplifier Class Efficiency Comparison": render_class_efficiency_sim,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. What controls the current flow in a BJT?", "options": ["Gate voltage", "Base current", "Light level"], "answer": "Base current"},
    {"q": "2. What controls the current flow in a MOSFET?", "options": ["Base current", "Gate-Source voltage", "Emitter resistance"], "answer": "Gate-Source voltage"},
    {"q": "3. In which region does a transistor act as a fully closed switch (ON)?", "options": ["Cutoff", "Saturation", "Active (linear)"], "answer": "Saturation"},
    {"q": "4. In which region does a transistor act as a fully open switch (OFF)?", "options": ["Cutoff", "Saturation", "Active (linear)"], "answer": "Cutoff"},
    {"q": "5. Which amplifier configuration provides the highest voltage AND current gain, but inverts the signal?", "options": ["Common Base", "Common Collector", "Common Emitter"], "answer": "Common Emitter"},
    {"q": "6. What is the main real-world use of an Emitter Follower (Common Collector) stage?", "options": ["Maximum voltage gain", "Impedance buffering, not voltage gain", "Generating oscillations"], "answer": "Impedance buffering, not voltage gain"},
    {"q": "7. Why is a Darlington pair useful?", "options": ["It reduces current gain", "It multiplies the current gain of two transistors together", "It only works with light"], "answer": "It multiplies the current gain of two transistors together"},
    {"q": "8. Which amplifier class offers the lowest distortion but the lowest efficiency?", "options": ["Class A", "Class B", "Class C"], "answer": "Class A"},
    {"q": "9. Why must a MOSFET's gate never be left floating (unconnected)?", "options": ["It can pick up stray static charge and switch on unpredictably", "It will always stay off safely", "It has no effect either way"], "answer": "It can pick up stray static charge and switch on unpredictably"},
    {"q": "10. What is unique about a UJT compared to a BJT or FET?", "options": ["It amplifies signals with very high gain", "It acts as a voltage-triggered switch rather than a linear amplifier", "It only works with AC power"], "answer": "It acts as a voltage-triggered switch rather than a linear amplifier"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A BJT amplifier stage is built, but the output signal is badly clipped (flattened) on one side.",
        "question": "What is the most likely cause?",
        "options": ["The DC bias point is set too close to cutoff or saturation, not centred in the active region", "The resistors are the wrong colour", "The signal frequency is too low"],
        "answer": "The DC bias point is set too close to cutoff or saturation, not centred in the active region",
        "explanation": "For an undistorted amplified output, the transistor's quiescent (resting) operating point needs to sit roughly in the middle of the active region — too close to either extreme causes clipping on that side of the waveform.",
    },
    {
        "scenario": "A transistor is connected directly from a microcontroller pin to a motor's positive supply, with no base resistor.",
        "question": "What is the likely outcome?",
        "options": ["The transistor and/or microcontroller pin can be damaged by excessive base current", "This is standard, completely safe practice", "The motor will simply run more efficiently"],
        "answer": "The transistor and/or microcontroller pin can be damaged by excessive base current",
        "explanation": "Without a base resistor to limit current, the low-resistance base-emitter junction can draw far more current than the microcontroller pin or transistor base is rated for.",
    },
    {
        "scenario": "A student wires a PNP transistor into a circuit using the exact same bias arrangement as an NPN transistor, and it doesn't turn on.",
        "question": "What is the most likely issue?",
        "options": ["PNP transistors need reversed polarities compared to NPN — current must flow OUT of the base to turn it on", "The transistor is definitely faulty", "PNP transistors don't actually exist"],
        "answer": "PNP transistors need reversed polarities compared to NPN — current must flow OUT of the base to turn it on",
        "explanation": "NPN and PNP transistors are mirror images of each other — biasing circuitry designed for one will not correctly turn on the other.",
    },
    {
        "scenario": "A Darlington pair is used to drive a relay, but the relay never fully turns off — a small current still flows even when the input is at 0V.",
        "question": "What is a well-known fix for this issue?",
        "options": ["Add a pull-down resistor from the base to ground to ensure a firm OFF state", "Add another Darlington stage", "Increase the supply voltage"],
        "answer": "Add a pull-down resistor from the base to ground to ensure a firm OFF state",
        "explanation": "Darlington pairs have very high gain, which can make them sensitive to tiny leakage currents holding them slightly on — a base pull-down resistor gives leakage current somewhere to go besides the base.",
    },
    {
        "scenario": "An RF power amplifier using a Class C stage sounds terrible when someone tries to use it for a hi-fi audio amplifier instead.",
        "question": "What is the fundamental issue?",
        "options": ["Class C amplifiers rely on a narrow-band tuned circuit and introduce heavy distortion — unsuitable for wideband audio", "Class C amplifiers are simply broken by design", "The speaker is the wrong impedance"],
        "answer": "Class C amplifiers rely on a narrow-band tuned circuit and introduce heavy distortion — unsuitable for wideband audio", 
        "explanation": "Class C amplifiers only conduct for a small slice of each cycle and depend on a resonant tank circuit tuned to a single frequency to reconstruct the waveform — completely unsuitable for the wide, varying frequency range of audio.",
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
st.sidebar.title("🔀 TRANSISTORS &")
st.sidebar.subheader("AMPLIFIERS LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore transistor types\n"
    "3. Study amplifier configurations\n"
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
        "🔎 Transistor Types Explorer",
        "📶 Amplifier Configurations & Classes",
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
st.title("🔀 Transistors & Amplifiers Learning Lab")
st.caption("An Interactive Beginner's Guide to Transistors & Amplifier Circuits")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Transistor Types Covered", len(TRANSISTOR_TYPES))
d2.metric("📶 Amplifier Topics", len(AMPLIFIER_CONFIGS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Transistors & Amplifiers")

    st.markdown(
        """
        ### What is a Transistor?
        A **transistor** is a semiconductor device that can either AMPLIFY a signal
        (make it bigger) or SWITCH it (turn it fully on or off) — using a small
        control input (current or voltage) to govern a much larger output. It is,
        without exaggeration, the single most important invention in modern
        electronics: every processor, memory chip, and amplifier is built from
        millions (or billions) of transistors.

        There are two broad transistor families, and this module covers examples
        of both.
        """
    )

    st.subheader("🔀 Two Transistor Families")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>⚡ BJT — Bipolar Junction Transistor</h4>'
            '<p><b>Current-controlled:</b> a small current into the Base controls a much '
            'larger current from Collector to Emitter. Think of it as a current amplifier.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>🔋 FET — Field-Effect Transistor</h4>'
            '<p><b>Voltage-controlled:</b> a voltage on an (almost current-free) Gate controls '
            'current between Drain and Source. Think of it as a voltage-controlled valve.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("📶 Amplification vs. Switching")
    st.markdown(
        '<div class="app-card">The SAME transistor can be used two very different ways: '
        'biased in its linear ("active") region, it can AMPLIFY a small signal into a larger '
        'one with the same shape. Driven hard between fully OFF ("cutoff") and fully ON '
        '("saturation"), it acts as an electronic SWITCH — the basis of every digital logic gate.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Head to **'Transistor Types Explorer'** in the sidebar to study each transistor type in detail.")

# ============================================================================
# 2. TRANSISTOR TYPES EXPLORER
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Transistor Types Explorer")
    st.caption("Expand each transistor type to see its symbol, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in TRANSISTOR_ORDER:
        c = TRANSISTOR_TYPES[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_transistor_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Terminals:** {c['terminals']}")
                st.markdown(f"**Control:** {c['control']}")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")
                if c["safety"]:
                    st.markdown(f'<div class="safety-note">⚠️ {c["safety"]}</div>', unsafe_allow_html=True)

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. AMPLIFIER CONFIGURATIONS & CLASSES
# ============================================================================
elif page.startswith("📶"):
    st.header("📶 Amplifier Configurations & Classes")
    st.caption("The key circuit topologies and operating classes used to build transistor amplifiers.")

    filter_tags = st.multiselect(
        "Filter transistor types by category",
        ["bjt", "fet", "hybrid", "amplifying", "switching", "power", "optical", "sensing", "special_purpose", "oscillator"],
        default=[],
    )
    if filter_tags:
        filtered = [n for n in TRANSISTOR_ORDER if any(t in TRANSISTOR_TYPES[n]["category"] for t in filter_tags)]
    else:
        filtered = TRANSISTOR_ORDER

    st.subheader("🧮 Transistor Type Reference Table")
    rows = []
    for name in filtered:
        c = TRANSISTOR_TYPES[name]
        rows.append({
            "Transistor Type": name,
            "Terminals": c["terminals"],
            "Control": c["control"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Key Amplifier Configurations & Classes")
    for cfg_name in AMPLIFIER_ORDER:
        cfg = AMPLIFIER_CONFIGS[cfg_name]
        with st.expander(f"**{cfg_name}**"):
            st.markdown(f"**Key facts:** {cfg['formula']}")
            st.markdown(f"**Explanation:** {cfg['explanation']}")
            st.markdown(f"**Used for:** {cfg['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any transistor type or amplifier topic and experiment with its behaviour.")

    simulatable_transistors = [n for n in TRANSISTOR_ORDER if TRANSISTOR_TYPES[n]["calc_key"] is not None]
    options = simulatable_transistors + list(EXTRA_SIMULATORS.keys())
    sel = st.selectbox("Select a transistor type or amplifier topic", options)

    if sel in EXTRA_SIMULATORS:
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #7c3aed, #4c1d95);">'
                 f'📶 <b>{sel}</b></div>'),
            unsafe_allow_html=True,
        )
        EXTRA_SIMULATORS[sel](key_prefix=f"sim_{sel}")
    else:
        c = TRANSISTOR_TYPES[sel]
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #0891b2, #164e63);">'
                 f'🔀 <b>{sel}</b> &nbsp;|&nbsp; {c["desc"]}</div>'),
            unsafe_allow_html=True,
        )
        col_symbol, col_calc = st.columns([1, 1.6])
        with col_symbol:
            st.markdown("##### 🔷 Symbol")
            st.markdown(f'<div class="symbol-box">{draw_transistor_svg(sel)}</div>', unsafe_allow_html=True)
            st.markdown(f"**Terminals:** {c['terminals']}")
        with col_calc:
            CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how transistors and amplifiers power real electronic systems.")

    APPLICATIONS = [
        ("🎵 Audio Amplifiers", "Class AB power amplifier stages drive loudspeakers with a good balance of sound quality and efficiency; small-signal BJT/FET stages provide preamp gain and tone shaping."),
        ("⚙️ Motor & Power Switching", "MOSFETs and IGBTs switch high currents to motors and heaters using PWM (Pulse Width Modulation), controlled by a low-power microcontroller signal through a gate driver."),
        ("📡 Radio Frequency (RF) Amplifiers", "Common Base/Common Gate stages and Class C amplifiers boost weak radio signals or drive transmitter power stages at specific tuned frequencies."),
        ("💻 Digital Logic & Processors", "Billions of MOSFETs, switched fully ON or fully OFF, form the logic gates inside every microprocessor and memory chip — the switching (not amplifying) use of a transistor."),
        ("🔌 Voltage Regulators", "Linear voltage regulator ICs use a BJT or MOSFET as a variable 'series pass' element, continuously adjusted to hold a steady output voltage."),
        ("👁️ Sensor Interfacing", "Phototransistors and optocouplers convert light signals into electrical ones for object detection, IR remote receivers, and electrically isolating two parts of a circuit."),
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
    st.header("📝 Transistors & Amplifiers Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Transistor Types Explorer' section and try again!")

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
