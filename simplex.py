import matplotlib.pyplot as plt
from funcoes_leitura import proibir_string
from funcoes_matriz import multiplicar_duas_matrizes, subtrair_duas_matrizes, gerar_matriz_identidade, juntar_matriz, mostrar_matriz, inverter_matriz

# GERA A STRING DE FUNÇÃO OBJETIVO
def gerar_string_funcao_objetivo(qtd_variaveis, maximizacao, coeficientes_funcao_objetivo):
    funcao_objetivo = 'max' if maximizacao == 1 else 'min'
    print()
    for i in range(qtd_variaveis):
        funcao_objetivo += ' {0}X{1} +'.format(
            coeficientes_funcao_objetivo[0][i], i+1)

    # AQUI SÓ FORMATA A STRING DA FUNÇÃO OBJETIVO
    funcao_objetivo = funcao_objetivo[0:len(
        funcao_objetivo)-1:] + funcao_objetivo[len(funcao_objetivo)::]

    return funcao_objetivo

# PEGA OS COEFICIENTES DAS VARIAVEIS DE DECISÃO DA FUNÇÃO OBJETIVO
def gerar_matriz_coeficiente_variavel_decisao(qtd_variaveis):
    coeficientes_funcao_objetivo = [[]]
    print()
    for i in range(qtd_variaveis):
        coeficientes_funcao_objetivo[0].append(
            float(proibir_string('Digite o coeficiente da variável de decisão {0}: '.format(i+1))))
    return coeficientes_funcao_objetivo


# GERA MATRIZ INCOGNITAS E VARIAVEIS DE BASE
def gerar_matriz_incognitas(qtd_variaveis):
    matriz_incognitas = []
    for i in range(qtd_variaveis):
        matriz_incognitas.append(['X{0}'.format(str(i+1))])
    for i in range(qtd_variaveis):
        matriz_incognitas.append(['S{0}'.format(str(i+1))])
    return matriz_incognitas


# GERA MATRIZ INDICES DAS VARIAVEIS DE BASE
def gerar_matriz_variaveis_base(qtd_variaveis):
    matriz_variaveis_base = []
    for i in range(qtd_variaveis):
        matriz_variaveis_base.append([qtd_variaveis+i])
    return matriz_variaveis_base

# GERAR MATRIZ DOS COEFICIENTES DA RESTRIÇÃO
def gerar_matriz_coeficiente_restricao(qtd_restricoes, qtd_variaveis):
    print()
    coeficientes_restricoes = []
    termos_independentes = []
    for i in range(qtd_restricoes):
        aux = []
        for j in range(qtd_variaveis):
            aux.append(
                float(proibir_string('Digite o coeficiente de x{0} na {1}ª restrição: '.format(j+1, i+1))))
        termos_independentes.append(
            [float(proibir_string('Digite o termo independente da restrição: '))])
        coeficientes_restricoes.append(aux)
        print()

    return coeficientes_restricoes, termos_independentes


def menu():

    qtd_variaveis = int(proibir_string('Digite a quantidade de variáveis de decisão: '))
    qtd_restricoes = int(proibir_string('Digite a quantidade de restricoes: '))

    print('\nInforme o modo a ser calculado')
    print('Modo Simplificado - [1]\nModo completo - [2]')
    modo = int(proibir_string('Sua opção: '))

    print('\nA função objetivo deverá ser maximizada ou minimizada?')
    print('Maximização - [1]\nMinimização - [2]')
    maximizacao = int(proibir_string('Sua Opção: '))

    passo_um(qtd_variaveis, qtd_restricoes, maximizacao, modo)

def passo_um(qtd_variaveis, qtd_restricoes, maximizacao, modo):

    coeficientes_funcao_objetivo = gerar_matriz_coeficiente_variavel_decisao(
        qtd_variaveis)

    matriz_incognitas = gerar_matriz_incognitas(qtd_variaveis)

    string_funcao_objetivo = gerar_string_funcao_objetivo(
        qtd_variaveis, maximizacao, coeficientes_funcao_objetivo)

    coeficientes_restricoes, termos_independentes = gerar_matriz_coeficiente_restricao(
        qtd_restricoes, qtd_variaveis)

    # GERA MATRIZ IDENTIDADE NA ORDEM DA MATRIZ DE COEFICIENTES DA RESTRIÇÃO
    identidade = gerar_matriz_identidade(len(coeficientes_restricoes))

    print('Foi escolhido o modo {0}\n'.format(
        'Simples' if modo == 1 else 'Completo'))

    print('\nFunção objetivo')
    print(string_funcao_objetivo)

    mostrar_matriz(coeficientes_funcao_objetivo, '\nMatriz dos coeficientes da função objetivo (C)')

    mostrar_matriz(matriz_incognitas[:qtd_variaveis], '\nMatriz das incógnitas (X)')

    mostrar_matriz(coeficientes_restricoes,
               '\nMatriz dos coeficientes das restrições (A)')

    mostrar_matriz(termos_independentes, '\nMatriz dos termos independentes das restrições (b)')

    if modo == 2:
        mostrar_matriz(identidade, '\nMatriz identidade (I)')

    coeficientes_restricoes_identidade = list(juntar_matriz(coeficientes_restricoes, identidade))

    if modo == 2:
        mostrar_matriz(coeficientes_restricoes_identidade,
               '\nMatriz dos coeficientes das restrições mais a matriz identidade (A | I)')

    inicializar_passo_dois(qtd_variaveis, identidade, coeficientes_funcao_objetivo, coeficientes_restricoes_identidade, termos_independentes, coeficientes_restricoes, modo, maximizacao)


