"""
💾 Digital Electronics Learning Lab
An Interactive Beginner's Guide to Number Systems, Combinational & Sequential Logic

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
    page_title="Digital Electronics Learning Lab",
    page_icon="💾",
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
        background: linear-gradient(135deg, #312e81, #4c1d95);
        border: 1px solid #a78bfa;
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
# CORE DIGITAL LOGIC CALCULATIONS (pure functions, no widgets)
# ============================================================================

def decimal_to_binary(n, bits=8):
    """Unsigned decimal -> zero-padded binary string, wrapped to fit `bits`."""
    n = int(n) & ((1 << bits) - 1)
    return format(n, f"0{bits}b")


def decimal_to_octal(n):
    return oct(int(n))[2:] if n >= 0 else "0"


def decimal_to_hex(n):
    return hex(int(n))[2:].upper() if n >= 0 else "0"


def binary_to_decimal(bstr):
    try:
        return int(bstr, 2)
    except (ValueError, TypeError):
        return None


def decimal_to_bcd(n):
    """Binary-Coded Decimal: each decimal digit encoded as its own 4-bit binary group."""
    digits = str(int(n))
    return " ".join(format(int(d), "04b") for d in digits)


def binary_to_gray(bstr):
    """Standard binary-to-Gray code conversion (XOR of adjacent bits)."""
    g = bstr[0]
    for i in range(1, len(bstr)):
        g += str(int(bstr[i - 1]) ^ int(bstr[i]))
    return g


def gray_to_binary(gstr):
    """Standard Gray-to-binary conversion (running XOR)."""
    b = gstr[0]
    for i in range(1, len(gstr)):
        b += str(int(b[i - 1]) ^ int(gstr[i]))
    return b


def ascii_code(char):
    return ord(char) if char else None


def ascii_char(code):
    try:
        code = int(code)
        if 0 <= code <= 1114111:
            return chr(code)
    except (ValueError, TypeError):
        pass
    return None


def half_adder(a, b):
    """Returns (sum, carry)."""
    return a ^ b, a & b


def full_adder(a, b, cin):
    """Returns (sum, carry_out)."""
    s = a ^ b ^ cin
    cout = (a & b) | (cin & (a ^ b))
    return s, cout


def mux_select(inputs, sel):
    """Multiplexer: pick one of len(inputs) data lines using sel as an index."""
    if 0 <= sel < len(inputs):
        return inputs[sel]
    return None


def decoder_outputs(value, n_outputs):
    """n-to-2^n decoder: one-hot output list with a single 1 at position `value`."""
    outputs = [0] * n_outputs
    if 0 <= value < n_outputs:
        outputs[value] = 1
    return outputs


def sr_latch_next(s, r, prev_q):
    """SR latch next state. Returns (next_q, valid)."""
    if s == 1 and r == 0:
        return 1, True
    if s == 0 and r == 1:
        return 0, True
    if s == 0 and r == 0:
        return prev_q, True
    return prev_q, False  # S=1,R=1 is the forbidden/invalid state for a basic NOR latch


def d_ff_next(d):
    """D flip-flop: next Q simply follows D on the clock edge."""
    return d


def jk_ff_next(j, k, prev_q):
    """JK flip-flop next state (the 'universal' flip-flop)."""
    if j == 0 and k == 0:
        return prev_q
    if j == 0 and k == 1:
        return 0
    if j == 1 and k == 0:
        return 1
    return 1 - prev_q  # J=K=1 toggles


def t_ff_next(t, prev_q):
    """T flip-flop: toggles on each clock pulse when T=1."""
    return prev_q if t == 0 else 1 - prev_q


def counter_next(count, bits):
    """N-bit binary counter: increments and wraps at 2^bits."""
    return (count + 1) % (2 ** bits)


def shift_register_next(reg_bits, bit_in):
    """Shift register: new bit enters on the left, oldest bit drops off the right."""
    return [bit_in] + reg_bits[:-1]


# ============================================================================
# NUMBER SYSTEMS & CODES DATA
# 7 number systems/codes, each with the fields the Explorer page needs.
# "calc_key" links an entry to its interactive render function further down.
# ============================================================================
NUMBER_SYSTEMS = {
    "Binary": {
        "desc": "Base-2: the native language of digital electronics, using only two digits, 0 and 1.",
        "digits": "0, 1",
        "example": "13 (decimal) = 1101 (binary)",
        "category": ["base", "core"],
        "explanation": "Every digital circuit — from a single logic gate to a supercomputer — ultimately represents everything as combinations of just two voltage levels: LOW (0) and HIGH (1). Binary is how we write numbers using only those two symbols.",
        "applications": "The fundamental representation used inside every digital computer, microcontroller, and digital circuit.",
        "calc_key": "base_converter",
    },
    "Decimal": {
        "desc": "Base-10: the everyday number system humans use, with ten digits from 0 to 9.",
        "digits": "0, 1, 2, 3, 4, 5, 6, 7, 8, 9",
        "example": "13 (decimal) stays 13",
        "category": ["base"],
        "explanation": "Decimal is simply the number system most humans grew up using — likely because we have ten fingers! Digital circuits don't use it directly, but it's how we usually communicate values to and from a digital system.",
        "applications": "Human-readable displays, everyday communication of numeric values.",
        "calc_key": None,
    },
    "Octal": {
        "desc": "Base-8: uses eight digits, 0 through 7 — historically a convenient shorthand for binary.",
        "digits": "0, 1, 2, 3, 4, 5, 6, 7",
        "example": "13 (decimal) = 15 (octal)",
        "category": ["base"],
        "explanation": "Each octal digit represents exactly 3 binary bits, making it a quick way to write long binary numbers more compactly — it was common in older computing systems before hexadecimal became the norm.",
        "applications": "Unix/Linux file permission notation, some legacy computer architectures.",
        "calc_key": None,
    },
    "Hexadecimal": {
        "desc": "Base-16: uses sixteen digits, 0-9 followed by A-F for the values 10 through 15.",
        "digits": "0–9, A, B, C, D, E, F",
        "example": "13 (decimal) = D (hexadecimal)",
        "category": ["base", "core"],
        "explanation": "Each hex digit represents exactly 4 binary bits (a 'nibble'), making it a very compact and popular way to write binary values — far more readable than a long string of 1s and 0s.",
        "applications": "Memory addresses, colour codes in web design (#FF5733), machine code and assembly programming.",
        "calc_key": None,
    },
    "BCD (Binary-Coded Decimal)": {
        "desc": "A code where EACH individual decimal digit is stored as its own separate 4-bit binary group.",
        "digits": "Groups of 4 bits, one group per decimal digit",
        "example": "47 (decimal) = 0100 0111 (BCD) — NOT the same as plain binary 101111",
        "category": ["code"],
        "explanation": "BCD trades some efficiency for convenience: instead of converting a whole number to pure binary, each digit gets its own 4-bit code, making conversion to/from a decimal display very simple.",
        "applications": "Digital clocks and calculators with seven-segment displays, financial systems where exact decimal representation matters.",
        "calc_key": "bcd_calc",
    },
    "Gray Code": {
        "desc": "A binary numbering system where only ONE bit changes between any two consecutive values.",
        "digits": "0, 1 (same symbols as binary, different ordering)",
        "example": "3 (binary 011) → 4 (binary 100) is a 3-bit change; in Gray code, 3 (010) → 4 (110) is only a 1-bit change",
        "category": ["code"],
        "explanation": "In plain binary, counting from 3 to 4 flips three bits at once — in real hardware, those bits never switch at exactly the same instant, causing brief, incorrect in-between values. Gray code guarantees only one bit ever changes at a time, avoiding that glitch.",
        "applications": "Rotary position encoders, Karnaugh maps, error-correction and communication systems.",
        "calc_key": "gray_calc",
    },
    "ASCII": {
        "desc": "American Standard Code for Information Interchange — a code that assigns a unique number to each text character.",
        "digits": "Numbers 0–127 (standard ASCII), each mapped to a letter, digit, punctuation mark, or control code",
        "example": "'A' = 65,  'a' = 97,  '0' = 48",
        "category": ["code", "core"],
        "explanation": "Computers only understand numbers, so ASCII defines an agreed-upon numeric code for every keyboard character — letting text be stored, transmitted, and displayed consistently across different systems.",
        "applications": "Text encoding in computer memory, serial communication, keyboards, and file formats.",
        "calc_key": "ascii_calc",
    },
}

NUMBER_SYSTEM_ORDER = list(NUMBER_SYSTEMS.keys())

# ============================================================================
# COMBINATIONAL & SEQUENTIAL CIRCUITS DATA
# (used on the "Digital Circuits Reference" page)
# ============================================================================
DIGITAL_CIRCUITS = {
    "Half Adder": {
        "formula": "SUM = A ⊕ B   |   CARRY = A · B",
        "explanation": "The simplest binary adder — combines two single bits and produces a Sum bit and a Carry bit, but has no way to accept a carry IN from a previous, less-significant column.",
        "use": "Building block for larger adders; the least-significant bit position of a multi-bit adder.",
    },
    "Full Adder": {
        "formula": "SUM = A ⊕ B ⊕ Cin   |   COUT = AB + Cin(A ⊕ B)",
        "explanation": "Extends the half adder by also accepting a Carry-IN from the previous bit position, making it possible to chain many full adders together to add numbers of any width.",
        "use": "The core building block of every binary adder circuit inside a computer's ALU (Arithmetic Logic Unit).",
    },
    "Multiplexer (MUX)": {
        "formula": "Output = Input[Select]   |   An n-select-line MUX chooses 1 of 2ⁿ data inputs",
        "explanation": "A multiplexer acts like a rotary switch controlled by digital 'select' lines — routing exactly one of several data inputs through to a single output.",
        "use": "Data routing, combining multiple signal sources onto one shared line (e.g. selecting one of several sensors to read).",
    },
    "Demultiplexer (DEMUX)": {
        "formula": "Output[Select] = Input, all other outputs = 0",
        "explanation": "The exact opposite of a multiplexer — takes a single input and routes it to exactly one of several possible outputs, chosen by the select lines.",
        "use": "Distributing a single data source to one of several destinations (e.g. driving one of several LEDs from one control line).",
    },
    "Encoder": {
        "formula": "2ⁿ input lines → n-bit binary output code",
        "explanation": "An encoder compresses many input lines (usually only one active at a time) down into a much smaller binary code representing which input was active.",
        "use": "Keypad encoding (converting one pressed key out of many into a binary code), priority interrupt systems.",
    },
    "Decoder": {
        "formula": "n-bit binary input → 2ⁿ one-hot output lines",
        "explanation": "A decoder is the reverse of an encoder — it takes a binary code and activates exactly one of many output lines corresponding to that code.",
        "use": "Memory address decoding, seven-segment display drivers, selecting one of many devices on a shared bus.",
    },
    "Digital Comparator": {
        "formula": "Outputs: (A > B), (A = B), (A < B)",
        "explanation": "Compares two binary numbers bit by bit and indicates their relationship — greater than, equal to, or less than — as three separate output signals.",
        "use": "Sorting circuits, address matching, magnitude comparison in control systems.",
    },
    "SR Latch": {
        "formula": "S=1,R=0 → Set (Q=1)   |   S=0,R=1 → Reset (Q=0)   |   S=0,R=0 → Hold (memory!)   |   S=1,R=1 → Invalid (forbidden)",
        "explanation": "The simplest memory element in digital electronics — built from just two cross-coupled NOR (or NAND) gates, it can 'remember' a single bit by holding its state even after the inputs that set it are removed.",
        "use": "The conceptual foundation every other flip-flop is built from; simple switch-debouncing circuits.",
    },
    "D Flip-Flop": {
        "formula": "On each clock edge: Q(next) = D",
        "explanation": "A D (Data/Delay) flip-flop simply copies its D input to its Q output — but ONLY at the instant of a clock edge, making it a clean, glitch-free single-bit memory cell.",
        "use": "Registers, data storage, synchronising signals to a clock in virtually all digital systems.",
    },
    "JK Flip-Flop": {
        "formula": "J=0,K=0 → Hold   |   J=0,K=1 → Reset (Q=0)   |   J=1,K=0 → Set (Q=1)   |   J=1,K=1 → Toggle",
        "explanation": "Known as the 'universal' flip-flop because it can be configured to behave like an SR latch, a D flip-flop, or a T flip-flop, depending on how its J and K inputs are driven — and it fixes the SR latch's forbidden-state problem by toggling instead.",
        "use": "Counters, general-purpose sequential logic design.",
    },
    "T Flip-Flop": {
        "formula": "T=0 → Hold   |   T=1 → Toggle (Q flips to the opposite state)",
        "explanation": "A T (Toggle) flip-flop flips its output every time it receives a clock pulse with T=1 — essentially a JK flip-flop with J and K permanently tied together.",
        "use": "The core building block of binary counters, where each bit needs to toggle at half the rate of the bit before it.",
    },
    "Asynchronous (Ripple) Counter": {
        "formula": "Each flip-flop is clocked by the OUTPUT of the previous flip-flop, not by a shared clock",
        "explanation": "Simple to build — just chain T or JK flip-flops together — but each stage's change 'ripples' through with a small delay, meaning all bits don't update at exactly the same instant.",
        "use": "Simple frequency division, low-speed counting applications where ripple delay doesn't matter.",
    },
    "Synchronous Counter": {
        "formula": "ALL flip-flops share the SAME clock signal, changing state at exactly the same instant",
        "explanation": "More complex to design than a ripple counter (extra logic decides each flip-flop's next state), but eliminates ripple delay entirely, making it far faster and more reliable for high-speed counting.",
        "use": "High-speed counting, frequency dividers in precision timing systems, digital clocks.",
    },
    "Shift Register": {
        "formula": "Each clock pulse shifts every stored bit one position (left or right); a new bit enters, the end bit exits",
        "explanation": "A chain of flip-flops connected so data shifts smoothly along the chain with each clock pulse — can convert between serial (one-bit-at-a-time) and parallel (all-bits-at-once) data formats.",
        "use": "Serial-to-parallel and parallel-to-serial data conversion, simple delay lines, driving multiple LEDs/displays from few control pins.",
    },
}

DIGITAL_CIRCUIT_ORDER = list(DIGITAL_CIRCUITS.keys())

# ============================================================================
# SVG ILLUSTRATIONS
# Small, clean diagrams illustrating each number system/code. Every returned
# string is flattened to one line with flat() so Streamlit's Markdown
# renderer never mis-parses an embedded blank line as the end of the block.
# ============================================================================
NUMBER_SYSTEM_COLORS = {
    "Binary": "#3b82f6",
    "Decimal": "#22c55e",
    "Octal": "#f59e0b",
    "Hexadecimal": "#8b5cf6",
    "BCD (Binary-Coded Decimal)": "#ec4899",
    "Gray Code": "#06b6d4",
    "ASCII": "#ef4444",
}


def _digit_tile(cx, cy, text, color, size=32):
    half = size / 2
    return (
        f'<rect x="{cx-half}" y="{cy-half}" width="{size}" height="{size}" rx="6" '
        f'fill="{color}22" stroke="{color}" stroke-width="2.5"/>'
        f'<text x="{cx}" y="{cy+6}" font-size="16" font-weight="bold" fill="{color}" text-anchor="middle">{text}</text>'
    )


def draw_number_system_svg(name):
    """Return a flattened, single-line SVG illustration for a number system/code."""
    color = NUMBER_SYSTEM_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Binary":
        tiles = "".join(_digit_tile(60 + i * 40, 70, d, color) for i, d in enumerate(["0", "1"]))
        body = f'<text x="110" y="30" font-size="13" font-weight="bold" fill="#111827" text-anchor="middle">Base 2</text>{tiles}'

    elif name == "Decimal":
        digits = "0123456789"
        tiles = "".join(_digit_tile(18 + i * 20, 75, d, color, size=18) for i, d in enumerate(digits))
        body = f'<text x="110" y="30" font-size="13" font-weight="bold" fill="#111827" text-anchor="middle">Base 10</text>{tiles}'

    elif name == "Octal":
        digits = "01234567"
        tiles = "".join(_digit_tile(30 + i * 22, 75, d, color, size=20) for i, d in enumerate(digits))
        body = f'<text x="110" y="30" font-size="13" font-weight="bold" fill="#111827" text-anchor="middle">Base 8</text>{tiles}'

    elif name == "Hexadecimal":
        digits = "0123456789ABCDEF"
        tiles = "".join(_digit_tile(18 + (i % 8) * 24, 60 + (i // 8) * 35, d, color, size=20) for i, d in enumerate(digits))
        body = f'<text x="110" y="20" font-size="13" font-weight="bold" fill="#111827" text-anchor="middle">Base 16</text>{tiles}'

    elif name == "BCD (Binary-Coded Decimal)":
        body = f"""
        <text x="55" y="60" font-size="26" font-weight="bold" fill="{color}" text-anchor="middle">4</text>
        <line x1="90" y1="60" x2="120" y2="60" stroke="{color}" stroke-width="3"/>
        <polygon points="120,60 110,54 110,66" fill="{color}"/>
        {_digit_tile(160, 60, "0100", color, size=64)}
        <text x="55" y="110" font-size="26" font-weight="bold" fill="{color}" text-anchor="middle">7</text>
        <line x1="90" y1="110" x2="120" y2="110" stroke="{color}" stroke-width="3"/>
        <polygon points="120,110 110,104 110,116" fill="{color}"/>
        {_digit_tile(160, 110, "0111", color, size=64)}
        """

    elif name == "Gray Code":
        body = f"""
        {_digit_tile(60, 45, "011", color, size=50)}
        <text x="110" y="50" font-size="16" font-weight="bold" fill="#111827" text-anchor="middle">→</text>
        {_digit_tile(160, 45, "010", color, size=50)}
        <text x="110" y="20" font-size="11" fill="#111827" text-anchor="middle">only 1 bit changes</text>
        {_digit_tile(60, 105, "011", "#9ca3af", size=50)}
        <text x="110" y="110" font-size="16" font-weight="bold" fill="#111827" text-anchor="middle">→</text>
        {_digit_tile(160, 105, "100", "#9ca3af", size=50)}
        <text x="110" y="130" font-size="11" fill="#111827" text-anchor="middle">binary: 3 bits change</text>
        """

    elif name == "ASCII":
        body = f"""
        {_digit_tile(60, 70, "A", color, size=56)}
        <text x="110" y="65" font-size="16" font-weight="bold" fill="#111827" text-anchor="middle">=</text>
        {_digit_tile(165, 70, "65", color, size=56)}
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same item is rendered on more than one page.
# Sequential-logic simulators use st.session_state to genuinely "remember"
# state between clicks, just like real flip-flops and counters.
# ============================================================================

