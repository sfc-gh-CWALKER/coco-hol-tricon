import streamlit as st

from components import attendee_schema

st.title("Getting Started")
st.markdown("Connect **Cortex Code Desktop** to Tricon's Snowflake account. Do this **before** the workshop if you can.")

st.space("small")

st.markdown("#### Step 1: Install Cortex Code Desktop")

with st.container(border=True):
    st.markdown("""
Install Cortex Code Desktop using the installer link shared by the Snowflake team. If your laptop requires IT approval to install software, request it ahead of time.

Open the app once to confirm it launches.
""")

st.space("small")

st.markdown("#### Step 2: Connect to Tricon's Snowflake account")

with st.container(border=True):
    st.markdown("""
Add a Snowflake connection in Cortex Code Desktop using your usual Tricon Snowflake login (the same authentication you use for Snowsight).

| Setting | Value |
|---------|-------|
| **Account** | Tricon's Snowflake account identifier (provided by your admin) |
| **Role** | `TRICON_HOL_ROLE` |
| **Warehouse** | `TRICON_HOL_WH` |
| **Database** | `TRICON_HOL` |

:material/info: The admin has already created the workshop database, warehouse, and role, and enabled the Cortex features we use. You do **not** need ACCOUNTADMIN.
""")

st.space("small")

st.markdown("#### Step 3: Enter your initials")

with st.container(border=True):
    st.markdown(f"""
Type your initials in the **sidebar** of this guide. Every prompt will then use your own schema, so you won't overwrite anyone else's work.

Your schema: **`TRICON_HOL.{attendee_schema()}`**
""")

st.space("small")

st.markdown("#### Step 4: Test the connection")

with st.container(border=True):
    st.markdown("Paste this into Cortex Code Desktop:")
    st.code("Run SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE() and confirm the role is TRICON_HOL_ROLE.", language="text", wrap_lines=True)
    st.caption("If you see a different role, ask Cortex Code to switch to TRICON_HOL_ROLE, or check your connection settings.")

st.space("small")

with st.expander(":material/help: No access to Tricon's account? Use a free trial instead"):
    st.markdown("""
Sign up at **[signup.snowflake.com](https://signup.snowflake.com/?t=a893d13cddae481c0bb3ed33aa5958a5d069f772a039de4e08203b69e1620f27&cloud=aws&region=us-east-2)** (AWS, Enterprise edition, US East (Ohio)). Activate your account from the email, connect Cortex Code Desktop with the ACCOUNTADMIN role, and then run this setup:

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
CREATE DATABASE TRICON_HOL;
CREATE WAREHOUSE TRICON_HOL_WH WAREHOUSE_SIZE = 'MEDIUM' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
```

The trial includes $400 of credits, which is more than enough for this lab.
""")
