# Electronics Learning Hub

A single Streamlit application that combines **8 interactive learning labs**
into one app, reachable at **one URL**, with a sidebar menu to switch
between topics:

| # | Topic | Icon |
|---|-------|------|
| 1 | Electrical Fundamentals | 🔋 |
| 2 | Electronic Components | ⚡ |
| 3 | Logic Gates | 🔌 |
| 4 | Digital Electronics | 💾 |
| 5 | Circuit Analysis | 🧮 |
| 6 | Diodes & Rectifiers | 🔺 |
| 7 | Transistors & Amplifiers | 🔀 |
| 8 | Measurements & Instruments | 📏 |

Built for first-year undergraduate Physics / Electronics students. No
external APIs, databases, or internet services are used — only
`streamlit`, `pandas`, and `matplotlib`.

## Navigation

The app opens on a **card-grid landing page** (not a plain sidebar
list) — each topic gets an icon, a level badge, a short blurb, and a
"Start Learning" button that jumps straight into that module. A small
"🏠 Hub Home" link is added to the bottom of every topic page's
sidebar so you can get back to the grid without hunting for a browser
back button.

## Project structure

```
electronics_learning_hub/
├── app.py                          # entry point — RUN THIS ONE
├── requirements.txt
├── README.md
├── modules/
    ├── home.py                     # card-grid landing page
    ├── app_fundamentals.py
    ├── app_components.py
    ├── app_gates.py
    ├── app_digital_electronics.py
    ├── app_circuit_analysis.py
    ├── app_rectifiers.py
    ├── app_amplifiers.py
    └── app_measurements.py
```

`app.py` uses Streamlit's built-in multi-page navigation
(`st.navigation` / `st.Page`) to stitch the 8 original, independently
built apps together **without modifying any of their internal code**.
Each module keeps its own `st.set_page_config(...)` call — that's safe
because Streamlit only ever executes the *one* page script currently
selected in the sidebar, never all 8 at once.

Each topic also gets its own URL slug, so pages are directly linkable,
e.g.:

```
https://your-app-url/circuit_analysis
https://your-app-url/amplifiers
```

## Running locally

1. **Install dependencies** (Python 3.9+ recommended):

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the combined app** (always run `app.py`, not the files inside
   `modules/`):

   ```bash
   streamlit run app.py
   ```

3. Streamlit will print a local URL (typically
   `http://localhost:8501`) — open it in your browser. Use the sidebar
   to jump between all 8 topics.

## Deploying to get one public URL

Any Streamlit-compatible host works. The easiest free option is
**Streamlit Community Cloud**:

1. Push this whole folder to a GitHub repository (keep the
   `modules/` subfolder structure intact).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in,
   and click "New app".
3. Point it at your repo, and set:
   - **Main file path:** `app.py`
4. Deploy. You'll get a single public URL
   (`https://<your-app-name>.streamlit.app`) that serves all 8 topics
   through the sidebar navigation.

Other options (Render, Railway, Hugging Face Spaces, an internal
server, etc.) work the same way — the only requirement is that the
process is started with `streamlit run app.py` and the `modules/`
folder is deployed alongside it.

## Notes / troubleshooting

- **"Unable to create Page. The file `...` could not be found."** — this
  means the platform's working directory isn't the repo root when it
  launches `app.py`. `app.py` now resolves `modules/*.py` as absolute
  paths anchored to its own file location (via `Path(__file__).parent`),
  which fixes this regardless of CWD. If you still hit it after
  updating, double-check that the `modules/` folder was actually pushed
  to your GitHub repo (browse the repo on GitHub.com and confirm the 8
  files are visible there) and that on Streamlit Community Cloud the
  **Main file path** is set to `app.py` (not `modules/app.py` or
  anything else).
- **Always launch via `app.py`.** Running e.g.
  `streamlit run modules/app_gates.py` directly will still work as a
  standalone app, but you'll lose the combined navigation and the
  single shared URL.
- If you add a 9th topic later, drop the new file into `modules/` and
  add one more `st.Page(...)` entry to the `pages` list in `app.py`.
- Requires Streamlit **1.36 or newer** (for `st.navigation`/`st.Page`).
  If your platform pins an older Streamlit version, bump it via
  `requirements.txt`.
