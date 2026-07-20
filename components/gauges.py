"""
Gauge component for Smart Energy Monitoring.
"""

from __future__ import annotations

import logging

import plotly.graph_objects as go
import streamlit as st

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

ACCENT_COLOR = "#5B8DEF"

FONT_COLOR = "#E8E9EB"

SECONDARY_FONT = "#9CA0A6"

TRANSPARENT = "rgba(0,0,0,0)"

NORMAL_COLOR = "rgba(255,255,255,.04)"

WARNING_COLOR = "rgba(193,91,84,.10)"

FONT_FAMILY = "Inter"

NUMBER_FONT = "JetBrains Mono"

GAUGE_HEIGHT = 340

PLOT_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}

# ==========================================================
# VALIDATION
# ==========================================================

def _validate_range(
    value: float,
    minimum: float,
    maximum: float,
) -> None:
    """
    Validate gauge range.
    """

    if minimum >= maximum:
        raise ValueError(
            "Minimum value must be smaller than maximum."
        )

    if value < minimum or value > maximum:

        logger.warning(
            "Gauge value %.2f outside range %.2f - %.2f",
            value,
            minimum,
            maximum,
        )

# ==========================================================
# LAYOUT
# ==========================================================

def _apply_layout(
    fig: go.Figure,
) -> None:
    """
    Apply common layout.
    """

    fig.update_layout(

        height=GAUGE_HEIGHT,

        margin=dict(
            l=18,
            r=57,
            t=70,
            b=10,
        ),

        paper_bgcolor=TRANSPARENT,

        plot_bgcolor=TRANSPARENT,

        font=dict(
            color=FONT_COLOR,
            family=FONT_FAMILY,
        ),

    )

# ==========================================================
# GAUGE
# ==========================================================

def gauge(
    title: str,
    value: float,
    minimum: float,
    maximum: float,
    unit: str = "",
) -> None:
    """
    Render Plotly gauge chart.
    """

    try:

        _validate_range(
            value,
            minimum,
            maximum,
        )

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=value,

                number=dict(

                    suffix=f" {unit}",

                    font=dict(

                        size=24,

                        color=FONT_COLOR,

                        family=NUMBER_FONT,

                    ),

                ),

                title=dict(

                    text=f"<b>{title}</b>",

                    font=dict(

                        size=13,

                        color=SECONDARY_FONT,

                        family=FONT_FAMILY,

                    ),

                ),

                gauge=dict(

                    shape="angular",

                    axis=dict(

                        range=[minimum, maximum],

                        tickwidth=1,

                        tickcolor="#6B6F75",

                        tickfont=dict(

                            size=10,

                            family=NUMBER_FONT,

                        ),

                    ),

                    bar=dict(

                        color=ACCENT_COLOR,

                        thickness=0.18,

                    ),

                    bgcolor=TRANSPARENT,

                    borderwidth=0,

                    steps=[

                        dict(

                            range=[
                                minimum,
                                maximum * 0.8,
                            ],

                            color=NORMAL_COLOR,

                        ),

                        dict(

                            range=[
                                maximum * 0.8,
                                maximum,
                            ],

                            color=WARNING_COLOR,

                        ),

                    ],

                    threshold=dict(

                        line=dict(

                            color=FONT_COLOR,

                            width=3,

                        ),

                        value=value,

                    ),

                ),

            )

        )

        _apply_layout(
            fig,
        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config=PLOT_CONFIG,

        )

    except Exception:

        logger.exception(
            "Failed rendering gauge."
        )

        st.error(
            "Unable to display gauge."
        )