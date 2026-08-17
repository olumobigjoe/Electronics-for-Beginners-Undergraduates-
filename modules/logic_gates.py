import streamlit as st
import pandas as pd

def run():
    st.title("⚡ Logic Gates Interactive Lab")
    st.write("Simulate digital logic gates and view interactive truth tables.")

    gate = st.selectbox("Choose Logic Gate:", ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"])

    if gate == "NOT":
        a = st.radio("Input A", [0, 1], horizontal=True)
        out = 0 if a == 1 else 1
        st.success(f"**Output Y:** `{out}`")
        df = pd.DataFrame({"Input A": [0, 1], "Output Y": [1, 0]})
        st.table(df)
    else:
        col1, col2 = st.columns(2)
        with col1:
            a = st.radio("Input A", [0, 1], horizontal=True, key="a_gate")
        with col2:
            b = st.radio("Input B", [0, 1], horizontal=True, key="b_gate")

        if gate == "AND": out = a & b
        elif gate == "OR": out = a | b
        elif gate == "NAND": out = int(not (a & b))
        elif gate == "NOR": out = int(not (a | b))
        elif gate == "XOR": out = a ^ b
        elif gate == "XNOR": out = int(not (a ^ b))

        st.success(f"**Output Y ({gate}):** `{out}`")

        # Full Truth Table
        inputs = [(0,0), (0,1), (1,0), (1,1)]
        res = []
        for x, y in inputs:
            if gate == "AND": r = x & y
            elif gate == "OR": r = x | y
            elif gate == "NAND": r = int(not (x & y))
            elif gate == "NOR": r = int(not (x | y))
            elif gate == "XOR": r = x ^ y
            elif gate == "XNOR": r = int(not (x ^ y))
            res.append(r)

        df = pd.DataFrame({"Input A": [0,0,1,1], "Input B": [0,1,0,1], f"Output Y ({gate})": res})
        st.subheader(f"Truth Table for {gate} Gate")
        st.table(df)
