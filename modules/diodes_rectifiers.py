import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.title("🔲 Diodes & Rectifiers Lab")
    st.write("Explore AC-to-DC conversion, half-wave, full-wave rectifiers, and Zener voltage regulation.")

    rect_type = st.radio("Select Rectifier Configuration:", ["Half-Wave Rectifier", "Full-Wave Bridge Rectifier"])
    
    col1, col2 = st.columns(2)
    with col1:
        v_peak = st.slider("Peak Input Voltage (V_pk)", 1.0, 50.0, 12.0)
        freq = st.slider("AC Frequency (Hz)", 10, 120, 50)
        filter_cap = st.checkbox("Enable Capacitor Filter")
        c_val = st.slider("Filter Capacitor (µF)", 10, 1000, 220) if filter_cap else 0

    t = np.linspace(0, 0.04, 1000)
    v_in = v_peak * np.sin(2 * np.pi * freq * t)

    if rect_type == "Half-Wave Rectifier":
        v_out = np.maximum(0, v_in - 0.7)
    else:
        v_out = np.abs(v_in) - 1.4
        v_out = np.maximum(0, v_out)

    if filter_cap and c_val > 0:
        rl = 1000.0
        dt = t[1] - t[0]
        for i in range(1, len(v_out)):
            if v_out[i] < v_out[i-1] * np.exp(-dt / (rl * c_val * 1e-6)):
                v_out[i] = v_out[i-1] * np.exp(-dt / (rl * c_val * 1e-6))

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t*1000, y=v_in, name="AC Input Voltage", line=dict(color='gray', dash='dash')))
        fig.add_trace(go.Scatter(x=t*1000, y=v_out, name="Rectified DC Output", line=dict(color='#22C55E', width=2.5)))
        fig.update_layout(title="AC Input vs Rectified Waveform", xaxis_title="Time (ms)", yaxis_title="Voltage (V)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