def inicializar_passo_dois(qtd_variaveis, identidade, coeficientes_funcao_objetivo, coeficientes_restricoes_identidade, termos_independentes, coeficientes_restricoes, modo, maximizacao):
    #GUARDA MATRIZ VARIAVEIS DE BASE EM UMA VARIÁVEL
    matriz_variaveis_base = gerar_matriz_variaveis_base(qtd_variaveis)
    #GUARDA MATRIZ IDENTIDADE EM UMA VARIÁVEL
    matriz_B = identidade
    #MOSTRA MATRIZES
    if modo == 2:
        mostrar_matriz(matriz_variaveis_base, '\nMatriz das variáveis de base (X_B)')
        mostrar_matriz(matriz_B, '\nMatriz B')

    coeficientes_funcao_objetivo_negativo = [[]]
    #GERA NOVA FUNÇÃO OBJETIVO NEGATIVA
    for i in range(len(coeficientes_funcao_objetivo[0])):
        if maximizacao == 2:
            coeficientes_funcao_objetivo[0][i] *= -1
        negativo = coeficientes_funcao_objetivo[0][i] * -1
        coeficientes_funcao_objetivo_negativo[0].append(negativo)

    if modo == 2:
        mostrar_matriz(coeficientes_funcao_objetivo_negativo, '\nMatriz dos coeficientes negativos da função objetivo (-C)')

    #CRIA A MATRIZ DOS COEFICIENTES DAS VARIÁVEIS DE BASE (C_B)
    coeficientes_variaveis_base = [[]]

    for i in range(qtd_variaveis):
        coeficientes_variaveis_base[0].append(0)


    passo_dois(qtd_variaveis, identidade, coeficientes_funcao_objetivo, termos_independentes, coeficientes_funcao_objetivo_negativo, matriz_variaveis_base, matriz_B, coeficientes_variaveis_base, coeficientes_restricoes, modo, maximizacao)

def passo_dois(qtd_variaveis, identidade, coeficientes_funcao_objetivo, termos_independentes, coeficientes_funcao_objetivo_negativo, matriz_variaveis_base, matriz_B, coeficientes_variaveis_base, coeficientes_restricoes, modo, maximizacao):
    #VERIFICA NÚMERO MAIS NEGATIVO DA MATRIZ DE COEFICIENTES DA FUNÇÃO OBJETIVO MULTIPLICADA POR -1
    auxiliar = 999999999999999
    guarda_indice_entrar = 0

    for i in range(len(coeficientes_funcao_objetivo_negativo[0])):
        if coeficientes_funcao_objetivo_negativo[0][i] < auxiliar:
            auxiliar = coeficientes_funcao_objetivo_negativo[0][i]
            guarda_indice_entrar = i
    #INVERTE A MATRIZ B
    inversa_matriz_B = inverter_matriz(matriz_B)
    if modo == 2:
        mostrar_matriz(inversa_matriz_B,'\nA inversa da matriz B é: ')
    #VERIFICA SE É POSSÍVEL MELHORAR A SOLUÇÃO
    if auxiliar >= 0:
        finalizacao(inversa_matriz_B, termos_independentes, coeficientes_variaveis_base, coeficientes_restricoes, qtd_variaveis, matriz_variaveis_base, maximizacao)
    else:
        if modo == 2:
            print('\nO valor que entrará na base será o {}'.format(auxiliar))
            print('\nA coluna que entrará é a coluna {}'.format(guarda_indice_entrar))
        multiplica_inversa_B_por_A = multiplicar_duas_matrizes(inversa_matriz_B, coeficientes_restricoes)
        coluna_pivo = []
        for i in range(len(multiplica_inversa_B_por_A)):
            coluna_pivo.append([multiplica_inversa_B_por_A[i][guarda_indice_entrar]])
        #CALCULA O MENOR NÚMERO RESULTANTE DA DIVISAO ENTRE TERMOS INDEPENDENTES E COLUNA PIVO
        auxiliar = 9999999999999
        guarda_indice_sair = 0
        for i in range(len(coluna_pivo)):
            if coluna_pivo[i][0] != 0:
                divisao_termos_pivo = termos_independentes[i][0] / coluna_pivo[i][0]
                if divisao_termos_pivo < auxiliar:
                    auxiliar = divisao_termos_pivo
                    guarda_indice_sair = i
        if modo == 2:
            print('\nÍndice que sai %d' %guarda_indice_sair)
        passo_tres(inversa_matriz_B, qtd_variaveis, identidade, termos_independentes, guarda_indice_entrar, guarda_indice_sair, matriz_variaveis_base, matriz_B, coluna_pivo, coeficientes_variaveis_base, coeficientes_funcao_objetivo, coeficientes_restricoes, modo, maximizacao)


