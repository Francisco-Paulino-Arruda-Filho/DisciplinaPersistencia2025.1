
def menu():
    print("=== Lista de tarefas")
    print("1- Adicionar tarefas")
    print("2- Listar tarefas")
    print("3- Visualizar tarefas")
    print("4-Retirar tarefas")
    print("5- Sair")
    print("6- Buscar tarefa por palavra-chave")
    return int(input("Escolha uma opção: "))

def adicionar_tarefa():
    tarefa = input("Digite a tarefa: ")
    with open('tarefas.txt', 'a', encoding='utf-8') as f:
        f.write(tarefa + '\n')
    print("Tarefa adicionada com sucesso!")

def listar_tarefas():
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
        if tarefas:
            print("=== Tarefas ===")
            for i, tarefa in enumerate(tarefas, start=1):
                print(f"{i}. {tarefa.strip()}")
        else:
            print("Nenhuma tarefa encontrada.")

def visualizar_tarefas():
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
        if tarefas:
            print("=== Tarefas ===")
            for i, tarefa in enumerate(tarefas, start=1):
                print(f"{i}. {tarefa.strip()}")
        else:
            print("Nenhuma tarefa encontrada.")

def buscar_tarefa_por_palavra_chave():
    palavra_chave = input("Digite a palavra-chave para buscar: ")
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
        tarefas_encontradas = [tarefa for tarefa in tarefas if palavra_chave.lower() in tarefa.lower()]
        if tarefas_encontradas:
            print("=== Tarefas encontradas ===")
            for i, tarefa in enumerate(tarefas_encontradas, start=1):
                print(f"{i}. {tarefa.strip()}")
        else:
            print("Nenhuma tarefa encontrada com a palavra-chave.")

def removerTarefas():
    with open('tarefas.txt', 'r', encoding='utf-8') as f:
        tarefas = f.readlines()
    if tarefas:
        print("=== Tarefas ===")
        for i, tarefa in enumerate(tarefas, start=1):
            print(f"{i}. {tarefa.strip()}")
        try:
            indice = int(input("Digite o número da tarefa que deseja remover: ")) - 1
            if 0 <= indice < len(tarefas):
                del tarefas[indice]
                with open('tarefas.txt', 'w', encoding='utf-8') as f:
                    f.writelines(tarefas)
                print("Tarefa removida com sucesso!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")
    else:
        print("Nenhuma tarefa encontrada.")

while True:
    opcao = menu()
    if opcao == 1:
        adicionar_tarefa()
    if opcao == 2:
        listar_tarefas()
    if opcao == 3:
        visualizar_tarefas()
    if opcao == 4:
        removerTarefas()
    if opcao == 5:
        print("Saindo do programa...")
        break
    if opcao == 6:
        buscar_tarefa_por_palavra_chave()