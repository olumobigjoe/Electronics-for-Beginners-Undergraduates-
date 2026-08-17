import streamlit as st

def run():
    st.title("💻 Digital Electronics for Beginners")
    st.write("Master Number Systems, Boolean Algebra, Combinational Logic, and Sequential Circuits.")

    tab1, tab2 = st.tabs(["🔢 Number System Converter", "➕ Half / Full Adder Simulator"])

    with tab1:
        st.subheader("Decimal / Binary / Hexadecimal Converter")
        dec_val = st.number_input("Enter Decimal Number:", min_value=0, max_value=65535, value=42)
        
        st.info(f"**Binary Representation:** `0b{bin(dec_val)[2:]}`")
        st.info(f"**Hexadecimal Representation:** `0x{hex(dec_val)[2:].upper()}`")
        st.info(f"**Octal Representation:** `0o{oct(dec_val)[2:]}`")

    with tab2:
        st.subheader("1-Bit Full Adder Simulator")
        st.write("Sum = A ⊕ B ⊕ Cin | Cout = (A · B) + (Cin · (A ⊕ B))")
        col1, col2, col3 = st.columns(3)
        with col1: a = st.selectbox("Input A", [0, 1])
        with col2: b = st.selectbox("Input B", [0, 1])
        with col3: cin = st.selectbox("Carry In (Cin)", [0, 1])

        sum_out = a ^ b ^ cin
        cout = (a & b) | (cin & (a ^ b))

        st.metric("Sum Output (S)", sum_out)
        st.metric("Carry Output (Cout)", cout)