def render_base_converter(key_prefix):
    st.markdown("**⚙️ Number Base Converter**")
    n = st.number_input("Decimal Value", min_value=0, max_value=65535, value=13, step=1, key=f"{key_prefix}_bc_n")
    bits = st.slider("Binary width (bits)", 4, 16, 8, key=f"{key_prefix}_bc_bits")
    b = decimal_to_binary(n, bits)
    o = decimal_to_octal(n)
    h = decimal_to_hex(n)
    st.markdown(
        f'<div class="status-good">✅ Binary = {b} &nbsp;|&nbsp; Octal = {o} &nbsp;|&nbsp; Hexadecimal = {h}</div>',
        unsafe_allow_html=True,
    )
    st.caption("Try entering a value larger than the binary width can hold — notice it wraps around, just like a real fixed-width register.")


def render_bcd_calc(key_prefix):
    st.markdown("**⚙️ Decimal → BCD Encoder**")
    n = st.number_input("Decimal Value", min_value=0, max_value=9999, value=47, step=1, key=f"{key_prefix}_bcd_n")
    bcd = decimal_to_bcd(n)
    plain_binary = decimal_to_binary(n, bits=max(4, len(bin(int(n))) - 2))
    st.markdown(f'<div class="status-good">✅ BCD = {bcd}</div>', unsafe_allow_html=True)
    st.caption(f"Compare to plain binary of the same value: {plain_binary} — notice BCD uses more bits but keeps each decimal digit separately recognisable.")


