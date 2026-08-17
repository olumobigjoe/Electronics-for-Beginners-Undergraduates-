import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.title("📐 Circuit Analysis Tools")
    st.write("Solve DC networks and time-domain RC/RL transient step responses.")

    tab1, tab2 = st.tabs(["⚡ RC Transient Response", "🔄 Thevenin Equivalent Solver"])

    with tab1:
        st.subheader("RC Series Circuit Step Response (Charging / Discharging)")
        v_step = st.slider("Source Voltage (V)", 1.0, 24.0, 5.0)
        r_k = st.slider("Resistor (kΩ)", 1.0, 100.0, 10.0) * 1000
        c_uf = st.slider("Capacitor (µF)", 0.1, 100.0, 10.0) * 1e-6

        tau = r_k * c_uf
        st.write(f"⏱️ **Time Constant (τ = R × C):** {tau*1000:.2f} ms")

        t = np.linspace(0, 5*tau, 500)
        vc_charge = v_step * (1 - np.exp(-t / tau))
        vc_discharge = v_step * np.exp(-t / tau)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t*1000, y=vc_charge, name="Capacitor Charging V_C(t)", line=dict(color='#2563EB', width=2.5)))
        fig.add_trace(go.Scatter(x=t*1000, y=vc_discharge, name="Capacitor Discharging V_C(t)", line=dict(color='#DC2626', dash='dash')))
        fig.update_layout(title="Capacitor Voltage vs Time", xaxis_title="Time (ms)", yaxis_title="Voltage (V)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Voltage Divider Thevenin Equivalent")
        st.write("Calculates Vth and Rth for a standard loaded voltage divider.")
        vs = st.number_input("Supply Voltage (Vs)", value=12.0)
        r1 = st.number_input("R1 (Ω)", value=1000.0)
        r2 = st.number_input("R2 (Ω)", value=2000.0)

        vth = vs * (r2 / (r1 + r2))
        rth = (r1 * r2) / (r1 + r2)

        st.success(f"**Thevenin Voltage (Vth):** {vth:.2f} V")
        st.success(f"**Thevenin Resistance (Rth):** {rth:.2f} Ω")
