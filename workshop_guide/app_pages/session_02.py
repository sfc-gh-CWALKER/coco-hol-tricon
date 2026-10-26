import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "Cortex Analyst & Semantic Views", "10:50 – 11:10", "20 min", "Semantic view with relationships, metrics, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries using a semantic view to understand your data's business meaning.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL — providing domain context and disambiguation hints.", "icon": "auto_fix_high"},
])


PROMPT_2_1 = """/semantic_studio In TRICON_HOL.SFR_<INITIALS>, create a semantic view called SFR_OPERATIONS_VIEW for use with Cortex Analyst. It should cover these tables: MARKETS, PROPERTIES, VENDORS, LEASES, WORK_ORDERS, MARKET_MONTHLY_PERFORMANCE.

Include:
- Relationships between the tables following these rules:
  - Do NOT specify join_type — omit it entirely (the proto enum doesn't accept string values like many_to_one)
  - Convention: left_table = fact/many side, right_table = dimension/one side (put the table with many rows as left_table)
  - Define primary_key.columns on dimension tables (MARKETS on MARKET_ID, PROPERTIES on PROPERTY_ID, VENDORS on VENDOR_ID) so the engine knows the "one" side
  - Use this template for each relationship:
    relationships:
      - name: <descriptive_name>
        left_table: <FACT_TABLE>
        right_table: <DIMENSION_TABLE>
        relationship_columns:
          - left_column: <FK_COLUMN>
            right_column: <PK_COLUMN>
  - Relationships needed: LEASES.PROPERTY_ID -> PROPERTIES.PROPERTY_ID; WORK_ORDERS.PROPERTY_ID -> PROPERTIES.PROPERTY_ID; WORK_ORDERS.VENDOR_ID -> VENDORS.VENDOR_ID; PROPERTIES.MARKET_ID -> MARKETS.MARKET_ID; MARKET_MONTHLY_PERFORMANCE.MARKET_ID -> MARKETS.MARKET_ID
- Facts for key numeric columns: LEASES.MONTHLY_RENT, LEASES.RENT_CHANGE_PCT, WORK_ORDERS.TOTAL_COST, WORK_ORDERS.DAYS_TO_COMPLETE, WORK_ORDERS.RESIDENT_SATISFACTION, PROPERTIES.ACQUISITION_PRICE, PROPERTIES.SQUARE_FEET, MARKET_MONTHLY_PERFORMANCE.OCCUPANCY_PCT, AVG_MONTHLY_RENT, MOVE_OUTS, AVG_DAYS_TO_RELEASE, BAD_DEBT_PCT
- Dimensions for categorical columns: MARKET_NAME, STATE, REGION, PROPERTY_TYPE, PROPERTY_STATUS, BEDROOMS, LEASE_TYPE, LEASE_STATUS, RESIDENT_SCORE_BAND, work order CATEGORY, PRIORITY, SOURCE, STATUS, VENDOR_NAME, TRADE, PREFERRED_VENDOR, and time dimensions LEASE_START_DATE, OPENED_DATE, MONTH
- Add useful SYNONYMS (e.g. 'homes'/'units'/'doors' for properties, 'tenant'/'resident', 'make-ready'/'turn'/'turnover', 'renewal increase' for RENT_CHANGE_PCT on renewals, 'R&M'/'repairs' for work orders)
- Metrics: total_work_order_cost (SUM TOTAL_COST), avg_days_to_complete, work_order_count, avg_monthly_rent on leases, avg_renewal_rent_change (AVG RENT_CHANGE_PCT where LEASE_TYPE='Renewal'), avg_new_lease_rent_change, lease_count, avg_occupancy_pct, total_move_outs
- An AI_SQL_GENERATION instruction with domain context: This is a single-family rental (SFR) portfolio. Occupancy and rent trends come from MARKET_MONTHLY_PERFORMANCE (monthly grain, one row per market per month) — never average occupancy across months without grouping by month or stating the period. 'Renewal' vs 'New Lease' is LEASE_TYPE. 'Blended rent growth' means the average of renewal and new lease rent change. 'Turnover' or 'make-ready' work orders have CATEGORY = 'Turnover / Make-Ready'. Open work orders are STATUS in ('In Progress','Scheduled') and have no cost yet. Dates in the data run through October 2026.

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 2.1", "Create the Semantic View", PROMPT_2_1)

render_explanation("What this prompt does", """
Creates a **semantic view** — a first-class Snowflake object that enables natural language to SQL.