def render_gray_calc(key_prefix):
    st.markdown("**⚙️ Binary ↔ Gray Code Converter**")
    direction = st.radio("Convert:", ["Binary → Gray", "Gray → Binary"], horizontal=True, key=f"{key_prefix}_gray_dir")
    bits = st.text_input("Value (binary digits only, e.g. 1011)", value="1011", key=f"{key_prefix}_gray_val")
    valid = all(ch in "01" for ch in str(bits)) and len(str(bits)) > 0
    if not valid:
        st.warning("⚠️ Please enter only 0s and 1s.")
    else:
        if direction == "Binary → Gray":
            result = binary_to_gray(str(bits))
            st.markdown(f'<div class="status-good">✅ Gray Code = {result}</div>', unsafe_allow_html=True)
        else:
            result = gray_to_binary(str(bits))
            st.markdown(f'<div class="status-good">✅ Binary = {result}</div>', unsafe_allow_html=True)


def render_ascii_calc(key_prefix):
    st.markdown("**⚙️ ASCII Lookup**")
    direction = st.radio("Convert:", ["Character → Code", "Code → Character"], horizontal=True, key=f"{key_prefix}_ascii_dir")
    if direction == "Character → Code":
        ch = st.text_input("Character", value="A", max_chars=1, key=f"{key_prefix}_ascii_ch")
        code = ascii_code(ch)
        if code is None:
            st.warning("⚠️ Enter a single character.")
        else:
            st.markdown(f'<div class="status-good">✅ \'{ch}\' = {code} (decimal) = {decimal_to_binary(code)} (binary)</div>', unsafe_allow_html=True)
    else:
        code = st.number_input("ASCII Code (0-127)", min_value=0, max_value=127, value=65, step=1, key=f"{key_prefix}_ascii_code")
        ch = ascii_char(code)
        st.markdown(f'<div class="status-good">✅ Code {code} = \'{ch}\'</div>', unsafe_allow_html=True)


