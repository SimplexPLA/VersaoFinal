def mostrar_matriz(matriz, mensagem):
    print(mensagem)
    for i in matriz:
        for j in i:
            print(j, end=" ")
        print()


def juntar_matriz(arrayA, arrayB):
    for a, b in zip(arrayA, arrayB):
        yield [*a, *b]


def gerar_matriz_identidade(ordem):
    identidade = []
    for i in range(ordem):
        aux = []
        for j in range(ordem):
            aux.append(1 if i == j else 0)
        identidade.append(aux)
    return identidade


#MULTIPLICA DUAS MATRIZES
def multiplicar_duas_matrizes(matriz_a, matriz_b):
    qtd_linhas_a, qtd_colunas_a = len(matriz_a), len(matriz_a[0])
    qtd_linhas_b, qtd_colunas_b = len(matriz_b), len(matriz_b[0])

    if qtd_colunas_a == qtd_linhas_b:
        matriz_multiplicada = []
        for i in range(qtd_linhas_a):
            matriz_multiplicada.append([])
            for j in range(qtd_colunas_b):
                matriz_multiplicada[i].append(0)
                for k in range(qtd_linhas_b):
                    matriz_multiplicada[i][j] += matriz_a[i][k] * matriz_b[k][j]

        return matriz_multiplicada
    else:
        return False

#SUBTRAI DUAS MATRIZES
def subtrair_duas_matrizes(matriz_a, matriz_b):
    matriz_subtraida = []
    for i in range(len(matriz_a)):
        matriz_subtraida.append([])
        for j in range(len(matriz_a[0])):
            matriz_subtraida[i].append(matriz_a[i][j] - matriz_b[i][j])
    return matriz_subtraida


#CALCULA MATRIZ INVERSA
def matriz_transposta(matriz):
    return list(map(list,zip(*matriz)))

def remover_linha_coluna(matriz,l,c):
    return [linha[:c] + linha[c+1:] for linha in matriz[:l]+matriz[l+1:]]

def pegar_determinante_matriz(matriz):
    #CASO BASE PARA MATRIZ 2x2
    if len(matriz) == 2:
        return matriz[0][0]*matriz[1][1]-matriz[0][1]*matriz[1][0]

    determinante = 0
    for c in range(len(matriz)):
        determinante += ((-1)**c)*matriz[0][c]*pegar_determinante_matriz(remover_linha_coluna(matriz,0,c))
    return determinante

def inverter_matriz(matriz):
    determinante = pegar_determinante_matriz(matriz)
    #CASO ESPECIAL PARA MATRIZ 2x2
    if len(matriz) == 2:
        return [[matriz[1][1]/determinante, -1*matriz[0][1]/determinante],
                [-1*matriz[1][0]/determinante, matriz[0][0]/determinante]]

    #ENCONTRAR MATRIZ DE COFATORES
    cofatores = []
    for l in range(len(matriz)):
        linha_cofator = []
        for c in range(len(matriz)):
            matriz_menor = remover_linha_coluna(matriz,l,c)
            linha_cofator.append(((-1)**(l+c)) * pegar_determinante_matriz(matriz_menor) / determinante)
        cofatores.append(linha_cofator)
    cofatores = matriz_transposta(cofatores)
    return cofatores

