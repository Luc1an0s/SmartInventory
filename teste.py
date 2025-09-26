import sqlite3
import pandas as pd

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

for _, falta in faltando.iterrows():
    produto_id = falta['produto_id']
    nome_produto = falta['nome_produto']
    loja_destino = falta['loja_id']
    qtd_falta = falta['estoque_atual']
    media_destino = falta['media_diaria']

    print(f"\n Produto crítico: {nome_produto} ({loja_destino}) - {qtd_falta} unidades")

    candidatos = estoque_df[
        (estoque_df['produto_id'] == produto_id) &
        (estoque_df['estoque_atual'] > estoque_df['estoque_minimo']) &
        (estoque_df['media_diaria'] <= media_destino)
    ]

    if candidatos.empty:
        print("Nenhum candidato válido para transferência.")
    else:
        print("Candidatos para transferência:")
        for _, candidato in candidatos.iterrows():
            loja_origem = candidato['loja_id']
            qtd_sugerida = int(candidato['estoque_atual'] - candidato['estoque_minimo'])
            media_origem = round(candidato['media_diaria'], 2)
            print(f"  ➤ {loja_origem}: sugerir {qtd_sugerida} unidades (média diária: {media_origem})")
