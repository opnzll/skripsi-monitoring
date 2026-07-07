import streamlit as st

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")


import streamlit as st
from streamlit_autorefresh import st_autorefresh

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

from components.cards import metric_card
from components.gauges import gauge

from components.charts import (
    power_chart,
    voltage_chart,
    current_chart,
)

from components.status import status_panel

from backend.services import get_dashboard_data


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Smart Energy Monitoring",

    page_icon="⚡",

    layout="wide",

    initial_sidebar_state="expanded"

)


# ==========================================================
# AUTO REFRESH
# ==========================================================

st_autorefresh(

    interval=2000,

    key="monitor_refresh"

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
# SIDEBAR
# ==========================================================

render_sidebar()


# ==========================================================
# HEADER
# ==========================================================

render_header()


# ==========================================================
# LOAD DASHBOARD DATA
# ==========================================================

try:

    dashboard = get_dashboard_data()

    latest = dashboard["latest"]

    history = dashboard["history"]

    stats = dashboard["stats"]

    last_update = dashboard["last_update"]

except Exception as e:

    st.error("❌ Failed to connect to the database.")

    st.exception(e)

    st.stop()


if dashboard is None:

    st.warning("No monitoring data available.")

    st.stop()

latest = dashboard["latest"]
stats = dashboard["stats"]
history = dashboard["history"]
last_update = dashboard["last_update"]


# ==========================================================
# PAGE TITLE
# ==========================================================

st.subheader("⚡ Real-Time Monitoring Dashboard")

st.caption(
    "Live electrical parameter monitoring from ESP32 & PZEM-004T."
)

st.divider()

# ==========================================================
# KPI
# ==========================================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(

        title="Voltage",

        value=round(float(latest["voltage"]), 2),

        unit="V",

        status="Normal",

        icon="⚡"

    )

with col2:

    metric_card(

        title="Current",

        value=round(float(latest["current"]), 2),

        unit="A",

        status="Realtime",

        icon="🔋"

    )

with col3:

    metric_card(

        title="Power",

        value=round(float(latest["power"]), 2),

        unit="W",

        status="Realtime",

        icon="💡"

    )

with col4:

    metric_card(

        title="Power Factor",

        value=round(float(latest["power_factor"]), 2),

        unit="",

        status="Good",

        icon="📈"

    )

st.divider()

# ==========================================================
# MAIN DASHBOARD
# ==========================================================

left, right = st.columns([1, 2])

# ----------------------------------------------------------
# LEFT PANEL
# ----------------------------------------------------------

with left:

    st.subheader("⚡ Voltage")

    gauge(

        title="",

        value=float(latest["voltage"]),

        minimum=180,

        maximum=260,

        unit="V"

    )

# ----------------------------------------------------------
# RIGHT PANEL
# ----------------------------------------------------------

with right:

    st.subheader("⚡ Power Consumption")

    power_chart(limit=120)

st.divider()


# ==========================================================
# SECOND ROW
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("Voltage Trend")

    voltage_chart(limit=120)

with right:

    st.subheader("Current Trend")

    current_chart(limit=120)

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader("🖥️ System Status")

col1, col2, col3 = st.columns(3, gap="large")

# ----------------------------------------------------------
# SYSTEM HEALTH
# ----------------------------------------------------------

with col1:

    status_panel()

# ----------------------------------------------------------
# DEVICE INFORMATION
# ----------------------------------------------------------

with col2:

    st.subheader("📡 Device Information")

    st.markdown(
        """
<div style="
background:#232220;
border:1px solid rgba(242,239,233,.09);
border-radius:18px;
padding:22px;
height:245px;
">

<table style="width:100%; border-collapse:collapse;">

<tr>
<td style="padding:10px;color:#B0AB9F;">Device</td>
<td style="padding:10px;text-align:right;color:white;"><b>ESP32 + PZEM-004T</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Refresh Rate</td>
<td style="padding:10px;text-align:right;color:white;"><b>2 Seconds</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Database</td>
<td style="padding:10px;text-align:right;color:white;"><b>MySQL</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Status</td>
<td style="padding:10px;text-align:right;color:#5B8C5A;"><b>● ONLINE</b></td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------
# LATEST READING
# ----------------------------------------------------------

with col3:

    st.subheader("⚡ Latest Reading")

    st.markdown(
        f"""
<div style="
background:#232220;
border:1px solid rgba(242,239,233,.09);
border-radius:18px;
padding:22px;
height:245px;
">

<table style="width:100%; border-collapse:collapse;">

<tr>
<td style="padding:10px;color:#B0AB9F;">Voltage</td>
<td style="padding:10px;text-align:right;color:white;"><b>{latest["voltage"]:.2f} V</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Current</td>
<td style="padding:10px;text-align:right;color:white;"><b>{latest["current"]:.2f} A</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Power</td>
<td style="padding:10px;text-align:right;color:white;"><b>{latest["power"]:.2f} W</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Frequency</td>
<td style="padding:10px;text-align:right;color:white;"><b>{latest["frequency"]:.2f} Hz</b></td>
</tr>

<tr>
<td style="padding:10px;color:#B0AB9F;">Power Factor</td>
<td style="padding:10px;text-align:right;color:white;"><b>{latest["power_factor"]:.2f}</b></td>
</tr>

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