**SFR concepts encoded in the view:**

- **Occupancy** lives at monthly market grain, so the AI instruction tells Analyst not to average it across months blindly.
- **Renewal vs new lease** rent change are separate metrics — the core revenue management lens.
- **Turnover / make-ready** is a work order category that drives both cost and days vacant.
- **Relationships** follow the left = fact (many) / right = dimension (one) rule: leases and work orders roll up to properties, properties and monthly performance roll up to markets, and work orders link to vendors.
- **Synonyms** let users say "homes", "doors", or "turns" and still hit the right columns.
""")


PROMPT_2_2 = """Ask Cortex Analyst these questions using TRICON_HOL.SFR_<INITIALS>.SFR_OPERATIONS_VIEW:

1. What was the average occupancy by market for September 2026, sorted from lowest to highest?
2. Compare average renewal rent change versus new lease rent change by region.
3. Which 5 vendors had the highest total work order cost in 2026, and what was their average days to complete?
4. Show the monthly trend of total move-outs across the portfolio for the last 12 months.

Show the generated SQL and results for each."""

render_prompt("Prompt 2.2", "Test with Natural Language Queries", PROMPT_2_2)

st.info("""
:material/lightbulb: **You can also test these in the Cortex Analyst UI!**

In Snowsight, navigate to **AI & ML → Cortex Analyst** in the left sidebar. Select your `SFR_OPERATIONS_VIEW` semantic view, and you'll see a playground where you can type natural language questions interactively.
""")

render_explanation("What this prompt does", """
Tests Cortex Analyst across different question types to validate the semantic view definitions.

| Question | What it validates |
|----------|-------------------|
| 1 | Time filter + dimension on the monthly performance table |
| 2 | Filtered metrics (renewal vs new) + join to MARKETS for region |
| 3 | Join WORK_ORDERS → VENDORS, aggregation, ranking |
| 4 | Time-series trend over the monthly grain |
""")


PROMPT_2_3 = """Now expand our SFR_OPERATIONS_VIEW in TRICON_HOL.SFR_<INITIALS>:

1. Add a metric emergency_work_order_pct = share of work orders with PRIORITY = 'Emergency'.
2. Add a metric cost_per_square_foot = total work order cost divided by total PROPERTIES.SQUARE_FEET.
3. Add a metric avg_turn_cost = average TOTAL_COST where CATEGORY = 'Turnover / Make-Ready'.
4. Add a verified query for "What is the average turn cost by market this year?" with its SQL.
Then test: "Which markets have the highest emergency work order percentage and average turn cost?"

Execute all SQL."""

render_prompt("Prompt 2.3", "Expand the Semantic View", PROMPT_2_3)

render_explanation("What this prompt does", """
Demonstrates iterative semantic view development — adding calculated metrics.

Adds operating metrics an SFR operations team watches weekly (emergency mix, R&M cost per sq ft, turn cost) and a **verified query**, which gives Cortex Analyst a trusted example to follow for similar questions.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Converts natural language to SQL using a semantic view for context."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object mapping tables to business concepts. Contains relationships, facts, dimensions, metrics, synonyms, and AI instructions."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions guiding SQL generation. Essential for domain-specific terminology."},
])

render_what_you_built([
    "SFR_OPERATIONS_VIEW semantic view with domain-specific metrics",
    "Natural language queries validated against the view",
    "Expanded view with calculated metrics",
])
