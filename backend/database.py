import logging

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger(__name__)

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
    pool_recycle=3600,
)

# ==========================================================
# GENERIC QUERY
# ==========================================================

def query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """
    Menjalankan perintah SELECT dan mengembalikan DataFrame.
    Jika terjadi kesalahan, mengembalikan DataFrame kosong.
    """

    try:
        with engine.connect() as conn:
            return pd.read_sql(
                text(sql),
                conn,
                params=params,
            )

    except SQLAlchemyError:
        logger.exception("Database query failed.")
        return pd.DataFrame()

    except Exception:
        logger.exception("Unexpected error while querying database.")
        return pd.DataFrame()


# ==========================================================
# EXECUTE
# ==========================================================

def execute(sql: str, params: dict | None = None) -> bool:
    """
    Menjalankan INSERT, UPDATE, atau DELETE.

    Returns
    -------
    bool
        True jika berhasil.
        False jika gagal.
    """

    try:
        with engine.begin() as conn:
            conn.execute(
                text(sql),
                params or {},
            )

        return True

    except SQLAlchemyError:
        logger.exception("Database execute failed.")
        return False

    except Exception:
        logger.exception("Unexpected execute error.")
        return False


# ==========================================================
# DATA TERBARU
# ==========================================================

def get_latest() -> pd.DataFrame:

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

def get_last(limit: int = 50) -> pd.DataFrame:

    sql = """
        SELECT *
        FROM monitoring_data
        ORDER BY created_at DESC
        LIMIT :limit
    """

    df = query(sql, {"limit": limit})

    if df.empty:
        return df

    return df.iloc[::-1].reset_index(drop=True)


# ==========================================================
# DATA HARI INI
# ==========================================================

def get_today() -> pd.DataFrame:

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

def get_statistics() -> pd.DataFrame:

    sql = """
        SELECT
            AVG(voltage) AS avg_voltage,
            AVG(current) AS avg_current,
            AVG(power) AS avg_power,
            AVG(power_factor) AS avg_pf,
            MAX(power) AS max_power,
            MIN(power) AS min_power,
            COUNT(*) AS total_data
        FROM monitoring_data
    """

    return query(sql)


# ==========================================================
# DATASET CLUSTERING
# ==========================================================

def get_cluster_dataset() -> pd.DataFrame:

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

def get_history(limit: int = 200) -> pd.DataFrame:

    sql = """
        SELECT *
        FROM monitoring_data
        ORDER BY created_at DESC
        LIMIT :limit
    """

    return query(sql, {"limit": limit})


# ==========================================================
# INSERT DATA
# ==========================================================

def insert_monitoring(
    voltage: float,
    current: float,
    power: float,
    energy: float,
    frequency: float,
    power_factor: float,
) -> bool:

    sql = """
        INSERT INTO monitoring_data (
            voltage,
            current,
            power,
            energy,
            frequency,
            power_factor
        )
        VALUES (
            :voltage,
            :current,
            :power,
            :energy,
            :frequency,
            :power_factor
        )
    """

    return execute(
        sql,
        {
            "voltage": voltage,
            "current": current,
            "power": power,
            "energy": energy,
            "frequency": frequency,
            "power_factor": power_factor,
        },
    )


# ==========================================================
# LAST UPDATE
# ==========================================================

def get_last_timestamp() -> pd.DataFrame:

    sql = """
        SELECT
            MAX(created_at) AS last_update
        FROM monitoring_data
    """

    return query(sql)


# ==========================================================
# DATABASE STATUS
# ==========================================================

def database_status() -> bool:
    """
    Mengecek apakah database dapat diakses.
    """

    try:
        df = query("SELECT 1")

        return not df.empty

    except Exception:
        logger.exception("Database connection check failed.")
        return False