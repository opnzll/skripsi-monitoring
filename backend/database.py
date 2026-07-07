import pandas as pd
from sqlalchemy import create_engine, text

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# ==========================================================
# DATABASE ENGINE
# ==========================================================

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

# ==========================================================
# GENERIC QUERY
# ==========================================================

def query(sql, params=None):
    """
    Menjalankan SELECT dan mengembalikan DataFrame.
    """

    with engine.connect() as conn:

        return pd.read_sql(
            text(sql),
            conn,
            params=params
        )

# ==========================================================
# EXECUTE
# ==========================================================

def execute(sql, params=None):
    """
    INSERT / UPDATE / DELETE.
    """

    with engine.begin() as conn:

        conn.execute(
            text(sql),
            params or {}
        )

# ==========================================================
# DATA TERBARU
# ==========================================================

def get_latest():

    sql = """

    SELECT *

    FROM monitoring_data

    ORDER BY created_at DESC

    LIMIT 1

    """

    return query(sql)

# ==========================================================
# LAST N DATA
# ==========================================================

def get_last(limit=50):

    sql = """

    SELECT *

    FROM monitoring_data

    ORDER BY created_at DESC

    LIMIT :limit

    """

    df = query(
        sql,
        {
            "limit": limit
        }
    )

    return df.iloc[::-1]

# ==========================================================
# DATA HARI INI
# ==========================================================

def get_today():

    sql = """

    SELECT *

    FROM monitoring_data

    WHERE DATE(created_at)=CURDATE()

    ORDER BY created_at

    """

    return query(sql)

# ==========================================================
# STATISTICS
# ==========================================================

def get_statistics():

    sql = """

    SELECT

        AVG(voltage) avg_voltage,

        AVG(current) avg_current,

        AVG(power) avg_power,

        AVG(power_factor) avg_pf,

        MAX(power) max_power,

        MIN(power) min_power,

        COUNT(*) total_data

    FROM monitoring_data

    """

    return query(sql)

# ==========================================================
# CLUSTER DATA
# ==========================================================

def get_cluster_dataset():

    sql = """

    SELECT

        voltage,

        current,

        power,

        energy,

        frequency,

        power_factor

    FROM monitoring_data

    ORDER BY created_at

    """

    return query(sql)

# ==========================================================
# HISTORY
# ==========================================================

def get_history(limit=200):

    sql = """

    SELECT *

    FROM monitoring_data

    ORDER BY created_at DESC

    LIMIT :limit

    """

    return query(
        sql,
        {
            "limit": limit
        }
    )

# ==========================================================
# INSERT MANUAL
# ==========================================================

def insert_monitoring(
    voltage,
    current,
    power,
    energy,
    frequency,
    power_factor
):

    sql = """

    INSERT INTO monitoring_data(

        voltage,

        current,

        power,

        energy,

        frequency,

        power_factor

    )

    VALUES(

        :voltage,

        :current,

        :power,

        :energy,

        :frequency,

        :power_factor

    )

    """

    execute(
        sql,
        {

            "voltage": voltage,

            "current": current,

            "power": power,

            "energy": energy,

            "frequency": frequency,

            "power_factor": power_factor

        }
    )

# ==========================================================
# LAST UPDATE
# ==========================================================

def get_last_timestamp():

    sql = """

    SELECT

        MAX(created_at) last_update

    FROM monitoring_data

    """

    return query(sql)

# ==========================================================
# DATABASE STATUS
# ==========================================================

def database_status():

    try:

        query("SELECT 1")

        return True

    except:

        return False