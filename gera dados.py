import pandas as pd
import random
from datetime import datetime, timedelta


nomes = ["Teclado", "Mouse", "Monitor", "HD Externo", "Notebook", "Impressora", "Webcam", "Caixa de Som", "Pen Drive", "SSD"]
categorias = ["Periféricos", "Armazenamento", "Computadores", "Impressão", "Áudio e Vídeo"]


dados = []
for i in range(1, 1001):
    nome = f"{random.choice(nomes)} {random.randint(100, 999)}"
    categoria = random.choice(categorias)
    quantidade = random.randint(0, 50)
    estoque_minimo = random.randint(5, 20)
    dias_atras = random.randint(0, 30)
    ultima_atualizacao = (datetime.today() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
    
    dados.append([i, nome, categoria, quantidade, estoque_minimo, ultima_atualizacao])


df = pd.DataFrame(dados, columns=["id", "nome_produto", "categoria", "quantidade", "estoque_minimo", "ultima_atualizacao"])


df.to_excel("estoque.xlsx", index=False)
print("Arquivo estoque.xlsx gerado com sucesso!")