import streamlit as st


def panel(title: str, rows: dict, icon: str = ""):
    """
    Single reusable info box. rows = {"Label": "Value", ...}
    Replaces the previously copy-pasted inline HTML tables
    (Device Info, Latest Reading, System Summary, Analysis Result).
    """

    row_html = "".join(
        f"<tr><td>{label}</td><td>{value}</td></tr>"
        for label, value in rows.items()
    )

    st.markdown(
        f"""
<div class="panel">
<h4>{icon} {title}</h4>
<table>{row_html}</table>
</div>
""",
        unsafe_allow_html=True,
    )