import pandas as pd

# Leitura e limpeza
estoque = pd.read_csv('estoque.csv', sep=',')
estoque.columns = estoque.columns.str.strip()

# Criação da coluna de valor total por produto
estoque['Valor_Total'] = estoque['Quantidade'] * estoque['Preco_Unitario']

# Seleciona o produto mais valioso de cada categoria
mais_valiosos = estoque.loc[estoque.groupby('Categoria')['Valor_Total'].idxmax()]

# Seleciona colunas desejadas
novo_dataframe = mais_valiosos[['Categoria', 'Produto', 'Valor_Total']]

# Salva no CSV
novo_dataframe.to_csv('produtos_mais_valiosos_por_categoria.csv', index=False)

# Exibe o DataFrame
print(novo_dataframe)
