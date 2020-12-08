def proibir_string(mensagem):
    invalido = True
    while invalido:
        verificacao = input(mensagem)
        try:
            float(verificacao)
            invalido = False
        except:
            print('Impossível continuar, não é um número, digite um valor válido.')
    return verificacao    
