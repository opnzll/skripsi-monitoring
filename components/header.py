import streamlit as st
from datetime import datetime


def render_header(eyebrow: str = ""):
    left, right = st.columns([6, 1])

    with left:
        if eyebrow:
            st.markdown(f'<div class="page-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
        st.title("⚡ Smart Energy Analytics")

    with right:
        st.markdown(
            f"""
<div style="text-align:right; padding-top:10px;">
    <span class="live-dot"></span>
    <span style="font-family:var(--font-mono); font-size:13px; color:var(--text-secondary);">
        {datetime.now().strftime("%H:%M:%S")}
    </span>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()