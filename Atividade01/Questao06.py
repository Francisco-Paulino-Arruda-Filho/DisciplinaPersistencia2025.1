import pandas as pd
import matplotlib.pyplot as plt

# Lê o CSV
estoque = pd.read_csv('estoque.csv', sep=',')

# Remove espaços dos nomes das colunas, se houver
estoque.columns = estoque.columns.str.strip()

# Cria uma nova coluna com o valor total por linha
estoque['Valor_Estoque'] = estoque['Quantidade'] * estoque['Preco_Unitario']

# Agrupa por categoria e soma o valor total
valor_total_por_categoria = (
    estoque.groupby('Categoria')['Valor_Estoque']
    .sum()
    .sort_values(ascending=False)
)

# Exibe o gráfico de barras
valor_total_por_categoria.plot(kind='bar', figsize=(8, 5), color='skyblue')

plt.title('Valor Total por Categoria')
plt.ylabel('Valor em R$')
plt.xlabel('Categoria')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
