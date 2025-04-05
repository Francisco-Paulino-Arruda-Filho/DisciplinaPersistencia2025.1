with open('arquivo2.txt', 'w', encoding='utf-8-sig') as f:
    while True:
        try:
            line = input()
            print(line, file=f)
        except EOFError:
            break
