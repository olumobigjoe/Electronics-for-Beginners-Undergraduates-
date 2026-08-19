"""
🔺 Diodes & Rectifiers Learning Lab
An Interactive Beginner's Guide to Diodes & Rectifier Circuits

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
    page_title="Diodes & Rectifiers Learning Lab",
    page_icon="🔺",
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
        background: linear-gradient(135deg, #7c2d12, #78350f);
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
# CORE DIODE / RECTIFIER CALCULATIONS (pure functions, no widgets)
# ============================================================================

def diode_current_ma(v, i_sat_na=1e-5, n=1.0):
    """Simplified Shockley diode equation, returns current in mA.
    i_sat given in nanoamps for realistic-looking curves at low voltage."""
    vt = 0.02585  # thermal voltage at room temperature (~25 mV)
    i_sat_a = i_sat_na * 1e-9
    v_clamped = max(min(v, 0.9), -5.0)  # keep the exponential well-behaved
    i_a = i_sat_a * (math.exp(v_clamped / (n * vt)) - 1)
    return i_a * 1000.0


def zener_regulator(vin, vz, r_series, r_load):
    """Simple series-resistor Zener shunt regulator analysis.
    Returns (i_total, i_load, i_zener, regulating)."""
    if r_series <= 0:
        return None, None, None, False
    i_total = (vin - vz) / r_series
    i_load = (vz / r_load) if r_load > 0 else 0.0
    i_zener = i_total - i_load
    regulating = i_zener > 0 and vin > vz
    return i_total, i_load, i_zener, regulating


def led_current_ma(vs, vf, r_ohm):
    """I = (Vs - Vf) / R, returned in milliamps. None if invalid."""
    if r_ohm in (None, 0):
        return None
    drop = vs - vf
    if drop <= 0:
        return 0.0
    return (drop / r_ohm) * 1000.0


def photodiode_current_ua(light_pct, responsivity=0.5):
    """Simplified, illustrative model: reverse photocurrent roughly
    proportional to light level. Returns microamps."""
    return light_pct * 2.0 * responsivity


def varactor_capacitance_pf(vr, c0_pf=100.0, vj=0.7, m=0.5):
    """Simplified junction capacitance model: C(V) = C0 / (1 + Vr/Vj)^m."""
    if vr < 0:
        vr = 0
    return c0_pf / ((1 + vr / vj) ** m)


def bridge_output_with_drop(vm, vf=0.7, diode_count=2):
    """Peak output after subtracting forward drops of conducting diodes."""
    return max(vm - diode_count * vf, 0)


def half_wave_output(vm):
    """Returns (Vdc, Vrms, ripple_factor, PIV) for an unfiltered half-wave rectifier."""
    vdc = vm / math.pi
    vrms = vm / 2.0
    ripple = 1.21
    piv = vm
    return vdc, vrms, ripple, piv


def full_wave_output(vm, config="bridge"):
    """Returns (Vdc, Vrms, ripple_factor, PIV) for an unfiltered full-wave rectifier.
    config: 'bridge' or 'center_tap' — PIV differs between the two."""
    vdc = 2 * vm / math.pi
    vrms = vm / math.sqrt(2)
    ripple = 0.482
    piv = vm if config == "bridge" else 2 * vm
    return vdc, vrms, ripple, piv


def ripple_voltage_pp(idc_a, freq_hz, cap_uf, full_wave=True):
    """Approximate peak-to-peak ripple voltage with a reservoir capacitor filter."""
    c_f = cap_uf * 1e-6
    factor = 2.0 if full_wave else 1.0
    if c_f <= 0 or freq_hz <= 0:
        return None
    return idc_a / (factor * freq_hz * c_f)


def clipper_output(vin, clip_level, direction="positive"):
    """Ideal diode clipper: clamps the signal at clip_level in one direction."""
    if direction == "positive":
        return min(vin, clip_level)
    return max(vin, clip_level)


def clamper_output_range(vm, clamp_type="positive"):
    """Ideal diode clamper (DC restorer): shifts the whole waveform so one
    extreme sits at 0V. Returns (new_min, new_max)."""
    if clamp_type == "positive":
        return 0.0, 2 * vm
    return -2 * vm, 0.0


# ============================================================================
# DIODE TYPES DATA
# 10 diode types, each with the fields the Explorer page needs.
# "calc_key" links a diode to its interactive render function further down.
# ============================================================================
DIODE_TYPES = {
    "PN Junction Diode": {
        "desc": "The basic general-purpose diode: allows current to flow easily in one direction only.",
        "forward_v": "≈ 0.6–0.7 V (silicon)",
        "connection": "Anode (+) to Cathode (−); current flows anode → cathode when forward biased.",
        "category": ["general_purpose", "rectifying"],
        "explanation": "At the junction between P-type and N-type semiconductor material, a 'depletion region' forms that blocks current — until forward bias voltage overcomes it, at which point current flows freely.",
        "applications": "General rectification, signal steering, reverse-polarity protection.",
        "safety": "Exceeding a diode's reverse voltage (breakdown) or forward current rating can permanently damage it.",
        "calc_key": "diode_bias",
    },
    "Zener Diode": {
        "desc": "A diode specially designed to operate safely in reverse breakdown, holding a constant voltage.",
        "forward_v": "≈ 0.6–0.7 V forward; breakdown voltage (Vz) set by design, e.g. 3.3V–100V+",
        "connection": "Used in REVERSE bias, deliberately operated in its breakdown region.",
        "category": ["regulation"],
        "explanation": "While a normal diode is never meant to enter reverse breakdown, a Zener diode is built to do exactly that safely — once in breakdown, its voltage stays remarkably constant even as current through it varies, making it ideal for voltage regulation.",
        "applications": "Simple voltage regulators, voltage reference circuits, overvoltage protection (clamping).",
        "safety": "A Zener diode always needs a series resistor to limit current — without one, it will draw excessive current and be destroyed.",
        "calc_key": "zener_reg",
    },
    "Schottky Diode": {
        "desc": "A fast-switching, low forward-voltage-drop diode formed from a metal-semiconductor junction rather than a PN junction.",
        "forward_v": "≈ 0.15–0.45 V (much lower than silicon PN diodes)",
        "connection": "Anode (+) to Cathode (−), same as a standard diode.",
        "category": ["general_purpose", "rectifying", "fast_switching"],
        "explanation": "Because it uses a metal-semiconductor junction instead of a PN junction, a Schottky diode has a much lower forward voltage drop and switches on/off far faster — at the cost of higher reverse leakage current.",
        "applications": "High-efficiency power supply rectification, RF detectors, reverse-polarity protection where low voltage drop matters.",
        "safety": "Generally has a lower maximum reverse voltage rating than standard PN diodes — check datasheet limits carefully.",
        "calc_key": None,
    },
    "LED": {
        "desc": "Light Emitting Diode — converts electrical energy directly into light when forward biased.",
        "forward_v": "≈ 1.8–3.3 V depending on colour",
        "connection": "Anode (+, longer leg) to Cathode (−, shorter leg / flat edge).",
        "category": ["optical"],
        "explanation": "As current flows through the LED's junction, electrons and holes recombine and release energy as photons (light) — the exact colour depends on the semiconductor material used.",
        "applications": "Indicator lights, displays, general lighting, optical communication.",
        "safety": "Always use a current-limiting resistor with an LED. Never connect an LED directly across a battery.",
        "calc_key": "led_calc",
    },
    "Photodiode": {
        "desc": "A diode that generates or modulates a current in response to light falling on its junction.",
        "forward_v": "N/A — typically operated reverse biased",
        "connection": "Operated in REVERSE bias; more light striking the junction increases reverse (photo)current.",
        "category": ["optical", "sensing"],
        "explanation": "A photodiode works almost opposite to an LED — instead of converting current into light, it converts incoming light into a small measurable current, with more light producing more current.",
        "applications": "Light meters, optical receivers (fibre optic communication), solar cells (a related device), camera light sensors.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "photodiode_calc",
    },
    "Varactor (Varicap) Diode": {
        "desc": "A diode whose junction capacitance changes with the reverse voltage applied across it.",
        "forward_v": "N/A — operated reverse biased only",
        "connection": "Operated in REVERSE bias; capacitance decreases as reverse voltage increases.",
        "category": ["reactive", "tuning"],
        "explanation": "Every reverse-biased diode has some junction capacitance, but a varactor diode is specially designed to make this effect large and predictable, letting a DC voltage electronically 'tune' a capacitance value.",
        "applications": "Electronic tuning in radios and TVs, voltage-controlled oscillators (VCOs), frequency synthesizers.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "varactor_calc",
    },
    "Tunnel Diode": {
        "desc": "A heavily-doped diode exhibiting 'negative resistance' over part of its forward operating range.",
        "forward_v": "Very low turn-on, with a distinctive current PEAK followed by a DROP as voltage increases further",
        "connection": "Anode (+) to Cathode (−), same as a standard diode, but used in a very specific bias region.",
        "category": ["special_purpose"],
        "explanation": "Unlike a normal diode where more forward voltage always means more current, a tunnel diode has a region where INCREASING voltage causes DECREASING current — this unusual 'negative resistance' region makes it useful for oscillators and fast switching.",
        "applications": "High-frequency oscillators, fast switching circuits, microwave amplifiers.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": None,
    },
    "PIN Diode": {
        "desc": "A diode with an added lightly-doped 'Intrinsic' layer between the P and N regions, useful as a variable RF resistor.",
        "forward_v": "Similar to a standard PN diode; behaviour depends heavily on frequency and bias current",
        "connection": "Anode (+) to Cathode (−); the middle 'i' (intrinsic) layer is not a separate terminal.",
        "category": ["special_purpose", "rf"],
        "explanation": "At radio frequencies, a PIN diode's DC bias current controls its effective RF resistance — making it act like a voltage-controlled RF switch or variable attenuator, rather than a simple rectifier.",
        "applications": "RF switches, attenuators, photodetectors in fibre optics (a variant), X-ray/nuclear radiation detectors.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": None,
    },
    "Laser Diode": {
        "desc": "A diode that emits coherent, focused laser light rather than the diffuse light of an LED, once driven above a threshold current.",
        "forward_v": "≈ 1.5–2.5 V depending on type, with a distinct threshold current for lasing to begin",
        "connection": "Anode (+) to Cathode (−), similar to an LED, but typically needs careful current-limited driving.",
        "category": ["optical"],
        "explanation": "Below a threshold current, a laser diode behaves much like an LED (incoherent light). Above threshold, the device enters 'lasing' — producing a narrow, coherent, highly-focused beam of light.",
        "applications": "Optical fibre communication, barcode scanners, laser pointers, optical storage (CD/DVD/Blu-ray readers).",
        "safety": "⚠️ Even low-power laser diodes can cause eye damage. Never look directly into a laser diode's beam or its reflections.",
        "calc_key": None,
    },
    "Bridge Rectifier": {
        "desc": "A pre-packaged assembly of four diodes arranged to convert AC into pulsating DC, using both halves of the AC waveform.",
        "forward_v": "≈ 1.2–1.4 V total drop (two diodes conduct in series at any instant)",
        "connection": "Two AC input terminals (~) and two DC output terminals (+ and −).",
        "category": ["rectifying"],
        "explanation": "Four diodes are arranged so that for either half of the AC cycle, current is always steered through the load in the same direction — giving a full-wave rectified output from a single two-wire AC source, without needing a centre-tapped transformer.",
        "applications": "AC-to-DC power supply rectification — by far the most common rectifier configuration in modern electronics.",
        "safety": "⚠️ Rated for a maximum reverse voltage (PIV) and forward current — exceeding either can destroy the diodes inside the package.",
        "calc_key": "bridge_calc",
    },
}

DIODE_ORDER = list(DIODE_TYPES.keys())

# ============================================================================
# RECTIFIER & WAVE-SHAPING CIRCUITS DATA (used on the Rectifier Circuits page)
# ============================================================================
RECTIFIER_CIRCUITS = {
    "Half-Wave Rectifier": {
        "formula": "Vdc = Vm / π   |   Vrms = Vm / 2   |   Ripple factor ≈ 1.21   |   PIV = Vm",
        "explanation": "Uses a single diode to pass only one half of the AC waveform, blocking the other half entirely. Simple, but wastes half the input power and has a high ripple factor.",
        "use": "Simple, low-cost, low-power applications where efficiency and smoothness aren't critical.",
    },
    "Full-Wave Rectifier (Centre-Tap)": {
        "formula": "Vdc = 2Vm / π   |   Vrms = Vm / √2   |   Ripple factor ≈ 0.482   |   PIV = 2Vm",
        "explanation": "Uses two diodes and a centre-tapped transformer secondary so that both halves of the AC waveform contribute to the output — but each diode must withstand double the peak voltage.",
        "use": "Full-wave rectification when a centre-tapped transformer is available; historically common before bridge rectifiers became cheap.",
    },
    "Full-Wave Bridge Rectifier": {
        "formula": "Vdc = 2Vm / π   |   Vrms = Vm / √2   |   Ripple factor ≈ 0.482   |   PIV = Vm",
        "explanation": "Uses four diodes arranged in a bridge to achieve full-wave rectification WITHOUT needing a centre-tapped transformer, and each diode only needs to withstand the peak voltage (not double).",
        "use": "The standard choice in almost all modern AC-to-DC power supplies.",
    },
    "Clipper Circuit": {
        "formula": "Output = min(Vin, Vclip)  or  max(Vin, Vclip), depending on diode orientation",
        "explanation": "Uses a diode (often with a reference voltage) to 'cut off' or clip part of a waveform above or below a chosen level, protecting downstream circuitry or shaping a signal.",
        "use": "Waveform shaping, protecting sensitive circuit inputs from overvoltage spikes.",
    },
    "Clamper Circuit": {
        "formula": "Shifts the entire waveform up or down so one extreme sits at ≈ 0V (a diode + capacitor 'DC restorer')",
        "explanation": "Unlike a clipper (which removes part of a signal), a clamper preserves the full waveform SHAPE but shifts its DC level — useful when you need to guarantee a signal never goes negative (or never goes positive).",
        "use": "TV/video signal 'DC restoration', ensuring a signal stays within a required voltage range without distorting its shape.",
    },
}

RECTIFIER_ORDER = list(RECTIFIER_CIRCUITS.keys())

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each diode type. Every returned
# string is flattened to one line with flat() so Streamlit's Markdown
# renderer never mis-parses an embedded blank line as the end of the block.
# ============================================================================
DIODE_COLORS = {
    "PN Junction Diode": "#3b82f6",
    "Zener Diode": "#8b5cf6",
    "Schottky Diode": "#f59e0b",
    "LED": "#eab308",
    "Photodiode": "#22c55e",
    "Varactor (Varicap) Diode": "#06b6d4",
    "Tunnel Diode": "#ef4444",
    "PIN Diode": "#a855f7",
    "Laser Diode": "#ec4899",
    "Bridge Rectifier": "#0ea5e9",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def _basic_diode_body(color, cathode_extra=""):
    """Standard triangle + bar diode body used as a base for several symbols."""
    return f"""
    <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
    <line x1="130" y1="35" x2="130" y2="105" stroke="{color}" stroke-width="6"/>
    {cathode_extra}
    """


def draw_diode_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the diode type."""
    color = DIODE_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "PN Junction Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        {_basic_diode_body(color)}
        {_lead(130, 70, 220, 70)}
        """

    elif name == "Zener Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <path d="M120,35 L130,35 L130,105 L140,105" fill="none" stroke="{color}" stroke-width="6" stroke-linejoin="round"/>
        {_lead(140, 105, 220, 70)}
        """

    elif name == "Schottky Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <path d="M120,35 L120,45 L130,45 L130,95 L140,95 L140,105" fill="none" stroke="{color}" stroke-width="5" stroke-linejoin="round"/>
        {_lead(140, 105, 220, 105)}
        {_lead(140, 105, 220, 35)}
        """

    elif name == "LED":
        body = f"""
        {_lead(0, 70, 60, 70)}
        {_basic_diode_body(color)}
        {_lead(130, 70, 220, 70)}
        <line x1="95" y1="25" x2="115" y2="5" stroke="{color}" stroke-width="3"/>
        <polygon points="115,5 106,7 113,14" fill="{color}"/>
        <line x1="115" y1="35" x2="135" y2="15" stroke="{color}" stroke-width="3"/>
        <polygon points="135,15 126,17 133,24" fill="{color}"/>
        """

    elif name == "Photodiode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        {_basic_diode_body(color)}
        {_lead(130, 70, 220, 70)}
        <line x1="115" y1="5" x2="95" y2="25" stroke="{color}" stroke-width="3"/>
        <polygon points="95,25 104,23 97,16" fill="{color}"/>
        <line x1="135" y1="15" x2="115" y2="35" stroke="{color}" stroke-width="3"/>
        <polygon points="115,35 124,33 117,26" fill="{color}"/>
        """

    elif name == "Varactor (Varicap) Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <line x1="130" y1="35" x2="130" y2="105" stroke="{color}" stroke-width="6"/>
        <line x1="140" y1="35" x2="140" y2="105" stroke="{color}" stroke-width="6"/>
        {_lead(140, 70, 220, 70)}
        """

    elif name == "Tunnel Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <line x1="128" y1="35" x2="128" y2="105" stroke="{color}" stroke-width="4"/>
        <line x1="136" y1="35" x2="136" y2="105" stroke="{color}" stroke-width="4"/>
        {_lead(136, 70, 220, 70)}
        """

    elif name == "PIN Diode":
        body = f"""
        {_lead(0, 70, 55, 70)}
        <path d="M55,35 L55,105 L85,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <rect x="85" y="55" width="30" height="30" fill="{color}11" stroke="{color}" stroke-width="2" stroke-dasharray="3,3"/>
        <text x="93" y="76" font-size="14" font-weight="bold" fill="{color}">i</text>
        <line x1="115" y1="35" x2="115" y2="105" stroke="{color}" stroke-width="6"/>
        {_lead(115, 70, 220, 70)}
        """

    elif name == "Laser Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        {_basic_diode_body(color)}
        {_lead(130, 70, 220, 70)}
        <rect x="140" y="55" width="20" height="30" fill="none" stroke="{color}" stroke-width="2"/>
        <line x1="160" y1="62" x2="200" y2="55" stroke="{color}" stroke-width="2.5"/>
        <line x1="160" y1="70" x2="205" y2="70" stroke="{color}" stroke-width="2.5"/>
        <line x1="160" y1="78" x2="200" y2="85" stroke="{color}" stroke-width="2.5"/>
        """

    elif name == "Bridge Rectifier":
        # Four diodes arranged in a diamond, AC in on left/right, DC out top/bottom
        d = color
        body = f"""
        <text x="2" y="35" font-size="13" font-weight="bold" fill="#111827">~</text>
        {_lead(15, 40, 55, 70, d, 3)}
        <text x="195" y="35" font-size="13" font-weight="bold" fill="#111827">~</text>
        {_lead(165, 70, 205, 40, d, 3)}
        {_lead(15, 100, 55, 70, d, 3)}
        {_lead(165, 70, 205, 100, d, 3)}
        <path d="M55,70 L75,55 L75,85 Z" fill="{d}22" stroke="{d}" stroke-width="3" stroke-linejoin="round"/>
        <line x1="75" y1="55" x2="75" y2="85" stroke="{d}" stroke-width="4"/>
        {_lead(75, 70, 110, 40, d, 3)}
        <path d="M145,70 L125,55 L125,85 Z" fill="{d}22" stroke="{d}" stroke-width="3" stroke-linejoin="round"/>
        <line x1="125" y1="55" x2="125" y2="85" stroke="{d}" stroke-width="4"/>
        {_lead(110, 40, 125, 70, d, 3)}
        {_lead(110, 40, 145, 70, d, 3)}
        <text x="103" y="20" font-size="16" font-weight="bold" fill="#111827">+</text>
        {_lead(110, 40, 110, 15, "#111827", 3)}
        <path d="M75,85 L95,100 L95,130 Z" fill="{d}22" stroke="{d}" stroke-width="3" stroke-linejoin="round"/>
        <line x1="95" y1="100" x2="95" y2="130" stroke="{d}" stroke-width="4"/>
        <path d="M145,85 L125,100 L125,130 Z" fill="{d}22" stroke="{d}" stroke-width="3" stroke-linejoin="round"/>
        <line x1="125" y1="100" x2="125" y2="130" stroke="{d}" stroke-width="4"/>
        {_lead(110, 100, 110, 130, "#111827", 3)}
        <text x="103" y="132" font-size="16" font-weight="bold" fill="#111827">−</text>
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same item is rendered on more than one page.
# ============================================================================

