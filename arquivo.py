#with open('arquivo.txt', 'r') as f:
#    for line in f:
#        print(line.strip())

with open('arquivo.txt', 'r', encoding='iso-8859-1') as f:
    b = f.read(100)

print(b)

# Abrindo o arquivo no modo binário para verificar os primeiros bytes

with open('arquivoBom.txt', 'rb') as file:
    primeiro_bytes = file.read(3) # Lê os primeiros 3 bytes
    # Verifica se a BOM está presente
    if primeiro_bytes == b'\xef\xbb\xbf':
        print("BOM detectada no arquivo!")
        # Ler o restante do arquivo, agora sem a BOM
        conteudo = file.read().decode('iso-8859-1')
    else:
        # Se não houver BOM, volta ao início e lê o arquivo inteiro
        file.seek(0)
        conteudo = file.read().decode('iso-8859-1')
    # Exibe o conteúdo do arquivo
    print(conteudo)