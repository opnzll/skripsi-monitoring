import streamlit as st

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from components.cards import metric_card

from backend.database import (
    get_history,
    get_last_timestamp
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="History",
    page_icon="📋",
    layout="wide"
)

# ==========================================================
# STYLE
# ==========================================================

with open("assets/style.css", encoding="utf-8") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

render_sidebar()
render_header()

# ==========================================================
# HEADER
# ==========================================================

st.title("📋 Historical Monitoring")

st.caption(
    "Browse, search and export historical electrical monitoring data collected from the IoT system."
)

st.divider()

# ==========================================================
# FILTER
# ==========================================================

left, right = st.columns([3,1])

with left:

    keyword = st.text_input(
        "🔍 Search Data",
        placeholder="Search voltage, current, power..."
    )

with right:

    rows = st.selectbox(
        "Rows",
        [50,100,250,500],
        index=1
    )

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    df = get_history(rows)

    last_update = get_last_timestamp()

except Exception as e:

    st.error("Database Error")

    st.exception(e)

    st.stop()

if df.empty:

    st.warning("No historical data available.")

    st.stop()

# ==========================================================
# SEARCH
# ==========================================================

if keyword:

    keyword = keyword.lower()

    df = df[
        df.astype(str)
        .apply(lambda x: x.str.lower())
        .apply(lambda x: x.str.contains(keyword))
        .any(axis=1)
    ]

# ==========================================================
# KPI
# ==========================================================

last = last_update.iloc[0]["last_update"]

c1,c2,c3,c4 = st.columns(4)

with c1:

    metric_card(
        title="Displayed",
        value=len(df),
        icon="📄"
    )

with c2:

    metric_card(
        title="Columns",
        value=len(df.columns),
        icon="📊"
    )

with c3:

    metric_card(
        title="Latest Voltage",
        value=f'{df.iloc[0]["voltage"]:.2f}',
        unit="V",
        icon="⚡"
    )

with c4:

    metric_card(
        title="Last Update",
        value=last.strftime("%H:%M:%S"),
        icon="🕒"
    )

st.divider()

# ==========================================================
# TABLE
# ==========================================================

st.subheader("📑 Historical Dataset")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# EXPORT
# ==========================================================

st.subheader("⬇ Export")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    file_name="monitoring_history.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

render_footer()