from backend.database import query

df = query("DESCRIBE users")
print(df)