CALC_RENDERERS = {
    "base_converter": render_base_converter,
    "bcd_calc": render_bcd_calc,
    "gray_calc": render_gray_calc,
    "ascii_calc": render_ascii_calc,
}


def render_half_adder_sim(key_prefix):
    st.markdown("**⚙️ Half Adder Simulator**")
    c1, c2 = st.columns(2)
    a = int(c1.toggle("Input A", value=False, key=f"{key_prefix}_ha_a"))
    b = int(c2.toggle("Input B", value=False, key=f"{key_prefix}_ha_b"))
    s, cout = half_adder(a, b)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if s else "bulb-off"}"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>SUM = {s}</p>", unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if cout else "bulb-off"}"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>CARRY = {cout}</p>", unsafe_allow_html=True)


def render_full_adder_sim(key_prefix):
    st.markdown("**⚙️ Full Adder Simulator**")
    c1, c2, c3 = st.columns(3)
    a = int(c1.toggle("Input A", value=False, key=f"{key_prefix}_fa_a"))
    b = int(c2.toggle("Input B", value=False, key=f"{key_prefix}_fa_b"))
    cin = int(c3.toggle("Carry In", value=False, key=f"{key_prefix}_fa_cin"))
    s, cout = full_adder(a, b, cin)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if s else "bulb-off"}"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>SUM = {s}</p>", unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if cout else "bulb-off"}"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>CARRY OUT = {cout}</p>", unsafe_allow_html=True)


