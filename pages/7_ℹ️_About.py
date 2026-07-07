import streamlit as st

# ==========================================================
# AUTHENTICATION
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/🔐_Login.py")

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

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

st.title("ℹ️ About")

st.caption(
    "Information about the Electrical Monitoring Dashboard and Machine Learning System."
)

st.divider()

# ==========================================================
# APPLICATION
# ==========================================================

st.subheader("🖥️ Application Information")

left, right = st.columns(2, gap="large")

with left:

    st.markdown("""
### Dashboard

- IoT Electrical Monitoring
- Real-time Visualization
- Historical Monitoring
- Data Analytics
- K-Means Clustering
""")

with right:

    st.markdown("""
### Developer

**Author :**

Naufal Zul Fikri

**Framework :**

Streamlit

**Programming Language :**

Python
""")

st.divider()

# ==========================================================
# TECHNOLOGY
# ==========================================================

st.subheader("⚙️ Technology Stack")

st.markdown("""
- ESP32
- PZEM-004T V3
- Python
- Streamlit
- Plotly
- Pandas
- Scikit-Learn
- MySQL
""")

st.divider()

# ==========================================================
# RESEARCH
# ==========================================================

st.subheader("📚 Research")

st.markdown("""
**Title**

Identification of Electrical System Operating Patterns Based on IoT Using K-Means Clustering Algorithm.

**Purpose**

This application performs real-time monitoring of electrical parameters and identifies operating patterns using Machine Learning.

**Parameters**

- Voltage
- Current
- Power
- Frequency
- Power Factor
""")

st.divider()

# ==========================================================
# VERSION
# ==========================================================

st.subheader("🚀 Version")

st.success("""
Dashboard Version : **1.0**

Status : **Production Ready**

Machine Learning : **K-Means**

Last Update : **2026**
""")

st.divider()

render_footer()