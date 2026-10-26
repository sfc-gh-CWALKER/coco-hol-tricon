-- =====================================================================
-- Tricon CoCo HOL - admin pre-provisioning (run once before Nov 9)
-- Run as ACCOUNTADMIN (or a role with CREATE ROLE / DATABASE / WAREHOUSE /
-- COMPUTE POOL and MANAGE GRANTS). Review with Tricon's Snowflake admin.
-- Attendees then work only in their own TRICON_HOL.SFR_<INITIALS> schema.
-- =====================================================================
USE ROLE ACCOUNTADMIN;

-- Cortex LLM models used by Analyst, Agents, and the RAG prompt.
-- Skip if Tricon policy disallows cross-region inference; then verify that
-- the models are available in-region instead.
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';

CREATE ROLE IF NOT EXISTS TRICON_HOL_ROLE COMMENT = 'CoCo hands-on lab attendees (Nov 9, 2026)';
GRANT ROLE TRICON_HOL_ROLE TO ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS TRICON_HOL COMMENT = 'CoCo HOL sandbox - synthetic data only';
GRANT USAGE, CREATE SCHEMA ON DATABASE TRICON_HOL TO ROLE TRICON_HOL_ROLE;

-- Shared lab warehouse. Multi-cluster requires Enterprise edition or higher;
-- drop the MIN/MAX_CLUSTER_COUNT lines on Standard edition.
CREATE WAREHOUSE IF NOT EXISTS TRICON_HOL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 3
  SCALING_POLICY = 'STANDARD'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;
GRANT USAGE, OPERATE ON WAREHOUSE TRICON_HOL_WH TO ROLE TRICON_HOL_ROLE;

-- Optional cost guardrail for the lab week.
CREATE RESOURCE MONITOR IF NOT EXISTS TRICON_HOL_MONITOR
  WITH CREDIT_QUOTA = 50 FREQUENCY = WEEKLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE TRICON_HOL_WH SET RESOURCE_MONITOR = TRICON_HOL_MONITOR;

-- Cortex functions, Analyst, Search, and Agents.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE TRICON_HOL_ROLE;

-- Optional Session 6 (Streamlit on container runtime).
CREATE COMPUTE POOL IF NOT EXISTS TRICON_HOL_POOL
  MIN_NODES = 1
  MAX_NODES = 3
  INSTANCE_FAMILY = CPU_X64_S
  AUTO_SUSPEND_SECS = 600
  INITIALLY_SUSPENDED = TRUE;
GRANT USAGE, MONITOR ON COMPUTE POOL TRICON_HOL_POOL TO ROLE TRICON_HOL_ROLE;

-- Grant the lab role to each attendee (repeat per user).
-- GRANT ROLE TRICON_HOL_ROLE TO USER <USERNAME>;

-- Pre-flight check as an attendee:
-- USE ROLE TRICON_HOL_ROLE; USE WAREHOUSE TRICON_HOL_WH;
-- CREATE SCHEMA TRICON_HOL.SFR_TEST; DROP SCHEMA TRICON_HOL.SFR_TEST;
-- SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-sonnet-4-6', 'Say ready');