def render_mux_sim(key_prefix):
    st.markdown("**⚙️ 4:1 Multiplexer Simulator**")
    cols = st.columns(4)
    inputs = [int(cols[i].toggle(f"D{i}", value=False, key=f"{key_prefix}_mux_d{i}")) for i in range(4)]
    sel = st.slider("Select (S1 S0)", 0, 3, 0, key=f"{key_prefix}_mux_sel")
    out = mux_select(inputs, sel)
    st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if out else "bulb-off"}"></div></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Output = D{sel} = {out}</p>", unsafe_allow_html=True)


def render_decoder_sim(key_prefix):
    st.markdown("**⚙️ 2-to-4 Decoder Simulator**")
    c1, c2 = st.columns(2)
    a = int(c1.toggle("Input A1 (MSB)", value=False, key=f"{key_prefix}_dec_a"))
    b = int(c2.toggle("Input A0 (LSB)", value=False, key=f"{key_prefix}_dec_b"))
    value = a * 2 + b
    outputs = decoder_outputs(value, 4)
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if outputs[i] else "bulb-off"}"></div></div>', unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>Y{i}</p>", unsafe_allow_html=True)


def render_sr_latch_sim(key_prefix):
    st.markdown("**⚙️ SR Latch Simulator** (has real memory — try toggling S and R off again!)")
    state_key = f"{key_prefix}_sr_q"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    c1, c2 = st.columns(2)
    s = int(c1.toggle("Set (S)", value=False, key=f"{key_prefix}_sr_s"))
    r = int(c2.toggle("Reset (R)", value=False, key=f"{key_prefix}_sr_r"))
    next_q, valid = sr_latch_next(s, r, st.session_state[state_key])
    if valid:
        st.session_state[state_key] = next_q
        st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if next_q else "bulb-off"}"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>Q = {next_q}</p>", unsafe_allow_html=True)
        if s == 0 and r == 0:
            st.caption("Both inputs are LOW — the latch is HOLDING its last state. This is memory!")
    else:
        st.markdown('<div class="status-bad">⚠️ S=1 and R=1 is the FORBIDDEN state for a basic SR latch — output is undefined. Set at least one input LOW.</div>', unsafe_allow_html=True)


