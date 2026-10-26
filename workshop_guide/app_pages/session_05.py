import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, personalize

render_session_header(5, "CoWork", "Extension", "optional", "Collaborative AI analysis with CoWork")

st.warning("""
:material/info: **Optional extension.** CoWork runs in Snowsight, not Cortex Code Desktop. Use this session if you finish early or during hackathon week, and check with your admin that CoWork is enabled for `TRICON_HOL_ROLE`.
""")

render_technologies_used([
    {"name": "Snowflake CoWork", "description": "An AI-powered collaborative workspace inside Snowsight where you can analyze data, generate insights, and share findings.", "icon": "group"},
    {"name": "Data Analysis", "description": "CoWork can query your Snowflake data, generate visualizations, and provide insights without writing SQL.", "icon": "analytics"},
    {"name": "Sharing & Collaboration", "description": "CoWork sessions can be shared with team members for collaborative data exploration.", "icon": "share"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open CoWork")
with st.container(border=True):
    st.markdown("""
In Snowsight, click **CoWork** in the left navigation panel. Start a new conversation.

CoWork discovers your tables in `TRICON_HOL.SFR_<INITIALS>` automatically. Paste each question below one at a time.
""")

st.space("small")

st.markdown("#### :material/chat: Questions to ask CoWork")
st.caption("Copy and paste each question into CoWork individually.")

questions = [
    ("Portfolio snapshot", "Give me a one-paragraph snapshot of the portfolio in TRICON_HOL.SFR_<INITIALS>: number of homes by market, latest month occupancy, and average rent. Show a chart."),
    ("Renewal vs new lease", "How does renewal rent change compare with new lease rent change by region over time? What should a revenue manager take away?"),
    ("Maintenance hotspots", "Which markets and work order categories are driving maintenance cost this year? Break it down and visualize it."),
    ("Vendor scorecard", "Build a vendor scorecard: total cost, work order count, average days to complete, and average resident satisfaction. Which vendors should we review?"),
    ("Resident pain points", "Read the resident service tickets and summarize the top recurring themes, with examples and suggested process fixes."),
]

for title, question in questions:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.code(personalize(question), language="text", wrap_lines=True)

st.space("small")

render_explanation("How CoWork works", """
**CoWork** is Snowflake's collaborative AI workspace — different from Cortex Code:

| Tool | Best for |
|------|----------|
| Cortex Code | Building infrastructure, creating objects, writing SQL |
| CoWork | Exploring data, generating insights, team collaboration |
| Cortex Agent | End-user Q&A interface (deployed as a product) |
""")

render_key_concepts([
    {"term": "CoWork", "definition": "Snowflake's collaborative AI workspace. Conversational interface that queries data, creates visualizations, and generates insights."},
    {"term": "Context Maintenance", "definition": "CoWork maintains conversation history so follow-up questions build on previous analysis."},
])

render_what_you_built([
    "Explored operations data through conversational AI",
    "Generated visualizations and cross-table analysis",
    "Demonstrated the CoWork collaborative analysis pattern",
])
