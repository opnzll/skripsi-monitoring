import streamlit as st
from pathlib import Path

from backend.services import get_analytics_data

from backend.analytics import (
    descriptive_statistics,
    power_quality,
)

from components.cards import metric_card
from components.charts import (
    current_chart,
    frequency_chart,
    pf_chart,
    power_chart,
    voltage_chart,
)
from components.footer import render_footer
from components.header import render_header
from components.sidebar import render_sidebar

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Energy Analytics",
    page_icon="📈",
    layout="wide",
)

# ==========================================================
# CONSTANTS
# ==========================================================

CHART_LIMIT = 200
CACHE_TTL = 30

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

# ==========================================================
# LOAD CSS
# ==========================================================

css_path = Path("assets/style.css")

if css_path.exists():

    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

# ==========================================================
# RENDER LAYOUT
# ==========================================================

render_sidebar()
render_header()

# ==========================================================
# CACHE
# ==========================================================

@st.cache_data(
    ttl=CACHE_TTL,
    show_spinner=False,
)
def load_analytics():

    return get_analytics_data()

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("📈 Energy Analytics")

st.caption(
    "Comprehensive statistical analysis and visualization of electrical monitoring data collected from the IoT monitoring system."
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    analytics = load_analytics()

    if analytics is None:

        st.warning("No analytics data available.")

        st.stop()

    df = analytics["dataset"]

    statistics = analytics["statistics"]

    if df.empty or statistics.empty:

        st.warning("No monitoring data available.")

        st.stop()

    stats = statistics.iloc[0]

except Exception as e:

    st.error("Failed to load monitoring data.")

    st.exception(e)

    st.stop()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📊 Executive Summary")

summary_cards = [
    {
        "title": "Average Voltage",
        "value": stats["avg_voltage"],
        "unit": "V",
        "icon": "⚡",
    },
    {
        "title": "Average Current",
        "value": stats["avg_current"],
        "unit": "A",
        "icon": "🔋",
    },
    {
        "title": "Average Power",
        "value": stats["avg_power"],
        "unit": "W",
        "icon": "💡",
    },
    {
        "title": "Total Records",
        "value": int(stats["total_data"]),
        "unit": "",
        "icon": "📊",
        "is_integer": True,
    },
]

columns = st.columns(len(summary_cards))

for column, card in zip(columns, summary_cards):

    with column:

        value = (
            f"{card['value']:,}"
            if card.get("is_integer", False)
            else f"{card['value']:.2f}"
        )

        metric_card(
            title=card["title"],
            value=value,
            unit=card["unit"],
            icon=card["icon"],
        )

st.divider()

# ==========================================================
# POWER ANALYSIS
# ==========================================================

st.subheader("⚡ Power Consumption")

st.caption(
    "Power consumption trend based on the latest monitoring records."
)

power_chart(limit=CHART_LIMIT)

st.divider()

# ==========================================================
# ELECTRICAL PARAMETERS
# ==========================================================

st.subheader("🔌 Electrical Parameters")

left_column, right_column = st.columns(2, gap="large")

with left_column:

    st.markdown("#### ⚡ Voltage Trend")

    voltage_chart(limit=CHART_LIMIT)

with right_column:

    st.markdown("#### 🔋 Current Trend")

    current_chart(limit=CHART_LIMIT)

st.divider()

# ==========================================================
# POWER QUALITY
# ==========================================================

st.subheader("⚙️ Power Quality")

st.caption(
    "Frequency stability and power factor analysis over the latest monitoring period."
)

left_column, right_column = st.columns(2, gap="large")

with left_column:

    st.markdown("#### 🌐 Frequency")

    frequency_chart(limit=CHART_LIMIT)

with right_column:

    st.markdown("#### 📈 Power Factor")

    pf_chart(limit=CHART_LIMIT)

st.divider()

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

st.subheader("📊 Descriptive Statistics")

summary = descriptive_statistics(df)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# RAW DATASET
# ==========================================================

st.subheader("📋 Latest Monitoring Dataset")

st.caption(
    "Latest monitoring records retrieved from the IoT monitoring system."
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# MONITORING INSIGHT
# ==========================================================

st.subheader("💡 Monitoring Insight")

quality = power_quality(df)

summary_info = {
    "Average Voltage": f"{stats['avg_voltage']:.2f} V",
    "Average Current": f"{stats['avg_current']:.2f} A",
    "Average Power": f"{stats['avg_power']:.2f} W",
    "Maximum Power": f"{stats['max_power']:.2f} W",
    "Minimum Power": f"{stats['min_power']:.2f} W",
    "Total Records": f"{int(stats['total_data']):,}",
}

analysis_info = {
    "Voltage Condition": quality["voltage_status"],
    "Power Factor": quality["pf_status"],
    "Frequency Stability": quality["frequency_status"],
    "Dataset Quality": "🟢 Ready",
    "Machine Learning": "🟢 Ready",
}

left_column, right_column = st.columns(2, gap="large")

# ----------------------------------------------------------
# SYSTEM SUMMARY
# ----------------------------------------------------------

with left_column:

    rows = ""

    for key, value in summary_info.items():

        rows += f"""
        <tr>
            <td style="padding:8px;color:#B0AB9F;">{key}</td>
            <td style="text-align:right;"><b>{value}</b></td>
        </tr>
        """

    st.markdown(
        f"""
        <div style="
        background:#232220;
        border:1px solid rgba(242,239,233,.09);
        border-radius:18px;
        padding:22px;
        height:375px;
        ">

        <h4 style="margin-top:0;">📊 System Summary</h4>

        <table style="width:100%;border-collapse:collapse;">
            {rows}
        </table>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------
# ANALYSIS RESULT
# ----------------------------------------------------------

with right_column:

    rows = ""

    for key, value in analysis_info.items():

        rows += f"""
        <tr>
            <td style="padding:10px;color:#B0AB9F;">{key}</td>
            <td style="text-align:right;"><b>{value}</b></td>
        </tr>
        """

    st.markdown(
        f"""
        <div style="
        background:#232220;
        border:1px solid rgba(242,239,233,.09);
        border-radius:18px;
        padding:22px;
        height:375px;
        ">

        <h4 style="margin-top:0;">🧠 Analysis Result</h4>

        <table style="width:100%;border-collapse:collapse;">
            {rows}
        </table>

        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

render_footer()