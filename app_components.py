"""
⚡ Electronic Components Learning Lab
An Interactive Beginner's Guide to Electronic Components

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
    page_title="Electronic Components Learning Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# NOTE: every HTML string below is written on a SINGLE physical line where it
# matters (no blank lines inside a block) — Streamlit's Markdown renderer
# treats a blank line inside an HTML block as the end of that block, and
# anything after gets shown as literal text instead of being rendered.
# ============================================================================
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}

    .concept-card {
        background: linear-gradient(135deg, #0e4d64, #075985);
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
        font-family: monospace;
        font-size: 1.05rem;
        white-space: pre;
        line-height: 1.4;
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
# CORE PHYSICS CALCULATIONS (pure functions, no widgets — reused everywhere)
# ============================================================================

def ohms_law_solve(v=None, i=None, r=None):
    """Given exactly two of (voltage, current, resistance), solve the third.
    Returns (result_value, result_label) or (None, error_message)."""
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


def capacitor_energy(capacitance_uF, voltage_v):
    """E = 1/2 C V^2. Capacitance given in microfarads, returns Joules."""
    c_farads = capacitance_uF * 1e-6
    energy_j = 0.5 * c_farads * (voltage_v ** 2)
    charge_c = c_farads * voltage_v
    return energy_j, charge_c


def inductor_energy(inductance_mH, current_a):
    """E = 1/2 L I^2. Inductance given in millihenries, returns Joules."""
    l_henries = inductance_mH * 1e-3
    return 0.5 * l_henries * (current_a ** 2)


def transformer_secondary_voltage(vp, np_turns, ns_turns):
    """Ideal transformer relationship: Vs / Vp = Ns / Np."""
    if np_turns in (None, 0):
        return None
    return vp * (ns_turns / np_turns)


def led_current_ma(vs, vf, r_ohm):
    """I = (Vs - Vf) / R, returned in milliamps. None if invalid."""
    if r_ohm in (None, 0):
        return None
    drop = vs - vf
    if drop <= 0:
        return 0.0
    return (drop / r_ohm) * 1000.0


def fuse_is_blown(current_a, rating_a):
    return current_a > rating_a


def thermistor_resistance_ohm(kind, temp_c):
    """Simplified, illustrative model only — NOT a real physical formula.
    NTC: resistance falls as temperature rises.
    PTC: resistance rises as temperature rises.
    Baseline 10,000 ohms at 25 degrees C."""
    baseline = 10000
    delta = temp_c - 25
    if kind == "NTC":
        r = baseline * (0.97 ** delta)
    else:
        r = baseline * (1.03 ** delta)
    return max(r, 50)


def ldr_resistance_ohm(light_pct):
    """Simplified, illustrative model only. 0% = dark (high resistance),
    100% = bright (low resistance)."""
    dark_r = 100000
    bright_r = 100
    fraction = light_pct / 100.0
    return dark_r - (dark_r - bright_r) * fraction


def regulator_can_supply(vin, desired_vout, dropout=2.0):
    """Simplified educational model: a linear regulator typically needs the
    input to exceed the desired output by a minimum 'dropout' voltage."""
    return vin >= (desired_vout + dropout)


def opamp_comparator_output(v_plus, v_minus):
    return "HIGH" if v_plus > v_minus else "LOW"


# ============================================================================
# COMPONENT DATA
# 16 components, each with the fields the Explorer / Comparison pages need.
# "calc_key" links a component to its interactive render function below.
# ============================================================================
COMPONENTS = {
    "Resistor": {
        "symbol": "──/\\/\\/\\/──",
        "desc": "A component that limits (resists) the flow of electric current.",
        "function": "Controls how much current flows in a circuit.",
        "unit": "Ohm (Ω)",
        "common_values": "10 Ω – 1 MΩ",
        "applications": "Current limiting, voltage division, LED protection, pull-up/pull-down circuits.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": True,
        "category": ["passive", "controls_current"],
        "explanation": "Think of a resistor as a narrow section of pipe: it doesn't stop water (current) but it slows it down. The higher the resistance, the more it restricts current for a given voltage.",
        "safety": "Resistors can get hot if they dissipate more power than their rating allows. Always check the power rating (in watts) for the circuit.",
        "calc_key": "resistor",
    },
    "Capacitor": {
        "symbol": "──| |──",
        "desc": "A component that stores electrical energy in an electric field between two plates.",
        "function": "Stores and releases electrical energy; smooths and filters signals.",
        "unit": "Farad (F), usually µF, nF, or pF",
        "common_values": "1 pF – 1000 µF",
        "applications": "Power supply smoothing, timing circuits, signal filtering, energy storage.",
        "type": "Passive",
        "stores_energy": True,
        "controls_current": False,
        "category": ["passive", "energy_storage", "filtering"],
        "explanation": "Imagine a small water tank connected to a pipe. It fills up (charges) when there's extra water pressure and releases water (discharges) when the pressure drops. A capacitor's voltage cannot change instantly.",
        "safety": "Large capacitors can retain a dangerous charge even after power is removed. Never touch capacitor terminals without discharging them safely.",
        "calc_key": "capacitor",
    },
    "Inductor": {
        "symbol": "──UUUU──",
        "desc": "A coil of wire that stores energy in a magnetic field when current flows through it.",
        "function": "Stores energy magnetically; opposes sudden changes in current.",
        "unit": "Henry (H), usually mH or µH",
        "common_values": "1 µH – 1 H",
        "applications": "Filtering, energy storage in power converters, transformers, chokes.",
        "type": "Passive",
        "stores_energy": True,
        "controls_current": False,
        "category": ["passive", "energy_storage", "filtering"],
        "explanation": "An inductor is like a heavy flywheel in a water system: it resists sudden changes in flow (current). Once flowing, it wants to keep flowing; once stopped, it resists starting again.",
        "safety": "Inductors can produce voltage spikes when current is suddenly interrupted. Circuits often include protection diodes near inductive loads (e.g. relay coils).",
        "calc_key": "inductor",
    },
    "Diode": {
        "symbol": "──▷|──",
        "desc": "A component that allows current to flow easily in one direction only.",
        "function": "Restricts current to a single direction (rectification, protection).",
        "unit": "Rated in volts (max reverse) and amps (max forward current)",
        "common_values": "Forward voltage drop ≈ 0.6–0.7 V (silicon)",
        "applications": "AC-to-DC rectification, reverse-polarity protection, signal demodulation.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": True,
        "category": ["active", "controls_current", "protection"],
        "explanation": "A diode behaves somewhat like a one-way valve for current — it lets current pass in the forward direction but blocks it in reverse. (This analogy is simplified; a real diode still allows a tiny leakage current in reverse.)",
        "safety": "Exceeding a diode's reverse voltage or forward current rating can permanently damage it.",
        "calc_key": "diode",
    },
    "LED": {
        "symbol": "  ↘ ↘\n──▷|──",
        "desc": "Light Emitting Diode — a diode that emits light when current flows through it in the forward direction.",
        "function": "Converts electrical energy directly into light.",
        "unit": "Forward voltage typically 1.8 V – 3.3 V depending on colour",
        "common_values": "Typical operating current: 10–20 mA",
        "applications": "Indicator lights, displays, general lighting, optical communication.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": False,
        "category": ["active", "indicator"],
        "explanation": "An LED only lights up when connected the correct way round (forward biased) and needs a resistor in series to limit current — without one, it can draw too much current and burn out almost instantly.",
        "safety": "Always use a current-limiting resistor with an LED. Never connect an LED directly across a battery.",
        "calc_key": "led",
    },
    "Transistor": {
        "symbol": "      C\n      |\n  B──◁\n      |\n      E",
        "desc": "A semiconductor device used to switch or amplify electronic signals.",
        "function": "Acts as an electrically-controlled switch or amplifier.",
        "unit": "Rated in volts, amps, and gain (hFE)",
        "common_values": "Base-emitter turn-on voltage ≈ 0.6–0.7 V (BJT)",
        "applications": "Digital switching, signal amplification, the building block of all modern ICs.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": True,
        "category": ["active", "switching", "amplification"],
        "explanation": "Think of a transistor as a tap controlled by a tiny signal: a small current or voltage at the Base terminal controls a much larger current flowing between Collector and Emitter.",
        "safety": "Transistors can overheat if operated beyond their rated current or voltage. Heat sinks are often required for power transistors.",
        "calc_key": "transistor",
    },
    "Transformer": {
        "symbol": "──)||(──",
        "desc": "A device that transfers electrical energy between two coils using a shared magnetic field, changing voltage in the process.",
        "function": "Steps AC voltage up or down between a primary and secondary coil.",
        "unit": "Rated by voltage, turns ratio, and power (VA)",
        "common_values": "Common ratios: 230V:12V, 230V:9V, etc.",
        "applications": "Power adapters, mains isolation, voltage step-up/step-down, audio matching.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": False,
        "category": ["passive", "voltage_conversion"],
        "explanation": "A transformer only works with AC (alternating current) because it relies on a *changing* magnetic field to transfer energy between coils — it cannot step DC voltage up or down.",
        "safety": "⚠️ Transformers connected to mains electricity involve dangerous voltages. Never open or experiment with mains transformers without qualified supervision.",
        "calc_key": "transformer",
    },
    "Potentiometer": {
        "symbol": "──/\\/\\/\\/──\n      ↑",
        "desc": "A variable resistor with three terminals, used to create an adjustable voltage divider.",
        "function": "Allows manual adjustment of resistance or output voltage.",
        "unit": "Ohm (Ω)",
        "common_values": "1 kΩ – 1 MΩ",
        "applications": "Volume controls, brightness dimmers, sensor calibration, joystick position sensing.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": True,
        "category": ["passive", "adjustment", "controls_current"],
        "explanation": "A potentiometer is like a resistor with a sliding tap: moving the slider changes how much resistance is between the tap and each end, letting you 'dial in' a voltage or resistance value.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "potentiometer",
    },
    "Switch": {
        "symbol": "──o  o──",
        "desc": "A mechanical device that opens or closes a circuit path.",
        "function": "Manually connects or disconnects current flow.",
        "unit": "Rated by voltage and current (e.g. 250V, 5A)",
        "common_values": "N/A",
        "applications": "Power on/off control, mode selection, safety isolation.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": True,
        "category": ["passive", "switching"],
        "explanation": "When a switch is open, the circuit path is broken and no current can flow — like a gap in a pipe. When closed, the path is complete and current can flow freely (limited only by the rest of the circuit).",
        "safety": "Ensure switches are rated for the voltage and current of the circuit they control.",
        "calc_key": "switch",
    },
    "Fuse": {
        "symbol": "──[~]──",
        "desc": "A safety device that breaks the circuit if current exceeds a safe level.",
        "function": "Protects circuits and wiring from overcurrent damage or fire.",
        "unit": "Amp (A) rating",
        "common_values": "0.5 A – 30 A depending on application",
        "applications": "Power supply protection, appliance protection, automotive circuits.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": False,
        "category": ["passive", "protection"],
        "explanation": "A fuse contains a thin wire that heats up and melts ('blows') if too much current passes through it, breaking the circuit before wires overheat or catch fire.",
        "safety": "⚠️ Always replace a blown fuse with one of the SAME rating. Never bridge or bypass a fuse — this removes vital protection.",
        "calc_key": "fuse",
    },
    "Thermistor": {
        "symbol": "──/\\/\\/\\/──\n     t°",
        "desc": "A resistor whose resistance changes significantly with temperature.",
        "function": "Senses temperature by converting it into a measurable resistance change.",
        "unit": "Ohm (Ω), rated at a reference temperature (usually 25°C)",
        "common_values": "Typically 1 kΩ – 100 kΩ at 25°C",
        "applications": "Temperature sensing, overheat protection, inrush current limiting.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": False,
        "category": ["passive", "sensing"],
        "explanation": "NTC (Negative Temperature Coefficient) thermistors decrease in resistance as temperature rises. PTC (Positive Temperature Coefficient) thermistors increase in resistance as temperature rises.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "thermistor",
    },
    "LDR": {
        "symbol": "  ↘ ↘\n──/\\/\\/\\/──",
        "desc": "Light Dependent Resistor — a resistor whose resistance changes with light intensity.",
        "function": "Senses light level by converting it into a measurable resistance change.",
        "unit": "Ohm (Ω)",
        "common_values": "~200 Ω (bright light) to >1 MΩ (darkness)",
        "applications": "Automatic street lighting, light meters, dark-activated alarms.",
        "type": "Passive",
        "stores_energy": False,
        "controls_current": False,
        "category": ["passive", "sensing"],
        "explanation": "An LDR's resistance falls as more light hits it, and rises in darkness — this makes it useful for circuits that need to 'notice' whether it's light or dark.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "ldr",
    },
    "Voltage Regulator": {
        "symbol": "──[ REG ]──",
        "desc": "A device that maintains a steady, fixed output voltage regardless of small changes in input voltage or load.",
        "function": "Provides a stable voltage supply for sensitive circuits.",
        "unit": "Rated output voltage (e.g. 5V, 3.3V) and max current",
        "common_values": "Common fixed outputs: 3.3V, 5V, 9V, 12V",
        "applications": "Powering microcontrollers, sensors, and ICs from a less stable supply (e.g. batteries).",
        "type": "Active",
        "stores_energy": False,
        "controls_current": False,
        "category": ["active", "protection", "voltage_conversion"],
        "explanation": "A voltage regulator is like a pressure-reducing valve: even if the input pressure (voltage) varies, the output stays steady — as long as the input is high enough above the desired output.",
        "safety": "Regulators can overheat if made to dissipate too much power (large input-to-output voltage difference at high current). Heat sinks are often required.",
        "calc_key": "regulator",
    },
    "Operational Amplifier": {
        "symbol": "V+──┐\n     ▷──Out\nV-──┘",
        "desc": "A high-gain amplifier with two inputs (inverting and non-inverting) and one output.",
        "function": "Amplifies the difference between its two input voltages; used for amplification, filtering, and comparison.",
        "unit": "Rated by supply voltage and gain-bandwidth product",
        "common_values": "N/A — behaviour depends on surrounding circuit",
        "applications": "Audio amplifiers, signal conditioning, comparators, active filters, instrumentation.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": False,
        "category": ["active", "amplification"],
        "explanation": "An op-amp constantly compares its two inputs. In a simple comparator setup, if the '+' input is higher than the '-' input, the output swings HIGH; otherwise it swings LOW.",
        "safety": "No special hazards beyond general low-voltage handling.",
        "calc_key": "opamp",
    },
    "Integrated Circuit": {
        "symbol": "┌────────┐\n│  IC    │\n└────────┘",
        "desc": "A complete miniature circuit — containing many transistors, resistors, and other components — built onto a single chip of semiconductor material.",
        "function": "Packs complex functionality (logic, memory, amplification, processing) into one small package.",
        "unit": "N/A — behaviour depends on the specific IC",
        "common_values": "N/A",
        "applications": "Microprocessors, memory chips, timers (e.g. 555 timer), logic gate chips, op-amps in IC form.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": False,
        "category": ["active", "complex"],
        "explanation": "Instead of wiring together dozens of individual transistors and resistors by hand, engineers design them all onto one tiny silicon chip — an IC. This is why devices like smartphones can be so small and powerful.",
        "safety": "Many ICs are sensitive to static electricity (ESD) and incorrect supply voltage — always check the datasheet before use.",
        "calc_key": None,
    },
    "Relay": {
        "symbol": "Coil:    ──(( ))──\nContact: ──o   o──",
        "desc": "An electromagnetic switch: a small control current energises a coil, which mechanically opens or closes a separate, often higher-power, contact circuit.",
        "function": "Lets a small control signal switch a much larger circuit safely.",
        "unit": "Rated coil voltage and contact current rating",
        "common_values": "Coil voltages: 5V, 12V, 24V; contacts often rated several amps",
        "applications": "Automotive circuits (headlights, starter motors), home automation, industrial control panels.",
        "type": "Active",
        "stores_energy": False,
        "controls_current": True,
        "category": ["active", "switching"],
        "explanation": "A relay is like a tiny electric hand: energising its coil physically pulls a switch contact closed (or open), letting a low-power circuit safely control a high-power one — with no direct electrical connection between the two.",
        "safety": "Relay coils can produce voltage spikes when switched off; protection diodes are commonly used across the coil.",
        "calc_key": "relay",
    },
}

COMPONENT_ORDER = list(COMPONENTS.keys())

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style schematic diagrams for every component (replaces the
# old ASCII-art symbols). Built the same safe way as the Logic Gates app:
# every returned string is flattened to one line with flat() so Streamlit's
# Markdown renderer never mis-parses an embedded blank line as the end of
# the HTML block.
# ============================================================================
COMPONENT_COLORS = {
    "Resistor": "#3b82f6",
    "Capacitor": "#8b5cf6",
    "Inductor": "#f59e0b",
    "Diode": "#ef4444",
    "LED": "#eab308",
    "Transistor": "#14b8a6",
    "Transformer": "#6366f1",
    "Potentiometer": "#0ea5e9",
    "Switch": "#22c55e",
    "Fuse": "#dc2626",
    "Thermistor": "#fb923c",
    "LDR": "#a3e635",
    "Voltage Regulator": "#0891b2",
    "Operational Amplifier": "#ec4899",
    "Integrated Circuit": "#7c3aed",
    "Relay": "#059669",
}


def _lead(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111827" stroke-width="4"/>'


def draw_component_svg(name):
    """Return a flattened, single-line SVG schematic symbol for a component."""
    color = COMPONENT_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Resistor":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 L72,45 L88,95 L104,45 L120,95 L136,45 L150,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        """

    elif name == "Capacitor":
        body = f"""
        {_lead(0, 70, 95, 70)}
        <line x1="95" y1="25" x2="95" y2="115" stroke="{color}" stroke-width="6"/>
        <line x1="105" y1="25" x2="105" y2="115" stroke="{color}" stroke-width="6"/>
        {_lead(105, 70, 220, 70)}
        """

    elif name == "Inductor":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 A10,20 0 0 1 80,70 A10,20 0 0 1 100,70 A10,20 0 0 1 120,70 A10,20 0 0 1 140,70 A10,20 0 0 1 150,70"
              fill="none" stroke="{color}" stroke-width="4"/>
        {_lead(150, 70, 220, 70)}
        """

    elif name == "Diode":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <line x1="130" y1="35" x2="130" y2="105" stroke="{color}" stroke-width="6"/>
        {_lead(130, 70, 220, 70)}
        """

    elif name == "LED":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,35 L60,105 L130,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        <line x1="130" y1="35" x2="130" y2="105" stroke="{color}" stroke-width="6"/>
        {_lead(130, 70, 220, 70)}
        <line x1="95" y1="25" x2="115" y2="5" stroke="{color}" stroke-width="3"/>
        <polygon points="115,5 106,7 113,14" fill="{color}"/>
        <line x1="115" y1="35" x2="135" y2="15" stroke="{color}" stroke-width="3"/>
        <polygon points="135,15 126,17 133,24" fill="{color}"/>
        """

    elif name == "Transistor":
        body = f"""
        <circle cx="110" cy="70" r="45" fill="none" stroke="{color}" stroke-width="3"/>
        {_lead(0, 70, 90, 70)}
        <line x1="90" y1="45" x2="90" y2="95" stroke="{color}" stroke-width="5"/>
        <line x1="90" y1="55" x2="140" y2="30" stroke="{color}" stroke-width="4"/>
        <line x1="140" y1="30" x2="140" y2="10" stroke="{color}" stroke-width="4"/>
        <line x1="90" y1="85" x2="140" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="140" y1="110" x2="140" y2="130" stroke="{color}" stroke-width="4"/>
        <polygon points="140,110 122,100 126,114" fill="{color}"/>
        <text x="145" y="14" font-size="14" font-weight="bold" fill="#111827">C</text>
        <text x="94" y="63" font-size="14" font-weight="bold" fill="#111827">B</text>
        <text x="145" y="134" font-size="14" font-weight="bold" fill="#111827">E</text>
        """

    elif name == "Transformer":
        body = f"""
        {_lead(0, 40, 65, 40)}
        {_lead(0, 100, 65, 100)}
        <path d="M65,40 A12,15 0 0 1 65,70 A12,15 0 0 1 65,100"
              fill="none" stroke="{color}" stroke-width="4"/>
        <line x1="100" y1="25" x2="100" y2="115" stroke="{color}" stroke-width="4"/>
        <line x1="108" y1="25" x2="108" y2="115" stroke="{color}" stroke-width="4"/>
        <path d="M155,40 A12,15 0 0 0 155,70 A12,15 0 0 0 155,100"
              fill="none" stroke="{color}" stroke-width="4"/>
        {_lead(155, 40, 220, 40)}
        {_lead(155, 100, 220, 100)}
        <text x="72" y="20" font-size="13" font-weight="bold" fill="#111827">Primary</text>
        <text x="118" y="20" font-size="13" font-weight="bold" fill="#111827">Secondary</text>
        """

    elif name == "Potentiometer":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 L72,45 L88,95 L104,45 L120,95 L136,45 L150,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        <line x1="105" y1="115" x2="105" y2="55" stroke="{color}" stroke-width="4"/>
        <polygon points="105,55 97,68 113,68" fill="{color}"/>
        {_lead(105, 115, 105, 130)}
        """

    elif name == "Switch":
        body = f"""
        {_lead(0, 70, 55, 70)}
        <circle cx="58" cy="70" r="5" fill="{color}"/>
        <line x1="58" y1="70" x2="140" y2="42" stroke="{color}" stroke-width="4"/>
        <circle cx="150" cy="70" r="5" fill="{color}"/>
        {_lead(150, 70, 220, 70)}
        """

    elif name == "Fuse":
        body = f"""
        {_lead(0, 70, 55, 70)}
        <rect x="55" y="50" width="110" height="40" rx="20" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <line x1="60" y1="70" x2="160" y2="70" stroke="{color}" stroke-width="3"/>
        {_lead(165, 70, 220, 70)}
        """

    elif name == "Thermistor":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 L72,50 L88,90 L104,50 L120,90 L136,50 L150,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        <line x1="55" y1="105" x2="165" y2="35" stroke="{color}" stroke-width="3"/>
        <text x="168" y="30" font-size="15" font-weight="bold" fill="#111827">t°</text>
        """

    elif name == "LDR":
        body = f"""
        {_lead(0, 70, 45, 70)}
        <circle cx="110" cy="70" r="55" fill="none" stroke="{color}" stroke-width="3"/>
        <path d="M65,70 L77,52 L93,88 L109,52 L125,88 L141,52 L155,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(175, 70, 220, 70)}
        <line x1="85" y1="15" x2="70" y2="0" stroke="{color}" stroke-width="3"/>
        <polygon points="70,0 74,10 80,4" fill="{color}"/>
        <line x1="110" y1="10" x2="110" y2="-6" stroke="{color}" stroke-width="3"/>
        <polygon points="110,-6 105,4 115,4" fill="{color}"/>
        """

    elif name == "Voltage Regulator":
        body = f"""
        {_lead(0, 55, 60, 55)}
        <rect x="60" y="25" width="100" height="60" rx="8" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="75" y="60" font-size="16" font-weight="bold" fill="#111827">REG</text>
        {_lead(160, 55, 220, 55)}
        {_lead(110, 85, 110, 130)}
        <text x="10" y="45" font-size="13" font-weight="bold" fill="#111827">IN</text>
        <text x="175" y="45" font-size="13" font-weight="bold" fill="#111827">OUT</text>
        <text x="115" y="128" font-size="13" font-weight="bold" fill="#111827">GND</text>
        """

    elif name == "Operational Amplifier":
        body = f"""
        {_lead(0, 45, 55, 45)}
        {_lead(0, 95, 55, 95)}
        <path d="M55,20 L55,120 L150,70 Z" fill="{color}22" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        <text x="65" y="50" font-size="18" font-weight="bold" fill="#111827">+</text>
        <text x="65" y="100" font-size="18" font-weight="bold" fill="#111827">−</text>
        """

    elif name == "Integrated Circuit":
        body = f"""
        <rect x="60" y="30" width="100" height="80" rx="4" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <path d="M95,30 A15,15 0 0 0 125,30" fill="none" stroke="{color}" stroke-width="3"/>
        <text x="88" y="78" font-size="16" font-weight="bold" fill="#111827">IC</text>
        {_lead(0, 45, 60, 45)}
        {_lead(0, 70, 60, 70)}
        {_lead(0, 95, 60, 95)}
        {_lead(160, 45, 220, 45)}
        {_lead(160, 70, 220, 70)}
        {_lead(160, 95, 220, 95)}
        """

    elif name == "Relay":
        body = f"""
        {_lead(0, 40, 40, 40)}
        {_lead(0, 100, 40, 100)}
        <path d="M40,40 A8,15 0 0 1 40,70 A8,15 0 0 1 40,100"
              fill="none" stroke="{color}" stroke-width="4"/>
        <rect x="55" y="15" width="8" height="110" fill="{color}"/>
        <line x1="80" y1="35" x2="80" y2="105" stroke="{color}" stroke-width="1.5" stroke-dasharray="4,4"/>
        <circle cx="120" cy="70" r="5" fill="{color}"/>
        <line x1="120" y1="70" x2="180" y2="45" stroke="{color}" stroke-width="4"/>
        <circle cx="185" cy="70" r="5" fill="{color}"/>
        {_lead(100, 70, 120, 70)}
        {_lead(185, 70, 220, 70)}
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)



# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same component is rendered on more than one page.
# ============================================================================

def render_resistor_calc(key_prefix):
    st.markdown("**⚙️ Ohm's Law Calculator** — `V = I × R`")
    solve_for = st.radio(
        "Solve for:", ["Voltage (V)", "Current (I)", "Resistance (R)"],
        horizontal=True, key=f"{key_prefix}_res_solve",
    )
    c1, c2 = st.columns(2)
    if solve_for == "Voltage (V)":
        i = c1.number_input("Current (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_res_i")
        r = c2.number_input("Resistance (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_res_r")
        result, label = ohms_law_solve(i=i, r=r)
    elif solve_for == "Current (I)":
        v = c1.number_input("Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_res_v")
        r = c2.number_input("Resistance (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_res_r2")
        result, label = ohms_law_solve(v=v, r=r)
    else:
        v = c1.number_input("Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_res_v2")
        i = c2.number_input("Current (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_res_i2")
        result, label = ohms_law_solve(v=v, i=i)

    if result is None:
        st.warning(f"⚠️ {label}")
    else:
        st.markdown(f'<div class="status-good">✅ {label} = {result:.3f}</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        currents = [x * 0.05 for x in range(21)]
        r_plot = r if solve_for != "Resistance (R)" else (result if result else 100)
        voltages = [i_val * r_plot for i_val in currents]
        ax.plot(currents, voltages, color="#38bdf8", linewidth=2)
        ax.set_xlabel("Current (A)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title(f"V vs I  (R = {r_plot:.1f} Ω)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)


def render_capacitor_calc(key_prefix):
    st.markdown("**⚙️ Capacitor Energy Calculator** — `E = ½CV²`")
    c1, c2 = st.columns(2)
    cap_uf = c1.number_input("Capacitance (µF)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_cap_c")
    volt = c2.number_input("Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_cap_v")
    energy_j, charge_c = capacitor_energy(cap_uf, volt)
    st.markdown(
        f'<div class="status-good">✅ Stored Energy = {energy_j*1000:.4f} mJ &nbsp;|&nbsp; Stored Charge = {charge_c*1000:.4f} mC</div>',
        unsafe_allow_html=True,
    )
    st.caption("Conceptual charging curve — voltage rises quickly at first, then levels off as the capacitor fills.")
    fig, ax = plt.subplots(figsize=(4.5, 3))
    t = [x * 0.1 for x in range(50)]
    v_curve = [volt * (1 - 2.71828 ** (-x)) for x in t]
    ax.plot(t, v_curve, color="#4ade80", linewidth=2)
    ax.set_xlabel("Time (relative units)")
    ax.set_ylabel("Capacitor Voltage (V)")
    ax.set_title("Conceptual Charging Curve")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_inductor_calc(key_prefix):
    st.markdown("**⚙️ Inductor Energy Calculator** — `E = ½LI²`")
    c1, c2 = st.columns(2)
    ind_mh = c1.number_input("Inductance (mH)", min_value=0.0, value=10.0, step=1.0, key=f"{key_prefix}_ind_l")
    curr = c2.number_input("Current (A)", min_value=0.0, value=1.0, step=0.1, key=f"{key_prefix}_ind_i")
    energy_j = inductor_energy(ind_mh, curr)
    st.markdown(f'<div class="status-good">✅ Stored Energy = {energy_j*1000:.4f} mJ</div>', unsafe_allow_html=True)


def render_diode_sim(key_prefix):
    st.markdown("**⚙️ Diode Bias Simulator**")
    bias = st.radio("Bias condition:", ["Forward biased", "Reverse biased"], horizontal=True, key=f"{key_prefix}_diode_bias")
    if bias == "Forward biased":
        st.markdown('<div class="status-good">✅ Diode is CONDUCTING — current flows through.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-bad">⛔ Diode is NOT CONDUCTING — current is blocked.</div>', unsafe_allow_html=True)


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
        st.markdown(f'<div class="status-bad">⚠️ Calculated current is {current_ma:.1f} mA — too high! This resistor value is likely to damage the LED. Increase R.</div>', unsafe_allow_html=True)
    else:
        bulb_class = "bulb-on"
        st.markdown(f'<div class="bulb-wrap"><div class="{bulb_class}"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-good">🟢 LED ON — Current = {current_ma:.2f} mA (a safe, typical range is roughly 10–20 mA)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="safety-note">⚠️ Safety: This is an educational calculation only. Never connect an LED without a resistor, and never experiment with mains electricity.</div>',
        unsafe_allow_html=True,
    )


def render_transistor_sim(key_prefix):
    st.markdown("**⚙️ Transistor Switch Simulator**")
    c1, c2 = st.columns(2)
    base_signal = c1.radio("Base signal:", ["LOW", "HIGH"], horizontal=True, key=f"{key_prefix}_trans_base")
    supply_ok = c2.radio("Supply condition:", ["Supply present", "No supply"], horizontal=True, key=f"{key_prefix}_trans_supply")
    is_on = (base_signal == "HIGH") and (supply_ok == "Supply present")
    if is_on:
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-good">✅ Transistor is ON — current flows from Collector to Emitter.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bulb-wrap"><div class="bulb-off"></div></div>', unsafe_allow_html=True)
        reason = "the base signal is LOW" if base_signal == "LOW" else "there is no supply"
        st.markdown(f'<div class="status-bad">⛔ Transistor is OFF — because {reason}.</div>', unsafe_allow_html=True)


def render_transformer_calc(key_prefix):
    st.markdown("**⚙️ Ideal Transformer Calculator** — `Vs / Vp = Ns / Np`")
    c1, c2, c3 = st.columns(3)
    vp = c1.number_input("Primary Voltage (V)", min_value=0.0, value=230.0, step=1.0, key=f"{key_prefix}_tf_vp")
    np_turns = c2.number_input("Primary Turns (Np)", min_value=1, value=1000, step=10, key=f"{key_prefix}_tf_np")
    ns_turns = c3.number_input("Secondary Turns (Ns)", min_value=1, value=50, step=10, key=f"{key_prefix}_tf_ns")
    vs = transformer_secondary_voltage(vp, np_turns, ns_turns)
    st.markdown(f'<div class="status-good">✅ Secondary Voltage = {vs:.2f} V</div>', unsafe_allow_html=True)
    st.caption("This is the *ideal* transformer relationship — real transformers have small losses.")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(["Primary", "Secondary"], [vp, vs], color=["#38bdf8", "#4ade80"])
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Primary vs Secondary Voltage")
    st.pyplot(fig)
    plt.close(fig)


def render_potentiometer(key_prefix):
    st.markdown("**⚙️ Potentiometer Position**")
    pos = st.slider("Wiper position", 0, 100, 50, format="%d%%", key=f"{key_prefix}_pot")
    label = "Minimum" if pos == 0 else ("Maximum" if pos == 100 else "Adjustable middle position")
    st.markdown(f'<div class="status-good">✅ Position: {pos}% — {label}</div>', unsafe_allow_html=True)
    st.progress(pos / 100)


def render_switch_sim(key_prefix):
    st.markdown("**⚙️ Switch Simulator**")
    on = st.toggle("Switch state (ON = closed)", value=False, key=f"{key_prefix}_switch")
    if on:
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-good">✅ Circuit = CLOSED — current path AVAILABLE.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bulb-wrap"><div class="bulb-off"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-bad">⛔ Circuit = OPEN — current path BLOCKED.</div>', unsafe_allow_html=True)


def render_fuse_sim(key_prefix):
    st.markdown("**⚙️ Fuse Protection Simulator**")
    c1, c2 = st.columns(2)
    current = c1.number_input("Circuit Current (A)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_fuse_i")
    rating = c2.number_input("Fuse Rating (A)", min_value=0.1, value=3.0, step=0.5, key=f"{key_prefix}_fuse_r")
    if fuse_is_blown(current, rating):
        st.markdown('<div class="status-bad">🔴 FUSE BLOWN — current exceeded the rating, protecting the circuit.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-good">🟢 FUSE OK — current is within the safe rating.</div>', unsafe_allow_html=True)
    st.caption("Simplified educational model — real fuses also depend on how long the overcurrent lasts.")


def render_thermistor_sim(key_prefix):
    st.markdown("**⚙️ Thermistor Simulator** (simplified educational model)")
    c1, c2 = st.columns(2)
    kind = c1.radio("Type:", ["NTC", "PTC"], horizontal=True, key=f"{key_prefix}_therm_kind")
    temp = c2.slider("Temperature (°C)", -20, 120, 25, key=f"{key_prefix}_therm_temp")
    r = thermistor_resistance_ohm(kind, temp)
    st.markdown(f'<div class="status-good">✅ Approximate Resistance ≈ {r:,.0f} Ω</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    temps = list(range(-20, 121, 5))
    curve = [thermistor_resistance_ohm(kind, t) for t in temps]
    ax.plot(temps, curve, color="#f59e0b", linewidth=2)
    ax.scatter([temp], [r], color="#ef4444", zorder=5)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Resistance (Ω)")
    ax.set_title(f"{kind} Resistance vs Temperature (conceptual)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_ldr_sim(key_prefix):
    st.markdown("**⚙️ LDR Simulator** (simplified educational model)")
    light = st.slider("Light level: Dark ← → Bright", 0, 100, 50, key=f"{key_prefix}_ldr_light")
    r = ldr_resistance_ohm(light)
    st.markdown(f'<div class="status-good">✅ Approximate Resistance ≈ {r:,.0f} Ω</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    levels = list(range(0, 101, 5))
    curve = [ldr_resistance_ohm(x) for x in levels]
    ax.plot(levels, curve, color="#facc15", linewidth=2)
    ax.scatter([light], [r], color="#ef4444", zorder=5)
    ax.set_xlabel("Light Level (%)")
    ax.set_ylabel("Resistance (Ω)")
    ax.set_title("LDR Resistance vs Light Level (conceptual)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_regulator_sim(key_prefix):
    st.markdown("**⚙️ Voltage Regulator Simulator** (simplified educational model)")
    c1, c2 = st.columns(2)
    vin = c1.number_input("Input Voltage (V)", min_value=0.0, value=9.0, step=0.5, key=f"{key_prefix}_reg_vin")
    vout = c2.number_input("Desired Output Voltage (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_reg_vout")
    if regulator_can_supply(vin, vout):
        st.markdown(f'<div class="status-good">✅ Regulator CAN supply a stable {vout:.1f} V output.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-bad">⛔ Input voltage is too close to (or below) the desired output. This simplified model assumes at least a 2 V "dropout" margin is needed.</div>', unsafe_allow_html=True)
    st.caption("Real regulator behaviour depends on the exact device's datasheet specifications.")


def render_opamp_sim(key_prefix):
    st.markdown("**⚙️ Op-Amp Comparator Simulator**")
    c1, c2 = st.columns(2)
    vp = c1.number_input("Non-inverting input V+ (V)", value=2.5, step=0.1, key=f"{key_prefix}_opamp_vp")
    vm = c2.number_input("Inverting input V− (V)", value=2.0, step=0.1, key=f"{key_prefix}_opamp_vm")
    out = opamp_comparator_output(vp, vm)
    if out == "HIGH":
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-good">✅ OUTPUT = HIGH (because V+ > V−)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bulb-wrap"><div class="bulb-off"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-bad">⛔ OUTPUT = LOW (because V+ ≤ V−)</div>', unsafe_allow_html=True)
    st.caption("Simplified comparator model — real op-amps have many more behaviours and configurations.")


def render_relay_sim(key_prefix):
    st.markdown("**⚙️ Relay Simulator**")
    coil_on = st.toggle("Coil energised (ON)", value=False, key=f"{key_prefix}_relay_coil")
    if coil_on:
        st.markdown('<div class="bulb-wrap"><div class="bulb-on"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-good">✅ Contact = CLOSED — the controlled (load) circuit is connected.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bulb-wrap"><div class="bulb-off"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="status-bad">⛔ Contact = OPEN — the controlled (load) circuit is disconnected.</div>', unsafe_allow_html=True)


CALC_RENDERERS = {
    "resistor": render_resistor_calc,
    "capacitor": render_capacitor_calc,
    "inductor": render_inductor_calc,
    "diode": render_diode_sim,
    "led": render_led_calc,
    "transistor": render_transistor_sim,
    "transformer": render_transformer_calc,
    "potentiometer": render_potentiometer,
    "switch": render_switch_sim,
    "fuse": render_fuse_sim,
    "thermistor": render_thermistor_sim,
    "ldr": render_ldr_sim,
    "regulator": render_regulator_sim,
    "opamp": render_opamp_sim,
    "relay": render_relay_sim,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. What does a resistor do in a circuit?", "options": ["Stores light energy", "Limits current flow", "Generates AC voltage"], "answer": "Limits current flow"},
    {"q": "2. What is the unit of capacitance?", "options": ["Henry", "Ohm", "Farad"], "answer": "Farad"},
    {"q": "3. What does an inductor store energy in?", "options": ["A magnetic field", "A chemical reaction", "A light beam"], "answer": "A magnetic field"},
    {"q": "4. In which direction does a forward-biased diode allow current to flow?", "options": ["Only in reverse", "Easily, in the forward direction", "It blocks all current"], "answer": "Easily, in the forward direction"},
    {"q": "5. What must always be used with an LED to protect it?", "options": ["A capacitor", "A current-limiting resistor", "A transformer"], "answer": "A current-limiting resistor"},
    {"q": "6. A transistor can be used as a:", "options": ["Switch or amplifier", "Voltage source", "Magnetic field generator"], "answer": "Switch or amplifier"},
    {"q": "7. A transformer changes voltage using:", "options": ["Chemical energy", "A shared magnetic field between coils", "Direct current only"], "answer": "A shared magnetic field between coils"},
    {"q": "8. What happens when a switch is open?", "options": ["Current flows freely", "The circuit path is blocked", "The circuit shorts out"], "answer": "The circuit path is blocked"},
    {"q": "9. What is the purpose of a fuse?", "options": ["To amplify current", "To protect a circuit from overcurrent", "To store energy"], "answer": "To protect a circuit from overcurrent"},
    {"q": "10. An LDR's resistance falls when:", "options": ["Light level increases", "Temperature decreases", "Voltage is removed"], "answer": "Light level increases"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A circuit is not turning on. The switch is open.",
        "question": "What should you check first?",
        "options": ["Close the switch", "Increase the resistor value indefinitely", "Remove the power source"],
        "answer": "Close the switch",
        "explanation": "An open switch breaks the current path entirely. Closing it re-completes the circuit so current can flow again.",
    },
    {
        "scenario": "An LED circuit has no current because the diode (LED) is reverse biased.",
        "question": "What is the most likely fix?",
        "options": ["Reverse the LED's polarity so it is forward biased", "Add more resistors in series", "Increase the supply voltage"],
        "answer": "Reverse the LED's polarity so it is forward biased",
        "explanation": "Diodes (including LEDs) only conduct in the forward direction. If it's connected backwards, current simply won't flow — flipping it fixes the problem.",
    },
    {
        "scenario": "A fuse has blown because the current exceeded its rating.",
        "question": "What was the fuse designed to do in this situation?",
        "options": ["Amplify the current", "Protect the circuit by breaking the current path", "Store the excess energy"],
        "answer": "Protect the circuit by breaking the current path",
        "explanation": "This is exactly what a fuse is for — sacrificing itself to prevent dangerous overcurrent from damaging the rest of the circuit or wiring.",
    },
    {
        "scenario": "A capacitor-smoothed power supply still shows a lot of voltage ripple.",
        "question": "What component property most directly helps reduce ripple?",
        "options": ["A larger capacitance value", "A higher resistor value", "A faster switch"],
        "answer": "A larger capacitance value",
        "explanation": "A larger capacitor can store more charge and release it more steadily between charging pulses, smoothing out voltage ripple more effectively.",
    },
    {
        "scenario": "A relay-controlled motor won't start even though the control signal to the relay coil reads HIGH.",
        "question": "What is a sensible first thing to check?",
        "options": ["Whether the relay coil is actually receiving enough voltage/current to energise", "Whether the motor needs more paint", "Whether the LED indicator is the correct colour"],
        "answer": "Whether the relay coil is actually receiving enough voltage/current to energise",
        "explanation": "If the coil isn't properly energised (wrong voltage, broken wire, bad connection), the contact won't close no matter what the logic signal says.",
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
st.sidebar.title("⚡ ELECTRONIC COMPONENTS")
st.sidebar.subheader("LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore the components\n"
    "3. Try the calculators\n"
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
        "🔧 Components Explorer",
        "📊 Component Comparison",
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
st.title("⚡ Electronic Components Learning Lab")
st.caption("An Interactive Beginner's Guide to Electronic Components")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔧 Components Covered", len(COMPONENTS))
d2.metric("🧮 Interactive Calculators", len(CALC_RENDERERS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Electronic Components")

    st.markdown(
        """
        ### What is an Electronic Component?
        An **electronic component** is a physical part used in an electronic circuit to
        **control, store, transfer, or change** electrical energy or signals.

        Think of an electronic circuit like a team — each component has a particular job.
        A resistor limits current, a capacitor stores energy, a transistor switches signals —
        and together they work as a system to create something useful, like a radio,
        a phone charger, or a computer.
        """
    )

    st.subheader("🔋 Electricity Basics")
    st.write(
        "Before exploring individual components, it helps to understand a few core ideas — "
        "using a simple water-pipe analogy:"
    )
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>💧 Voltage</h4>'
            '<p>Like <b>pressure</b> pushing water through a pipe. '
            'Higher voltage pushes current through a circuit more strongly. Measured in Volts (V).</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>🌊 Current</h4>'
            '<p>Like the <b>amount of water flowing</b> through the pipe per second. '
            'Measured in Amperes (A).</p></div>',
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            '<div class="concept-card"><h4>🚧 Resistance</h4>'
            '<p>Like a <b>narrowing in the pipe</b> that restricts flow. '
            'Measured in Ohms (Ω).</p></div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "⚠️ Note: this water analogy is a simplified teaching tool — real electrical behaviour "
        "involves electric and magnetic fields, not literal fluid flow."
    )

    b4, b5 = st.columns(2)
    with b4:
        st.markdown(
            '<div class="concept-card"><h4>⚡ Power</h4>'
            '<p>The rate at which electrical energy is used or delivered. '
            'Power (Watts) = Voltage × Current.</p></div>',
            unsafe_allow_html=True,
        )
    with b5:
        st.markdown(
            '<div class="concept-card"><h4>🔌 Electrical Energy</h4>'
            '<p>The total amount of electrical work done over time — '
            'related to power multiplied by how long it acts.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("🟢🔵 Active vs Passive Components")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            '<div class="app-card"><b>Passive Components</b> — cannot amplify a signal or add '
            'energy on their own; they only store, dissipate, or redirect energy already present. '
            'Examples: Resistor, Capacitor, Inductor, Transformer.</div>',
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            '<div class="app-card"><b>Active Components</b> — can control or amplify current/voltage '
            'using an external power source, and can add gain to a signal. '
            'Examples: Diode, Transistor, Operational Amplifier, Integrated Circuit.</div>',
            unsafe_allow_html=True,
        )

    st.success("👉 Head to **'Components Explorer'** in the sidebar to study each component in detail.")

# ============================================================================
# 2. COMPONENTS EXPLORER
# ============================================================================
elif page.startswith("🔧"):
    st.header("🔧 Components Explorer")
    st.caption("Expand each component to see its symbol, key facts, explanation, and (where relevant) an interactive calculator.")

    for name in COMPONENT_ORDER:
        c = COMPONENTS[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_component_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Type:** {c['type']}")
                st.markdown(f"**Main Function:** {c['function']}")
                st.markdown(f"**Unit:** {c['unit']}")
                st.markdown(f"**Common Values:** {c['common_values']}")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")
                if c["safety"]:
                    st.markdown(f'<div class="safety-note">⚠️ {c["safety"]}</div>', unsafe_allow_html=True)

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. COMPONENT COMPARISON
# ============================================================================
elif page.startswith("📊"):
    st.header("📊 Component Comparison")
    st.caption("Select components to compare, or filter by category.")

    filter_tags = st.multiselect(
        "Filter by category",
        ["active", "passive", "energy_storage", "controls_current", "switching", "protection", "sensing"],
        default=[],
    )

    if filter_tags:
        filtered_names = [n for n in COMPONENT_ORDER if any(t in COMPONENTS[n]["category"] for t in filter_tags)]
    else:
        filtered_names = COMPONENT_ORDER

    selected = st.multiselect(
        "Select components to compare",
        filtered_names,
        default=filtered_names[:3] if len(filtered_names) >= 3 else filtered_names,
    )

    if selected:
        rows = []
        for name in selected:
            c = COMPONENTS[name]
            rows.append({
                "Component": name,
                "Main Function": c["function"],
                "Unit": c["unit"],
                "Active/Passive": c["type"],
                "Stores Energy?": "Yes" if c["stores_energy"] else "No",
                "Controls Current?": "Yes" if c["controls_current"] else "No",
                "Common Application": c["applications"].split(",")[0].split(".")[0],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Select at least one component above to see the comparison table.")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any component with an interactive model and experiment with its behaviour.")

    simulatable = [n for n in COMPONENT_ORDER if COMPONENTS[n]["calc_key"] is not None]
    sel = st.selectbox("Select a component", simulatable)
    c = COMPONENTS[sel]

    st.markdown(
        flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #0369a1, #075985);">'
             f'⚡ <b>{sel}</b> &nbsp;|&nbsp; {c["function"]}</div>'),
        unsafe_allow_html=True,
    )

    col_symbol, col_calc = st.columns([1, 1.6])
    with col_symbol:
        st.markdown("##### 🔷 Symbol")
        st.markdown(f'<div class="symbol-box">{draw_component_svg(sel)}</div>', unsafe_allow_html=True)
        st.markdown(f"**Type:** {c['type']}")
    with col_calc:
        CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how electronic components come together inside everyday devices.")

    APPLICATIONS = [
        ("📱 Smartphones", "Integrated Circuits act as the processor and memory; Capacitors and Resistors condition power and signals; LEDs provide indicators and camera flash; Transistors form the millions of tiny switches inside every chip."),
        ("💻 Computers", "Processors are enormous ICs containing billions of transistors; Memory chips store data; Capacitors stabilise power delivery; Resistors set precise voltage and current levels throughout the board."),
        ("🔊 Audio Systems", "Operational Amplifiers boost weak audio signals; Capacitors filter unwanted noise; Resistors and Potentiometers set gain and volume; Transistors provide the power needed to drive speakers."),
        ("🚗 Cars", "Sensors (often using LDRs or thermistors) monitor conditions; Relays switch high-power circuits like starter motors and headlights; Fuses protect the wiring; LEDs serve as indicator and tail lights; Control modules use ICs to manage engine timing."),
        ("🏠 Home Electronics", "Switches turn appliances on and off; Fuses protect household wiring; Transformers and Voltage Regulators convert mains power to safe low voltages; LEDs are used throughout for lighting and indicators."),
        ("🚨 Security Systems", "Sensors (light, motion) feed signals into the system; Relays switch alarms and locks; LEDs show system status; Transistors and ICs process the logic that decides when to trigger an alert."),
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
    st.header("📝 Electronic Components Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Components Explorer' section and try again!")

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
