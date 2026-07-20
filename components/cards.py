"""
Metric card component.
"""

from __future__ import annotations

import logging

import streamlit as st

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

STATUS_OK = "ok"

STATUS_WARN = "warn"

STATUS_DANGER = "danger"

VALID_STATUS = {
    STATUS_OK,
    STATUS_WARN,
    STATUS_DANGER,
}

# ==========================================================
# HELPERS
# ==========================================================

def _safe(value) -> str:
    """
    Convert None to '-'.
    """

    return "-" if value is None else str(value)


def _unit_html(unit: str) -> str:
    """
    Build unit HTML.
    """

    if not unit:
        return ""

    return (
        f'<span class="metric-unit">'
        f"{unit}"
        f"</span>"
    )


def _status_html(
    status: str,
    status_type: str,
) -> str:
    """
    Build status HTML.
    """

    if not status:
        return ""

    if status_type not in VALID_STATUS:

        logger.warning(
            "Unknown status type: %s",
            status_type,
        )

        status_type = STATUS_OK

    return (
        f'<div class="metric-status {status_type}">'
        f"● {status}"
        f"</div>"
    )

# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(
    title: str,
    value,
    unit: str = "",
    status: str = "",
    status_type: str = STATUS_OK,
    icon: str = "",
) -> None:
    """
    Render metric card.
    """

    try:

        st.markdown(
            f"""
<div class="metric-card">

<div class="metric-title">
<span class="metric-icon">{icon}</span>
{_safe(title)}
</div>

<div class="metric-value">
{_safe(value)}
{_unit_html(unit)}
</div>

{_status_html(
status,
status_type,
)}

</div>
""",
            unsafe_allow_html=True,
        )

    except Exception:

        logger.exception(
            "Failed rendering metric card."
        )

        raise