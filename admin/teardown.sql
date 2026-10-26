-- Tricon CoCo HOL - teardown after the hackathon week. Run as ACCOUNTADMIN.
-- Removes all attendee schemas (semantic views, search services, agents, apps).
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS TRICON_HOL;
DROP COMPUTE POOL IF EXISTS TRICON_HOL_POOL;
DROP WAREHOUSE IF EXISTS TRICON_HOL_WH;
DROP RESOURCE MONITOR IF EXISTS TRICON_HOL_MONITOR;
DROP ROLE IF EXISTS TRICON_HOL_ROLE;
-- Re-disable cross-region inference only if it was off before the lab:
-- ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'DISABLED';
