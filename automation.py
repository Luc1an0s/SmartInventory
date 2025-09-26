import sqlite3
import smtplib
from email.message import EmailMessage
import os

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
SMTP_SERVIDOR = os.getenv("SMTP_SERVIDOR", "smtp.gmail.com")
SMTP_PORTA = int(os.getenv("SMTP_PORTA", 587)) 

conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

cursor.execute("SELECT nome_produto, quantidade FROM produtos WHERE quantidade < estoque_minimo")
produtos_criticos = cursor.fetchall()

if produtos_criticos:
    corpo = "⚠️ Produtos com estoque abaixo do mínimo:\n\n"
    for nome, qtd in produtos_criticos:
        corpo += f"- {nome}: {qtd} unidades\n"

    msg = EmailMessage()
    msg.set_content(corpo)
    msg["Subject"] = "Alerta de Estoque Baixo"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)

conn.close()