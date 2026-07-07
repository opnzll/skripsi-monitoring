import streamlit as st
import plotly.graph_objects as go

from backend.database import get_last

ACCENT = "#5B8DEF"


def line_chart(title: str, column: str, unit: str, limit: int = 100):

    df = get_last(limit)

    if df.empty:
        st.warning("No monitoring data available.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["created_at"],
            y=df[column],
            mode="lines",
            name=title,
            line=dict(color=ACCENT, width=2),
            fill="tozeroy",
            fillcolor="rgba(91,141,239,.08)",
            hovertemplate=f"<b>%{{y:.2f}} {unit}</b><extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified",
        showlegend=False,
        font=dict(color="#E8E9EB", family="Inter"),
        xaxis=dict(title="", showgrid=False, zeroline=False, showline=False),
        yaxis=dict(title=unit, gridcolor="rgba(255,255,255,.06)", zeroline=False),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True, "scrollZoom": False}
    )


def voltage_chart(limit=100):   line_chart("Voltage", "voltage", "Volt", limit)
def current_chart(limit=100):   line_chart("Current", "current", "Ampere", limit)
def power_chart(limit=100):     line_chart("Power", "power", "Watt", limit)
def energy_chart(limit=100):    line_chart("Energy", "energy", "kWh", limit)
def frequency_chart(limit=100): line_chart("Frequency", "frequency", "Hz", limit)
def pf_chart(limit=100):        line_chart("Power Factor", "power_factor", "PF", limit)