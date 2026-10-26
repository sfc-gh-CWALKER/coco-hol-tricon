import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "11:10 – 11:25", "15 min", "Knowledge base, Cortex Search service, and RAG query pattern")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits.", "icon": "preview"},
])


PROMPT_3_1 = """In TRICON_HOL.SFR_<INITIALS>:

1. First, create a unified text table for search called SFR_KNOWLEDGE_BASE that combines:
   - RESIDENT_SERVICE_TICKETS: doc_id = TICKET_ID, doc_type = 'Resident Ticket', content = CATEGORY || ': ' || DESCRIPTION || ' Resolution: ' || RESOLUTION_NOTES, metadata_category = CATEGORY, metadata_priority = PRIORITY, doc_date = TICKET_DATE
   - PROPERTY_INSPECTIONS: doc_id = INSPECTION_ID, doc_type = 'Inspection', content = INSPECTION_TYPE || ' inspection of ' || PROPERTY_ID || ': ' || FINDINGS, metadata_category = INSPECTION_TYPE, metadata_priority = CASE WHEN CONDITION_RATING <= 2 THEN 'High' WHEN CONDITION_RATING = 3 THEN 'Medium' ELSE 'Low' END, doc_date = INSPECTION_DATE
   - OPERATING_PROCEDURES: doc_id = DOC_ID, doc_type = 'SOP', content = TITLE || ': ' || CONTENT, metadata_category = CATEGORY, metadata_priority = 'Reference', doc_date = EFFECTIVE_DATE

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE SFR_DOCS_SEARCH
     ON content
     ATTRIBUTES metadata_category, metadata_priority, doc_type
     WAREHOUSE = TRICON_HOL_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_category, metadata_priority, doc_date
       FROM SFR_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify with SHOW CORTEX SEARCH SERVICES."""

render_prompt("Prompt 3.1", "Create Cortex Search Service", PROMPT_3_1)

render_explanation("What this prompt does", """
Builds a unified knowledge base from unstructured text sources and creates a hybrid search service.

The search service automatically embeds, indexes, and serves results with auto-refresh when source data changes.
""")


PROMPT_3_2 = """In TRICON_HOL.SFR_<INITIALS>, query our SFR_DOCS_SEARCH service using SEARCH_PREVIEW:

1. "water leak damage drywall mitigation" (limit 5)
2. "make-ready QA failed pest treatment skipped" (limit 5)
3. "renewal increase too high retention concession" filtered to doc_type = 'Resident Ticket' (limit 3)
4. "what approval is needed for a roof replacement" filtered to doc_type = 'SOP' (limit 3)

Execute all searches and show results."""

render_prompt("Prompt 3.2", "Query the Search Service", PROMPT_3_2)

render_explanation("What this prompt does", """
Tests different search capabilities across the document corpus:

| Search | Tests |
|--------|-------|
| 1 | Semantic match across tickets and inspections |
| 2 | Linking a resident complaint to a process gap |
| 3 | Attribute filter on doc_type |
| 4 | Question-style query against SOPs (policy lookup) |
""")


PROMPT_3_3 = """In TRICON_HOL.SFR_<INITIALS>, implement a RAG pattern:

1. Question: "What are the most common causes of move-in complaints and make-ready failures, and what does our SOP say we should do to prevent them?"

2. Retrieve top 5 documents from SFR_DOCS_SEARCH, then pass to SNOWFLAKE.CORTEX.COMPLETE() with instructions to answer ONLY from the provided documents, cite doc_ids, and structure the answer with: 1) Common incident types, 2) Root causes, 3) Effective measures, 4) Recommendations.

Use claude-sonnet-4-6 as the model. Execute and show the RAG response."""

render_prompt("Prompt 3.3", "RAG Pattern: Search + Generate", PROMPT_3_3)

render_explanation("What this prompt does", """
Implements the full **RAG** pattern: retrieve relevant documents, then generate a grounded answer with citations.
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created with SQL. Handles embedding, indexing, reranking, and auto-refresh automatically."},
    {"term": "RAG", "definition": "Retrieval Augmented Generation: retrieve documents, include as context in LLM prompt, generate grounded answer."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact matching). Better than either alone."},
])

render_what_you_built([
    "SFR_KNOWLEDGE_BASE — unified document table",
    "SFR_DOCS_SEARCH — Cortex Search service with hybrid search",
    "Search queries across multiple document types",
    "Full RAG pipeline for grounded Q&A",
])
