import random
import time
import sys

# Função de loading
def loading():
    total = 100
    for i in range(0, total + 1):
        time.sleep(0.03)  
        percent = i * 100 // total
        color = "\033[31m" if percent <= 30 else ("\033[33m" if percent <= 70 else "\033[32m")
        progress_bar = "\rProgresso: {}% [{}{}]".format(percent, "=" * (i // 5), " " * ((total - i) // 5))
        sys.stdout.write(color + progress_bar + "\033[0m")
        sys.stdout.flush()
    print("\nConcluído!")

# Configurações dos navios
CONFIGURACAO = {
    'destroyer': 3,
    'porta-avioes': 5,
    'submarino': 2,
    'torpedeiro': 3,
    'cruzador': 2,
    'couracado': 4
}

# Frotas de cada país
PAISES = {
    'Brasil': {
        'cruzador': 1,
        'torpedeiro': 2,
        'destroyer': 1,
        'couracado': 1,
        'porta-avioes': 1
    },
    'França': {
        'cruzador': 3,
        'porta-avioes': 1,
        'destroyer': 1,
        'submarino': 1,
        'couracado': 1
    },
    'Austrália': {
        'couracado': 1,
        'cruzador': 3,
        'submarino': 1,
        'porta-avioes': 1,
        'torpedeiro': 1
    },
    'Rússia': {
        'cruzador': 1,
        'porta-avioes': 1,
        'couracado': 2,
        'destroyer': 1,
        'submarino': 1
    },
    'Japão': {
        'torpedeiro': 2,
        'cruzador': 1,
        'destroyer': 2,
        'couracado': 1,
        'submarino': 1
    }
}

# Cores para o terminal
CORES = {
    'reset': '\u001b[0m',
    'red': '\u001b[31m',
    'black': '\u001b[30m',
    'green': '\u001b[32m',
    'yellow': '\u001b[33m',
    'blue': '\u001b[34m',
    'magenta': '\u001b[35m',
    'cyan': '\u001b[36m',
    'white': '\u001b[37m'
}

# Símbolos para o tabuleiro
AGUA = '▓▓▓'
ATINGIDO = '▓▓▓'
NAVIO = '▓▓▓'

# Define os códigos de escape ANSI para cores
COR_AGUA = '\033[94m'  # Azul
COR_ATINGIDO = '\033[91m'  # Vermelho
COR_NAVIO = '\u001b[32m'  # Verde

# Define os símbolos coloridos para representar os estados do tabuleiro
AGUA_COLORIDA = COR_AGUA + AGUA + CORES['reset']
NAVIO_COLORIDO = COR_NAVIO + NAVIO + CORES['reset']
ATINGIDO_COLORIDO = COR_ATINGIDO + ATINGIDO + CORES['reset']

# Função para imprimir o tabuleiro
N = 10

def cria_mapa(N):
    mapa = []
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append('')
        mapa.append(linha)
    return mapa

def imprimir_mapa(mapa, ocultar_navios=True):
    global N
    tamanho_mapa = len(mapa)
    print("  ", end="")
    for i in range(tamanho_mapa):
        print(chr(65+i).center(3), end="")
    print()
    for j in range(tamanho_mapa):
        print(str(j+1).rjust(2), end="")
        for i in range(tamanho_mapa):
            if not ocultar_navios or (ocultar_navios and mapa[i][j] == '' or mapa[i][j] == NAVIO_COLORIDO or mapa[i][j] == ATINGIDO_COLORIDO):
                print(mapa[i][j].rjust(3), end="")
            else:
                print(AGUA_COLORIDA.rjust(3), end="")
        print(str(j+1).rjust(2))
    print("  ", end="")
    for i in range(tamanho_mapa):
        print(chr(65+i).center(3), end="")
    print()

def turno_jogador(mapa, mapa_pc):
    global N
    while True:
        tiro = input("Escolha um local para atacar (por exemplo, A1): ").upper()
        linha = ord(tiro[0]) - ord('A')
        coluna = int(tiro[1:]) - 1
        if linha < 0 or linha >= N or coluna < 0 or coluna >= N:
            print("Por favor, escolha uma coordenada válida!")
            continue
        if mapa_pc[linha][coluna] == AGUA_COLORIDA or mapa_pc[linha][coluna] == ATINGIDO_COLORIDO:
            print("Você já atirou nesse local! Tente novamente.")
            continue
        if mapa_pc[linha][coluna] == NAVIO_COLORIDO:
            print("BOOOMM!! Acertou um navio!")
            mapa_pc[linha][coluna] = ATINGIDO_COLORIDO
            imprimir_mapa(mapa_pc, True)  # Atualiza o mapa do computador após o ataque
            break
        else:
            print("SPLASHH!! Água!")
            mapa_pc[linha][coluna] = AGUA_COLORIDA
            imprimir_mapa(mapa_pc, True)  # Atualiza o mapa do computador após o ataque
            break

def turno_computador(mapa, mapa_jogador):
    global N
    while True:
        linha = random.randint(0, N - 1)
        coluna = random.randint(0, N - 1)
        if mapa[linha][coluna] == '':
            print(f"O computador atacou o local {chr(linha + ord('A'))}{coluna + 1}")
            if mapa_jogador[linha][coluna] == NAVIO_COLORIDO:
                print("BOOOM!! O computador acertou um dos seus navios!")
                mapa_jogador[linha][coluna] = ATINGIDO_COLORIDO
            else:
                print("SPLASHH!!!! O computador acertou a água!")
                mapa_jogador[linha][coluna] = AGUA_COLORIDA
            imprimir_mapa(mapa_jogador, False)  # Atualiza o mapa do jogador após o ataque do computador
            break

def foi_derrotado(mapa):
    for linha in mapa:
        if NAVIO_COLORIDO in linha:
            return False
    return True

def batalha(mapa_jogador, mapa_pc):
    while True:
        turno_jogador(mapa_jogador, mapa_pc)
        if foi_derrotado(mapa_pc):
            return "Jogador"
        turno_computador(mapa_pc, mapa_jogador)
        if foi_derrotado(mapa_jogador):
            return "Computador"

mapa1 = cria_mapa(N)
imprimir_mapa(mapa1)

mapa_jogador = cria_mapa(N)
imprimir_mapa(mapa_jogador)

print('\n- - - - - - - - - - - - - - - - - - - - - - - - -')
print('|                                              |')
print('|              JOGO BATALHA NAVAL              |')
print('|                                              |')
print('- - - - - - - - - - - - - - - - - - - - - - - - -')
print('\n----> Felipe Mendes e Gabriel Crescenzo e Arthur Soria\n')

terminal_paises = ''
for nacao, navios in PAISES.items():
    terminal_paises += f'{nacao}:\n'
    for navio, quantidade in navios.items():
        terminal_paises += f'   > {quantidade} {navio}\n'
    terminal_paises += '\n' 
print(terminal_paises)

paises = ['Brasil', 'Austrália', 'Japão', 'Rússia', 'França']
while True:
    pais_jogador = input('Escolha o país que você deseja jogar: ').capitalize()
    if pais_jogador in paises:
        print('\n- Parabéns! Você escolheu ' + pais_jogador + '.')
        paises.remove(pais_jogador)
        pais_computador = random.choice(paises)
        print('- O computador escolheu ' + pais_computador + '.\n')
        imprimir_mapa(mapa_jogador, True)
        imprimir_mapa(mapa1)
        break
    else:
        print('Escolha um país válido!\n')

print("Você escolheu a nação {}".format(pais_jogador))
print("Frota do país selecionado:")
for navio, quantidade in PAISES[pais_jogador].items():
    print(f"   > {quantidade} {navio}")

def posicao_suporta(mapa, blocos, linha, coluna, orientacao):
    tamanho_mapa = len(mapa)
    if orientacao == 'h':
        if linha + blocos > tamanho_mapa:
            return False
        for i in range(blocos):
            if mapa[linha + i][coluna] != '':
                return False
    else:
        if coluna + blocos > tamanho_mapa:
            return False
        for i in range(blocos):
            if mapa[linha][coluna + i] != '':
                return False
    return True

def aloca_navios(mapa, blocos):
    tamanho_mapa = len(mapa)
    for tipo_navio, quantidade in blocos.items():
        navios_restantes = quantidade
        print(f"Você deve alocar: {quantidade} {tipo_navio}")
        for _ in range(quantidade):
            navio_alocado = False
            while not navio_alocado:
                imprimir_mapa(mapa)
                print(f"Navios restantes para alocar: {navios_restantes}")
                coordenada = input(f"Digite a coordenada para alocar o {tipo_navio} (por exemplo, A1): ").upper()
                orientacao = input("Digite a orientação (h para horizontal, v para vertical): ").lower()
                linha = ord(coordenada[0]) - ord('A')
                coluna = int(coordenada[1:]) - 1
                tamanho_navio = 1  
                if tipo_navio == 'porta-avioes':
                    tamanho_navio = 5
                elif tipo_navio == 'couracado':
                    tamanho_navio = 4
                elif tipo_navio == 'cruzador':
                    tamanho_navio = 2
                elif tipo_navio == 'destroyer':
                    tamanho_navio = 3
                elif tipo_navio == 'torpedeiro':
                    tamanho_navio = 3
                elif tipo_navio == 'submarino' :
                    tamanho_navio = 2
                if posicao_suporta(mapa, tamanho_navio, linha, coluna, orientacao):
                    if orientacao == 'h':
                        for i in range(linha, linha + tamanho_navio):
                            mapa[i][coluna] = NAVIO_COLORIDO
                    elif orientacao == 'v':
                        for j in range(coluna, coluna + tamanho_navio):
                            mapa[linha][j] = NAVIO_COLORIDO
                    navios_restantes -= 1
                    navio_alocado = True
                else: 
                    print("Posição inválida. Tente novamente. ")
            print("Navio alocado com sucesso! \n")
        imprimir_mapa(mapa)

def aloca_navios_computador(mapa, pais):
    frota_pais = PAISES[pais]
    for tipo_navio, quantidade in frota_pais.items():
        navios_restantes = quantidade
        for _ in range(quantidade):
            navio_alocado = False
            while not navio_alocado:
                linha = random.randint(0, len(mapa) - 1)
                coluna = random.randint(0, len(mapa) - 1)
                orientacao = random.choice(['h', 'v'])
                tamanho_navio = CONFIGURACAO[tipo_navio]
                if posicao_suporta(mapa, tamanho_navio, linha, coluna, orientacao):
                    if orientacao == 'h':
                        for i in range(linha, linha + tamanho_navio):
                            mapa[i][coluna] = NAVIO_COLORIDO
                    elif orientacao == 'v':
                        for j in range(coluna, coluna + tamanho_navio):
                            mapa[linha][j] = NAVIO_COLORIDO
                    navios_restantes -= 1
                    navio_alocado = True
                else: 
                    continue

N = 10
mapa_jogador = [[''] * N for _ in range(N)]
aloca_navios(mapa_jogador, PAISES[pais_jogador])  

N = 10
mapa_pc = [[''] * N for _ in range(N)]
aloca_navios_computador(mapa_pc, pais_computador)

while True:
    resultado = batalha(mapa_jogador, mapa_pc)
    if resultado == "Jogador":
        print("\nParabéns! Você destruiu todos os navios do computador.")
    else:
        print("\nO computador destruiu todos os seus navios. Game over.")

    jogar_novamente = input("Deseja jogar novamente? (s/n): ")
    if jogar_novamente.lower() != 's':
        break