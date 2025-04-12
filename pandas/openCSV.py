import pandas as pd

df = pd.read_csv('veiculos.csv')

print(df.head(11))

df2 = pd.read_csv('frequencia_notas.csv')

df2["presenca_bin"] = df2["Presenca"].map({"Sim": 1, "Não": 0})

total_aulas = df2.groupby("Aluno")["presenca_bin"].count()

print(total_aulas)

cursos = df2[["Aluno", "Curso"]].drop_duplicates()
aux = pd.merge(df2, cursos)

print(cursos)

print(df2.head(11))