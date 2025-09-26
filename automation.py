import sqlite3
import pandas as pd
import smtplib
from email.message import EmailMessage
import os

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
SMTP_SERVIDOR = os.getenv("SMTP_SERVIDOR", "smtp.gmail.com")
SMTP_PORTA = int(os.getenv("SMTP_PORTA", 587))

conn = sqlite3.connect("estoque.db")

produtos_df = pd.read_sql("SELECT * FROM produtos", conn)
vendas_df = pd.read_sql("SELECT * FROM vendas", conn)

vendas_df['data'] = pd.to_datetime(vendas_df['data'])
vendas_por_dia = vendas_df.groupby(['loja_id', 'produto_id', 'data']).sum().reset_index()
media_diaria = vendas_por_dia.groupby(['loja_id', 'produto_id'])['quantidade'].mean().reset_index()
media_diaria.rename(columns={'quantidade': 'media_diaria'}, inplace=True)

estoque_df = produtos_df.rename(columns={'id': 'produto_id', 'quantidade': 'estoque_atual'})
estoque_df = estoque_df.merge(media_diaria, on=['loja_id', 'produto_id'], how='left')

faltando = estoque_df[estoque_df['estoque_atual'] < estoque_df['estoque_minimo']]

corpo = "⚠️ Produtos com estoque abaixo do mínimo:\n\n"

sugestoes = []
for _, falta in faltando.iterrows():
    produto_id = falta['produto_id']
    nome_produto = falta['nome_produto']
    loja_destino = falta['loja_id']
    qtd_falta = falta['estoque_atual']
    media_destino = falta['media_diaria']

    corpo += f"- {nome_produto} ({loja_destino}): {qtd_falta} unidades\n"

    candidatos = estoque_df[
        (estoque_df['produto_id'] == produto_id) &
        (estoque_df['estoque_atual'] > estoque_df['estoque_minimo']) &
        (estoque_df['media_diaria'] < media_destino)
    ]

    for _, candidato in candidatos.iterrows():
        loja_origem = candidato['loja_id']
        qtd_sugerida = int(candidato['estoque_atual'] - candidato['estoque_minimo'])
        sugestoes.append((nome_produto, loja_origem, loja_destino, qtd_sugerida))

        corpo += f"  ➤ Sugestão: transferir {qtd_sugerida} unidades da loja {loja_origem}\n"

if not faltando.empty:
    msg = EmailMessage()
    msg.set_content(corpo)
    msg["Subject"] = "🚨 Alerta de Estoque + Sugestões de Transferência"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)

conn.close()
print("E-mail enviado com sugestões de transferência!")
