from pathlib import Path

import streamlit as st

from components import attendee_schema, is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="Tricon SFR Operations AI Lab",
    page_icon=":material/house:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

with st.sidebar:
    st.text_input(
        "Your initials",
        key="initials",
        max_chars=4,
        placeholder="e.g. CW",
        help="Personalizes every prompt with your own schema so attendees don't overwrite each other.",
    )
    st.caption(f"Your schema: `TRICON_HOL.{attendee_schema()}`")

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Core Lab": [
            st.Page("app_pages/session_01.py", title=_title(1, "Data Prep"), icon=":material/database:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Cortex Analyst & Semantic Views"), icon=":material/chat:"),
            st.Page("app_pages/session_03.py", title=_title(3, "Cortex Search"), icon=":material/search:"),
            st.Page("app_pages/session_04.py", title=_title(4, "Cortex Agents"), icon=":material/smart_toy:"),
        ],
        "Optional Extensions": [
            st.Page("app_pages/session_05.py", title=_title(5, "CoWork"), icon=":material/group:"),
            st.Page("app_pages/session_06.py", title=_title(6, "Streamlit"), icon=":material/web:"),
        ],
    },
    position="sidebar",
)

page.run()
