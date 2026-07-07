import streamlit as st
import plotly.graph_objects as go

ACCENT = "#5B8DEF"


def gauge(title: str, value: float, minimum: float, maximum: float, unit: str = ""):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": f" {unit}", "font": {"size": 24, "color": "#E8E9EB", "family": "JetBrains Mono"}},
            title={"text": f"<b>{title}</b>", "font": {"size": 13, "color": "#9CA0A6", "family": "Inter"}},
            gauge={
                "shape": "angular",
                "axis": {"range": [minimum, maximum], "tickwidth": 1, "tickcolor": "#6B6F75",
                         "tickfont": {"size": 10, "family": "JetBrains Mono"}},
                "bar": {"color": ACCENT, "thickness": 0.18},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [minimum, maximum * 0.8], "color": "rgba(255,255,255,.04)"},
                    {"range": [maximum * 0.8, maximum], "color": "rgba(193,91,84,.10)"},
                ],
                "threshold": {"line": {"color": "#E8E9EB", "width": 3}, "value": value},
            }
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(l=18, r=57, t=70, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8E9EB", family="Inter"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})