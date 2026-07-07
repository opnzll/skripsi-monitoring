import streamlit as st


def metric_card(
    title: str,
    value,
    unit: str = "",
    status: str = "",
    status_type: str = "ok",   # "ok" | "warn" | "danger"
    icon: str = ""
):
    """
    Flat metric card. status_type controls the status color
    via CSS class (ok/warn/danger) instead of hardcoded color.
    """

    unit_html = f'<span class="metric-unit">{unit}</span>' if unit else ""
    status_html = (
        f'<div class="metric-status {status_type}">● {status}</div>'
        if status else ""
    )

    st.markdown(
        f"""
<div class="metric-card">
<div class="metric-title"><span class="metric-icon">{icon}</span> {title}</div>
<div class="metric-value">{value}{unit_html}</div>
{status_html}
</div>
""",
        unsafe_allow_html=True,
    )