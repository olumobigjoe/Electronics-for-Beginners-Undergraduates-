# Electronics for Beginners - Unified Streamlit App

A comprehensive, interactive web application bringing together 8 fundamental electronics learning modules into a single, seamless Streamlit interface.

## Featured Modules
1. **Diodes & Rectifiers** - Learn about PN junction diodes, half-wave & full-wave rectifiers, and Zener voltage regulation.
2. **Electrical Fundamentals** - Interactive calculators & visualizers for Ohm's Law, Kirchhoff's Laws, and Power equations.
3. **Electronic Measurements & Instrumentation** - Explore Multimeters, Oscilloscopes, Signal Generators, and Measurement Errors.
4. **Intro to Electronic Components** - Comprehensive guide to Resistors, Capacitors, Inductors, and Diodes.
5. **Logic Gates Lab** - Interactive truth table simulator and logic circuit builder.
6. **Transistors & Amplifiers** - BJT & MOSFET operations, biasing configurations, and amplifier frequency responses.
7. **Circuit Analysis Tools** - Nodal Analysis, Mesh Analysis, Thevenin & Norton Equivalents, and RC/RL Transient Analysis.
8. **Digital Electronics for Beginners** - Number systems conversion, Boolean Algebra, Combinational, and Sequential circuits.

---

## Installation & Setup

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/your-username/electronics-for-beginners.git
   cd electronics-for-beginners
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

---

## File Structure
```text
electronics_for_beginners/
│
├── app.py                   # Main entry point with interactive 8-box landing page
├── requirements.txt         # Project dependencies
├── README.md                # Documentation & Setup Guide
└── modules/                 # Sub-modules directory
    ├── __init__.py
    ├── diodes_rectifiers.py
    ├── electrical_fundamentals.py
    ├── electronic_measurements.py
    ├── intro_components.py
    ├── logic_gates.py
    ├── transistors_amplifiers.py
    ├── circuit_analysis.py
    └── digital_electronics.py
```
