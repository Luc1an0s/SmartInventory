import sqlite3
import pandas as pd
import smtplib
from email.message import EmailMessage
import os

conn = sqlite3.connect("estoque.db")
produtos_df = pd.read_sql("SELECT * FROM produtos", conn)
vendas_df = pd.read_sql("SELECT * FROM vendas", conn)
conn.close()

vendas_df['data'] = pd.to_datetime(vendas_df['data'])
vendas_por_dia = vendas_df.groupby(['loja_id', 'produto_id', 'data']).sum().reset_index()
media_diaria = vendas_por_dia.groupby(['loja_id', 'produto_id'])['quantidade'].mean().reset_index()
media_diaria.rename(columns={'quantidade': 'media_diaria'}, inplace=True)

estoque_df = produtos_df.rename(columns={'id': 'produto_id', 'quantidade': 'estoque_atual'})
estoque_df = estoque_df.merge(media_diaria, on=['loja_id', 'produto_id'], how='left')
estoque_df['media_diaria'] = estoque_df['media_diaria'].fillna(0)

faltando = estoque_df[estoque_df['estoque_atual'] < estoque_df['estoque_minimo']]

corpo = "📦 Relatório de Estoque Crítico e Sugestões de Transferência\n\n"

for _, falta in faltando.iterrows():
    produto_id = falta['produto_id']
    nome_produto = falta['nome_produto']
    loja_destino = falta['loja_id']
    qtd_falta = falta['estoque_atual']
    media_destino = falta['media_diaria']

    corpo += f"🔍 {nome_produto} ({loja_destino}) - {qtd_falta} unidades (média: {round(media_destino, 2)})\n"

    todas_lojas = estoque_df[estoque_df['produto_id'] == produto_id]
    candidatos = todas_lojas[
        (todas_lojas['loja_id'] != loja_destino) &
        (todas_lojas['estoque_atual'] > todas_lojas['estoque_minimo']) &
        (todas_lojas['media_diaria'] <= media_destino + 0.5)
    ]

    if candidatos.empty:
        corpo += " Nenhum candidato válido para transferência.\n"
    else:
        for _, candidato in candidatos.iterrows():
            loja_origem = candidato['loja_id']
            qtd_sugerida = int(candidato['estoque_atual'] - candidato['estoque_minimo'])
            media_origem = round(candidato['media_diaria'], 2)
            corpo += f"  ➤ {loja_origem}: sugerir {qtd_sugerida} unidades (média: {media_origem})\n"

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
SMTP_SERVIDOR = os.getenv("SMTP_SERVIDOR", "smtp.gmail.com")
SMTP_PORTA = int(os.getenv("SMTP_PORTA", 587))

msg = EmailMessage()
msg.set_content(corpo)
msg["Subject"] = "🚨 Alerta de Estoque Crítico"
msg["From"] = EMAIL_REMETENTE
msg["To"] = EMAIL_DESTINATARIO

try:
    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)
    print("E-mail enviado com sucesso!")
except Exception as e:
    print("Erro ao enviar e-mail:", e)
