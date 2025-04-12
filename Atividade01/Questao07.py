import pandas as pd

# Lê o CSV
estoque = pd.read_csv('estoque.csv', sep=',')

estoque["Nivel_Estoque"] = estoque["Quantidade"].apply(
    lambda x: "Baixo" if x < 10 else ("Alto" if x > 50 else "Medio")
)

print(estoque["Nivel_Estoque"].value_counts())