def render_diode_bias(key_prefix):
    st.markdown("**⚙️ Diode I-V Characteristic & Bias Simulator**")
    v = st.slider("Applied Voltage (V)", -2.0, 0.9, 0.5, step=0.05, key=f"{key_prefix}_diode_v")
    i_ma = diode_current_ma(v)
    state = "CONDUCTING (forward biased)" if v > 0.6 else ("Reverse biased — blocking" if v < 0 else "Near turn-on threshold")
    if v > 0.6:
        st.markdown(f'<div class="status-good">✅ {state} — Current ≈ {i_ma:.3f} mA</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-bad">⛔ {state} — Current ≈ {i_ma:.6f} mA</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    vs = [x * 0.02 - 2.0 for x in range(146)]
    curr = [diode_current_ma(x) for x in vs]
    ax.plot(vs, curr, color="#3b82f6", linewidth=2)
    ax.scatter([v], [i_ma], color="#ef4444", zorder=5)
    ax.axhline(0, color="#9ca3af", linewidth=0.8)
    ax.axvline(0, color="#9ca3af", linewidth=0.8)
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (mA)")
    ax.set_title("Diode I-V Characteristic (simplified)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_zener_reg(key_prefix):
    st.markdown("**⚙️ Zener Voltage Regulator Simulator**")
    c1, c2 = st.columns(2)
    vin = c1.number_input("Input Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_z_vin")
    vz = c1.number_input("Zener Voltage (V)", min_value=0.1, value=5.6, step=0.1, key=f"{key_prefix}_z_vz")
    r_series = c2.number_input("Series Resistor (Ω)", min_value=1.0, value=220.0, step=10.0, key=f"{key_prefix}_z_rs")
    r_load = c2.number_input("Load Resistance (Ω)", min_value=1.0, value=1000.0, step=100.0, key=f"{key_prefix}_z_rl")
    i_total, i_load, i_zener, regulating = zener_regulator(vin, vz, r_series, r_load)
    if i_total is None:
        st.warning("⚠️ Series resistor must be greater than 0.")
    elif regulating:
        st.markdown(f'<div class="status-good">✅ Regulating! Output ≈ {vz:.2f} V. Total current = {i_total*1000:.1f} mA, Load current = {i_load*1000:.1f} mA, Zener current = {i_zener*1000:.1f} mA</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-bad">⛔ NOT regulating — either Vin is too low, or the load is drawing more current than the series resistor can supply. Output will sag below Vz.</div>', unsafe_allow_html=True)
    st.caption("For proper regulation, the Zener must always carry some current (Izener > 0) — try lowering Vin or the series resistor to see regulation fail.")


def render_led_calc(key_prefix):
    st.markdown("**⚙️ LED Circuit Calculator** — `I = (Vs − Vf) / R`")
    c1, c2, c3 = st.columns(3)
    vs = c1.number_input("Supply Voltage (V)", min_value=0.0, value=9.0, step=0.5, key=f"{key_prefix}_led_vs")
    vf = c2.number_input("LED Forward Voltage (V)", min_value=0.0, value=2.0, step=0.1, key=f"{key_prefix}_led_vf")
    r = c3.number_input("Resistor (Ω)", min_value=0.0, value=470.0, step=10.0, key=f"{key_prefix}_led_r")
    current_ma = led_current_ma(vs, vf, r)
    if current_ma is None:
        st.warning("⚠️ Resistor value must be greater than 0 to protect the LED.")
    elif current_ma <= 0:
        st.markdown('<div class="status-bad">⛔ Supply voltage is too low — LED will NOT light.</div>', unsafe_allow_html=True)
    elif current_ma > 30:
        st.markdown(f'<div class="status-bad">⚠️ Calculated current is {current_ma:.1f} mA — too high! Increase R to protect the LED.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-good">🟢 LED ON — Current = {current_ma:.2f} mA</div>', unsafe_allow_html=True)
    st.markdown('<div class="safety-note">⚠️ Always use a current-limiting resistor with an LED.</div>', unsafe_allow_html=True)


def render_photodiode_calc(key_prefix):
    st.markdown("**⚙️ Photodiode Light Response Simulator** (simplified educational model)")
    light = st.slider("Light level: Dark ← → Bright", 0, 100, 50, key=f"{key_prefix}_pd_light")
    responsivity = st.slider("Responsivity (A/W, illustrative)", 0.1, 1.0, 0.5, step=0.05, key=f"{key_prefix}_pd_resp")
    i_ua = photodiode_current_ua(light, responsivity)
    st.markdown(f'<div class="status-good">✅ Approximate Photocurrent ≈ {i_ua:.2f} µA</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    levels = list(range(0, 101, 5))
    curve = [photodiode_current_ua(x, responsivity) for x in levels]
    ax.plot(levels, curve, color="#22c55e", linewidth=2)
    ax.scatter([light], [i_ua], color="#ef4444", zorder=5)
    ax.set_xlabel("Light Level (%)")
    ax.set_ylabel("Photocurrent (µA)")
    ax.set_title("Photocurrent vs Light Level (conceptual)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_varactor_calc(key_prefix):
    st.markdown("**⚙️ Varactor Diode Capacitance Calculator** — `C(V) = C0 / (1 + Vr/Vj)^m`")
    c1, c2 = st.columns(2)
    vr = c1.number_input("Reverse Voltage (V)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_var_vr")
    c0 = c2.number_input("C0 — Capacitance at 0V (pF)", min_value=1.0, value=100.0, step=5.0, key=f"{key_prefix}_var_c0")
    cap = varactor_capacitance_pf(vr, c0)
    st.markdown(f'<div class="status-good">✅ Junction Capacitance ≈ {cap:.2f} pF</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    vrs = [x * 0.2 for x in range(51)]
    curve = [varactor_capacitance_pf(x, c0) for x in vrs]
    ax.plot(vrs, curve, color="#06b6d4", linewidth=2)
    ax.scatter([vr], [cap], color="#ef4444", zorder=5)
    ax.set_xlabel("Reverse Voltage (V)")
    ax.set_ylabel("Capacitance (pF)")
    ax.set_title("Varactor Capacitance vs Reverse Voltage")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_bridge_calc(key_prefix):
    st.markdown("**⚙️ Bridge Rectifier Output Calculator**")
    c1, c2 = st.columns(2)
    vm = c1.number_input("AC Peak Input Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_br_vm")
    vf = c2.number_input("Diode Forward Drop (V)", min_value=0.0, value=0.7, step=0.05, key=f"{key_prefix}_br_vf")
    peak_out = bridge_output_with_drop(vm, vf, diode_count=2)
    vdc, vrms, ripple, piv = full_wave_output(vm, config="bridge")
    st.markdown(f'<div class="status-good">✅ Peak Output (after diode drops) ≈ {peak_out:.2f} V &nbsp;|&nbsp; Ideal Vdc ≈ {vdc:.2f} V &nbsp;|&nbsp; PIV per diode = {piv:.2f} V</div>', unsafe_allow_html=True)
    st.caption("Two diodes conduct in series at any instant in a bridge rectifier, so their forward drops (≈ 1.2–1.4V total) subtract directly from the peak output.")


CALC_RENDERERS = {
    "diode_bias": render_diode_bias,
    "zener_reg": render_zener_reg,
    "led_calc": render_led_calc,
    "photodiode_calc": render_photodiode_calc,
    "varactor_calc": render_varactor_calc,
    "bridge_calc": render_bridge_calc,
}


def render_half_wave_sim(key_prefix):
    st.markdown("**⚙️ Half-Wave Rectifier Output Calculator**")
    vm = st.number_input("AC Peak Input Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_hw_vm")
    vdc, vrms, ripple, piv = half_wave_output(vm)
    st.markdown(f'<div class="status-good">✅ Vdc = {vdc:.2f} V &nbsp;|&nbsp; Vrms = {vrms:.2f} V &nbsp;|&nbsp; Ripple Factor ≈ {ripple:.2f} &nbsp;|&nbsp; PIV = {piv:.2f} V</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 3))
    t = [x * 0.01 for x in range(201)]
    wave = [max(vm * math.sin(2 * math.pi * x), 0) for x in t]
    ax.plot(t, wave, color="#f97316", linewidth=2)
    ax.axhline(vdc, color="#22c55e", linestyle="--", linewidth=1.5, label="Vdc (average)")
    ax.set_xlabel("Time (cycles)")
    ax.set_ylabel("Output Voltage (V)")
    ax.set_title("Half-Wave Rectified Output")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_full_wave_sim(key_prefix):
    st.markdown("**⚙️ Full-Wave Rectifier Output Calculator**")
    c1, c2 = st.columns(2)
    vm = c1.number_input("AC Peak Input Voltage (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_fw_vm")
    config = c2.radio("Configuration", ["Bridge", "Centre-Tap"], horizontal=True, key=f"{key_prefix}_fw_cfg")
    cfg_key = "bridge" if config == "Bridge" else "center_tap"
    vdc, vrms, ripple, piv = full_wave_output(vm, cfg_key)
    st.markdown(f'<div class="status-good">✅ Vdc = {vdc:.2f} V &nbsp;|&nbsp; Vrms = {vrms:.2f} V &nbsp;|&nbsp; Ripple Factor ≈ {ripple:.2f} &nbsp;|&nbsp; PIV = {piv:.2f} V</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 3))
    t = [x * 0.01 for x in range(201)]
    wave = [abs(vm * math.sin(2 * math.pi * x)) for x in t]
    ax.plot(t, wave, color="#3b82f6", linewidth=2)
    ax.axhline(vdc, color="#22c55e", linestyle="--", linewidth=1.5, label="Vdc (average)")
    ax.set_xlabel("Time (cycles)")
    ax.set_ylabel("Output Voltage (V)")
    ax.set_title(f"Full-Wave Rectified Output ({config})")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_ripple_sim(key_prefix):
    st.markdown("**⚙️ Ripple Voltage with Filter Capacitor**")
    c1, c2 = st.columns(2)
    idc_ma = c1.number_input("DC Load Current (mA)", min_value=0.1, value=100.0, step=10.0, key=f"{key_prefix}_rp_idc")
    freq = c1.number_input("Supply Frequency (Hz)", min_value=1.0, value=50.0, step=10.0, key=f"{key_prefix}_rp_freq")
    cap_uf = c2.number_input("Filter Capacitor (µF)", min_value=1.0, value=1000.0, step=100.0, key=f"{key_prefix}_rp_c")
    full_wave = c2.toggle("Full-wave rectified (unchecked = half-wave)", value=True, key=f"{key_prefix}_rp_fw")
    vr_pp = ripple_voltage_pp(idc_ma / 1000.0, freq, cap_uf, full_wave)
    if vr_pp is None:
        st.warning("⚠️ Check that frequency and capacitance are greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Approximate Peak-to-Peak Ripple ≈ {vr_pp*1000:.1f} mV</div>', unsafe_allow_html=True)
        st.caption("Larger capacitance (or full-wave instead of half-wave) reduces ripple — try changing either value.")


def render_clipper_sim(key_prefix):
    st.markdown("**⚙️ Diode Clipper Simulator**")
    c1, c2 = st.columns(2)
    clip_level = c1.number_input("Clip Level (V)", value=3.0, step=0.5, key=f"{key_prefix}_cl_level")
    direction = c2.radio("Clip direction", ["positive", "negative"], horizontal=True, key=f"{key_prefix}_cl_dir")
    vm = st.number_input("Input Signal Peak Amplitude (V)", min_value=0.1, value=5.0, step=0.5, key=f"{key_prefix}_cl_vm")
    fig, ax = plt.subplots(figsize=(5, 3))
    t = [x * 0.01 for x in range(201)]
    vin = [vm * math.sin(2 * math.pi * x) for x in t]
    vout = [clipper_output(v, clip_level, direction) for v in vin]
    ax.plot(t, vin, color="#9ca3af", linewidth=1.5, linestyle="--", label="Input")
    ax.plot(t, vout, color="#ec4899", linewidth=2, label="Output (clipped)")
    ax.axhline(clip_level if direction == "positive" else -clip_level, color="#f59e0b", linewidth=1, linestyle=":")
    ax.set_xlabel("Time (cycles)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Diode Clipper: Input vs Output")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_clamper_sim(key_prefix):
    st.markdown("**⚙️ Diode Clamper Simulator** (ideal, diode drop ignored)")
    c1, c2 = st.columns(2)
    vm = c1.number_input("Input Signal Peak Amplitude (V)", min_value=0.1, value=5.0, step=0.5, key=f"{key_prefix}_clmp_vm")
    clamp_type = c2.radio("Clamp direction", ["positive", "negative"], horizontal=True, key=f"{key_prefix}_clmp_type")
    new_min, new_max = clamper_output_range(vm, clamp_type)
    st.markdown(f'<div class="status-good">✅ Output range shifts to: {new_min:.2f} V to {new_max:.2f} V</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 3))
    t = [x * 0.01 for x in range(201)]
    vin = [vm * math.sin(2 * math.pi * x) for x in t]
    shift = -min(vin) if clamp_type == "positive" else -max(vin)
    vout = [v + shift for v in vin]
    ax.plot(t, vin, color="#9ca3af", linewidth=1.5, linestyle="--", label="Input")
    ax.plot(t, vout, color="#14b8a6", linewidth=2, label="Output (clamped)")
    ax.axhline(0, color="#f59e0b", linewidth=1, linestyle=":")
    ax.set_xlabel("Time (cycles)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Diode Clamper: Input vs Output")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


EXTRA_SIMULATORS = {
    "Half-Wave Rectifier": render_half_wave_sim,
    "Full-Wave Rectifier": render_full_wave_sim,
    "Ripple & Filter Capacitor": render_ripple_sim,
    "Clipper Circuit": render_clipper_sim,
    "Clamper Circuit": render_clamper_sim,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. In which direction does a forward-biased diode allow current to flow easily?", "options": ["Only in reverse", "Anode to cathode", "It blocks all current"], "answer": "Anode to cathode"},
    {"q": "2. What makes a Zener diode different from a regular diode?", "options": ["It only conducts AC", "It is designed to operate safely in reverse breakdown", "It has no forward voltage drop"], "answer": "It is designed to operate safely in reverse breakdown"},
    {"q": "3. What is a key advantage of a Schottky diode over a standard silicon diode?", "options": ["Higher forward voltage drop", "Lower forward voltage drop and faster switching", "It works only with AC"], "answer": "Lower forward voltage drop and faster switching"},
    {"q": "4. What must always be used in series with a Zener diode?", "options": ["A capacitor", "A current-limiting resistor", "Another Zener diode"], "answer": "A current-limiting resistor"},
    {"q": "5. What is the main advantage of a full-wave bridge rectifier over a half-wave rectifier?", "options": ["It uses fewer diodes", "It produces a smoother output using both halves of the AC cycle", "It doesn't need a transformer at all"], "answer": "It produces a smoother output using both halves of the AC cycle"},
    {"q": "6. What does PIV stand for in rectifier circuits?", "options": ["Peak Inverse Voltage", "Power Input Value", "Pulse Interval Voltage"], "answer": "Peak Inverse Voltage"},
    {"q": "7. Increasing the filter capacitor value in a power supply will generally:", "options": ["Increase the ripple voltage", "Decrease the ripple voltage", "Have no effect on ripple"], "answer": "Decrease the ripple voltage"},
    {"q": "8. What does a diode clipper circuit do to a waveform?", "options": ["Shifts its DC level without changing its shape", "Cuts off part of the signal above or below a set level", "Amplifies the entire signal"], "answer": "Cuts off part of the signal above or below a set level"},
    {"q": "9. What does a diode clamper circuit do to a waveform?", "options": ["Cuts off part of the signal", "Shifts the whole waveform's DC level while keeping its shape", "Converts AC to DC directly"], "answer": "Shifts the whole waveform's DC level while keeping its shape"},
    {"q": "10. A photodiode is typically operated in which bias condition to sense light?", "options": ["Forward bias", "Reverse bias", "No bias at all"], "answer": "Reverse bias"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A student builds a simple half-wave rectifier, but the DC output reads 0V even though the AC input is present.",
        "question": "What is the most likely cause?",
        "options": ["The diode is installed backwards (reverse biased for the whole cycle)", "The diode is too large", "The AC frequency is too low"], 
        "answer": "The diode is installed backwards (reverse biased for the whole cycle)",
        "explanation": "If the diode's orientation is reversed, it blocks current during the half-cycle it should conduct, leaving no path for current to reach the load at all.",
    },
    {
        "scenario": "In a bridge rectifier power supply, one of the four diodes fails as an open circuit.",
        "question": "What would you expect to observe at the output?",
        "options": ["The output becomes pure, ripple-free DC", "The circuit now behaves like a half-wave rectifier, with higher ripple", "No change at all"],
        "answer": "The circuit now behaves like a half-wave rectifier, with higher ripple",
        "explanation": "With one diode open, only one conduction path remains functional through the bridge, so only one half of the AC cycle gets rectified — exactly like a half-wave rectifier.",
    },
    {
        "scenario": "A Zener regulator circuit is built without any series resistor, connecting the Zener diode directly across the supply.",
        "question": "What is the likely outcome?",
        "options": ["Perfect voltage regulation with no downsides", "Excessive current flows through the Zener, likely destroying it", "The Zener simply won't conduct at all"],
        "answer": "Excessive current flows through the Zener, likely destroying it",
        "explanation": "Without a series resistor to limit current, the Zener has nothing to prevent runaway current once it enters breakdown — it will overheat and fail.",
    },
    {
        "scenario": "A power supply's output shows much more ripple (a bigger wobble on the DC) than expected.",
        "question": "What is a sensible first thing to check?",
        "options": ["Whether the filter capacitor value is too small (or has failed) for the load current", "Whether the diodes are the wrong colour", "Whether the load resistor has too much resistance to draw any current"],
        "answer": "Whether the filter capacitor value is too small (or has failed) for the load current",
        "explanation": "Ripple voltage is inversely proportional to filter capacitance — a capacitor that's too small (or a failed/dried-out electrolytic capacitor) can't hold the voltage steady between rectified pulses.",
    },
    {
        "scenario": "A rectifier diode fails shortly after a power supply is put into service, and the reverse voltage it experiences is close to its PIV rating.",
        "question": "What is the most likely design issue?",
        "options": ["The diode's PIV rating has too little safety margin for this application", "The diode was simply too cheap", "The AC frequency was too high"],
        "answer": "The diode's PIV rating has too little safety margin for this application",
        "explanation": "Good design practice leaves headroom between a diode's PIV rating and the actual peak reverse voltage it will see — operating right at the rated limit leaves no margin for voltage spikes or component tolerance.",
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
st.sidebar.title("🔺 DIODES & RECTIFIERS")
st.sidebar.subheader("LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore diode types\n"
    "3. Study rectifier circuits\n"
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
        "🔎 Diode Types Explorer",
        "⚡ Rectifier Circuits",
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
st.title("🔺 Diodes & Rectifiers Learning Lab")
st.caption("An Interactive Beginner's Guide to Diodes & Rectifier Circuits")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Diode Types Covered", len(DIODE_TYPES))
d2.metric("⚡ Rectifier Circuits", len(RECTIFIER_CIRCUITS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Diodes & Rectifiers")

    st.markdown(
        """
        ### What is a Diode?
        A **diode** is a semiconductor device that allows current to flow easily in
        ONE direction, while blocking it in the other. It's the electronic equivalent
        of a one-way valve — and it's the fundamental building block behind every
        power supply, radio receiver, and LED indicator you've ever used.

        Diodes are formed at the junction between P-type and N-type semiconductor
        material. This "PN junction" creates a one-way barrier to current flow that
        can be controlled with an applied voltage.
        """
    )

    st.subheader("🔁 Forward Bias vs. Reverse Bias")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>➡️ Forward Bias</h4>'
            '<p>Positive voltage applied to the anode relative to the cathode. Once past a small '
            '"turn-on" threshold (~0.6–0.7V for silicon), current flows easily.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>⬅️ Reverse Bias</h4>'
            '<p>Negative voltage applied to the anode relative to the cathode. The diode blocks '
            'almost all current — until a much higher "breakdown" voltage is reached.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("⚡ What is Rectification?")
    st.markdown(
        '<div class="app-card"><b>Rectification</b> is the process of converting AC (alternating '
        'current, which reverses direction) into DC (direct current, which flows one way). Diodes '
        'make this possible by only allowing current through during the part of the AC cycle where '
        'they are forward biased — the foundation of every AC-to-DC power supply.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Head to **'Diode Types Explorer'** in the sidebar to study each diode type in detail.")

# ============================================================================
# 2. DIODE TYPES EXPLORER
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Diode Types Explorer")
    st.caption("Expand each diode type to see its symbol, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in DIODE_ORDER:
        c = DIODE_TYPES[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_diode_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Forward Voltage:** {c['forward_v']}")
                st.markdown(f"**Connection:** {c['connection']}")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")
                if c["safety"]:
                    st.markdown(f'<div class="safety-note">⚠️ {c["safety"]}</div>', unsafe_allow_html=True)

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. RECTIFIER CIRCUITS
# ============================================================================
elif page.startswith("⚡"):
    st.header("⚡ Rectifier Circuits")
    st.caption("The key circuit topologies for converting AC to DC, and for shaping waveforms.")

    filter_tags = st.multiselect(
        "Filter diode types by category",
        ["general_purpose", "rectifying", "regulation", "optical", "sensing", "reactive", "tuning", "special_purpose", "rf", "fast_switching"],
        default=[],
    )
    if filter_tags:
        filtered = [n for n in DIODE_ORDER if any(t in DIODE_TYPES[n]["category"] for t in filter_tags)]
    else:
        filtered = DIODE_ORDER

    st.subheader("🧮 Diode Type Reference Table")
    rows = []
    for name in filtered:
        c = DIODE_TYPES[name]
        rows.append({
            "Diode Type": name,
            "Forward Voltage": c["forward_v"],
            "Connection": c["connection"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Key Rectifier & Wave-Shaping Circuits")
    for circuit_name in RECTIFIER_ORDER:
        rc = RECTIFIER_CIRCUITS[circuit_name]
        with st.expander(f"**{circuit_name}**"):
            st.markdown(f"**Formula:** `{rc['formula']}`")
            st.markdown(f"**Explanation:** {rc['explanation']}")
            st.markdown(f"**Used for:** {rc['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any diode type or rectifier circuit and experiment with its behaviour.")

    simulatable_diodes = [n for n in DIODE_ORDER if DIODE_TYPES[n]["calc_key"] is not None]
    options = simulatable_diodes + list(EXTRA_SIMULATORS.keys())
    sel = st.selectbox("Select a diode type or circuit", options)

    if sel in EXTRA_SIMULATORS:
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #7c3aed, #4c1d95);">'
                 f'⚡ <b>{sel}</b></div>'),
            unsafe_allow_html=True,
        )
        EXTRA_SIMULATORS[sel](key_prefix=f"sim_{sel}")
    else:
        c = DIODE_TYPES[sel]
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #ea580c, #9a3412);">'
                 f'🔺 <b>{sel}</b> &nbsp;|&nbsp; {c["desc"]}</div>'),
            unsafe_allow_html=True,
        )
        col_symbol, col_calc = st.columns([1, 1.6])
        with col_symbol:
            st.markdown("##### 🔷 Symbol")
            st.markdown(f'<div class="symbol-box">{draw_diode_svg(sel)}</div>', unsafe_allow_html=True)
            st.markdown(f"**Forward Voltage:** {c['forward_v']}")
        with col_calc:
            CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how diodes and rectifiers are used across real electronic systems.")

    APPLICATIONS = [
        ("🔌 AC-to-DC Power Supplies", "Bridge rectifiers convert mains AC into pulsating DC; filter capacitors smooth it; Zener diodes or regulator ICs hold the output at a precise, stable voltage."),
        ("📻 Radio & Signal Demodulation", "Diodes recover the original audio signal from an amplitude-modulated (AM) radio wave by rectifying and filtering the high-frequency carrier."),
        ("💡 Indicator Lights & Displays", "LEDs (a type of diode) provide efficient, long-lasting indicator lights, backlighting, and full digital displays."),
        ("☀️ Solar Cells & Light Sensing", "Photodiodes (and the closely related solar cell) convert light directly into electrical current, used in light meters, optical receivers, and renewable energy."),
        ("📡 RF Tuning & Communication", "Varactor diodes let radios and TVs electronically tune to different frequencies; PIN diodes act as fast RF switches and attenuators."),
        ("🛡️ Circuit Protection", "Diodes protect sensitive circuits from reverse-polarity connection, voltage spikes (clamping/clipping), and back-EMF from relay or motor coils."),
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
    st.header("📝 Diodes & Rectifiers Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Diode Types Explorer' section and try again!")

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
