import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "10:35 – 10:50", "15 min", "Your personal schema, stage, and 9 operational tables loaded from CSV")

render_technologies_used([
    {"name": "Database & Schema", "description": "Snowflake's organizational hierarchy for objects. A database contains schemas, and schemas contain tables, views, and other objects.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "Virtual Warehouse", "description": "Snowflake's compute engine. A warehouse provides the CPU and memory to execute queries and load data.", "icon": "memory"},
])


PROMPT_1_1 = """Set up my workspace for the Tricon single-family rental AI workshop. The database TRICON_HOL and warehouse TRICON_HOL_WH already exist, so do not create them.

1. Use role TRICON_HOL_ROLE and warehouse TRICON_HOL_WH
2. Create a schema called SFR_<INITIALS> in the TRICON_HOL database (IF NOT EXISTS)
3. Create an internal stage called DATA in TRICON_HOL.SFR_<INITIALS> with a directory table and server-side encryption
4. Set the session context to TRICON_HOL.SFR_<INITIALS>

Execute all SQL and confirm each object was created."""

render_prompt("Prompt 1.1", "Create Your Schema & Stage", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates your personal workspace inside the shared, admin-provisioned database:

```sql
USE ROLE TRICON_HOL_ROLE;
USE WAREHOUSE TRICON_HOL_WH;
CREATE SCHEMA IF NOT EXISTS TRICON_HOL.SFR_<INITIALS>;
CREATE STAGE TRICON_HOL.SFR_<INITIALS>.DATA
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
USE SCHEMA TRICON_HOL.SFR_<INITIALS>;
```

Each attendee works in their own schema, so everyone can create objects with the same names (semantic view, search service, agent) without collisions.
""")


PROMPT_1_2 = """The 9 workshop CSV files are unzipped on my computer in the folder ~/Downloads/tricon_sfr_data (adjust if I saved them elsewhere).

1. Upload all 9 CSV files to the stage @TRICON_HOL.SFR_<INITIALS>.DATA using PUT with AUTO_COMPRESS=FALSE
2. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
3. For all 9 tables (MARKETS, PROPERTIES, VENDORS, LEASES, WORK_ORDERS, MARKET_MONTHLY_PERFORMANCE, RESIDENT_SERVICE_TICKETS, PROPERTY_INSPECTIONS, OPERATING_PROCEDURES), create the table in TRICON_HOL.SFR_<INITIALS> with column types inferred from the data, using CREATE TABLE ... USING TEMPLATE with INFER_SCHEMA. Make sure the column names are uppercase.
4. Load each table with COPY INTO

The key requirement is that all 9 tables are created and populated. Execute all SQL."""

st.markdown("""
**Before running the prompt below, download and unzip the data:**

1. Download the zip file containing all CSVs: [tricon_sfr_data.zip](https://github.com/sfc-gh-cwalker/coco-hol-tricon/raw/main/workshop_guide/data/tricon_sfr_data.zip)
2. Unzip it to a folder called `tricon_sfr_data` in your Downloads folder.
3. Copy the prompt below into Cortex Code Desktop. Desktop can read your local files, so it uploads the CSVs for you.

:material/info: If PUT is blocked on your network, upload the CSVs in Snowsight instead (**Catalog → TRICON_HOL → your schema → Stages → DATA → + Files**), then ask Cortex Code to skip step 1.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all operational data tables from CSV files uploaded to the internal stage `DATA`:

```sql
CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE TABLE LEASES
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(INFER_SCHEMA(
      LOCATION => '@TRICON_HOL.SFR_<INITIALS>.DATA/leases.csv',
      FILE_FORMAT => 'csv_format'
    ))
  );

COPY INTO LEASES
  FROM @TRICON_HOL.SFR_<INITIALS>.DATA/leases.csv
  FILE_FORMAT = csv_format;
```

**The tables**:

| Table | Rows | Description |
|-------|------|-------------|
| `MARKETS` | 14 | Operating markets with region, target occupancy, base market rent |
| `PROPERTIES` | 120 | Homes: market, beds/baths, sq ft, acquisition date & price, status |
| `VENDORS` | 15 | Maintenance vendors by trade with quality rating and SLA |
| `LEASES` | 200 | New and renewal leases with rent, rent change %, term, status |
| `WORK_ORDERS` | 300 | Maintenance work orders: category, priority, vendor, cost, days to complete |
| `MARKET_MONTHLY_PERFORMANCE` | 336 | 24 months x 14 markets: occupancy, rent, rent growth, move-outs, bad debt |
| `RESIDENT_SERVICE_TICKETS` | 40 | Free-text resident requests with resolution notes |
| `PROPERTY_INSPECTIONS` | 25 | Move-out, annual, pre-acquisition, QA, and storm inspection findings |
| `OPERATING_PROCEDURES` | 20 | Standard operating procedures (SOPs) and KPI definitions |

""")


PROMPT_1_3 = """Run a query in TRICON_HOL.SFR_<INITIALS> that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query. You should see approximately **1,070 total rows** across 9 tables.
""")


render_key_concepts([
    {"term": "Internal Stage", "definition": "A named Snowflake stage that stores files within Snowflake's managed storage. Files are uploaded via Snowsight UI or PUT command."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "SFR_<INITIALS> schema with a DATA stage in TRICON_HOL",
    "9 operational data tables loaded from CSV (~1,070 total rows)",
])
