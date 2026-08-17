import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.title("📻 Transistors & Amplifiers")
    st.write("Understand Bipolar Junction Transistors (BJTs) and Field Effect Transistors (FETs).")

    mode = st.selectbox("Select Topic:", ["BJT Collector Curves (I_C vs V_CE)", "Common Emitter Amplifier Bias Point"])

    if mode == "BJT Collector Curves (I_C vs V_CE)":
        st.subheader("BJT Characteristic Output Curves")
        ib_step = st.slider("Base Current Step (µA)", 10, 100, 20)
        beta = st.slider("Transistor Current Gain (β / hFE)", 50, 300, 100)

        vce = np.linspace(0, 15, 200)
        fig = go.Figure()

        for ib_uA in range(ib_step, ib_step * 6, ib_step):
            ib_A = ib_uA * 1e-6
            ic_sat = beta * ib_A * (1 - np.exp(-vce / 0.5))
            fig.add_trace(go.Scatter(x=vce, y=ic_sat * 1000, mode='lines', name=f'Ib = {ib_uA} µA'))

        fig.update_layout(title="BJT Output Characteristic Curves", xaxis_title="V_CE (Volts)", yaxis_title="I_C (mA)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.subheader("DC Load Line & Q-Point Analysis")
        vcc = st.slider("Supply Voltage (Vcc)", 5.0, 30.0, 12.0)
        rc = st.slider("Collector Resistance Rc (Ω)", 100, 5000, 1000)
        rb = st.slider("Base Resistance Rb (kΩ)", 10, 500, 100) * 1000
        beta = 100

        ib = (vcc - 0.7) / rb
        ic = beta * ib
        vce = vcc - ic * rc

        st.metric("Operating Point (Q-Point)", f"Vce = {vce:.2f} V, Ic = {ic*1000:.2f} mA")

        vce_line = np.linspace(0, vcc, 100)
        ic_line = ((vcc - vce_line) / rc) * 1000

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=vce_line, y=ic_line, name='DC Load Line', line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=[vce], y=[ic*1000], mode='markers', name='Q-Point', marker=dict(size=14, color='blue')))
        fig.update_layout(title="DC Load Line and Q-Point", xaxis_title="V_CE (V)", yaxis_title="I_C (mA)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
