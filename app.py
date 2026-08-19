"""
Electronics Learning Hub
A single Streamlit application that combines all 8 topic modules into one
app (one URL, one sidebar navigation menu):

    1. Electrical Fundamentals
    2. Electronic Components
    3. Logic Gates
    4. Digital Electronics
    5. Circuit Analysis
    6. Diodes & Rectifiers
    7. Transistors & Amplifiers
    8. Measurements & Instruments

HOW THIS WORKS
--------------
Streamlit's built-in multi-page navigation (`st.navigation` / `st.Page`,
available in Streamlit >= 1.36) is used to stitch the 8 original,
independent single-file apps together WITHOUT modifying their internal
code. Each module keeps its own `st.set_page_config(...)` call — that is
fine, because Streamlit only executes the ONE page script that is
currently selected in the sidebar; the other 7 scripts are not run at
the same time, so there is no "set_page_config called twice" conflict.

This file (app.py) is the only entry point. It must be run with:

    streamlit run app.py

Do NOT run any of the files inside modules/ directly with `streamlit
run` on their own if you want the combined experience — run app.py.
"""

from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------
# Resolve module paths relative to THIS file's location on disk (not the
# process's current working directory). Some deployment platforms
# (Streamlit Community Cloud among them) can launch the app with a CWD
# that differs from the repo root, which makes plain relative strings
# like "modules/app_fundamentals.py" fail with:
#   "Unable to create Page. The file `...` could not be found."
# Anchoring to __file__ makes this work the same locally and deployed.
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
MODULES_DIR = BASE_DIR / "modules"

REQUIRED_MODULES = [
    "app_fundamentals.py",
    "app_components.py",
    "app_gates.py",
    "app_digital_electronics.py",
    "app_circuit_analysis.py",
    "app_rectifiers.py",
    "app_amplifiers.py",
    "app_measurements.py",
]

missing = [m for m in REQUIRED_MODULES if not (MODULES_DIR / m).is_file()]

if missing:
    # Surface a clear, actionable diagnostic in the app itself instead of
    # a bare stack trace. This tells you exactly what Streamlit Cloud
    # actually sees on disk, which is the fastest way to tell whether the
    # `modules/` folder made it into the deployed repo at all.
    st.error(
        "Setup problem: one or more topic files are missing, so the app "
        "can't build its navigation menu."
    )
    st.write(f"**Expected folder:** `{MODULES_DIR}`")
    st.write(f"**Folder exists:** {MODULES_DIR.is_dir()}")
    if MODULES_DIR.is_dir():
        found = sorted(p.name for p in MODULES_DIR.iterdir())
        st.write(f"**Files actually found in `modules/`:** {found or '(empty)'}")
    else:
        st.write(f"**Files found in app root (`{BASE_DIR}`):**")
        st.write(sorted(p.name for p in BASE_DIR.iterdir()))
    st.write(f"**Missing:** {missing}")
    st.info(
        "Fix: open your GitHub repo in the browser and confirm there is a "
        "`modules/` folder at the repo root containing these 8 files "
        "(exact names, lowercase). If it's not there, the folder was "
        "never pushed / got flattened during upload — re-add it and "
        "redeploy. If it IS there but this still fails, check for a "
        "`.gitignore` rule or nested extra folder (e.g. "
        "`elect_4_beginners/modules/` inside `modules/`)."
    )
    st.stop()

# ----------------------------------------------------------------------
# Define every topic as a Page, plus a Home landing page. `title`/`icon`
# feed the (now hidden) built-in nav; `url_path` makes each topic
# deep-linkable, e.g. https://your-app-url/circuit_analysis
# ----------------------------------------------------------------------
home_page = st.Page(
    str("home.py"),
    title="Home",
    icon="🏠",
    default=True,
)

topic_pages = {
    "fundamentals": st.Page(
        str("app_fundamentals.py"),
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),
    "components": st.Page(
        str( "app_components.py"),
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),
    "logic_gates": st.Page(
        str("app_gates.py"),
        title="Logic Gates",
        icon="🔌",
        url_path="logic_gates",
    ),
    "digital_electronics": st.Page(
        str("app_digital_electronics.py"),
        title="Digital Electronics",
        icon="💾",
        url_path="digital_electronics",
    ),
    "circuit_analysis": st.Page(
        str("app_circuit_analysis.py"),
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit_analysis",
    ),
    "rectifiers": st.Page(
        str("app_rectifiers.py"),
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),
    "amplifiers": st.Page(
        str("app_amplifiers.py"),
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),
    "measurements": st.Page(
        str("app_measurements.py"),
        title="Measurements & Instruments",
        icon="📏",
        url_path="measurements",
    ),
}

# Stash the Page objects in session_state BEFORE navigation runs, so the
# home page's "Start Learning" buttons can look them up and call
# st.switch_page(...) on them (page identity, not just a path string).
st.session_state["_pages_by_key"] = topic_pages

pages = [home_page] + list(topic_pages.values())

# Every page (including the ones you didn't touch) can still put its own
# content in the sidebar the way it always did — we're only hiding
# Streamlit's *automatic* page-list widget, not the sidebar itself.
#
# IMPORTANT ORDERING: this Home link is added AFTER nav.run(), not
# before. Each page script's first command must be its own
# st.set_page_config() call — anything st.* rendered in app.py before
# nav.run() would break that rule and crash every page. Adding it after
# nav.run() means it renders at the bottom of whatever sidebar content
# that page already built, which is a safe trade-off.
nav = st.navigation(pages, position="hidden")
nav.run()

with st.sidebar:
    st.divider()
    st.page_link(home_page, label="🏠 Hub Home")
