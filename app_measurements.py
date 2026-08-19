"""
📏 Measurements & Instruments Learning Lab
An Interactive Beginner's Guide to Electrical Measurements & Instruments

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
    page_title="Measurements & Instruments Learning Lab",
    page_icon="📏",
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
        background: linear-gradient(135deg, #1e3a5f, #0c4a6e);
        border: 1px solid #38bdf8;
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
# CORE MEASUREMENT CALCULATIONS (pure functions, no widgets — reused everywhere)
# ============================================================================

def percent_error(measured, true_value):
    """Percentage error of a measurement against a known/true value."""
    if true_value == 0:
        return None
    return ((measured - true_value) / true_value) * 100.0


def voltmeter_loading(vs, r_source, r_load, r_meter):
    """Voltage divider with a voltmeter (finite resistance r_meter) connected
    across r_load. Returns (ideal_voltage, measured_voltage, error_pct)."""
    if (r_source + r_load) == 0:
        return None, None, None
    v_ideal = vs * r_load / (r_source + r_load)
    if r_meter <= 0:
        return v_ideal, 0.0, None
    r_parallel = (r_load * r_meter) / (r_load + r_meter)
    if (r_source + r_parallel) == 0:
        return v_ideal, None, None
    v_measured = vs * r_parallel / (r_source + r_parallel)
    err = percent_error(v_measured, v_ideal)
    return v_ideal, v_measured, err


def ammeter_insertion(voltage, r_circuit, r_ammeter):
    """Extra series resistance an ammeter introduces. Returns
    (ideal_current, measured_current, error_pct)."""
    if r_circuit <= 0:
        return None, None, None
    ideal_current = voltage / r_circuit
    measured_current = voltage / (r_circuit + r_ammeter)
    err = percent_error(measured_current, ideal_current)
    return ideal_current, measured_current, err


def scope_reading(volts_per_div, vertical_divs, time_per_div, horizontal_divs_per_cycle):
    """Interpret oscilloscope grid readings into real values."""
    peak_voltage = volts_per_div * vertical_divs
    period = time_per_div * horizontal_divs_per_cycle
    frequency = (1.0 / period) if period > 0 else None
    return peak_voltage, period, frequency


def waveform_period_omega(frequency):
    """Period and angular frequency from a signal's frequency."""
    if frequency <= 0:
        return None, None
    period = 1.0 / frequency
    omega = 2 * math.pi * frequency
    return period, omega


def psu_supply_check(voltage, current_limit, load_resistance):
    """Whether a bench power supply's current limit is enough for a given load."""
    max_power = voltage * current_limit
    if load_resistance <= 0:
        return max_power, None, None
    required_current = voltage / load_resistance
    within_limit = required_current <= current_limit
    return max_power, required_current, within_limit


def logic_level(voltage, low_thresh=0.8, high_thresh=2.0):
    """Classify a voltage into a simplified TTL-style logic level."""
    if voltage <= low_thresh:
        return "LOW"
    if voltage >= high_thresh:
        return "HIGH"
    return "UNDEFINED (in the forbidden zone)"


def lcr_reactances(frequency, inductance_mh, capacitance_uf):
    """Inductive and capacitive reactance at a given frequency."""
    if frequency <= 0:
        return None, None
    l_henries = inductance_mh * 1e-3
    c_farads = capacitance_uf * 1e-6
    x_l = 2 * math.pi * frequency * l_henries
    x_c = (1.0 / (2 * math.pi * frequency * c_farads)) if c_farads > 0 else None
    return x_l, x_c


def frequency_from_period(period_ms):
    """Frequency counter: convert a measured period (ms) into frequency (Hz)."""
    if period_ms <= 0:
        return None
    return 1.0 / (period_ms / 1000.0)


def shunt_resistance(ig_ma, rg_ohm, desired_full_scale_a):
    """Classic galvanometer-to-ammeter conversion: shunt resistor needed to
    extend a galvanometer's full-scale current to a larger ammeter range."""
    ig = ig_ma / 1000.0
    if desired_full_scale_a <= ig:
        return None
    return (ig * rg_ohm) / (desired_full_scale_a - ig)


