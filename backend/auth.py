from werkzeug.security import check_password_hash

from backend.database import query, execute


# ==========================================================
# LOGIN
# ==========================================================

def authenticate(username, password):

    sql = """

    SELECT *

    FROM users

    WHERE username=:username

    LIMIT 1

    """

    user = query(

        sql,

        {

            "username": username

        }

    )

    if user.empty:

        return None

    user = user.iloc[0]

    if not check_password_hash(

        user["password"],

        password

    ):

        return None

    execute(

        """

        UPDATE users

        SET last_login = NOW()

        WHERE id=:id

        """,

        {

            "id": int(user["id"])

        }

    )

    return {

        "id": int(user["id"]),

        "fullname": user["fullname"],

        "username": user["username"],

        "role": user["role"]

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

        False

    )