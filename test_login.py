from backend.auth import authenticate

user = authenticate(

    "admin",

    "admin123"

)

print(user)