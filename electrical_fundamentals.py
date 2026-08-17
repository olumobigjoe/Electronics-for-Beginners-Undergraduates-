import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.title("🔌 Electrical Fundamentals")
    st.write("Understand core electrical concepts: Voltage, Current, Resistance, Ohm's Law, and Power.")

    tab1, tab2, tab3 = st.tabs(["⚡ Ohm's Law Calculator & Plot", "🔋 Kirchhoff's Laws (KVL/KCL)", "🔥 Power & Energy"])

    with tab1:
        st.subheader("Ohm's Law Simulator: V = I × R")
        col1, col2 = st.columns(2)
        with col1:
            voltage = st.slider("Voltage (V)", 0.1, 50.0, 12.0, 0.1)
            resistance = st.slider("Resistance (Ω)", 1.0, 1000.0, 220.0, 5.0)
            current = voltage / resistance
            power = voltage * current

            st.metric(label="Calculated Current (I)", value=f"{current*1000:.2f} mA")
            st.metric(label="Calculated Power (P)", value=f"{power:.3f} W")

        with col2:
            r_vals = np.linspace(10, 1000, 200)
            i_vals = (voltage / r_vals) * 1000
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=r_vals, y=i_vals, mode='lines', name='Current vs Resistance', line=dict(color='#3B82F6', width=3)))
            fig.add_trace(go.Scatter(x=[resistance], y=[current*1000], mode='markers', name='Operating Point', marker=dict(size=12, color='red')))
            fig.update_layout(title="Current vs. Resistance at Fixed Voltage", xaxis_title="Resistance (Ω)", yaxis_title="Current (mA)", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Kirchhoff's Voltage Law (KVL) Series Circuit")
        st.write("The sum of all electrical potential differences around any closed loop is zero ($V_{total} = V_1 + V_2 + V_3$).")
        vs = st.number_input("Source Voltage (V_src)", value=12.0)
        r1 = st.number_input("Resistor 1 (Ω)", value=100.0)
        r2 = st.number_input("Resistor 2 (Ω)", value=220.0)
        r3 = st.number_input("Resistor 3 (Ω)", value=470.0)

        r_eq = r1 + r2 + r3
        i_circuit = vs / r_eq
        v1, v2, v3 = i_circuit * r1, i_circuit * r2, i_circuit * r3

        st.success(f"**Total Resistance:** {r_eq:.1f} Ω | **Circuit Current:** {i_circuit*1000:.2f} mA")
        st.write(f"- Voltage drop across R1 ($V_1$): **{v1:.2f} V**")
        st.write(f"- Voltage drop across R2 ($V_2$): **{v2:.2f} V**")
        st.write(f"- Voltage drop across R3 ($V_3$): **{v3:.2f} V**")
        st.write(f"- KVL Check: $V_1 + V_2 + V_3 = {v1+v2+v3:.2f} V$ (Equal to source)")

    with tab3:
        st.subheader("Joule Heating & Power Consumption")
        st.latex(r"P = V \times I = I^2 \times R = \frac{V^2}{R}")
        st.write("Calculate thermal power generated in an electrical component over time.")
        t_hrs = st.slider("Operating Duration (Hours)", 1, 24, 5)
        p_watts = st.number_input("Power Rating (Watts)", value=60.0)
        energy_kwh = (p_watts * t_hrs) / 1000.0
        st.info(f"⚡ Total Energy Consumed: **{energy_kwh:.3f} kWh**")
