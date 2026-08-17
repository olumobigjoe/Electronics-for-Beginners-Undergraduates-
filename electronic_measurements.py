import streamlit as st
import numpy as np
import plotly.graph_objects as go

def run():
    st.title("📊 Electronic Measurements & Instrumentation")
    st.write("Virtual Oscilloscope, Multimeter basics, and Signal Generator analysis.")

    st.subheader("🎛️ Virtual Oscilloscope & Signal Generator")
    col1, col2 = st.columns(2)
    with col1:
        wave_type = st.selectbox("Waveform Type:", ["Sine", "Square", "Triangular", "Sawtooth"])
        amplitude = st.slider("Amplitude (Vpk)", 0.5, 20.0, 5.0)
        freq_hz = st.slider("Signal Frequency (Hz)", 50, 5000, 1000)
        dc_offset = st.slider("DC Offset (V)", -5.0, 5.0, 0.0)

    t = np.linspace(0, 3/freq_hz, 1000)
    if wave_type == "Sine":
        y = amplitude * np.sin(2 * np.pi * freq_hz * t) + dc_offset
    elif wave_type == "Square":
        y = amplitude * np.sign(np.sin(2 * np.pi * freq_hz * t)) + dc_offset
    elif wave_type == "Triangular":
        from scipy import signal
        y = amplitude * signal.sawtooth(2 * np.pi * freq_hz * t, width=0.5) + dc_offset
    else:
        from scipy import signal
        y = amplitude * signal.sawtooth(2 * np.pi * freq_hz * t) + dc_offset

    v_rms = np.sqrt(np.mean(y**2))
    v_pp = np.max(y) - np.min(y)

    with col2:
        st.metric("Peak-to-Peak Voltage (Vpp)", f"{v_pp:.2f} V")
        st.metric("Calculated RMS Voltage (Vrms)", f"{v_rms:.2f} V")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t*1000, y=y, line=dict(color='#10B981', width=2.5), name="Channel 1"))
    fig.update_layout(
        title="Oscilloscope Trace (CH1)",
        xaxis_title="Time (ms)",
        yaxis_title="Voltage (V)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
