import pandas as pd

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

def descriptive_statistics(df):

    return pd.DataFrame({

        "Parameter": [

            "Voltage",

            "Current",

            "Power",

            "Frequency",

            "Power Factor"

        ],

        "Average": [

            round(df["voltage"].mean(), 2),

            round(df["current"].mean(), 2),

            round(df["power"].mean(), 2),

            round(df["frequency"].mean(), 2),

            round(df["power_factor"].mean(), 2)

        ],

        "Maximum": [

            round(df["voltage"].max(), 2),

            round(df["current"].max(), 2),

            round(df["power"].max(), 2),

            round(df["frequency"].max(), 2),

            round(df["power_factor"].max(), 2)

        ],

        "Minimum": [

            round(df["voltage"].min(), 2),

            round(df["current"].min(), 2),

            round(df["power"].min(), 2),

            round(df["frequency"].min(), 2),

            round(df["power_factor"].min(), 2)

        ]

    })


# ==========================================================
# POWER QUALITY
# ==========================================================

def power_quality(df):

    avg_pf = df["power_factor"].mean()

    avg_freq = df["frequency"].mean()

    avg_voltage = df["voltage"].mean()

    voltage_status = (

        "Normal"

        if 220 <= avg_voltage <= 240

        else "Warning"

    )

    pf_status = (

        "Good"

        if avg_pf >= 0.85

        else "Low"

    )

    frequency_status = (

        "Stable"

        if 49 <= avg_freq <= 51

        else "Unstable"

    )

    return {

        "avg_voltage": round(avg_voltage, 2),

        "avg_pf": round(avg_pf, 2),

        "avg_frequency": round(avg_freq, 2),

        "voltage_status": voltage_status,

        "pf_status": pf_status,

        "frequency_status": frequency_status

    }