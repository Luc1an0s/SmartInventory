import pandas as pd
import sqlite3


df = pd.read_excel("estoque.xlsx")


conn = sqlite3.connect("estoque.db")

df.to_sql("produtos", conn, if_exists="replace", index=False)

conn.close()
