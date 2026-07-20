import streamlit as st
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

from backend.services import get_dashboard_data

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

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Smart Energy Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CONSTANTS
# ==========================================================

REFRESH_INTERVAL = 2000  # milliseconds
CACHE_TTL = 5            # seconds

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

# ==========================================================
# AUTO REFRESH
# ==========================================================

st_autorefresh(
    interval=REFRESH_INTERVAL,
    key="dashboard_refresh",
)

# ==========================================================
# LOAD CUSTOM CSS
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
# CACHE DASHBOARD DATA
# ==========================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def load_dashboard_data():
    """
    Load dashboard data from backend service.

    Cache is refreshed every 5 seconds to reduce
    unnecessary database queries.
    """
    return get_dashboard_data()

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    dashboard = load_dashboard_data()

    if dashboard is None:
        st.warning("⚠️ No monitoring data available.")
        st.stop()

    latest = dashboard.get("latest")
    history = dashboard.get("history")
    stats = dashboard.get("stats")
    last_update = dashboard.get("last_update")

    if latest is None:
        st.warning("⚠️ Monitoring data is empty.")
        st.stop()

except Exception as e:

    st.error("❌ Failed to load dashboard data.")
    st.exception(e)
    st.stop()

# ==========================================================
# PAGE TITLE
# ==========================================================

st.subheader("⚡ Real-Time Monitoring Dashboard")
st.caption("Live electrical parameter monitoring from ESP32 & PZEM-004T.")
st.divider()

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 Key Performance Indicators")

kpi_items = [
    {
        "title": "Voltage",
        "value": float(latest["voltage"]),
        "unit": "V",
        "status": "Normal",
        "icon": "⚡",
    },
    {
        "title": "Current",
        "value": float(latest["current"]),
        "unit": "A",
        "status": "Realtime",
        "icon": "🔋",
    },
    {
        "title": "Power",
        "value": float(latest["power"]),
        "unit": "W",
        "status": "Realtime",
        "icon": "💡",
    },
    {
        "title": "Power Factor",
        "value": float(latest["power_factor"]),
        "unit": "",
        "status": "Good",
        "icon": "📈",
    },
]

columns = st.columns(len(kpi_items))

for column, item in zip(columns, kpi_items):

    with column:

        metric_card(
            title=item["title"],
            value=item["value"],
            unit=item["unit"],
            status=item["status"],
            icon=item["icon"],
        )

st.divider()

# ==========================================================
# MAIN DASHBOARD
# ==========================================================

left_column, right_column = st.columns([1, 2])

# ----------------------------------------------------------
# VOLTAGE GAUGE
# ----------------------------------------------------------

with left_column:

    st.subheader("⚡ Voltage")

    gauge(
        title="",
        value=float(latest["voltage"]),
        minimum=180,
        maximum=260,
        unit="V",
    )

# ----------------------------------------------------------
# POWER CHART
# ----------------------------------------------------------

with right_column:

    st.subheader("⚡ Power Consumption")

    power_chart(limit=120)

st.divider()

# ==========================================================
# TREND CHARTS
# ==========================================================

left_column, right_column = st.columns(2)

with left_column:

    st.subheader("Voltage Trend")

    voltage_chart(limit=120)

with right_column:

    st.subheader("Current Trend")

    current_chart(limit=120)

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader("🖥️ System Status")

system_col, device_col, reading_col = st.columns(3, gap="large")

# ----------------------------------------------------------
# SYSTEM HEALTH
# ----------------------------------------------------------

with system_col:

    status_panel()

# ----------------------------------------------------------
# DEVICE INFORMATION
# ----------------------------------------------------------

device_info = {
    "Device": "ESP32 + PZEM-004T",
    "Refresh Rate": f"{REFRESH_INTERVAL // 1000} Seconds",
    "Database": "MySQL",
    "Status": "● ONLINE",
}

with device_col:

    st.subheader("📡 Device Information")

    rows = ""

    for key, value in device_info.items():

        color = "#5B8C5A" if key == "Status" else "white"

        rows += f"""
        <tr>
            <td style="padding:10px;color:#B0AB9F;">{key}</td>
            <td style="padding:10px;text-align:right;color:{color};">
                <b>{value}</b>
            </td>
        </tr>
        """

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
        {rows}
        </table>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------
# LATEST SENSOR READING
# ----------------------------------------------------------

latest_reading = {
    "Voltage": f'{latest["voltage"]:.2f} V',
    "Current": f'{latest["current"]:.2f} A',
    "Power": f'{latest["power"]:.2f} W',
    "Frequency": f'{latest["frequency"]:.2f} Hz',
    "Power Factor": f'{latest["power_factor"]:.2f}',
}

with reading_col:

    st.subheader("⚡ Latest Reading")

    rows = ""

    for key, value in latest_reading.items():

        rows += f"""
        <tr>
            <td style="padding:10px;color:#B0AB9F;">{key}</td>
            <td style="padding:10px;text-align:right;color:white;">
                <b>{value}</b>
            </td>
        </tr>
        """

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