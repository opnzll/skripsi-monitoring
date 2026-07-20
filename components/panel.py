"""
Reusable information panel component.
"""

from __future__ import annotations

import html
import logging

import streamlit as st

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# HELPERS
# ==========================================================

def _safe(value) -> str:
    """
    Convert None to '-' and escape HTML.
    """

    if value is None:
        return "-"

    return html.escape(str(value))


def _build_rows(rows: dict[str, object]) -> str:
    """
    Generate HTML table rows.
    """

    html_rows = []

    for label, value in rows.items():

        html_rows.append(
            f"""
<tr>
<td>{_safe(label)}</td>
<td>{_safe(value)}</td>
</tr>
"""
        )

    return "".join(html_rows)


# ==========================================================
# PANEL
# ==========================================================

def panel(
    title: str,
    rows: dict[str, object],
    icon: str = "",
) -> None:
    """
    Render reusable information panel.

    Parameters
    ----------
    title:
        Panel title.

    rows:
        Dictionary in the form:
        {"Label": "Value"}

    icon:
        Optional emoji or icon.
    """

    try:

        table_rows = _build_rows(rows)

        st.markdown(
            f"""
<div class="panel">

<h4>{_safe(icon)} {_safe(title)}</h4>

<table>

{table_rows}

</table>

</div>
""",
            unsafe_allow_html=True,
        )

    except Exception:

        logger.exception(
            "Failed rendering panel."
        )

        raise