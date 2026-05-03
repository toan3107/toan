from functools import lru_cache

X = "X"
O = "O"
EMPTY = " "

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

MOVE_ORDER = (4, 0, 2, 6, 8, 1, 3, 5, 7)


def opponent(player):
    return O if player == X else X


def print_board(board):
    cells = [value if value != EMPTY else str(index + 1) for index, value in enumerate(board)]
    print()
    print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]} ")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]} ")
    print()


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def terminal_value(board):
    result = winner(board)
    if result == X:
        return 1
    if result == O:
        return -1
    if EMPTY not in board:
        return 0
    return None


def legal_moves(board):
    return [move for move in MOVE_ORDER if board[move] == EMPTY]


def make_move(board, move, player):
    new_board = list(board)
    new_board[move] = player
    return tuple(new_board)


@lru_cache(maxsize=None)
def minimax(board, turn):
    value = terminal_value(board)
    if value is not None:
        return value

    next_turn = opponent(turn)
    scores = [minimax(make_move(board, move, turn), next_turn) for move in legal_moves(board)]

    if turn == X:
        return max(scores)
    return min(scores)


def best_move(board, player):
    moves = legal_moves(board)
    next_turn = opponent(player)
    choices = [(move, minimax(make_move(board, move, player), next_turn)) for move in moves]

    if player == X:
        return max(choices, key=lambda item: item[1])
    return min(choices, key=lambda item: item[1])


def choose_symbol():
    while True:
        symbol = input("Chọn quân của bạn (X/O): ").strip().upper()
        if symbol in (X, O):
            return symbol
        print("Vui lòng nhập X hoặc O.")


def read_human_move(board):
    while True:
        raw = input("Nhập ô muốn đi (1-9): ").strip()
        if not raw.isdigit():
            print("Vui lòng nhập một số từ 1 đến 9.")
            continue

        move = int(raw) - 1
        if move < 0 or move > 8:
            print("Ô phải nằm trong khoảng từ 1 đến 9.")
            continue

        if board[move] != EMPTY:
            print("Ô này đã có quân, hãy chọn ô khác.")
            continue

        return move


def print_result(board, human, computer):
    result = winner(board)
    final_value = terminal_value(board)

    if result == human:
        print("Kết quả: Bạn thắng.")
    elif result == computer:
        print("Kết quả: Máy thắng.")
    else:
        print("Kết quả: Hòa.")

    print(f"Giá trị đánh giá cuối: {final_value}")


def run_game():
    board = tuple([EMPTY] * 9)
    human = choose_symbol()
    computer = opponent(human)
    turn = X

    print()
    print(f"Bạn là {human}. Máy là {computer}.")
    print("X là MAX, O là MIN.")

    empty_best_move, empty_value = best_move(board, X)
    print(f"Nước đi tốt nhất từ bàn cờ rỗng cho X: ô {empty_best_move + 1}")
    print(f"Giá trị Minimax từ bàn cờ rỗng: {empty_value}")

    while terminal_value(board) is None:
        print_board(board)

        if turn == human:
            move = read_human_move(board)
            board = make_move(board, move, human)
        else:
            move, value = best_move(board, computer)
            row = move // 3 + 1
            col = move % 3 + 1
            print(f"Nước đi tốt nhất của máy: ô {move + 1} (hàng {row}, cột {col})")
            print(f"Giá trị Minimax: {value}")
            board = make_move(board, move, computer)

        turn = opponent(turn)

    print_board(board)
    print_result(board, human, computer)


run_game()
