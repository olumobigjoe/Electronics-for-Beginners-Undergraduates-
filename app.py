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

REQUIRED_MODULES = [
    "home.py",
    "app_fundamentals.py",
    "app_components.py",
    "app_gates.py",
    "app_digital_electronics.py",
    "app_circuit_analysis.py",
    "app_rectifiers.py",
    "app_amplifiers.py",
    "app_measurements.py",
]

# Auto-detect where the module files actually live: prefer a modules/
# subfolder, but fall back to the repo root if they were uploaded flat
# (a common outcome of GitHub's web "Upload files" button, which can
# flatten subfolder structure). This makes the app resilient to either
# layout without needing another round-trip to fix the repo.
_candidates = [BASE_DIR / "modules", BASE_DIR]
MODULES_DIR = next(
    (d for d in _candidates if all((d / m).is_file() for m in REQUIRED_MODULES)),
    BASE_DIR / "modules",  # default guess if neither location is complete
)

missing = [m for m in REQUIRED_MODULES if not (MODULES_DIR / m).is_file()]

if missing:
    # Surface a clear, actionable diagnostic in the app itself instead of
    # a bare stack trace. Both a modules/ subfolder and a flat repo-root
    # layout were checked automatically — this only fires if NEITHER
    # location has all 9 files.
    st.error(
        "Setup problem: one or more topic files are missing, so the app "
        "can't build its navigation menu."
    )
    st.write(f"**Checked (in order):** `{_candidates[0]}`, `{_candidates[1]}`")
    st.write(f"**Best-guess folder:** `{MODULES_DIR}`")
    st.write(f"**Files found there:** {sorted(p.name for p in MODULES_DIR.iterdir()) if MODULES_DIR.is_dir() else '(folder does not exist)'}")
    st.write(f"**Files found at repo root (`{BASE_DIR}`):** {sorted(p.name for p in BASE_DIR.iterdir())}")
    st.write(f"**Still missing:** {missing}")
    st.info(
        "Fix: make sure all 9 files (home.py + the 8 app_*.py files) "
        "exist together either in a `modules/` subfolder OR all together "
        "at the repo root — exact lowercase names, no typos."
    )
    st.stop()

# ----------------------------------------------------------------------
# Define every topic as a Page, plus a Home landing page. `title`/`icon`
# feed the (now hidden) built-in nav; `url_path` makes each topic
# deep-linkable, e.g. https://your-app-url/circuit_analysis
# ----------------------------------------------------------------------
home_page = st.Page(
    str(MODULES_DIR / "home.py"),
    title="Home",
    icon="🏠",
    default=True,
)

topic_pages = {
    "fundamentals": st.Page(
        str(MODULES_DIR / "app_fundamentals.py"),
        title="Electrical Fundamentals",
        icon="🔋",
        url_path="fundamentals",
    ),
    "components": st.Page(
        str(MODULES_DIR / "app_components.py"),
        title="Electronic Components",
        icon="⚡",
        url_path="components",
    ),
    "logic_gates": st.Page(
        str(MODULES_DIR / "app_gates.py"),
        title="Logic Gates",
        icon="🔌",
        url_path="logic_gates",
    ),
    "digital_electronics": st.Page(
        str(MODULES_DIR / "app_digital_electronics.py"),
        title="Digital Electronics",
        icon="💾",
        url_path="digital_electronics",
    ),
    "circuit_analysis": st.Page(
        str(MODULES_DIR / "app_circuit_analysis.py"),
        title="Circuit Analysis",
        icon="🧮",
        url_path="circuit_analysis",
    ),
    "rectifiers": st.Page(
        str(MODULES_DIR / "app_rectifiers.py"),
        title="Diodes & Rectifiers",
        icon="🔺",
        url_path="rectifiers",
    ),
    "amplifiers": st.Page(
        str(MODULES_DIR / "app_amplifiers.py"),
        title="Transistors & Amplifiers",
        icon="🔀",
        url_path="amplifiers",
    ),
    "measurements": st.Page(
        str(MODULES_DIR / "app_measurements.py"),
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
