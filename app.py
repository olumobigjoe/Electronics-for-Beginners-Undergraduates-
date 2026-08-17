import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Electronics for Beginners",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clickable card styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .card-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.25s ease-in-out;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .card-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6;
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.4;
        margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize navigation state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

def navigate_to(page_name):
    st.session_state.current_page = page_name

# Sidebar Navigation
st.sidebar.title("⚡ Navigation")
nav_options = [
    "🏠 Home (All Modules)",
    "🔌 Electrical Fundamentals",
    "🧰 Intro to Electronic Components",
    "🔲 Diodes & Rectifiers",
    "📻 Transistors & Amplifiers",
    "⚡ Logic Gates Lab",
    "💻 Digital Electronics",
    "📐 Circuit Analysis",
    "📊 Electronic Measurements"
]

mapping = {
    "🏠 Home (All Modules)": "Home",
    "🔌 Electrical Fundamentals": "Electrical Fundamentals",
    "🧰 Intro to Electronic Components": "Intro to Electronic Components",
    "🔲 Diodes & Rectifiers": "Diodes & Rectifiers",
    "📻 Transistors & Amplifiers": "Transistors & Amplifiers",
    "⚡ Logic Gates Lab": "Logic Gates Lab",
    "💻 Digital Electronics": "Digital Electronics",
    "📐 Circuit Analysis": "Circuit Analysis",
    "📊 Electronic Measurements": "Electronic Measurements"
}

# Determine current selectbox index
inverse_mapping = {v: k for k, v in mapping.items()}
current_label = inverse_mapping.get(st.session_state.current_page, "🏠 Home (All Modules)")

selected_nav = st.sidebar.selectbox("Select Topic:", nav_options, index=nav_options.index(current_label))
st.session_state.current_page = mapping[selected_nav]

# Sidebar helper info
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Select any module above or click the cards on the main dashboard to begin learning.")

# Import modules dynamically
from modules import (
    electrical_fundamentals,
    intro_components,
    diodes_rectifiers,
    transistors_amplifiers,
    logic_gates,
    digital_electronics,
    circuit_analysis,
    electronic_measurements
)

# -------------------------- HOME LANDING PAGE --------------------------
if st.session_state.current_page == "Home":
    st.markdown('<div class="main-title">⚡ Electronics for Beginners</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Master electronic principles, circuit theory, and digital logic through interactive tools and simulations.</div>', unsafe_allow_html=True)
    
    # 8 Main Interactive Cards Configuration
    cards = [
        {
            "id": "Electrical Fundamentals",
            "title": "1. Electrical Fundamentals",
            "icon": "🔌",
            "desc": "Master Ohm's Law, Kirchhoff's Laws (KCL/KVL), and Power calculations with interactive visualizers."
        },
        {
            "id": "Intro to Electronic Components",
            "title": "2. Intro to Components",
            "icon": "🧰",
            "desc": "Explore fundamental passives and active components: Resistors, Capacitors, Inductors, and Diodes."
        },
        {
            "id": "Diodes & Rectifiers",
            "title": "3. Diodes & Rectifiers",
            "icon": "🔲",
            "desc": "Simulate Half-Wave, Full-Wave Bridge rectifiers, filtering, and Zener voltage regulation."
        },
        {
            "id": "Transistors & Amplifiers",
            "title": "4. Transistors & Amplifiers",
            "icon": "📻",
            "desc": "Analyze BJT and MOSFET characteristics, DC biasing points, and amplifier frequency response."
        },
        {
            "id": "Logic Gates Lab",
            "title": "5. Logic Gates Lab",
            "icon": "⚡",
            "desc": "Interactive truth table builder and real-time simulator for AND, OR, NOT, NAND, NOR, XOR, and XNOR."
        },
        {
            "id": "Digital Electronics",
            "title": "6. Digital Electronics",
            "icon": "💻",
            "desc": "Learn binary/hex conversions, Boolean simplification, Adders, Multiplexers, and Flip-Flops."
        },
        {
            "id": "Circuit Analysis",
            "title": "7. Circuit Analysis",
            "icon": "📐",
            "desc": "Solve complex networks using Nodal & Mesh Analysis, Thevenin/Norton theorems, and RC/RL transient step response."
        },
        {
            "id": "Electronic Measurements",
            "title": "8. Measurements & Setup",
            "icon": "📊",
            "desc": "Learn oscilloscope controls, multimeter operation, signal generation, and measurement accuracy analysis."
        }
    ]

    # Grid Display (2 rows of 4 cards)
    row1 = cards[:4]
    row2 = cards[4:]

    cols1 = st.columns(4)
    for idx, card in enumerate(row1):
        with cols1[idx]:
            st.markdown(f'''
                <div class="card-container">
                    <div>
                        <div class="card-icon">{card['icon']}</div>
                        <div class="card-title">{card['title']}</div>
                        <div class="card-desc">{card['desc']}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Explore Module ➔", key=f"btn_{card['id']}"):
                st.session_state.current_page = card['id']
                st.rerun()

    st.write("") # Spacer

    cols2 = st.columns(4)
    for idx, card in enumerate(row2):
        with cols2[idx]:
            st.markdown(f'''
                <div class="card-container">
                    <div>
                        <div class="card-icon">{card['icon']}</div>
                        <div class="card-title">{card['title']}</div>
                        <div class="card-desc">{card['desc']}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Explore Module ➔", key=f"btn_{card['id']}"):
                st.session_state.current_page = card['id']
                st.rerun()

# -------------------------- ROUTING TO SUB-MODULES --------------------------
elif st.session_state.current_page == "Electrical Fundamentals":
    electrical_fundamentals.run()
elif st.session_state.current_page == "Intro to Electronic Components":
    intro_components.run()
elif st.session_state.current_page == "Diodes & Rectifiers":
    diodes_rectifiers.run()
elif st.session_state.current_page == "Transistors & Amplifiers":
    transistors_amplifiers.run()
elif st.session_state.current_page == "Logic Gates Lab":
    logic_gates.run()
elif st.session_state.current_page == "Digital Electronics":
    digital_electronics.run()
elif st.session_state.current_page == "Circuit Analysis":
    circuit_analysis.run()
elif st.session_state.current_page == "Electronic Measurements":
    electronic_measurements.run()
