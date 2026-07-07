from backend.database import query

df = query("SHOW CREATE TABLE monitoring_data")

print(df.iloc[0,1])