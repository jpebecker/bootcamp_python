#jogo da velha = tic tac toe
import random
table = [
    ["-", "0", "1", "2"],
    ["0", " ", " ", " "],
    ["1", " ", " ", " "],
    ["2", " ", " ", " "],
]
def show_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 15)
def check_winner(board, player):
    for row in range(1, 4):#linha
        if all(board[row][col] == player for col in range(1, 4)):
            return True
    for col in range(1, 4):#coluna
        if all(board[row][col] == player for row in range(1, 4)):
            return True
    if all(board[i][i] == player for i in range(1, 4)): #diagonal principal
        return True
    if all(board[i][4 - i] == player for i in range(1, 4)): #diagonal secundaria
        return True
    return False

def draw(board):
    for row in range(1, 4):
        for col in range(1, 4):
            if board[row][col] == " ":
                return False
    return True

def reset(board): #limpa o tabuleiro
    for row in range(1, 4):
        for col in range(1, 4):
            board[row][col] = " "

def get_true_pos(player): #verifica se a posicao digitada é valida
    while True:
        try:
            row = min(max(int(input(f'Digite a LINHA da peça "{player}": ')) + 1, 1), 3)
            col = min(max(int(input(f'Digite a COLUNA da peça "{player}": ')) + 1, 1), 3)
            return [row, col]
        except ValueError:
            print("Valor inválido! Digite números inteiros.")

#bot movement
def bot_move(board, bot_symbol, player_symbol):
    #tenta vencer
    for r in range(1, 4):
        for c in range(1, 4):
            if board[r][c] == " ":
                board[r][c] = bot_symbol
                if check_winner(board, bot_symbol):
                    return (r, c)
                board[r][c] = " "

    #bloqueia o jogador se nao conseguir vencer de imediato
    for r in range(1, 4):
        for c in range(1, 4):
            if board[r][c] == " ":
                board[r][c] = player_symbol
                if check_winner(board, player_symbol):
                    board[r][c] = " "
                    return (r, c)
                board[r][c] = " "

    #movimento aleatorio caso os dois ultimos sejam falso
    options = [
        (r, c)
        for r in range(1, 4)
        for c in range(1, 4)
        if board[r][c] == " "
    ]
    return random.choice(options)

#gamemode
print("=== JOGO DA VELHA ===")
print("1 - Jogador vs Jogador")
print("2 - Jogador vs Bot")
mode = input("Insira o modo de jogo (1 ou 2): ")

players = ['X', 'O']
actual_player = random.choice(players)
Win = False

while not Win:
    if draw(table):
        print('Jogo deu Velha. Resetando tabuleiro...\n')
        reset(table)
        continue

    show_board(table)

    if mode == "2" and actual_player == 'O':
        print('Bot turn:')
        entry_pos = bot_move(table, 'O', 'X')
    else:
        entry_pos = get_true_pos(actual_player)

    print(f'Posicionando peça em [{entry_pos[0]-1},{entry_pos[1]-1}]')

    if table[entry_pos[0]][entry_pos[1]] == " ":
        table[entry_pos[0]][entry_pos[1]] = actual_player
        Win = check_winner(table, actual_player)
        if not Win:
            actual_player = players[players.index(actual_player) - 1]  # alterna jogador
    else:
        print('Slot já ocupado. Tente outra posição.')

show_board(table)
print(f'O jogador de "{actual_player}" ganhou!')