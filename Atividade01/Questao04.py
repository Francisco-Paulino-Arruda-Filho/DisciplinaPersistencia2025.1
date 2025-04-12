import pandas as pd
from Questao03 import filtrar_produtos_baixo_estoque

# Carrega os dados
estoque = pd.read_csv('estoque.csv', sep=',')

# Salva os produtos com baixo estoque
filtrar_produtos_baixo_estoque().to_csv('estoque_baixo.csv', index=False)

# Cria novo DataFrame com valor total por produto e inclui a categoria
estoque['Valor Total'] = estoque['Quantidade'] * estoque['Preco_Unitario']
valor_total_por_produto = estoque.groupby(['Produto', 'Categoria'], as_index=False)['Valor Total'].sum()

# Exporta para Excel com uma aba por categoria
with pd.ExcelWriter('valor_total_estoque.xlsx') as writer:
    for categoria, df_categoria in valor_total_por_produto.groupby('Categoria'):
        df_categoria[['Produto', 'Valor Total']].to_excel(writer, sheet_name=str(categoria), index=False)
