import streamlit as st

st.title("Tricon SFR Operations AI Lab")
st.markdown("Building an AI-powered portfolio operations assistant for single-family rental — with Cortex Code Desktop, in Tricon's own Snowflake account")

st.space("small")

col1, col2, col3 = st.columns(3)
col1.metric("Sections", "4 + 2", help="4 core sessions plus 2 optional extensions")
col2.metric("Prompts", "13", help="Cortex Code prompts across all sessions")
col3.metric("Duration", "90 min", help="Total workshop time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each section has **numbered prompts** that you copy and paste into the appropriate tool:

- **Cortex Code Desktop** — for building infrastructure, creating objects, and writing SQL/Python
- **Cortex Analyst** — for testing natural language queries against your semantic view
- **Snowflake CoWork** — for collaborative data exploration and analysis

All prompts build on each other, so run them in order. Enter your initials in the sidebar first; every prompt then uses your own schema.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
A single-family rental operator runs a scattered-site and build-to-rent portfolio across 14 Sun Belt and Midwest markets. Operations, revenue management, and asset management teams juggle leases, renewals, work orders, vendor performance, inspections, and resident tickets — and the answers to everyday questions are split between structured reports and free-text notes.

:material/info: **All data in this lab is synthetic.** Markets resemble an SFR footprint, but no Tricon, resident, or vendor data is used.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Markets, properties, vendors, leases, work orders |
| **Unstructured** | Resident service tickets, property inspection findings, operating procedures (SOPs) |
| **Time series** | Monthly market performance: occupancy, rent, rent growth, move-outs, days to re-lease, bad debt |
""")

st.space("small")

st.markdown("#### What we're building")

with st.container(border=True):
    st.markdown("""
In 90 min, we build a complete AI-powered operations platform:

**1. Data Foundation** — Load structured and unstructured operations data into Snowflake from pre-generated CSV files.

**2. Natural Language Analytics** — Create a Semantic View over operational tables and query them with plain English via Cortex Analyst.

**3. Intelligent Search** — Build a Cortex Search service over resident tickets, inspection findings, and SOPs for hybrid semantic + keyword search.

**4. AI Agents** — Create a Cortex Agent that orchestrates structured data queries AND document search through a single conversational interface.

**5. Collaborative AI** *(optional)* — Use CoWork to collaboratively analyze data with AI assistance.

**6. Operations Dashboard** *(optional)* — Deploy a Streamlit app with live KPIs, charts, and an AI chat interface.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- **Cortex Code Desktop** installed and connected to Tricon's Snowflake account (see **Getting Started**)
- The `TRICON_HOL_ROLE` role and `TRICON_HOL_WH` warehouse, both pre-provisioned by your admin
- Your initials entered in the sidebar
""")

st.space("medium")
st.caption("Built for the November 9, 2026 workshop  :material/location_on:  Tricon Residential, Tustin, CA (India team joining virtually)")
