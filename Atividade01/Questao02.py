import pandas as pd

estoque = pd.read_csv('estoque.csv', sep=',')

# Calcula o valor total por produto: soma(Quantidade * Preço) agrupado por Produto
valor_total_por_produto = estoque.groupby('Produto').apply(lambda x: (x['Quantidade'] * x['Preco_Unitario']).sum()).reset_index(name='Valor Total')

print(valor_total_por_produto)