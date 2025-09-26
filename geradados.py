import pandas as pd
import random
from datetime import datetime, timedelta

nomes = ["Teclado", "Mouse", "Monitor", "HD Externo", "Notebook", "Impressora", "Webcam", "Caixa de Som", "Pen Drive", "SSD"]
categorias = ["Periféricos", "Armazenamento", "Computadores", "Impressão", "Áudio e Vídeo"]
lojas = ["Manaus", "Belém", "Fortaleza", "Recife", "Salvador"]

estoque = []
for i in range(1, 1001):
    loja = random.choice(lojas)
    nome = f"{random.choice(nomes)} {random.randint(100, 999)}"
    categoria = random.choice(categorias)
    quantidade = random.randint(0, 50)
    estoque_minimo = random.randint(5, 20)
    dias_atras = random.randint(0, 30)
    ultima_atualizacao = (datetime.today() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
    
    estoque.append([i, loja, nome, categoria, quantidade, estoque_minimo, ultima_atualizacao])

estoque_df = pd.DataFrame(estoque, columns=["id", "loja_id", "nome_produto", "categoria", "quantidade", "estoque_minimo", "ultima_atualizacao"])
estoque_df.to_excel("estoque.xlsx", index=False)
print("Arquivo estoque.xlsx gerado com sucesso!")

vendas = []
for _ in range(3000):
    loja = random.choice(lojas)
    produto_id = random.randint(1, 1000)
    quantidade = random.randint(1, 5)
    data = (datetime.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
    vendas.append([loja, produto_id, quantidade, data])

vendas_df = pd.DataFrame(vendas, columns=["loja_id", "produto_id", "quantidade", "data"])
vendas_df.to_excel("vendas.xlsx", index=False)
print("Arquivo vendas.xlsx gerado com sucesso!")
