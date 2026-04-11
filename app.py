"""
app.py — Streamlit Frontend for the Dev Toolkit Finder

A simple, clean UI that takes a developer's query and runs the
3-agent pipeline (Researcher → Synthesizer → Judge).
"""

import streamlit as st
from simple_agent import run_pipeline

# ── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Dev Toolkit Finder",
    page_icon="🛠️",
    layout="centered",
)

# ── Custom Styling ───────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="stApp"] {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }

    .score-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        border: 1px solid #334155;
    }

    .score-card h4 {
        margin: 0 0 0.3rem 0;
        color: #a5b4fc;
        font-size: 0.95rem;
    }

    .score-card .score-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #818cf8;
    }

    .score-card .reason {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    .overall-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }

    .agent-step {
        border-left: 3px solid #667eea;
        padding-left: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────

st.markdown('<h1 class="main-title">🛠️ Dev Toolkit Finder</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered developer tool recommendations — Search, Compare, Decide.</p>', unsafe_allow_html=True)


# ── Input Section ────────────────────────────────────────────────────────────

user_query = st.text_input(
    "What kind of developer tool are you looking for?",
    placeholder="e.g. Free open-source alternative to Postman for API testing",
    key="query_input",
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    search_clicked = st.button("🔍  Find Tools", use_container_width=True, type="primary")


# ── Run Pipeline ─────────────────────────────────────────────────────────────

if search_clicked and user_query.strip():
    with st.status("🤖 Running AI Agent Pipeline...", expanded=True) as status:

        # Agent 1
        st.write("**Agent 1 — Researcher:** Searching the web via Tavily...")
        try:
            result = run_pipeline(user_query.strip())
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

        status.update(label="✅ Pipeline complete!", state="complete", expanded=False)

    # ── Results ──────────────────────────────────────────────────────────────

    st.divider()

    # Show the synthesized recommendations
    st.markdown("## 🏆 Top Tool Recommendations")
    st.markdown(result["recommendations"])

    st.divider()

    # ── Judge Scores ─────────────────────────────────────────────────────────

    st.markdown("## 📊 LLM-as-Judge Evaluation")

    judge = result["judge"]

    # Overall score badge
    overall = judge.get("overall_score", "N/A")
    summary = judge.get("summary", "")
    st.markdown(
        f'<div class="overall-badge">Overall Quality Score: {overall} / 5.0<br>'
        f'<span style="font-weight:400; font-size:0.9rem;">{summary}</span></div>',
        unsafe_allow_html=True,
    )

    # Individual score cards
    scores = judge.get("scores", {})
    cols = st.columns(2)
    for idx, (criterion, data) in enumerate(scores.items()):
        with cols[idx % 2]:
            score_val = data.get("score", "N/A")
            reason = data.get("reason", "")
            st.markdown(
                f'<div class="score-card">'
                f'<h4>{criterion.upper()}</h4>'
                f'<span class="score-value">{score_val}/5</span>'
                f'<p class="reason">{reason}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Behind the Scenes ────────────────────────────────────────────────────

    st.divider()
    with st.expander("🔬 Behind the Scenes — Raw Research Data"):
        st.markdown(result["raw_research"])

elif search_clicked:
    st.warning("Please enter a query to search for tools.")


# ── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")
