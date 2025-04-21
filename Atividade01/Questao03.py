import pandas as pd

def filtrar_produtos_baixo_estoque():
    estoque = pd.read_csv('estoque.csv', sep=',')
    return estoque[estoque.groupby('Produto')['Quantidade'].transform('sum') < 10]

print(filtrar_produtos_baixo_estoque())

estoque = pd.read_csv('estoque.csv', sep=',')

estoque_abaixo_10 = estoque[estoque['Quantidade'] < 10]
print(estoque_abaixo_10[['Produto', 'Quantidade']])

        
'''
import pandas as pd

estoque = pd.read_csv('estoque.csv', sep=',')

produtos_baixo_estoque = estoque[estoque.groupby('Produto')['Quantidade'].transform('sum') < 10]

print(produtos_baixo_estoque[['Produto', 'Quantidade']])

produtos_baixo_estoque.to_csv('produtos_baixo_estoque.csv', index=False)
'''
