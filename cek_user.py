from werkzeug.security import check_password_hash
from backend.database import query

username = "opnzll"
password = "2204840"

df = query(
    """
    SELECT password
    FROM users
    WHERE username=:username
    """,
    {"username": username},
)

if df.empty:
    print("User tidak ditemukan")
else:
    print("Password cocok:", check_password_hash(df.iloc[0]["password"], password))