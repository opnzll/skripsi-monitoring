"""
Reusable Plotly chart components for Smart Energy Monitoring.
"""

from __future__ import annotations

import logging

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from backend.services import get_history_data

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

ACCENT_COLOR = "#5B8DEF"

FILL_COLOR = "rgba(91,141,239,.08)"

TRANSPARENT = "rgba(0,0,0,0)"

GRID_COLOR = "rgba(255,255,255,.06)"

FONT_COLOR = "#E8E9EB"

FONT_FAMILY = "Inter"

DEFAULT_LIMIT = 100

CHART_HEIGHT = 340

PLOT_CONFIG = {

    "displayModeBar": False,

    "responsive": True,

    "scrollZoom": False,

}

# ==========================================================
# CACHE
# ==========================================================

@st.cache_data(
    ttl=5,
    show_spinner=False,
)
def load_chart_data(
    limit: int,
) -> pd.DataFrame:
    """
    Load monitoring history.
    """

    return get_history_data(limit)["history"]

# ==========================================================
# VALIDATION
# ==========================================================

def _validate_column(
    df: pd.DataFrame,
    column: str,
) -> bool:
    """
    Validate requested dataframe column.
    """

    if column not in df.columns:

        logger.error(
            "Column '%s' was not found.",
            column,
        )

        st.error(
            f"Column '{column}' was not found."
        )

        return False

    return True

# ==========================================================
# TRACE
# ==========================================================

def _create_trace(
    df: pd.DataFrame,
    column: str,
    title: str,
    unit: str,
) -> go.Scatter:
    """
    Create reusable Plotly trace.
    """

    return go.Scatter(

        x=df["created_at"],

        y=df[column],

        mode="lines",

        name=title,

        line=dict(

            color=ACCENT_COLOR,

            width=2,

        ),

        fill="tozeroy",

        fillcolor=FILL_COLOR,

        hovertemplate=(
            f"<b>%{{y:.2f}} {unit}</b>"
            "<extra></extra>"
        ),

    )

# ==========================================================
# LAYOUT
# ==========================================================

def _apply_layout(
    fig: go.Figure,
    unit: str,
) -> None:
    """
    Apply common Plotly layout.
    """

    fig.update_layout(

        template="plotly_dark",

        height=CHART_HEIGHT,

        paper_bgcolor=TRANSPARENT,

        plot_bgcolor=TRANSPARENT,

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20,

        ),

        hovermode="x unified",

        showlegend=False,

        font=dict(

            color=FONT_COLOR,

            family=FONT_FAMILY,

        ),

        xaxis=dict(

            title="",

            showgrid=False,

            zeroline=False,

            showline=False,

        ),

        yaxis=dict(

            title=unit,

            gridcolor=GRID_COLOR,

            zeroline=False,

        ),

    )

# ==========================================================
# GENERIC LINE CHART
# ==========================================================

def line_chart(
    title: str,
    column: str,
    unit: str,
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Render reusable Plotly line chart.

    Parameters
    ----------
    title:
        Chart title.

    column:
        DataFrame column name.

    unit:
        Display unit.

    limit:
        Number of monitoring records.
    """

    try:

        df = load_chart_data(limit)

        if df.empty:

            logger.warning(
                "Monitoring dataset is empty."
            )

            st.warning(
                "No monitoring data available."
            )

            return

        if not _validate_column(
            df,
            column,
        ):
            return

        fig = go.Figure()

        fig.add_trace(

            _create_trace(

                df=df,

                column=column,

                title=title,

                unit=unit,

            )

        )

        _apply_layout(

            fig,

            unit,

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config=PLOT_CONFIG,

        )

    except Exception:

        logger.exception(

            "Failed rendering '%s' chart.",

            title,

        )

        st.error(

            "Unable to display chart."

        )

# ==========================================================
# SPECIFIC CHARTS
# ==========================================================

def voltage_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display voltage trend.
    """

    line_chart(
        title="Voltage",
        column="voltage",
        unit="Volt",
        limit=limit,
    )


def current_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display current trend.
    """

    line_chart(
        title="Current",
        column="current",
        unit="Ampere",
        limit=limit,
    )


def power_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display power trend.
    """

    line_chart(
        title="Power",
        column="power",
        unit="Watt",
        limit=limit,
    )


def energy_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display energy trend.
    """

    line_chart(
        title="Energy",
        column="energy",
        unit="kWh",
        limit=limit,
    )


def frequency_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display frequency trend.
    """

    line_chart(
        title="Frequency",
        column="frequency",
        unit="Hz",
        limit=limit,
    )


def pf_chart(
    limit: int = DEFAULT_LIMIT,
) -> None:
    """
    Display power factor trend.
    """

    line_chart(
        title="Power Factor",
        column="power_factor",
        unit="PF",
        limit=limit,
    )