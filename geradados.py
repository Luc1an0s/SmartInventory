import pandas as pd
import random
from datetime import datetime, timedelta

nomes = ["Teclado", "Mouse", "Monitor", "HD Externo", "Notebook", "Impressora", "Webcam", "Caixa de Som", "Pen Drive", "SSD"]
categorias = ["Periféricos", "Armazenamento", "Computadores", "Impressão", "Áudio e Vídeo"]
lojas = ["Manaus", "Belém", "Fortaleza", "Recife", "Salvador"]

produtos_base = []
for i in range(1, 101):
    nome = f"{random.choice(nomes)} {random.randint(100, 999)}"
    categoria = random.choice(categorias)
    produtos_base.append((i, nome, categoria))

estoque = []
for produto_id, nome, categoria in produtos_base:
    for loja in lojas:
        quantidade = random.randint(0, 50)
        estoque_minimo = random.randint(5, 20)
        dias_atras = random.randint(0, 30)
        ultima_atualizacao = (datetime.today() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        estoque.append([produto_id, loja, nome, categoria, quantidade, estoque_minimo, ultima_atualizacao])

estoque_df = pd.DataFrame(estoque, columns=["produto_id", "loja_id", "nome_produto", "categoria", "estoque_atual", "estoque_minimo", "ultima_atualizacao"])
estoque_df.to_excel("estoque.xlsx", index=False)
print("estoque.xlsx gerado com produtos replicados entre lojas")


vendas = []
for _ in range(3000):
    loja = random.choice(lojas)
    produto_id = random.randint(1, 100)
    quantidade = random.randint(1, 5)
    data = (datetime.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
    vendas.append([loja, produto_id, quantidade, data])

vendas_df = pd.DataFrame(vendas, columns=["loja_id", "produto_id", "quantidade", "data"])
vendas_df.to_excel("vendas.xlsx", index=False)
print("vendas.xlsx gerado com produtos distribuídos entre lojas")
