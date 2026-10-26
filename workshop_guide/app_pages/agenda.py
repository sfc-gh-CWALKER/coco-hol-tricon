import streamlit as st

st.title("Workshop agenda")

AGENDA = [
    ("10:30 – 10:35", "Welcome, check CoCo Desktop is connected, enter your initials", None, None),
    ("10:35 – 10:50", "Session 1: Data Prep", "15 min", "1"),
    ("10:50 – 11:10", "Session 2: Cortex Analyst & Semantic Views", "20 min", "2"),
    ("11:10 – 11:25", "Session 3: Cortex Search", "15 min", "3"),
    ("11:25 – 11:50", "Session 4: Cortex Agents", "25 min", "4"),
    ("11:50 – 12:00", "Wrap-up: what you built, hackathon ideas, Q&A", None, None),
    ("Extension", "Session 5: CoWork", "optional", "5"),
    ("Extension", "Session 6: Streamlit", "optional", "6"),
]

for time, title, duration, session_num in AGENDA:
    col1, col2 = st.columns([1, 4])
    col1.markdown(f"**{time}**")
    if session_num:
        col2.markdown(f":material/play_circle: **{title}** :gray-badge[{duration}]")
    else:
        col2.markdown(f":gray[{title}]")

st.caption("Sessions 1–4 are the core lab. Sessions 5–6 are for fast finishers or for the hackathon week (Nov 10–13).")

st.space("medium")

st.markdown("##### What you'll build by end of session")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | 9 | Leases, work orders, monthly market performance, resident tickets |
| **Semantic Views** | 1 | SFR_OPERATIONS_VIEW with relationships, metrics, and AI instructions |
| **Cortex Search Services** | 1 | SFR_DOCS_SEARCH over tickets, inspections, and SOPs |
| **Cortex Agents** | 1 | SFR_OPERATIONS_AGENT with Analyst + Search + a turnover cost tool |
| **Streamlit Apps** (optional) | 1 | Operations dashboard with AI chat |
""")

st.space("small")

st.markdown("##### Location")
with st.container(border=True):
    st.markdown("""
:material/location_on: **Tricon Residential, Tustin, CA** — India team joining virtually

November 9, 2026 — 10:30 AM to 12:00 PM PT
""")