def passo_tres(inversa_matriz_B, qtd_variaveis, identidade, termos_independentes, guarda_indice_entrar, guarda_indice_sair, matriz_variaveis_base, matriz_B, coluna_pivo, coeficientes_variaveis_base, coeficientes_funcao_objetivo, coeficientes_restricoes, modo, maximizacao):
    #SUBSTITUI O ÍNDICE ANTIGO PELO NOVO ÍNDICE
    matriz_variaveis_base[guarda_indice_sair][0] = guarda_indice_entrar
    for i in range(len(coluna_pivo)):
        matriz_B[i][guarda_indice_sair] = coluna_pivo[i][0]
    if modo == 2:
        mostrar_matriz(matriz_B, '\nA matriz B é:')

    #INVERTE A MATRIZ B
    inversa_matriz_B = inverter_matriz(matriz_B)
    if modo == 2:
        mostrar_matriz(inversa_matriz_B,'\nA inversa da matriz B é: ')
    #SUBSTITUINDO VALOR EM C_B
    coeficientes_variaveis_base[0][guarda_indice_sair] = coeficientes_funcao_objetivo[0][guarda_indice_entrar]
    if modo == 2:
        mostrar_matriz(coeficientes_variaveis_base,'\nC_B atualizada: ')
    #ATUALIZANO -C
    resultado = multiplicar_duas_matrizes(coeficientes_variaveis_base, inversa_matriz_B)
    if modo == 2:
        mostrar_matriz(resultado, '\nC_B * B-1')
        mostrar_matriz(coeficientes_restricoes, '\nMatriz A')
    resultado = multiplicar_duas_matrizes(resultado, coeficientes_restricoes)
    if modo == 2:
        mostrar_matriz(resultado, '\nC_B * B-1 * A')
    coeficientes_funcao_objetivo_negativo = subtrair_duas_matrizes(resultado, coeficientes_funcao_objetivo)

    if modo == 2:
        mostrar_matriz(coeficientes_funcao_objetivo_negativo, '\nMatriz -C atualizada')
        mostrar_matriz(coeficientes_variaveis_base, '\nMatriz C_B atualizada')
    passo_dois(qtd_variaveis, identidade, coeficientes_funcao_objetivo, termos_independentes, coeficientes_funcao_objetivo_negativo, matriz_variaveis_base, matriz_B, coeficientes_variaveis_base, coeficientes_restricoes, modo, maximizacao)

def finalizacao(inversa_matriz_B, termos_independentes, coeficientes_variaveis_base, coeficientes_restricoes, qtd_variaveis, matriz_variaveis_base, maximizacao):
    solucao_base = multiplicar_duas_matrizes(inversa_matriz_B, termos_independentes)
    solucao_simplex = []
    for i in range(qtd_variaveis):
        solucao_simplex.append([0.0])
    for i in range(len(matriz_variaveis_base)):
        if matriz_variaveis_base[i][0] < qtd_variaveis:
            solucao_simplex[matriz_variaveis_base[i][0]][0] = solucao_base[i]
    mostrar_matriz(solucao_simplex, '\nA matriz solução do Simplex é: ')
    Z = multiplicar_duas_matrizes(coeficientes_variaveis_base, solucao_base)
    print("\nZ = {}".format(Z[0][0] if maximizacao == 1 else -Z[0][0]))
    if qtd_variaveis == 2:
        solucao_grafica(coeficientes_restricoes, termos_independentes, solucao_simplex)

def solucao_grafica(coeficientes_restricoes, termos_independentes, solucao_simplex):
    for i in range(len(coeficientes_restricoes)):
        ponto_y = termos_independentes[i][0] / coeficientes_restricoes[i][1]
        ponto_x = termos_independentes[i][0] / coeficientes_restricoes[i][0]
        plt.plot([ponto_x, 0], [0, ponto_y])
    plt.plot([solucao_simplex[0][0]], [solucao_simplex[1][0]], 'ro')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()

menu()