# ============================================================================
# INSTRUMENT DATA
# 12 core measuring instruments, each with the fields the Explorer page
# needs. "calc_key" links an instrument to its interactive render function
# further down.
# ============================================================================
INSTRUMENTS = {
    "Multimeter": {
        "desc": "A single handheld instrument that can measure voltage, current, resistance, and more, selected via a mode dial.",
        "measures": "Voltage, Current, Resistance, Continuity (and often capacitance, frequency)",
        "connection": "Depends on mode: like a voltmeter (parallel) for voltage, like an ammeter (series) for current.",
        "category": ["general_purpose", "voltage", "current", "resistance"],
        "explanation": "A multimeter is the electronics student's most-used tool — one device that becomes a voltmeter, ammeter, or ohmmeter depending on which mode you select on its dial.",
        "applications": "General troubleshooting, continuity checks, verifying power supply voltages, basic component testing.",
        "safety": "Always double-check the mode and range BEFORE connecting — measuring resistance on a live (powered) circuit, or current in the wrong mode, can damage the meter or the circuit.",
        "calc_key": "multimeter_mode",
    },
    "Voltmeter": {
        "desc": "An instrument that measures the voltage (potential difference) between two points in a circuit.",
        "measures": "Voltage (V)",
        "connection": "Connected in PARALLEL across the component being measured.",
        "category": ["voltage"],
        "explanation": "A voltmeter is designed to have very high internal resistance so that connecting it disturbs the circuit as little as possible — like measuring water pressure without blocking any flow.",
        "applications": "Checking battery voltage, verifying power supply rails, measuring voltage drops across components.",
        "safety": "Never connect a voltmeter in series — it has very high resistance and will effectively block current flow, giving a misleading reading (or no reading at all).",
        "calc_key": "voltmeter_loading",
    },
    "Ammeter": {
        "desc": "An instrument that measures the electric current flowing through a circuit.",
        "measures": "Current (A)",
        "connection": "Connected in SERIES so the current to be measured flows directly through it.",
        "category": ["current"],
        "explanation": "An ammeter is designed to have very low internal resistance so it barely affects the current it's measuring — like inserting a paddlewheel into a pipe without restricting the flow.",
        "applications": "Measuring current draw of a circuit, checking battery discharge current, verifying fuse sizing.",
        "safety": "⚠️ Never connect an ammeter directly across a voltage source (in parallel) — its very low resistance will cause a large, dangerous current surge and can destroy the meter.",
        "calc_key": "ammeter_loading",
    },
    "Ohmmeter": {
        "desc": "An instrument that measures the resistance of a component or conductor.",
        "measures": "Resistance (Ω)",
        "connection": "Connected directly across the component, which must be UNPOWERED and often isolated from the rest of the circuit.",
        "category": ["resistance"],
        "explanation": "An ohmmeter works by sending a small known current through the component and measuring the resulting voltage drop, then calculating resistance using Ohm's Law internally.",
        "applications": "Checking for continuity/breaks in wires, verifying resistor values, testing fuses.",
        "safety": "⚠️ Never measure resistance on a live (powered) circuit — the meter's internal current source can be damaged and readings will be meaningless.",
        "calc_key": "percent_error",
    },
    "Oscilloscope": {
        "desc": "An instrument that displays how a voltage signal changes over time, as a graph on a screen.",
        "measures": "Voltage vs. Time (waveform shape, amplitude, frequency, period)",
        "connection": "Connected in parallel (like a voltmeter), usually via a probe with a ground clip.",
        "category": ["waveform", "voltage"],
        "explanation": "While a multimeter gives you a single number, an oscilloscope shows the whole *shape* of a signal over time — essential for seeing waveforms, noise, timing, and glitches that a multimeter can't reveal.",
        "applications": "Debugging digital signals, analysing audio waveforms, measuring signal timing and frequency, power supply ripple inspection.",
        "safety": "Be careful with ground clip placement — connecting it to the wrong point can create a short circuit through the oscilloscope's chassis ground.",
        "calc_key": "scope_calc",
    },
    "Function Generator": {
        "desc": "An instrument that generates electrical waveforms (sine, square, triangle) at a chosen frequency and amplitude.",
        "measures": "N/A — it's a signal SOURCE, not a measuring instrument",
        "connection": "Its output connects to the circuit under test, typically alongside an oscilloscope to view the result.",
        "category": ["waveform", "source"],
        "explanation": "A function generator is the opposite of a multimeter — instead of measuring an existing signal, it creates one, letting you test how circuits respond to different frequencies and waveform shapes.",
        "applications": "Testing filter circuits, characterising amplifiers, simulating sensor signals, audio equipment testing.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "waveform_calc",
    },
    "Power Supply": {
        "desc": "A bench instrument that provides a controllable, stable DC voltage and current to power a circuit under test.",
        "measures": "N/A — it's a power SOURCE, though most bench units also display voltage/current output",
        "connection": "Its output terminals connect directly to the circuit being powered.",
        "category": ["source"],
        "explanation": "A good bench power supply lets you set both a voltage AND a current limit — if the circuit tries to draw more current than the limit, the supply 'current-limits' rather than letting the voltage collapse or damaging anything.",
        "applications": "Powering prototype circuits safely, testing how circuits behave at different voltages, simulating battery levels.",
        "safety": "Always set a sensible current limit before connecting an unfamiliar circuit — this is your first line of defence against accidental short circuits.",
        "calc_key": "psu_calc",
    },
    "Wattmeter": {
        "desc": "An instrument that measures electrical power directly, combining both a voltage-sensing and current-sensing element.",
        "measures": "Power (W)",
        "connection": "Uses both a series current coil AND a parallel voltage coil simultaneously.",
        "category": ["power"],
        "explanation": "Rather than measuring voltage and current separately and multiplying them yourself, a wattmeter does both at once internally and displays power directly.",
        "applications": "Measuring appliance power consumption, verifying motor power draw, energy auditing.",
        "safety": "Ensure the current coil is rated for the circuit's current — exceeding it can damage the coil.",
        "calc_key": "wattmeter_calc",
    },
    "Logic Probe": {
        "desc": "A simple handheld tool that indicates whether a point in a digital circuit is HIGH, LOW, or pulsing.",
        "measures": "Digital logic state (HIGH / LOW / pulsing), not an exact voltage",
        "connection": "Touched directly to the test point, with power and ground leads clipped to the circuit's supply rails.",
        "category": ["digital"],
        "explanation": "A logic probe is a fast, simple alternative to an oscilloscope when you just need to know 'is this pin HIGH or LOW right now?' rather than the exact voltage or waveform shape.",
        "applications": "Quickly checking digital circuit nodes, debugging logic gate outputs, verifying clock signals are toggling.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "logic_level",
    },
    "LCR Meter": {
        "desc": "An instrument that measures Inductance (L), Capacitance (C), and Resistance (R) of a component.",
        "measures": "Inductance (H), Capacitance (F), Resistance (Ω)",
        "connection": "Connected directly across the component, which should be removed from any powered circuit.",
        "category": ["resistance", "reactive"],
        "explanation": "Unlike a simple ohmmeter, an LCR meter applies an AC test signal, letting it distinguish resistive behaviour from the frequency-dependent behaviour of capacitors and inductors.",
        "applications": "Verifying unmarked or aged capacitor/inductor values, sorting components by tolerance, filter design verification.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "lcr_calc",
    },
    "Frequency Counter": {
        "desc": "An instrument that precisely measures the frequency (or period) of a repeating signal.",
        "measures": "Frequency (Hz), Period (s)",
        "connection": "Connected in parallel to the signal being measured, similar to a voltmeter.",
        "category": ["waveform"],
        "explanation": "A frequency counter works by literally counting how many signal cycles occur in a fixed time window (or timing a single cycle very precisely), giving a far more accurate frequency reading than reading it off an oscilloscope screen.",
        "applications": "Calibrating oscillators, verifying clock signal accuracy, radio frequency measurement.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "freq_calc",
    },
    "Galvanometer": {
        "desc": "A sensitive instrument that detects and measures very small electric currents using a moving coil and needle.",
        "measures": "Very small currents (µA range), used as the core movement inside many analogue meters",
        "connection": "Connected in series, similar to an ammeter, but only tolerates tiny currents directly.",
        "category": ["current"],
        "explanation": "A galvanometer is the sensitive heart of classic analogue meters — by adding a 'shunt' resistor in parallel, its tiny full-scale current range can be extended to measure much larger currents as a full ammeter.",
        "applications": "The core movement in analogue multimeters, null-detection in bridge circuits (e.g. Wheatstone bridge), sensitive laboratory measurements.",
        "safety": "Extremely sensitive to overcurrent — even a modest current with no shunt resistor can bend or destroy the needle movement.",
        "calc_key": "shunt_calc",
    },
}

