"""
Analytics utilities for Smart Energy Monitoring.

Provides:
- Descriptive statistics
- Power quality analysis
"""

from __future__ import annotations

import logging

import pandas as pd

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

FEATURES = {
    "Voltage": "voltage",
    "Current": "current",
    "Power": "power",
    "Frequency": "frequency",
    "Power Factor": "power_factor",
}

VOLTAGE_MIN = 220
VOLTAGE_MAX = 240

FREQUENCY_MIN = 49
FREQUENCY_MAX = 51

POWER_FACTOR_MIN = 0.85

# ==========================================================
# VALIDATION
# ==========================================================

def _validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate analytics dataset.
    """

    if df.empty:
        raise ValueError("Analytics dataset is empty.")

    missing = [
        column
        for column in FEATURES.values()
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


# ==========================================================
# HELPER
# ==========================================================

def _summary(series: pd.Series) -> tuple[float, float, float]:
    """
    Return average, maximum and minimum values.
    """

    return (
        round(series.mean(), 2),
        round(series.max(), 2),
        round(series.min(), 2),
    )


# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

def descriptive_statistics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate descriptive statistics table.
    """

    try:

        _validate_dataframe(df)

        rows = []

        for label, column in FEATURES.items():

            avg, maximum, minimum = _summary(
                df[column]
            )

            rows.append(
                {
                    "Parameter": label,
                    "Average": avg,
                    "Maximum": maximum,
                    "Minimum": minimum,
                }
            )

        return pd.DataFrame(rows)

    except Exception:

        logger.exception(
            "Failed generating descriptive statistics."
        )

        raise


# ==========================================================
# POWER QUALITY
# ==========================================================

def power_quality(
    df: pd.DataFrame,
) -> dict:
    """
    Evaluate electrical power quality.
    """

    try:

        _validate_dataframe(df)

        avg_voltage = round(
            df["voltage"].mean(),
            2,
        )

        avg_frequency = round(
            df["frequency"].mean(),
            2,
        )

        avg_pf = round(
            df["power_factor"].mean(),
            2,
        )

        voltage_status = (
            "Normal"
            if VOLTAGE_MIN <= avg_voltage <= VOLTAGE_MAX
            else "Warning"
        )

        frequency_status = (
            "Stable"
            if FREQUENCY_MIN <= avg_frequency <= FREQUENCY_MAX
            else "Unstable"
        )

        pf_status = (
            "Good"
            if avg_pf >= POWER_FACTOR_MIN
            else "Low"
        )

        return {

            "avg_voltage": avg_voltage,

            "avg_frequency": avg_frequency,

            "avg_pf": avg_pf,

            "voltage_status": voltage_status,

            "frequency_status": frequency_status,

            "pf_status": pf_status,

        }

    except Exception:

        logger.exception(
            "Failed analyzing power quality."
        )

        raise