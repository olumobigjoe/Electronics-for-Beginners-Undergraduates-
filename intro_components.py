import streamlit as st

def run():
    st.title("🧰 Intro to Electronic Components")
    st.write("Learn about the building blocks of modern hardware electronics.")

    component = st.selectbox("Select a Component to Study:", ["Resistors", "Capacitors", "Inductors", "Diodes"])

    if component == "Resistors":
        st.header("Resistors (R)")
        st.write("Resistors limit the flow of electric current in a circuit and lower voltage levels.")
        
        st.subheader("🎨 4-Band Resistor Color Code Calculator")
        colors = {
            "Black": (0, 1), "Brown": (1, 10), "Red": (2, 100), "Orange": (3, 1000),
            "Yellow": (4, 10000), "Green": (5, 100000), "Blue": (6, 1000000),
            "Violet": (7, 10000000), "Grey": (8, 100000000), "White": (9, 1000000000)
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            b1 = st.selectbox("Band 1 (Digit)", list(colors.keys()), index=1)
        with col2:
            b2 = st.selectbox("Band 2 (Digit)", list(colors.keys()), index=0)
        with col3:
            mult = st.selectbox("Band 3 (Multiplier)", list(colors.keys()), index=2)

        val = (colors[b1][0] * 10 + colors[b2][0]) * colors[mult][1]
        st.success(f"**Calculated Resistance:** {val:,} Ω ({val/1000:.2f} kΩ)")

    elif component == "Capacitors":
        st.header("Capacitors (C)")
        st.write("Capacitors store electrical energy in an electric field between two conductive plates.")
        st.latex(r"C = \epsilon \frac{A}{d}")
        st.latex(r"Q = C \times V")
        
        c_uf = st.number_input("Capacitance (µF)", value=100.0)
        v_volts = st.number_input("Applied Voltage (V)", value=12.0)
        energy = 0.5 * (c_uf * 1e-6) * (v_volts ** 2)
        st.metric("Stored Energy (Joules)", f"{energy*1000:.3f} mJ")

    elif component == "Inductors":
        st.header("Inductors (L)")
        st.write("Inductors store energy in a magnetic field when electric current flows through them.")
        st.latex(r"V_L = L \frac{di}{dt}")
        st.latex(r"E_L = \frac{1}{2} L I^2")

    elif component == "Diodes":
        st.header("Diodes")
        st.write("Diodes allow electric current to flow in one direction only (forward bias) while blocking it in the reverse direction.")
        st.markdown("- **Anode (+):** Positive terminal\n- **Cathode (-):** Negative terminal\n- **Forward Cut-in Voltage ($V_D$):** ~0.7V for Silicon, ~0.3V for Germanium")