INSTRUMENT_ORDER = list(INSTRUMENTS.keys())

# ============================================================================
# MEASUREMENT CONCEPTS & ERROR TYPES (used on the "Measurement Concepts" page)
# ============================================================================
MEASUREMENT_CONCEPTS = {
    "Accuracy": {
        "meaning": "How close a measured value is to the TRUE value.",
        "explanation": "An accurate thermometer reading 25.1°C when the true temperature is 25.0°C is very accurate — it's close to the truth, even if it's not perfectly exact.",
    },
    "Precision": {
        "meaning": "How close repeated measurements are to EACH OTHER, regardless of whether they're correct.",
        "explanation": "A scale that reads 51.2 kg, 51.3 kg, and 51.2 kg for the same object every time is very precise — but if your true weight is 60 kg, it's precise and also badly inaccurate.",
    },
    "Resolution": {
        "meaning": "The smallest change an instrument can actually detect and display.",
        "explanation": "A multimeter that only displays whole volts (5V, 6V, 7V…) has poor resolution compared to one that displays to two decimal places (5.23V) — even if both are equally accurate.",
    },
    "Range": {
        "meaning": "The span of values an instrument can measure, from minimum to maximum.",
        "explanation": "A voltmeter with a 0–20V range simply cannot measure 230V mains safely or correctly — always match the instrument's range to what you're measuring.",
    },
    "Error (Systematic)": {
        "meaning": "A consistent, repeatable error caused by a flaw in the instrument or method — e.g. incorrect calibration.",
        "explanation": "If a scale always reads 0.5 kg too high because it wasn't zeroed properly, every single measurement is offset in the same direction — this is systematic error.",
    },
    "Error (Random)": {
        "meaning": "Unpredictable, varying error from one measurement to the next, often from noise or small environmental changes.",
        "explanation": "Tiny fluctuations in room temperature or your own hand shakiness might cause repeated measurements to scatter slightly above and below the true value — this is random error.",
    },
    "Calibration": {
        "meaning": "The process of comparing an instrument's readings against a known, trusted reference and adjusting it to correct systematic error.",
        "explanation": "Calibrating a multimeter against a certified reference voltage source ensures its readings can be trusted — instruments drift out of calibration over time and need periodic rechecking.",
    },
    "Loading Effect": {
        "meaning": "The way a measuring instrument itself changes the circuit it's connected to, introducing measurement error.",
        "explanation": "A voltmeter with insufficient internal resistance, or an ammeter with too much internal resistance, both disturb the very circuit they're trying to measure — a fundamental limitation of real (non-ideal) instruments.",
    },
}

