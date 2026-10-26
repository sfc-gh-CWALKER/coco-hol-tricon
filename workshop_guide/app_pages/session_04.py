import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Agents", "11:25 – 11:50", "25 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools, executes them, reflects on results, and generates responses.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for documents, custom UDFs for logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities with custom business logic.", "icon": "build"},
])


PROMPT_4_1 = """In TRICON_HOL.SFR_<INITIALS>, create a Cortex Agent called SFR_OPERATIONS_AGENT.

It should:
- Use auto as the orchestration model
- Have two tools: the SFR_OPERATIONS_VIEW semantic view (for structured data queries) and the SFR_DOCS_SEARCH Cortex Search service (for unstructured document search)
- Include instructions defining it as the Tricon SFR Portfolio Operations Assistant, guiding it to use structured data for occupancy, rent and rent growth, leases and renewals, work order cost and speed, vendor performance, and market comparisons and search for resident complaints, inspection findings, root causes, and what our operating procedures (SOPs) require
- Mention domain context: single-family rental homes across 14 markets; scattered-site and build-to-rent communities; key KPIs are occupancy, blended rent growth, days to re-lease, turnover cost, and resident satisfaction. KPI definitions are in SOP-020 and should be cited when defining metrics. Always state the time period of any number and never invent data.
- Include 3-4 sample questions spanning both tools

Execute and show confirmation."""

render_prompt("Prompt 4.1", "Create the Cortex Agent", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** combining structured analytics with document search:

- **Structured questions** → routed to Cortex Analyst via the semantic view
- **Unstructured questions** → routed to Cortex Search
- **Mixed questions** → Agent uses both tools and synthesizes
""")


PROMPT_4_2 = """Test our SFR_OPERATIONS_AGENT with these queries:

1. (Structured) "Which three markets had the lowest occupancy in September 2026, and how does each compare to its target occupancy?"
2. (Unstructured) "What does our SOP require when a resident reports mold, and have we had tickets like that?"
3. (Mixed) "Which work order categories cost the most this year, and what do tickets and inspections say is driving them?"

Show the responses and note which tools the agent selected."""

render_prompt("Prompt 4.2", "Test the Agent", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests the agent with structured, unstructured, and mixed queries to validate tool routing.
""")


PROMPT_4_3 = """In TRICON_HOL.SFR_<INITIALS>, add a custom tool to the agent:

1. Create a UDF:

CREATE OR REPLACE FUNCTION CALCULATE_TURNOVER_COST(
    monthly_rent FLOAT, days_vacant INT, make_ready_cost FLOAT)
RETURNS OBJECT
COMMENT = 'Estimates the full cost of a resident move-out: lost rent while vacant, make-ready cost, and leasing cost (half a month of rent).'
AS $$
  OBJECT_CONSTRUCT(
    'lost_rent', ROUND(monthly_rent * 12 / 365 * days_vacant, 2),
    'make_ready_cost', make_ready_cost,
    'leasing_cost', ROUND(monthly_rent * 0.5, 2),
    'total_turnover_cost', ROUND(monthly_rent * 12 / 365 * days_vacant + make_ready_cost + monthly_rent * 0.5, 2),
    'months_of_rent', ROUND((monthly_rent * 12 / 365 * days_vacant + make_ready_cost + monthly_rent * 0.5) / NULLIF(monthly_rent, 0), 1)
  )
$$;

2. Recreate SFR_OPERATIONS_AGENT with CALCULATE_TURNOVER_COST as an additional tool.

3. Test with: "A home renting for $2,150 a month sat vacant for 28 days and needed $3,400 of make-ready. What did that turnover cost in total, and would it have been cheaper to offer the resident a 4% smaller renewal increase for 12 months?"

Execute all SQL."""

render_prompt("Prompt 4.3", "Agent with Custom Tool", PROMPT_4_3)

render_explanation("What this prompt does", """
Adds a **custom UDF tool** for domain-specific calculations. The Agent can now query data, search documents, AND run custom business logic.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A Snowflake object that orchestrates LLMs, Analyst, Search, and custom tools to answer complex questions."},
    {"term": "Tool Routing", "definition": "The Agent selects the right tool for each question based on the question type and tool descriptions."},
    {"term": "Custom Tools", "definition": "SQL UDFs registered as Agent tools. Enable domain-specific calculations and business logic."},
])

render_what_you_built([
    "SFR_OPERATIONS_AGENT — Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, and mixed queries",
    "CALCULATE_TURNOVER_COST as a custom tool",
    "Enhanced agent with three tool types",
])
