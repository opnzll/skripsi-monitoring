import streamlit as st

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

from backend.services import get_analytics_data

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from components.cards import metric_card

from components.charts import (
    power_chart,
    voltage_chart,
    current_chart,
    frequency_chart,
    pf_chart
)

from backend.analytics import (
    descriptive_statistics,
    power_quality
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Energy Analytics",

    page_icon="📈",

    layout="wide"

)

# ==========================================================
# LOAD CSS
# ==========================================================

with open("assets/style.css", encoding="utf-8") as css:

    st.markdown(

        f"<style>{css.read()}</style>",

        unsafe_allow_html=True

    )

# ==========================================================
# HEADER
# ==========================================================

render_sidebar()

render_header()

st.title("📈 Energy Analytics")

st.caption(
    "Comprehensive statistical analysis and visualization of electrical monitoring data collected from the IoT monitoring system."
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    analytics = get_analytics_data()

    df = analytics["dataset"]

    stats = analytics["statistics"].iloc[0]

except Exception as e:

    st.error("Failed to load monitoring data.")

    st.exception(e)

    st.stop()

if df.empty:

    st.warning("No monitoring data available.")

    st.stop()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    metric_card(

        title="Average Voltage",

        value=f"{stats['avg_voltage']:.2f}",

        unit="V",

        icon="⚡"

    )

with c2:

    metric_card(

        title="Average Current",

        value=f"{stats['avg_current']:.2f}",

        unit="A",

        icon="🔋"

    )

with c3:

    metric_card(

        title="Average Power",

        value=f"{stats['avg_power']:.2f}",

        unit="W",

        icon="💡"

    )

with c4:

    metric_card(

        title="Total Records",

        value=f"{int(stats['total_data']):,}",

        icon="📊"

    )

st.divider()

# ==========================================================
# POWER ANALYSIS
# ==========================================================

st.subheader("⚡ Power Consumption")

st.caption(
    "Power consumption trend based on the latest monitoring records."
)

power_chart(limit=200)

st.divider()

# ==========================================================
# ELECTRICAL PARAMETERS
# ==========================================================

st.subheader("🔌 Electrical Parameters")

left, right = st.columns(2, gap="large")

with left:

    st.markdown("#### ⚡ Voltage Trend")

    voltage_chart(limit=200)

with right:

    st.markdown("#### 🔋 Current Trend")

    current_chart(limit=200)

st.divider()

# ==========================================================
# POWER QUALITY
# ==========================================================

st.subheader("⚙️ Power Quality")

st.caption(
    "Frequency stability and power factor analysis over the latest monitoring period."
)

left, right = st.columns(2, gap="large")

with left:

    st.markdown("#### 🌐 Frequency")

    frequency_chart(limit=200)

with right:

    st.markdown("#### 📈 Power Factor")

    pf_chart(limit=200)

st.divider()

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

st.subheader("📊 Descriptive Statistics")

summary = descriptive_statistics(df)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
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

    hide_index=True

)

st.divider()

# ==========================================================
# MONITORING INSIGHT
# ==========================================================

st.subheader("💡 Monitoring Insight")

quality = power_quality(df)

voltage_status = quality["voltage_status"]

pf_status = quality["pf_status"]

freq_status = quality["frequency_status"]

# ----------------------------------------------------------
# SYSTEM SUMMARY
# ----------------------------------------------------------

with left:

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

<tr>
<td style="padding:8px;color:#B0AB9F;">Average Voltage</td>
<td style="text-align:right;"><b>{stats['avg_voltage']:.2f} V</b></td>
</tr>

<tr>
<td style="padding:8px;color:#B0AB9F;">Average Current</td>
<td style="text-align:right;"><b>{stats['avg_current']:.2f} A</b></td>
</tr>

<tr>
<td style="padding:8px;color:#B0AB9F;">Average Power</td>
<td style="text-align:right;"><b>{stats['avg_power']:.2f} W</b></td>
</tr>

<tr>
<td style="padding:8px;color:#B0AB9F;">Maximum Power</td>
<td style="text-align:right;"><b>{stats['max_power']:.2f} W</b></td>
</tr>

<tr>
<td style="padding:8px;color:#B0AB9F;">Minimum Power</td>
<td style="text-align:right;"><b>{stats['min_power']:.2f} W</b></td>
</tr>

<tr>
<td style="padding:8px;color:#B0AB9F;">Total Records</td>
<td style="text-align:right;"><b>{int(stats['total_data']):,}</b></td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True
    )

# ----------------------------------------------------------
# ANALYSIS RESULT
# ----------------------------------------------------------

with right:

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

<tr>
<td style="padding:10px;color:#B0AB9F;">Voltage Condition</td>
<td style="text-align:right;"><b>{voltage_status}</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Power Factor</td>
<td style="text-align:right;"><b>{pf_status}</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Frequency Stability</td>
<td style="text-align:right;"><b>{freq_status}</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Dataset Quality</td>
<td style="text-align:right;"><b>🟢 Ready</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Machine Learning</td>
<td style="text-align:right;"><b>🟢 Ready</b></td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

render_footer()