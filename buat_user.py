from werkzeug.security import generate_password_hash
from backend.database import execute

username = "opnzll"
password = "2204840"

success = execute(
    """
    INSERT INTO users (
        fullname,
        username,
        password,
        role
    )
    VALUES (
        :fullname,
        :username,
        :password,
        :role
    )
    """,
    {
        "fullname": "Raden Rafi",
        "username": username,
        "password": generate_password_hash(password),
        "role": "Administrator",
    },
)

if success:
    print("User berhasil dibuat!")
else:
    print("Gagal membuat user.")