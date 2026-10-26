import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(6, "Streamlit", "Extension", "optional", "Operations dashboard with AI chat interface")

st.warning("""
:material/info: **Optional extension.** The core AI platform (semantic view, search, agent) is already complete after Sessions 1–4. This session adds a visual frontend in Snowsight Workspaces and is a good starting point for hackathon week.
""")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on Snowflake's warehouse runtime using only built-in packages — no external network access required.", "icon": "web"},
    {"name": "Workspaces", "description": "An IDE-like environment in Snowsight where you can author, preview, and deploy Streamlit apps with Cortex Code assistance.", "icon": "code"},
    {"name": "st.connection(\"snowflake\")", "description": "The Streamlit connection API for Snowflake. No credentials needed — inherits the logged-in user's session.", "icon": "terminal"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open Workspaces")
with st.container(border=True):
    st.markdown("""
For this section, open **Workspaces** in Snowsight (left navigation panel → Projects → Workspaces). Workspaces provides an IDE-like environment where Cortex Code can create and edit Streamlit app files directly.

Paste the prompts below into Cortex Code **within Workspaces** so the generated code is written directly into your app files.
""")


PROMPT_6_1 = """In Workspaces, create a Streamlit app called SFR_OPS_DASHBOARD in TRICON_HOL.SFR_<INITIALS>.

Use the existing compute pool TRICON_HOL_POOL, which your admin already created. Do not create a new compute pool.

The app should use ONLY built-in Streamlit features (no external pip packages like plotly — use st.bar_chart, st.line_chart, st.metric, and st.dataframe instead). This avoids needing an External Access Integration.

Build 2 pages:

PAGE 1 - Operations Dashboard:
- KPI cards: total homes, latest month occupancy %, average monthly rent, open work orders
- Line chart: occupancy % by month for a market selected in a dropdown
- Bar chart: work order cost by category for the current year
- Table: top 10 most expensive open or recent work orders with vendor name
- Use st.bar_chart and st.line_chart for visualizations (NOT plotly)
- Use st.metric for KPI cards
- Use st.dataframe for tables

PAGE 2 - Intelligence Chat:
- A chat interface using our SFR_OPERATIONS_AGENT via SNOWFLAKE.CORTEX.AGENT()
- Sidebar with summary stats from the data

Important:
- Use st.connection("snowflake") for the connection — do NOT use get_active_session()
- Do NOT include plotly or any external packages in dependencies
- Only use streamlit built-in chart types (st.bar_chart, st.line_chart, st.area_chart)
- Make it visually clean with st.columns for layout

Generate all the app code."""

render_prompt("Prompt 6.1", "Create the Streamlit App", PROMPT_6_1)

st.success("""
:material/rocket_launch: **Preview and Deploy your app!**

Once Cortex Code has generated your app files in Workspaces:

1. **Run** — Click the **Run** button (▶️) in the top-right of the Workspaces editor to preview your app locally.

2. **Deploy** — When happy with the preview, click **Deploy** to publish the app to your Snowflake account so others with the appropriate role can access it.

Try modifying the app (add a chart, change KPI labels) and re-run to see changes live!
""")

render_explanation("What this prompt does", """
Creates a Streamlit in Snowflake application using only built-in packages:

**Why no plotly/external packages?**
The container runtime needs an External Access Integration (EAI) to download pip packages from pypi.org, and EAIs require admin approval. Using only Streamlit's built-in chart types (`st.bar_chart`, `st.line_chart`, `st.metric`, `st.dataframe`) means the app works without any EAI configuration.

**Built-in chart alternatives**:
| Instead of... | Use... |
|---------------|--------|
| `plotly.express.bar()` | `st.bar_chart(df, x=..., y=...)` |
| `plotly.express.line()` | `st.line_chart(df, x=..., y=...)` |
| `plotly.express.area()` | `st.area_chart(df, x=..., y=...)` |
| Custom tables | `st.dataframe(df)` with column_config |

**Connection pattern**:
```python
conn = st.connection("snowflake")
df = conn.query("SELECT * FROM ...")
st.dataframe(df)
```

This completes the workshop!
""")


render_key_concepts([
    {"term": "Workspaces", "definition": "Snowsight's built-in IDE for authoring Streamlit apps. Supports file editing, preview (Run), and deployment — all without leaving the browser."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes. Your admin pre-created TRICON_HOL_POOL with an instance family (CPU_X64_S) and min/max nodes; Snowflake handles provisioning."},
    {"term": "Built-in Charts", "definition": "Streamlit includes st.bar_chart, st.line_chart, st.area_chart, and st.map — no external packages needed. These work on all Snowflake runtimes without EAI."},
    {"term": "External Access Integration (EAI)", "definition": "Required to install pip packages on container runtime. Using only built-in packages avoids this requirement entirely."},
])

render_what_you_built([
    "TRICON_HOL_POOL — shared compute pool used by the Streamlit app",
    "SFR_OPS_DASHBOARD — 2-page Streamlit app using built-in components",
    "Operations Dashboard with KPIs and charts (no external dependencies)",
    "AI-powered chat interface connected to SFR_OPERATIONS_AGENT",
])