MEASUREMENT_CONCEPT_ORDER = list(MEASUREMENT_CONCEPTS.keys())

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each instrument. Every returned
# string is flattened to one line with flat() so Streamlit's Markdown
# renderer never mis-parses an embedded blank line as the end of the block.
# ============================================================================
INSTRUMENT_COLORS = {
    "Multimeter": "#6366f1",
    "Voltmeter": "#f97316",
    "Ammeter": "#3b82f6",
    "Ohmmeter": "#8b5cf6",
    "Oscilloscope": "#06b6d4",
    "Function Generator": "#ec4899",
    "Power Supply": "#22c55e",
    "Wattmeter": "#eab308",
    "Logic Probe": "#14b8a6",
    "LCR Meter": "#a855f7",
    "Frequency Counter": "#0ea5e9",
    "Galvanometer": "#f43f5e",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def draw_instrument_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the instrument."""
    color = INSTRUMENT_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Multimeter":
        # Rectangle body with digital display and a mode dial
        body = f"""
        <rect x="55" y="15" width="110" height="110" rx="8" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <rect x="68" y="28" width="84" height="28" rx="3" fill="#111827"/>
        <text x="80" y="48" font-size="16" font-weight="bold" fill="#4ade80">12.4V</text>
        <circle cx="110" cy="92" r="24" fill="none" stroke="{color}" stroke-width="3"/>
        <line x1="110" y1="92" x2="122" y2="76" stroke="{color}" stroke-width="3"/>
        <circle cx="110" cy="92" r="3" fill="{color}"/>
        {_lead(0, 130, 55, 130)}
        {_lead(165, 130, 220, 130)}
        """

    elif name == "Voltmeter":
        body = f"""
        {_lead(0, 40, 65, 40)}
        {_lead(0, 100, 65, 100)}
        <circle cx="110" cy="70" r="45" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="97" y="82" font-size="30" font-weight="bold" fill="{color}">V</text>
        <line x1="65" y1="40" x2="90" y2="55" stroke="{color}" stroke-width="4"/>
        <line x1="65" y1="100" x2="90" y2="85" stroke="{color}" stroke-width="4"/>
        """

    elif name == "Ammeter":
        body = f"""
        {_lead(0, 70, 65, 70)}
        <circle cx="110" cy="70" r="45" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="97" y="82" font-size="30" font-weight="bold" fill="{color}">A</text>
        {_lead(155, 70, 220, 70)}
        """

    elif name == "Ohmmeter":
        body = f"""
        {_lead(0, 40, 65, 40)}
        {_lead(0, 100, 65, 100)}
        <circle cx="110" cy="70" r="45" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="92" y="82" font-size="28" font-weight="bold" fill="{color}">Ω</text>
        <line x1="65" y1="40" x2="90" y2="55" stroke="{color}" stroke-width="4"/>
        <line x1="65" y1="100" x2="90" y2="85" stroke="{color}" stroke-width="4"/>
        """

    elif name == "Oscilloscope":
        # Screen showing a sine wave
        body = f"""
        <rect x="35" y="20" width="150" height="100" rx="6" fill="#111827" stroke="{color}" stroke-width="4"/>
        <path d="M45,70 C60,35 75,35 90,70 C105,105 120,105 135,70 C150,35 165,35 175,70"
              fill="none" stroke="{color}" stroke-width="3"/>
        <line x1="35" y1="70" x2="185" y2="70" stroke="#374151" stroke-width="1"/>
        <line x1="110" y1="20" x2="110" y2="120" stroke="#374151" stroke-width="1"/>
        """

    elif name == "Function Generator":
        # Box with a waveform icon
        body = f"""
        <rect x="35" y="25" width="150" height="90" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <path d="M55,70 L70,70 L80,45 L95,95 L110,45 L125,95 L140,70 L165,70"
              fill="none" stroke="{color}" stroke-width="3"/>
        {_lead(185, 70, 220, 70)}
        """

    elif name == "Power Supply":
        body = f"""
        <rect x="35" y="25" width="150" height="90" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <rect x="50" y="38" width="70" height="22" rx="3" fill="#111827"/>
        <text x="58" y="55" font-size="13" font-weight="bold" fill="#4ade80">5.00V</text>
        <circle cx="150" cy="80" r="18" fill="none" stroke="{color}" stroke-width="3"/>
        <text x="143" y="86" font-size="16" font-weight="bold" fill="{color}">+</text>
        <circle cx="185" cy="80" r="0" fill="none"/>
        {_lead(185, 45, 220, 45)}
        {_lead(185, 95, 220, 95)}
        <text x="188" y="40" font-size="11" font-weight="bold" fill="#111827">+</text>
        <text x="188" y="112" font-size="11" font-weight="bold" fill="#111827">−</text>
        """

    elif name == "Wattmeter":
        body = f"""
        {_lead(0, 70, 40, 70)}
        <circle cx="110" cy="70" r="45" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="93" y="82" font-size="28" font-weight="bold" fill="{color}">W</text>
        {_lead(180, 70, 220, 70)}
        <line x1="80" y1="30" x2="95" y2="42" stroke="{color}" stroke-width="3"/>
        <line x1="140" y1="30" x2="125" y2="42" stroke="{color}" stroke-width="3"/>
        """

    elif name == "Logic Probe":
        # Pen-shaped probe with an indicator light at the tip
        body = f"""
        <rect x="85" y="20" width="40" height="80" rx="10" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <polygon points="85,100 125,100 105,130" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <circle cx="105" cy="128" r="5" fill="#facc15"/>
        <rect x="95" y="35" width="20" height="14" rx="3" fill="#111827"/>
        {_lead(105, 20, 105, 5)}
        """

    elif name == "LCR Meter":
        body = f"""
        <rect x="35" y="25" width="150" height="90" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="55" y="80" font-size="22" font-weight="bold" fill="{color}">L C R</text>
        {_lead(35, 90, 15, 105)}
        {_lead(185, 90, 205, 105)}
        """

    elif name == "Frequency Counter":
        body = f"""
        <rect x="35" y="30" width="150" height="80" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <rect x="50" y="55" width="120" height="30" rx="3" fill="#111827"/>
        <text x="58" y="76" font-size="15" font-weight="bold" fill="#4ade80">1.000 kHz</text>
        {_lead(0, 70, 35, 70)}
        """

    elif name == "Galvanometer":
        body = f"""
        {_lead(0, 70, 65, 70)}
        <circle cx="110" cy="70" r="45" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="95" y="82" font-size="26" font-weight="bold" fill="{color}">G</text>
        <line x1="110" y1="70" x2="128" y2="45" stroke="{color}" stroke-width="3"/>
        <circle cx="110" cy="70" r="3" fill="{color}"/>
        {_lead(155, 70, 220, 70)}
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same instrument is rendered on more than one page.
# ============================================================================

def render_multimeter_mode(key_prefix):
    st.markdown("**⚙️ Multimeter Mode Simulator**")
    mode = st.selectbox("Select mode", ["DC Voltage", "AC Voltage", "Resistance", "Continuity"], key=f"{key_prefix}_mm_mode")
    if mode in ("DC Voltage", "AC Voltage"):
        val = st.number_input(f"{mode} present at test points (V)", value=5.0, step=0.5, key=f"{key_prefix}_mm_v")
        st.markdown(f'<div class="status-good">✅ Display reads: {val:.2f} V ({mode})</div>', unsafe_allow_html=True)
        st.caption("The meter's mode dial must match the type of signal present, or the reading will be wrong or unstable.")
    elif mode == "Resistance":
        val = st.number_input("Resistance of component (Ω)", min_value=0.0, value=470.0, step=10.0, key=f"{key_prefix}_mm_r")
        st.markdown(f'<div class="status-good">✅ Display reads: {val:.1f} Ω</div>', unsafe_allow_html=True)
        st.markdown('<div class="safety-note">⚠️ This mode only gives a correct reading if the component is unpowered and isolated from the rest of the circuit.</div>', unsafe_allow_html=True)
    else:
        connected = st.toggle("Are the two probe tips electrically connected?", value=False, key=f"{key_prefix}_mm_cont")
        if connected:
            st.markdown('<div class="status-good">✅ 🔊 BEEP — Continuity detected (near 0 Ω path)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-bad">⛔ No beep — no continuous path (open circuit)</div>', unsafe_allow_html=True)


def render_voltmeter_loading(key_prefix):
    st.markdown("**⚙️ Voltmeter Loading Effect Calculator**")
    st.caption("A real voltmeter has finite internal resistance, which slightly disturbs the very voltage it's trying to measure.")
    c1, c2 = st.columns(2)
    vs = c1.number_input("Supply Voltage (V)", min_value=0.0, value=10.0, step=0.5, key=f"{key_prefix}_vm_vs")
    r_source = c1.number_input("Source Resistance (Ω)", min_value=0.0, value=1000.0, step=100.0, key=f"{key_prefix}_vm_rs")
    r_load = c2.number_input("Load Resistance Being Measured (Ω)", min_value=0.1, value=1000.0, step=100.0, key=f"{key_prefix}_vm_rl")
    r_meter = c2.number_input("Voltmeter Internal Resistance (Ω)", min_value=0.0, value=1000000.0, step=10000.0, key=f"{key_prefix}_vm_rm")
    v_ideal, v_measured, err = voltmeter_loading(vs, r_source, r_load, r_meter)
    if v_ideal is None or v_measured is None:
        st.warning("⚠️ Check your resistance values.")
    else:
        st.markdown(f'<div class="status-good">✅ Ideal Voltage = {v_ideal:.4f} V &nbsp;|&nbsp; Measured Voltage = {v_measured:.4f} V &nbsp;|&nbsp; Error = {err:.3f}%</div>', unsafe_allow_html=True)
        st.caption("Try lowering the voltmeter's internal resistance — notice the error grows as the meter 'loads' the circuit more.")


def render_ammeter_loading(key_prefix):
    st.markdown("**⚙️ Ammeter Insertion Error Calculator**")
    st.caption("A real ammeter has some internal resistance, which slightly reduces the current it's trying to measure.")
    c1, c2 = st.columns(2)
    voltage = c1.number_input("Circuit Voltage (V)", min_value=0.0, value=10.0, step=0.5, key=f"{key_prefix}_am_v")
    r_circuit = c1.number_input("Circuit Resistance (Ω)", min_value=0.1, value=100.0, step=10.0, key=f"{key_prefix}_am_rc")
    r_ammeter = c2.number_input("Ammeter Internal Resistance (Ω)", min_value=0.0, value=1.0, step=0.5, key=f"{key_prefix}_am_ra")
    ideal_i, measured_i, err = ammeter_insertion(voltage, r_circuit, r_ammeter)
    if ideal_i is None:
        st.warning("⚠️ Circuit resistance must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Ideal Current = {ideal_i*1000:.2f} mA &nbsp;|&nbsp; Measured Current = {measured_i*1000:.2f} mA &nbsp;|&nbsp; Error = {err:.3f}%</div>', unsafe_allow_html=True)
        st.caption("Try raising the ammeter's internal resistance — notice how much more it disturbs the circuit's current.")


def render_percent_error_calc(key_prefix):
    st.markdown("**⚙️ Percentage Error Calculator** (e.g. for an Ohmmeter reading)")
    c1, c2 = st.columns(2)
    measured = c1.number_input("Measured Value", value=97.0, step=1.0, key=f"{key_prefix}_pe_m")
    true_val = c2.number_input("True / Reference Value", value=100.0, step=1.0, key=f"{key_prefix}_pe_t")
    err = percent_error(measured, true_val)
    if err is None:
        st.warning("⚠️ True value must be non-zero.")
    elif abs(err) <= 2:
        st.markdown(f'<div class="status-good">✅ Error = {err:.3f}% — within a typical acceptable tolerance.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-bad">⚠️ Error = {err:.3f}% — larger than a typical acceptable tolerance; check calibration or the component itself.</div>', unsafe_allow_html=True)


def render_scope_calc(key_prefix):
    st.markdown("**⚙️ Oscilloscope Reading Interpreter**")
    st.caption("Read values directly off the scope's grid (graticule), just like in the lab.")
    c1, c2 = st.columns(2)
    volts_per_div = c1.number_input("Volts / Division (V)", min_value=0.01, value=1.0, step=0.1, key=f"{key_prefix}_sc_vdiv")
    vertical_divs = c1.number_input("Peak height (divisions)", min_value=0.1, value=3.0, step=0.5, key=f"{key_prefix}_sc_vcnt")
    time_per_div = c2.number_input("Time / Division (ms)", min_value=0.001, value=1.0, step=0.1, key=f"{key_prefix}_sc_tdiv")
    horiz_divs = c2.number_input("One full cycle (divisions)", min_value=0.1, value=4.0, step=0.5, key=f"{key_prefix}_sc_hcnt")
    peak_v, period_ms, freq = scope_reading(volts_per_div, vertical_divs, time_per_div, horiz_divs)
    if freq is None:
        st.warning("⚠️ Period must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Peak Voltage = {peak_v:.2f} V &nbsp;|&nbsp; Period = {period_ms:.3f} ms &nbsp;|&nbsp; Frequency = {freq*1000:.2f} Hz</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        t = [x * 0.02 for x in range(101)]
        wave = [peak_v * math.sin(2 * math.pi * x) for x in t]
        ax.plot([x * period_ms for x in t], wave, color="#06b6d4", linewidth=2)
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Reconstructed Waveform")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


def render_waveform_calc(key_prefix):
    st.markdown("**⚙️ Function Generator Output Calculator**")
    freq = st.number_input("Set Frequency (Hz)", min_value=0.1, value=1000.0, step=100.0, key=f"{key_prefix}_wf_f")
    period, omega = waveform_period_omega(freq)
    if period is None:
        st.warning("⚠️ Frequency must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Period = {period*1000:.4f} ms &nbsp;|&nbsp; Angular Frequency ω = {omega:.2f} rad/s</div>', unsafe_allow_html=True)


def render_psu_calc(key_prefix):
    st.markdown("**⚙️ Power Supply Current-Limit Checker**")
    c1, c2 = st.columns(2)
    voltage = c1.number_input("Set Voltage (V)", min_value=0.0, value=9.0, step=0.5, key=f"{key_prefix}_ps_v")
    current_limit = c1.number_input("Current Limit (A)", min_value=0.01, value=0.5, step=0.05, key=f"{key_prefix}_ps_ilim")
    load_r = c2.number_input("Load Resistance (Ω)", min_value=0.1, value=50.0, step=5.0, key=f"{key_prefix}_ps_rl")
    max_p, req_i, within = psu_supply_check(voltage, current_limit, load_r)
    if req_i is None:
        st.warning("⚠️ Load resistance must be greater than 0.")
    elif within:
        st.markdown(f'<div class="status-good">✅ Load needs {req_i*1000:.1f} mA — within the {current_limit:.2f} A limit. Supply delivers this normally.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-bad">⚠️ Load needs {req_i*1000:.1f} mA — EXCEEDS the {current_limit:.2f} A limit. Supply will current-limit and voltage will sag below the set value.</div>', unsafe_allow_html=True)
    st.caption(f"Maximum power the supply could deliver at this setting: {max_p:.2f} W")


def render_wattmeter_calc(key_prefix):
    st.markdown("**⚙️ Wattmeter Power Calculator** — `P = V × I`")
    c1, c2 = st.columns(2)
    v = c1.number_input("Voltage (V)", min_value=0.0, value=230.0, step=1.0, key=f"{key_prefix}_wm_v")
    i = c2.number_input("Current (A)", min_value=0.0, value=2.5, step=0.1, key=f"{key_prefix}_wm_i")
    power = v * i
    st.markdown(f'<div class="status-good">✅ Power = {power:.2f} W</div>', unsafe_allow_html=True)


def render_logic_level_calc(key_prefix):
    st.markdown("**⚙️ Logic Probe Level Simulator** (simplified TTL-style thresholds)")
    voltage = st.slider("Voltage at test point (V)", 0.0, 5.0, 2.5, step=0.1, key=f"{key_prefix}_lp_v")
    level = logic_level(voltage)
    if level == "HIGH":
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-good">✅ {voltage:.1f} V → Logic {level}</div>', unsafe_allow_html=True)
    elif level == "LOW":
        st.markdown('<div class="bulb-wrap"><div class="bulb-off"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-bad">⛔ {voltage:.1f} V → Logic {level}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-bad">⚠️ {voltage:.1f} V → {level}</div>', unsafe_allow_html=True)
    st.caption("Simplified thresholds used here: ≤0.8V = LOW, ≥2.0V = HIGH, in between = undefined.")


def render_lcr_calc(key_prefix):
    st.markdown("**⚙️ LCR Meter: Reactance Calculator**")
    c1, c2, c3 = st.columns(3)
    freq = c1.number_input("Test Frequency (Hz)", min_value=1.0, value=1000.0, step=100.0, key=f"{key_prefix}_lcr_f")
    ind = c2.number_input("Inductance (mH)", min_value=0.0, value=10.0, step=1.0, key=f"{key_prefix}_lcr_l")
    cap = c3.number_input("Capacitance (µF)", min_value=0.0, value=1.0, step=0.1, key=f"{key_prefix}_lcr_c")
    x_l, x_c = lcr_reactances(freq, ind, cap)
    if x_l is None:
        st.warning("⚠️ Frequency must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Inductive Reactance Xₗ = {x_l:.2f} Ω &nbsp;|&nbsp; Capacitive Reactance Xᴄ = {x_c:.2f} Ω</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        freqs = [f for f in range(10, int(freq) * 3 + 100, max(1, int(freq // 20)))]
        xl_curve = [2 * math.pi * f * (ind * 1e-3) for f in freqs]
        xc_curve = [(1.0 / (2 * math.pi * f * (cap * 1e-6))) if cap > 0 else 0 for f in freqs]
        ax.plot(freqs, xl_curve, color="#f59e0b", label="Xₗ (inductive)")
        ax.plot(freqs, xc_curve, color="#8b5cf6", label="Xᴄ (capacitive)")
        ax.axvline(freq, color="#9ca3af", linestyle="--", linewidth=1)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Reactance (Ω)")
        ax.set_title("Reactance vs Frequency")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


def render_freq_calc(key_prefix):
    st.markdown("**⚙️ Frequency Counter: Period → Frequency**")
    period_ms = st.number_input("Measured Period (ms)", min_value=0.001, value=1.0, step=0.1, key=f"{key_prefix}_fc_p")
    freq = frequency_from_period(period_ms)
    if freq is None:
        st.warning("⚠️ Period must be greater than 0.")
    else:
        st.markdown(f'<div class="status-good">✅ Frequency = {freq:.2f} Hz</div>', unsafe_allow_html=True)


def render_shunt_calc(key_prefix):
    st.markdown("**⚙️ Galvanometer → Ammeter Shunt Calculator**")
    st.caption("Classic instrument-design problem: extend a sensitive galvanometer's range using a parallel shunt resistor.")
    c1, c2, c3 = st.columns(3)
    ig_ma = c1.number_input("Galvanometer Full-Scale Current (mA)", min_value=0.001, value=1.0, step=0.1, key=f"{key_prefix}_sh_ig")
    rg = c2.number_input("Galvanometer Coil Resistance (Ω)", min_value=0.1, value=50.0, step=5.0, key=f"{key_prefix}_sh_rg")
    desired_range = c3.number_input("Desired Ammeter Range (A)", min_value=0.01, value=1.0, step=0.1, key=f"{key_prefix}_sh_range")
    rsh = shunt_resistance(ig_ma, rg, desired_range)
    if rsh is None:
        st.warning("⚠️ Desired range must be larger than the galvanometer's own full-scale current.")
    else:
        st.markdown(f'<div class="status-good">✅ Required Shunt Resistance ≈ {rsh:.4f} Ω (connected in parallel with the galvanometer)</div>', unsafe_allow_html=True)


CALC_RENDERERS = {
    "multimeter_mode": render_multimeter_mode,
    "voltmeter_loading": render_voltmeter_loading,
    "ammeter_loading": render_ammeter_loading,
    "percent_error": render_percent_error_calc,
    "scope_calc": render_scope_calc,
    "waveform_calc": render_waveform_calc,
    "psu_calc": render_psu_calc,
    "wattmeter_calc": render_wattmeter_calc,
    "logic_level": render_logic_level_calc,
    "lcr_calc": render_lcr_calc,
    "freq_calc": render_freq_calc,
    "shunt_calc": render_shunt_calc,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. How should a voltmeter be connected to measure voltage across a component?", "options": ["In series", "In parallel", "It doesn't matter"], "answer": "In parallel"},
    {"q": "2. How should an ammeter be connected to measure current?", "options": ["In series", "In parallel", "Across the power supply directly"], "answer": "In series"},
    {"q": "3. What happens if you connect an ammeter directly across a voltage source?", "options": ["Nothing, it's perfectly safe", "A large, potentially dangerous current surge occurs", "It automatically switches to voltmeter mode"], "answer": "A large, potentially dangerous current surge occurs"},
    {"q": "4. What does an oscilloscope show that a multimeter cannot?", "options": ["The exact resistance of a component", "How a voltage signal changes shape over time", "The colour of a wire"], "answer": "How a voltage signal changes shape over time"},
    {"q": "5. What is the difference between accuracy and precision?", "options": ["They mean exactly the same thing", "Accuracy is closeness to the true value; precision is repeatability", "Precision is closeness to the true value; accuracy is repeatability"], "answer": "Accuracy is closeness to the true value; precision is repeatability"},
    {"q": "6. What is 'loading effect' in measurement?", "options": ["When an instrument runs out of battery", "When the instrument itself disturbs the circuit being measured", "When too many instruments are used at once"], "answer": "When the instrument itself disturbs the circuit being measured"},
    {"q": "7. Why must resistance never be measured on a powered (live) circuit?", "options": ["It looks unprofessional", "The meter's own internal current source can be damaged and readings are meaningless", "It uses too much battery power"], "answer": "The meter's own internal current source can be damaged and readings are meaningless"},
    {"q": "8. What does a function generator do?", "options": ["Measures voltage", "Generates test waveforms at a chosen frequency", "Measures resistance"], "answer": "Generates test waveforms at a chosen frequency"},
    {"q": "9. What is calibration?", "options": ["Cleaning an instrument", "Comparing and adjusting an instrument against a known reference", "Charging an instrument's battery"], "answer": "Comparing and adjusting an instrument against a known reference"},
    {"q": "10. A galvanometer's range can be extended to become an ammeter by adding a:", "options": ["Series resistor", "Shunt (parallel) resistor", "Capacitor"], "answer": "Shunt (parallel) resistor"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A student accidentally connects an ammeter directly across a 9V battery instead of in series with the circuit.",
        "question": "What is the most likely outcome?",
        "options": ["A very large current flows, possibly damaging the meter or blowing its fuse", "Nothing happens — this is a safe way to use an ammeter", "The meter automatically switches to voltmeter mode"],
        "answer": "A very large current flows, possibly damaging the meter or blowing its fuse",
        "explanation": "An ammeter has very low internal resistance. Connected directly across a voltage source (in parallel, not in series), it presents almost no opposition to current — resulting in a large surge.",
    },
    {
        "scenario": "A voltmeter is connected in series in a circuit instead of in parallel, and the circuit stops working.",
        "question": "What is the most likely cause?",
        "options": ["The voltmeter's very high resistance is blocking almost all current flow", "The voltmeter is broken", "The circuit's power supply failed"],
        "answer": "The voltmeter's very high resistance is blocking almost all current flow",
        "explanation": "A voltmeter is designed with very high internal resistance so it barely affects a circuit when connected in parallel — but in series, that same high resistance acts almost like an open circuit.",
    },
    {
        "scenario": "A multimeter set to resistance (Ω) mode is connected to a circuit that is still powered on, and the reading is erratic or the meter appears damaged.",
        "question": "What went wrong?",
        "options": ["Resistance mode should never be used on a live, powered circuit", "The battery in the meter is low", "The circuit resistance is simply too high"],
        "answer": "Resistance mode should never be used on a live, powered circuit",
        "explanation": "Resistance mode works by injecting the meter's own small test current — an external voltage already present interferes with this and can give false readings or damage the meter.",
    },
    {
        "scenario": "Two students measure the same resistor five times each. Student A gets 98, 99, 98, 99, 98 Ω. Student B gets 90, 105, 95, 110, 100 Ω. The true value is 100 Ω.",
        "question": "How would you best describe Student A's measurements compared to Student B's?",
        "options": ["Student A is more precise but slightly less accurate on average; Student B is less precise", "Student A and B are identical in every way", "Student B is clearly better because the average happens to be closer"],
        "answer": "Student A is more precise but slightly less accurate on average; Student B is less precise",
        "explanation": "Student A's readings are tightly clustered (high precision) but consistently slightly below 100 Ω (a small systematic error). Student B's readings scatter widely (low precision/high random error) despite averaging near the true value.",
    },
    {
        "scenario": "An oscilloscope trace looks like a jumbled, unstable mess that won't hold still on screen, even though the signal itself should be a clean repeating wave.",
        "question": "What is a sensible first thing to check?",
        "options": ["The oscilloscope's trigger settings", "Whether the wall outlet is grounded", "The colour of the probe cable"],
        "answer": "The oscilloscope's trigger settings",
        "explanation": "The trigger tells the scope exactly when to start drawing each sweep so repeating waveforms line up on screen. Incorrect trigger level or source is one of the most common reasons for an unstable-looking trace.",
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
st.sidebar.title("📏 MEASUREMENTS &")
st.sidebar.subheader("INSTRUMENTS LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore the instruments\n"
    "3. Study measurement concepts\n"
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
        "🔎 Instruments Explorer",
        "📐 Measurement Concepts",
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
st.title("📏 Measurements & Instruments Learning Lab")
st.caption("An Interactive Beginner's Guide to Electrical Measurements & Instruments")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Instruments Covered", len(INSTRUMENTS))
d2.metric("📐 Measurement Concepts", len(MEASUREMENT_CONCEPTS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Measurements & Instruments")

    st.markdown(
        """
        ### Why Measurement Matters
        You cannot fix, design, or even understand a circuit you cannot measure.
        **Measuring instruments** are the eyes and ears of every electronics student —
        they turn invisible electrical quantities like voltage and current into numbers,
        graphs, and beeps you can actually work with.

        This module covers the essential instruments you'll use constantly — from
        the humble multimeter to the oscilloscope — and the core ideas of *accuracy*,
        *precision*, and *measurement error* that determine how much you can trust
        any reading.
        """
    )

    st.subheader("🎯 Accuracy vs. Precision — A Quick Analogy")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>🎯 Accuracy</h4>'
            '<p>Like arrows landing close to the BULLSEYE — how close a measurement is to the true value.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>🔬 Precision</h4>'
            '<p>Like arrows landing close to EACH OTHER — how repeatable a measurement is, whether or not it\'s correct.</p></div>',
            unsafe_allow_html=True,
        )
    st.caption("A great instrument is both accurate AND precise — but it's entirely possible to have one without the other.")

    st.subheader("🧰 Two Instrument Families")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            '<div class="app-card"><b>Measuring Instruments</b> — sense an existing electrical '
            'quantity and report it: voltmeters, ammeters, ohmmeters, oscilloscopes, wattmeters, '
            'frequency counters, LCR meters, galvanometers.</div>',
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            '<div class="app-card"><b>Source Instruments</b> — generate a controlled electrical '
            'quantity for testing purposes: function generators and bench power supplies.</div>',
            unsafe_allow_html=True,
        )

    st.success("👉 Head to **'Instruments Explorer'** in the sidebar to study each instrument in detail.")

# ============================================================================
# 2. INSTRUMENTS EXPLORER
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Instruments Explorer")
    st.caption("Expand each instrument to see its symbol/diagram, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in INSTRUMENT_ORDER:
        c = INSTRUMENTS[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_instrument_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Measures:** {c['measures']}")
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
# 3. MEASUREMENT CONCEPTS
# ============================================================================
elif page.startswith("📐"):
    st.header("📐 Measurement Concepts")
    st.caption("The core ideas that determine how much you can trust any measurement.")

    filter_names = st.multiselect(
        "Filter instruments by category",
        ["general_purpose", "voltage", "current", "resistance", "waveform", "power", "digital", "reactive", "source"],
        default=[],
    )
    if filter_names:
        filtered = [n for n in INSTRUMENT_ORDER if any(t in INSTRUMENTS[n]["category"] for t in filter_names)]
    else:
        filtered = INSTRUMENT_ORDER

    st.subheader("🧮 Instrument Reference Table")
    rows = []
    for name in filtered:
        c = INSTRUMENTS[name]
        rows.append({
            "Instrument": name,
            "Measures": c["measures"],
            "Connection": c["connection"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Key Measurement Concepts")
    for concept_name in MEASUREMENT_CONCEPT_ORDER:
        m = MEASUREMENT_CONCEPTS[concept_name]
        with st.expander(f"**{concept_name}** — {m['meaning']}"):
            st.markdown(f"**In plain English:** {m['explanation']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any instrument with an interactive model and experiment with its behaviour.")

    simulatable = [n for n in INSTRUMENT_ORDER if INSTRUMENTS[n]["calc_key"] is not None]
    sel = st.selectbox("Select an instrument", simulatable)
    c = INSTRUMENTS[sel]

    st.markdown(
        flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #0369a1, #075985);">'
             f'📏 <b>{sel}</b> &nbsp;|&nbsp; {c["measures"]}</div>'),
        unsafe_allow_html=True,
    )

    col_symbol, col_calc = st.columns([1, 1.6])
    with col_symbol:
        st.markdown("##### 🔷 Symbol / Diagram")
        st.markdown(f'<div class="symbol-box">{draw_instrument_svg(sel)}</div>', unsafe_allow_html=True)
        st.markdown(f"**Connection:** {c['connection']}")
    with col_calc:
        CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how measuring instruments are used across different fields.")

    APPLICATIONS = [
        ("🔧 Electronics Repair", "Multimeters diagnose faulty components; oscilloscopes reveal signal problems invisible to a multimeter; logic probes quickly trace digital circuit faults."),
        ("🚗 Automotive Diagnostics", "Multimeters check battery and alternator voltage; oscilloscopes analyse sensor waveforms and ignition timing; specialised meters test spark plug performance."),
        ("⚡ Power Quality Analysis", "Wattmeters and power analysers measure real power consumption and efficiency; oscilloscopes detect voltage sag, spikes, and harmonic distortion on the mains supply."),
        ("🏥 Medical Diagnostics", "Instruments built on the same voltmeter/oscilloscope principles record tiny bioelectric signals — ECG machines are essentially specialised, highly sensitive oscilloscopes."),
        ("🏭 Industrial Calibration", "LCR meters and precision multimeters are regularly calibrated against certified reference standards to keep manufacturing quality control trustworthy."),
        ("📡 Telecommunications", "Frequency counters verify oscillator and transmitter accuracy; spectrum-analysis tools (built on similar principles) check that signals stay within their licensed frequency bands."),
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
    st.header("📝 Measurements & Instruments Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Instruments Explorer' section and try again!")

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
