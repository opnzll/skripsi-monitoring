from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="clock")
WIB = ZoneInfo("Asia/Jakarta")


def render_header(eyebrow: str = ""):

    left, right = st.columns([6, 1])

    with left:

        if eyebrow:
            st.markdown(
                f'<div class="page-eyebrow">{eyebrow}</div>',
                unsafe_allow_html=True
            )

        st.title("⚡ Smart Energy Analytics")

    with right:

        current_time = datetime.now(WIB)

        st.markdown(
            f"""
<div style="text-align:right;padding-top:10px;">
    <span class="live-dot"></span>
    <div style="
        font-family:var(--font-mono);
        font-size:13px;
        color:var(--text-secondary);
    ">
        {current_time.strftime("%H:%M:%S")}
    </div>
    <div style="
        font-size:11px;
        color:var(--text-secondary);
        margin-top:2px;
    ">
        {current_time.strftime("%d-%m-%Y")}
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()