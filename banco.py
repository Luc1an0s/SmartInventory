import pandas as pd
import sqlite3


df = pd.read_excel("estoque.xlsx")

conn = sqlite3.connect("estoque.db")

df.to_sql("produtos", conn, if_exists="replace", index=False)

conn.close()

vendas_df = pd.read_excel("vendas.xlsx")

conn = sqlite3.connect("estoque.db")

vendas_df.to_sql("vendas", conn, if_exists="replace", index=False)

conn.close()
print("Tabela 'vendas' inserida no banco de dados!")