def render_d_ff_sim(key_prefix):
    st.markdown("**⚙️ D Flip-Flop Simulator** — Q only updates when you click the clock!")
    state_key = f"{key_prefix}_dff_q"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    d = int(st.toggle("D Input", value=False, key=f"{key_prefix}_dff_d"))
    if st.button("🕐 Clock Pulse", key=f"{key_prefix}_dff_clk"):
        st.session_state[state_key] = d_ff_next(d)
    q = st.session_state[state_key]
    st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if q else "bulb-off"}"></div></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Q = {q}</p>", unsafe_allow_html=True)
    st.caption("Notice: changing D alone does nothing — Q only updates the moment you click the clock, just like a real clocked flip-flop.")


def render_jk_ff_sim(key_prefix):
    st.markdown("**⚙️ JK Flip-Flop Simulator** — Q only updates when you click the clock!")
    state_key = f"{key_prefix}_jkff_q"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    c1, c2 = st.columns(2)
    j = int(c1.toggle("J Input", value=False, key=f"{key_prefix}_jk_j"))
    k = int(c2.toggle("K Input", value=False, key=f"{key_prefix}_jk_k"))
    if st.button("🕐 Clock Pulse", key=f"{key_prefix}_jk_clk"):
        st.session_state[state_key] = jk_ff_next(j, k, st.session_state[state_key])
    q = st.session_state[state_key]
    st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if q else "bulb-off"}"></div></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Q = {q}</p>", unsafe_allow_html=True)
    if j == 1 and k == 1:
        st.caption("J=K=1 — each clock pulse will TOGGLE the output.")


def render_counter_sim(key_prefix):
    st.markdown("**⚙️ Binary Counter Simulator**")
    bits = st.slider("Counter width (bits)", 2, 6, 4, key=f"{key_prefix}_cnt_bits")
    state_key = f"{key_prefix}_cnt_val"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    c1, c2 = st.columns(2)
    if c1.button("🕐 Clock Pulse (+1)", key=f"{key_prefix}_cnt_clk"):
        st.session_state[state_key] = counter_next(st.session_state[state_key], bits)
    if c2.button("🔄 Reset", key=f"{key_prefix}_cnt_reset"):
        st.session_state[state_key] = 0
    count = st.session_state[state_key] % (2 ** bits)
    st.markdown(f'<div class="status-good">✅ Count = {count} (decimal) = {decimal_to_binary(count, bits)} (binary)</div>', unsafe_allow_html=True)
    cols = st.columns(bits)
    binstr = decimal_to_binary(count, bits)
    for i, ch in enumerate(binstr):
        with cols[i]:
            st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if ch == "1" else "bulb-off"}"></div></div>', unsafe_allow_html=True)


def render_shift_register_sim(key_prefix):
    st.markdown("**⚙️ Shift Register Simulator**")
    n = st.slider("Register width (bits)", 4, 8, 4, key=f"{key_prefix}_sr_n")
    state_key = f"{key_prefix}_sr_reg"
    if state_key not in st.session_state or len(st.session_state[state_key]) != n:
        st.session_state[state_key] = [0] * n
    bit_in = int(st.toggle("Bit to shift in", value=False, key=f"{key_prefix}_sr_bitin"))
    c1, c2 = st.columns(2)
    if c1.button("🕐 Shift", key=f"{key_prefix}_sr_shift"):
        st.session_state[state_key] = shift_register_next(st.session_state[state_key], bit_in)
    if c2.button("🔄 Clear", key=f"{key_prefix}_sr_clear"):
        st.session_state[state_key] = [0] * n
    reg = st.session_state[state_key]
    st.markdown(f'<div class="status-good">✅ Register contents = {"".join(str(b) for b in reg)}</div>', unsafe_allow_html=True)
    cols = st.columns(n)
    for i, bit in enumerate(reg):
        with cols[i]:
            st.markdown(f'<div class="bulb-wrap"><div class="{"bulb-on" if bit else "bulb-off"}"></div></div>', unsafe_allow_html=True)
    st.caption("Each 'Shift' click moves every bit one place to the right and inserts the new bit on the left.")


EXTRA_SIMULATORS = {
    "Half Adder": render_half_adder_sim,
    "Full Adder": render_full_adder_sim,
    "4:1 Multiplexer": render_mux_sim,
    "2-to-4 Decoder": render_decoder_sim,
    "SR Latch": render_sr_latch_sim,
    "D Flip-Flop": render_d_ff_sim,
    "JK Flip-Flop": render_jk_ff_sim,
    "Binary Counter": render_counter_sim,
    "Shift Register": render_shift_register_sim,
}

# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. What is the binary representation of decimal 5?", "options": ["101", "110", "011"], "answer": "101"},
    {"q": "2. How many binary digits (bits) does one hexadecimal digit represent?", "options": ["2", "3", "4"], "answer": "4"},
    {"q": "3. Why was Gray code designed to only change one bit at a time?", "options": ["To use fewer bits overall", "To avoid glitches from multiple bits changing at slightly different instants", "To make numbers look nicer"], "answer": "To avoid glitches from multiple bits changing at slightly different instants"},
    {"q": "4. What does a Half Adder NOT have that a Full Adder does?", "options": ["A Sum output", "A Carry-In input", "A Carry-Out output"], "answer": "A Carry-In input"},
    {"q": "5. What does a Multiplexer do?", "options": ["Selects one of several inputs to send to a single output", "Converts binary to decimal", "Stores one bit of memory"], "answer": "Selects one of several inputs to send to a single output"},
    {"q": "6. What makes the S=1, R=1 condition special in a basic SR latch?", "options": ["It's the normal 'hold' state", "It's a forbidden/invalid state with undefined output", "It resets the latch safely"], "answer": "It's a forbidden/invalid state with undefined output"},
    {"q": "7. When does a D flip-flop's output actually change?", "options": ["The instant D changes", "Only on a clock edge", "Never — it's a fixed circuit"], "answer": "Only on a clock edge"},
    {"q": "8. What happens to a JK flip-flop's output when J=1 and K=1 on a clock pulse?", "options": ["It holds its state", "It resets to 0", "It toggles to the opposite state"], "answer": "It toggles to the opposite state"},
    {"q": "9. What is the key advantage of a synchronous counter over an asynchronous (ripple) counter?", "options": ["It uses fewer flip-flops", "All bits change at exactly the same instant, avoiding ripple delay", "It doesn't need a clock signal"], "answer": "All bits change at exactly the same instant, avoiding ripple delay"},
    {"q": "10. What does a shift register do with its stored bits on each clock pulse?", "options": ["Erases them all", "Moves every bit one position, with a new bit entering and the oldest leaving", "Doubles every bit's value"], "answer": "Moves every bit one position, with a new bit entering and the oldest leaving"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "A student builds an SR latch and sets both S and R to 1 at the same time, then wonders why the output behaves unpredictably when they release the inputs.",
        "question": "What is the underlying issue?",
        "options": ["S=1, R=1 is a forbidden/invalid state for a basic SR latch — its output is undefined", "The latch is simply broken", "SR latches cannot store any data at all"],
        "answer": "S=1, R=1 is a forbidden/invalid state for a basic SR latch — its output is undefined",
        "explanation": "A basic SR latch relies on exactly one of S or R being active to define its next state — driving both HIGH at once breaks the assumption the circuit depends on, leading to unpredictable behaviour when they're released.",
    },
    {
        "scenario": "A digital display shows garbage numbers momentarily whenever a binary counter rolls over from 0111 to 1000 (7 to 8), because the four bits don't all change at exactly the same instant.",
        "question": "What design choice would help avoid this specific problem?",
        "options": ["Using Gray code instead of plain binary for the counter", "Adding more decimal digits to the display", "Increasing the supply voltage"], 
        "answer": "Using Gray code instead of plain binary for the counter",
        "explanation": "Gray code guarantees that consecutive values differ by only one bit, eliminating the brief, incorrect in-between values that occur when multiple binary bits change at slightly different times.",
    },
    {
        "scenario": "A ripple counter built from several flip-flops works correctly at low speed, but produces incorrect counts at high clock speeds.",
        "question": "What is the most likely explanation?",
        "options": ["The propagation delay of each stage 'rippling' through the chain becomes significant at high speed", "Ripple counters are simply incapable of counting correctly", "The flip-flops need more power at higher speeds"],
        "answer": "The propagation delay of each stage 'rippling' through the chain becomes significant at high speed",
        "explanation": "In a ripple counter, each flip-flop only updates after the previous one has already toggled — at high enough clock speeds, this cumulative rippling delay can cause the count to be read incorrectly before it has fully settled.",
    },
    {
        "scenario": "A student wires a D flip-flop and changes the D input, expecting the output Q to change immediately — but it doesn't.",
        "question": "What have they misunderstood?",
        "options": ["D flip-flops are broken by design", "Q only updates on a clock edge, not simply whenever D changes", "D flip-flops don't have an output at all"],
        "answer": "Q only updates on a clock edge, not simply whenever D changes",
        "explanation": "A defining feature of an edge-triggered flip-flop is that its output only updates at the precise moment of a clock edge — changing the data input alone does nothing until that edge arrives.",
    },
    {
        "scenario": "A shift register meant to display a moving pattern of lights appears to lose its pattern after several clock pulses, ending up all zeros.",
        "question": "What is the most likely explanation for a basic (non-recirculating) shift register?",
        "options": ["Bits naturally 'fall off' the end of a basic shift register as new bits (in this case, zeros) are shifted in", "The register has a hardware fault", "Shift registers cannot hold a 1 for more than one clock cycle"],
        "answer": "Bits naturally 'fall off' the end of a basic shift register as new bits (in this case, zeros) are shifted in",
        "explanation": "Unless it's specifically wired as a 'recirculating' shift register (feeding the output back around to the input), each shift permanently discards the oldest bit — if zeros keep entering, the pattern will eventually shift out entirely.",
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
st.sidebar.title("💾 DIGITAL ELECTRONICS")
st.sidebar.subheader("LEARNING LAB")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Student Instructions**")
st.sidebar.markdown(
    "1. Start with Introduction\n"
    "2. Explore number systems & codes\n"
    "3. Study combinational & sequential circuits\n"
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
        "🔢 Number Systems & Codes",
        "🔌 Digital Circuits Reference",
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
st.title("💾 Digital Electronics Learning Lab")
st.caption("An Interactive Beginner's Guide to Number Systems, Combinational & Sequential Logic")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔢 Number Systems & Codes", len(NUMBER_SYSTEMS))
d2.metric("🔌 Circuits Covered", len(DIGITAL_CIRCUITS))
d3.metric("🧪 Troubleshooting Cases", len(TROUBLESHOOTING))
d4.metric("📝 Quiz Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Introduction to Digital Electronics")

    st.markdown(
        """
        ### Analogue vs. Digital
        An **analogue** signal can take on any value across a continuous range — like
        the smoothly varying voltage from a microphone. A **digital** signal, by
        contrast, only ever takes on a small number of discrete states — almost
        always just two: LOW (0) and HIGH (1).

        This module builds on the "Logic Gates" module by going further: how we
        represent NUMBERS and TEXT digitally, how simple gates combine into useful
        **combinational circuits** (like adders and multiplexers), and how digital
        circuits can gain **memory** through **sequential circuits** (like flip-flops
        and counters).
        """
    )

    st.subheader("🧠 Combinational vs. Sequential Logic")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>🔀 Combinational Logic</h4>'
            '<p>Output depends ONLY on the current inputs, with no memory of the past. '
            'Given the same inputs, you always get the same output — like a light switch.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>⏱️ Sequential Logic</h4>'
            '<p>Output depends on the current inputs AND the circuit\'s previous state — '
            'it has MEMORY. The same input can produce different outputs depending on history.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("🔢 Why So Many Number Systems?")
    st.markdown(
        '<div class="app-card">Digital circuits fundamentally only understand BINARY (0s and 1s) — '
        'but binary numbers get long and hard for humans to read quickly. Hexadecimal and octal exist '
        'purely as convenient shorthand for binary, while codes like BCD, Gray code, and ASCII solve '
        'specific practical problems in how digital systems represent decimal numbers, avoid switching '
        'glitches, and encode text.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Head to **'Number Systems & Codes'** in the sidebar to explore each one in detail.")

# ============================================================================
# 2. NUMBER SYSTEMS & CODES
# ============================================================================
elif page.startswith("🔢"):
    st.header("🔢 Number Systems & Codes Explorer")
    st.caption("Expand each entry to see an illustration, key facts, explanation, and (where relevant) an interactive converter.")

    for name in NUMBER_SYSTEM_ORDER:
        c = NUMBER_SYSTEMS[name]
        with st.expander(f"**{name}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_number_system_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Digits used:** {c['digits']}")
                st.markdown(f"**Example:** {c['example']}")
            with col2:
                st.markdown(f"**In plain English:** {c['explanation']}")
                st.markdown(f"**Typical Applications:** {c['applications']}")

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. DIGITAL CIRCUITS REFERENCE
# ============================================================================
elif page.startswith("🔌"):
    st.header("🔌 Digital Circuits Reference")
    st.caption("Key combinational and sequential circuits every digital electronics student should know.")

    filter_tags = st.multiselect(
        "Filter number systems/codes by category",
        ["base", "core", "code"],
        default=[],
    )
    if filter_tags:
        filtered = [n for n in NUMBER_SYSTEM_ORDER if any(t in NUMBER_SYSTEMS[n]["category"] for t in filter_tags)]
    else:
        filtered = NUMBER_SYSTEM_ORDER

    st.subheader("🧮 Number System Reference Table")
    rows = []
    for name in filtered:
        c = NUMBER_SYSTEMS[name]
        rows.append({
            "System / Code": name,
            "Digits Used": c["digits"],
            "Example": c["example"],
            "Category": ", ".join(c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Combinational & Sequential Circuits")
    for circuit_name in DIGITAL_CIRCUIT_ORDER:
        rc = DIGITAL_CIRCUITS[circuit_name]
        with st.expander(f"**{circuit_name}**"):
            st.markdown(f"**Key facts:** {rc['formula']}")
            st.markdown(f"**Explanation:** {rc['explanation']}")
            st.markdown(f"**Used for:** {rc['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Interactive Simulator")
    st.caption("Pick any circuit and experiment with its behaviour — sequential circuits genuinely remember their state between clicks.")

    sel = st.selectbox("Select a circuit", list(EXTRA_SIMULATORS.keys()))
    st.markdown(
        flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #7c3aed, #4c1d95);">'
             f'💾 <b>{sel}</b></div>'),
        unsafe_allow_html=True,
    )
    EXTRA_SIMULATORS[sel](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Practical Applications")
    st.caption("See how number systems, combinational logic, and sequential logic power real digital systems.")

    APPLICATIONS = [
        ("💻 Computer Processors (CPUs)", "Full adders chain together to build the Arithmetic Logic Unit (ALU); flip-flops form registers that hold data between operations; hexadecimal is used throughout to represent memory addresses and machine code."),
        ("🔢 Digital Clocks & Calculators", "BCD makes it simple to convert internal binary counts directly into individual decimal digits for seven-segment displays; counters (built from flip-flops) track seconds, minutes, and hours."),
        ("🎛️ Rotary Position Encoders", "Gray code is used so that as a shaft rotates, only one bit changes at a time — preventing false position readings that plain binary would cause."),
        ("📡 Serial Communication", "Shift registers convert parallel data (all bits at once, inside a device) into serial data (one bit at a time, for transmission over a single wire) and back again."),
        ("⌨️ Keyboards & Text Systems", "ASCII (or its modern successor, Unicode) assigns a unique numeric code to every character you type, letting computers store and transmit text reliably."),
        ("🧠 Computer Memory", "Decoders select exactly which memory location (out of millions) a binary address refers to; multiplexers route data between memory, the CPU, and other components."),
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
    st.header("📝 Digital Electronics Quiz")
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
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Number Systems & Codes' section and try again!")

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
