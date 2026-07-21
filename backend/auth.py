from werkzeug.security import check_password_hash

from config import DB_HOST, DB_NAME
from backend.database import query, execute


# ==========================================================
# LOGIN
# ==========================================================

def authenticate(username, password):

    sql = """
    SELECT *
    FROM users
    WHERE username = :username
    LIMIT 1
    """

    user = query(
        sql,
        {
            "username": username
        }
    )

    print("=" * 60)
    print("AUTH DB        :", DB_HOST, "/", DB_NAME)
    print("Username Input :", repr(username))
    print("Password Input :", repr(password))
    print("Jumlah User    :", len(user))

    if user.empty:
        print("❌ USER TIDAK DITEMUKAN")
        return None

    user = user.iloc[0]

    print("Username DB    :", user["username"])
    print("Role           :", user["role"])
    print("Hash DB        :", user["password"][:40] + "...")

    result = check_password_hash(
        user["password"],
        password,
    )

    print("Password Cocok :", result)

    if not result:
        print("❌ PASSWORD SALAH")
        return None

    print("✅ LOGIN BERHASIL")

    execute(
        """
        UPDATE users
        SET last_login = NOW()
        WHERE id = :id
        """,
        {
            "id": int(user["id"])
        }
    )

    return {
        "id": int(user["id"]),
        "fullname": user["fullname"],
        "username": user["username"],
        "role": user["role"],
    }


# ==========================================================
# SESSION
# ==========================================================

def login(session, user):

    session["logged_in"] = True
    session["user"] = user


def logout(session):

    session.clear()


def is_logged_in(session):

    return session.get(
        "logged_in",
        False,
    )