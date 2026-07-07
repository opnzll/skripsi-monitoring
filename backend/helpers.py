from datetime import datetime

# ==========================================================
# FORMAT NUMBER
# ==========================================================

def format_number(value, decimal=2):

    try:

        return f"{float(value):.{decimal}f}"

    except:

        return "-"


# ==========================================================
# FORMAT UNIT
# ==========================================================

def with_unit(value, unit, decimal=2):

    try:

        return f"{float(value):.{decimal}f} {unit}"

    except:

        return "-"


# ==========================================================
# FORMAT DATETIME
# ==========================================================

def format_datetime(value):

    if value is None:

        return "-"

    if isinstance(value, datetime):

        return value.strftime("%d-%m-%Y %H:%M:%S")

    return str(value)


# ==========================================================
# STATUS VOLTAGE
# ==========================================================

def voltage_status(voltage):

    if voltage < 210:

        return "Low"

    elif voltage <= 240:

        return "Normal"

    else:

        return "High"


# ==========================================================
# STATUS POWER FACTOR
# ==========================================================

def power_factor_status(pf):

    if pf >= 0.90:

        return "Excellent"

    elif pf >= 0.85:

        return "Good"

    else:

        return "Poor"


# ==========================================================
# STATUS FREQUENCY
# ==========================================================

def frequency_status(freq):

    if 49 <= freq <= 51:

        return "Stable"

    return "Unstable"