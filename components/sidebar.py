import streamlit as st
from backend.auth import logout


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
<div class="brand-block">
    <div class="brand-row">
        <div class="brand-icon">⚡</div>
        <div>
            <div class="brand-title">Smart Energy</div>
            <div class="brand-subtitle">IoT Monitoring System</div>
        </div>
    </div>
    <div class="brand-status">
        <span class="status-dot"></span> System Online
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        user = st.session_state.get("user", {})
        fullname = user.get("fullname", "Administrator")
        role = user.get("role", "Administrator")
        initial = fullname[0].upper() if fullname else "A"

        st.markdown(
            f"""
<div class="user-row">
    <div class="user-avatar">{initial}</div>
    <div>
        <div class="user-name">{fullname}</div>
        <div class="user-role">{role}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.page_link("pages/1_📊_Monitoring.py", label="Monitoring", icon="📊")
        st.page_link("pages/2_📈_Analytics.py", label="Analytics", icon="📈")
        st.page_link("pages/6_📋_History.py", label="History", icon="📋")
        st.page_link("pages/3_🧠_Clustering.py", label="Clustering Analysis", icon="🧠")

        st.divider()

        if st.button("Logout", use_container_width=True):
            logout(st.session_state)
            st.switch_page("pages/🔐_Login.py")

        st.caption("v2.0")