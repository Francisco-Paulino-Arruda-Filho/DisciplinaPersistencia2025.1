from os import write    
import csv
import pickle
import json
import yaml
import toml # type: ignore

dados_pkl = {
    'nome': 'João',
    'idade': 30,
    'notas': [8.5, 7.0, 9.2],
    'aprovado': True
}

dados_csv = {
    'nome': 'Maria',
    'idade': 25,
    'notas': [9.0, 8.5, 10.0],
    'aprovado': True
}

dados_json = {
    'nome': 'Carlos',
    'idade': 28,
    'notas': [7.5, 8.0, 9.0],
    'aprovado': True
}

dados_yaml = {
    'nome': 'Ana',
    'idade': 22,
    'notas': [9.5, 8.0, 9.5],
    'aprovado': True
}

dados_toml = {
    'nome': 'Lucas',
    'idade': 27,
    'notas': [8.0, 7.5, 9.0],
    'aprovado': True
}

with open('dados.pkl', 'wb') as f:
    pickle.dump(dados_pkl, f)

print(dados_pkl)

with open('dados.json', 'w') as f:
    json.dump(dados_json, f)
print(dados_json)

with open('dados.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(dados_csv.keys())
    writer.writerow(dados_csv.values())

with open('dados.yaml', 'w') as f:
    yaml.dump(dados_yaml, f)
print(dados_yaml)


with open('dados.toml', 'w') as f:
    toml.dump(dados_toml, f)
print(dados_toml)


print(dados_csv)