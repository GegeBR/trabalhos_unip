import heapq  # Importa a biblioteca heapq para utilizar fila de prioridade (min-heap)

####################################################################################
# Função que lê o tabuleiro de um arquivo texto
####################################################################################

def ler_tabuleiro(nome_arquivo):
    try:
        # Abre o arquivo e lê todas as linhas, removendo quebras de linha
        with open(nome_arquivo, 'r') as f:
            linhas = f.read().splitlines()
        
        # Verifica se o arquivo está vazio
        if not linhas:
            raise ValueError("Arquivo vazio")

        # Tenta converter a primeira linha para inteiro, que representa o tamanho do tabuleiro (n x n)
        n = int(linhas[0])

        # Verifica se o número de linhas subsequentes é suficiente para formar o tabuleiro
        if len(linhas) < n + 1:
            raise ValueError("Número de linhas insuficiente")

        # Constrói a grade (tabuleiro), convertendo todas as letras para minúsculas
        # Isso garante que 'T' maiúsculo também seja tratado como 't'
        grid = [list(linha.lower()) for linha in linhas[1:n+1]]

        # Valida cada linha do tabuleiro
        for linha in grid:
            # Verifica se a linha tem exatamente n caracteres
            if len(linha) != n:
                raise ValueError("Linha com tamanho incorreto")
            # Verifica se cada caractere é válido: apenas 't' (torre) ou '0' (caminho livre) são permitidos
            for c in linha:
                if c not in ('t', '0'):
                    raise ValueError("Caracteres inválidos")

        # Retorna o tamanho e o tabuleiro processado
        return n, grid

    except Exception:
        # Caso qualquer erro ocorra, exibe uma mensagem genérica e encerra o programa
        print("Arquivo de entrada fora do padrão!")
        exit(1)


####################################################################################
# Bloco principal do programa
####################################################################################
if __name__ == "__main__":
    n, tabuleiro = ler_tabuleiro("in.txt")  # Lê o tabuleiro do arquivo "in.txt"
    for linha in tabuleiro:  # Imprime o tabuleiro lido
        print(linha)

####################################################################################
# Função que calcula o mapa de dano com base na posição das torres ('t')
####################################################################################
def calcular_mapa_de_dano(grid, n):
    dano = [[0 for _ in range(n)] for _ in range(n)]  # Inicializa a matriz de dano com zeros

    # Direções ao redor de uma célula (8 vizinhos)
    direcoes = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1), (1, 0),  (1, 1)]

    for i in range(n):
        for j in range(n):
            if grid[i][j].lower() == 't':  # Se a célula contém uma torre
                dano[i][j] = None  # A própria torre é marcada como intransitável
                for dx, dy in direcoes:  # Para cada direção adjacente
                    ni, nj = i + dx, j + dy
                    # Se estiver dentro dos limites e não for uma torre
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] != 't':
                        dano[ni][nj] += 10  # A célula adjacente recebe +10 de dano
    return dano  # Retorna o mapa de dano

# Imprime o mapa de dano
print("\nMapa de Dano:")
mapa_dano = calcular_mapa_de_dano(tabuleiro, n)
for linha in mapa_dano:
    print(linha)

####################################################################################
# Função que encontra o caminho de menor dano usando Dijkstra (com heap)
####################################################################################
def encontrar_menor_dano(grid, mapa_dano, n):
    # Direções possíveis (sem diagonais)
    direcoes = {
        'N': (-1, 0),
        'S': (1, 0),
        'L': (0, 1),
        'O': (0, -1)
    }

    melhor_dano = [[float('inf')] * n for _ in range(n)]  # Inicializa dano mínimo como infinito
    fila = []  # Fila de prioridade (heap)

    heapq.heappush(fila, (0, 0, 0, ""))  # Começa do canto superior esquerdo (0,0), sem dano e sem caminho

    while fila:
        dano, i, j, caminho = heapq.heappop(fila)  # Pega o próximo estado com menor dano

        if i == n - 1 and j == n - 1:  # Chegou no destino (canto inferior direito)
            return caminho, dano  # Retorna o caminho e o dano total acumulado

        for direcao, (di, dj) in direcoes.items():  # Tenta mover para cada direção
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and mapa_dano[ni][nj] is not None:
                novo_dano = dano + mapa_dano[ni][nj]  # Calcula novo dano acumulado
                if novo_dano < melhor_dano[ni][nj]:  # Se for melhor que o anterior
                    melhor_dano[ni][nj] = novo_dano  # Atualiza
                    heapq.heappush(fila, (novo_dano, ni, nj, caminho + direcao))  # Enfileira novo estado

    return None, float('inf')  # Se não encontrar caminho, retorna infinito

####################################################################################
# Chamada da função de busca e saída dos resultados
####################################################################################
caminho, dano = encontrar_menor_dano(tabuleiro, mapa_dano, n)

print("\nMelhor Caminho:")
print(caminho)
print("Dano total sofrido:", dano)

# Escreve o caminho e o dano em um arquivo de saída
with open("out.txt", "w") as f:
    f.write("Melhor caminho possível para o jogador: " + caminho + "\n")
    f.write("Menor dano sofrido: " + str(dano))

####################################################################################
# Exibe o caminho visualmente no tabuleiro
####################################################################################
print("\nCaminho visual no tabuleiro:")

i = j = 0
tabuleiro_visual = [row.copy() for row in tabuleiro]  # Copia o tabuleiro original
tabuleiro_visual[i][j] = '*'  # Marca o ponto de partida

# Percorre o caminho e marca com '*'
for direcao in caminho:
    if direcao == 'N': i -= 1
    elif direcao == 'S': i += 1
    elif direcao == 'L': j += 1
    elif direcao == 'O': j -= 1
    tabuleiro_visual[i][j] = '*'

# Imprime o tabuleiro com o caminho traçado
for linha in tabuleiro_visual:
    print(''.join(linha))