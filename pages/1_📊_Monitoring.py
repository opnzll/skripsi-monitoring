import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

from streamlit_autorefresh import st_autorefresh

from backend.database import get_latest, get_last, get_statistics

from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import metric_card
from components.gauges import gauge
from components.charts import voltage_chart, power_chart
from components.status import status_panel
from components.panel import panel
from components.footer import render_footer

st.set_page_config(page_title="Smart Energy Monitoring", page_icon="⚡", layout="wide")

with open("assets/style.css", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st_autorefresh(interval=2000, key="monitoring")

render_sidebar()
render_header()

latest = get_latest()

if latest.empty:
    st.warning("Belum ada data monitoring.")
    st.stop()

latest = latest.iloc[0]

st.title("📊 Monitoring Dashboard")
st.caption("Real-time electrical parameters from ESP32 & PZEM-004T.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Voltage", round(latest["voltage"], 2), "V", "Normal", "ok", "⚡")
with col2:
    metric_card("Current", round(latest["current"], 2), "A", "Normal", "ok", "🔋")
with col3:
    metric_card("Power", round(latest["power"], 2), "W", "Realtime", "ok", "💡")
with col4:
    metric_card("Power Factor", round(latest["power_factor"], 2), "", "Stable", "ok", "📊")

st.divider()

# Only the two most critical parameters get a full gauge.
# Others are represented as trend lines to avoid an overloaded page.

left, right = st.columns([1, 2])
with left:
    gauge("Voltage", latest["voltage"], 180, 250, "V")
with right:
    voltage_chart()

left, right = st.columns([1, 2])
with left:
    gauge("Power", latest["power"], 0, 2500, "W")
with right:
    power_chart()

st.divider()

status_panel()

st.divider()

st.subheader("Latest Monitoring Data")

history = get_last(20)
stats = get_statistics()

if not stats.empty:
    stats = stats.iloc[0]

st.dataframe(history, use_container_width=True, hide_index=True)

st.divider()

left, right = st.columns(2, gap="large")

with left:
    panel("Statistics", {
        "Average Voltage": f"{stats['avg_voltage']:.2f} V",
        "Average Current": f"{stats['avg_current']:.2f} A",
        "Average Power": f"{stats['avg_power']:.2f} W",
        "Total Records": int(stats["total_data"]),
    }, icon="📈")

with right:
    panel("Today's Summary", {
        "Max Power": f"{stats['max_power']:.2f} W",
        "Min Power": f"{stats['min_power']:.2f} W",
        "Auto Refresh": "Every 2 seconds",
        "Database": "Connected",
    }, icon="✅")

render_footer()