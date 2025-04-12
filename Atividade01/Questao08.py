import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do CSV
df = pd.read_csv('estoque.csv')
# Garantir que a coluna de data está em formato datetime
df['Data_Atualizacao'] = pd.to_datetime(df['Data_Atualizacao'])

# Agrupar por mês
df['AnoMes'] = df['Data_Atualizacao'].dt.to_period('M')
monthly = df.groupby('AnoMes').agg({
    'Produto': 'count',
    'Quantidade': 'mean'
}).rename(columns={
    'Produto': 'Atualizações',
    'Quantidade': 'Quantidade Média'
})

# Converter o índice de volta para datetime para o gráfico
monthly.index = monthly.index.to_timestamp()

# Plotar
plt.figure(figsize=(12, 6))
plt.plot(monthly.index, monthly['Atualizações'], marker='o', label='Atualizações')
plt.plot(monthly.index, monthly['Quantidade Média'], marker='s', label='Quantidade Média')
plt.title('Análise Temporal de Estoque')
plt.xlabel('Mês')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
