import copy
import time

def print_board(board):
    for i in range(3):
        print(f" {board[i*3]} | {board[i*3+1]} | {board[i*3+2]} ")
        if i < 2:
            print("-----------")

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[i] == player for i in line) for line in win_conditions)

def check_draw(board):
    return ' ' not in board

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, is_maximizing, ai_player, human_player, count):
    count[0] += 1
    if check_win(board, ai_player):
        return 1
    if check_win(board, human_player):
        return -1
    if check_draw(board):
        return 0

    best_score = -float('inf') if is_maximizing else float('inf')
    for move in get_available_moves(board):
        new_board = copy.deepcopy(board)
        new_board[move] = ai_player if is_maximizing else human_player
        score = minimax(new_board, not is_maximizing, ai_player, human_player, count)
        if is_maximizing:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)
    return best_score

def alphabeta(board, is_maximizing, ai_player, human_player, alpha, beta, count):
    count[0] += 1
    if check_win(board, ai_player):
        return 1
    if check_win(board, human_player):
        return -1
    if check_draw(board):
        return 0

    best_score = -float('inf') if is_maximizing else float('inf')
    for move in get_available_moves(board):
        new_board = copy.deepcopy(board)
        new_board[move] = ai_player if is_maximizing else human_player
        score = alphabeta(new_board, not is_maximizing, ai_player, human_player, alpha, beta, count)
        
        if is_maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)
        
        if beta <= alpha:
            break
    return best_score

def compare_algorithms():
    test_cases = [
        ("Empty Board", [' ']*9),
        ("Early Game", ['X', 'O', 'X', ' ', ' ', ' ', ' ', ' ', ' ']),
        ("Mid Game", ['X', 'O', 'X', 'O', 'X', ' ', ' ', ' ', 'O']),
        ("End Game", ['X', 'O', 'X', 'O', 'X', 'O', ' ', ' ', ' '])
    ]

    print("\n" + "="*50)
    print("Performance Comparison: Minimax vs Alpha-Beta Pruning")
    print("="*50 + "\n")

    for name, board in test_cases:
        print(f"\nTest Case: {name}")
        print_board(board)
        
        # Minimax
        start_time = time.time()
        count = [0]
        _ = minimax(copy.deepcopy(board), True, 'X', 'O', count)
        minimax_time = time.time() - start_time
        minimax_nodes = count[0]

        # Alpha-Beta
        start_time = time.time()
        count = [0]
        _ = alphabeta(copy.deepcopy(board), True, 'X', 'O', -float('inf'), float('inf'), count)
        ab_time = time.time() - start_time
        ab_nodes = count[0]

        # Print results
        print(f"Minimax:  {minimax_nodes:6d} nodes  |  {minimax_time:.4f} seconds")
        print(f"AlphaBeta: {ab_nodes:6d} nodes  |  {ab_time:.4f} seconds")
        print(f"Improvement: {(1 - ab_nodes/minimax_nodes)*100:.1f}% node reduction")
        print("-"*50)

def play_game():
    board = [' ']*9
    ai_player = 'X'
    human_player = 'O'
    algorithm = input("Choose algorithm (M/A): ").upper()
    
    while True:
        print_board(board)
        
        # Human move
        try:
            move = int(input("Your move (1-9): ")) - 1
            if move not in get_available_moves(board):
                print("Invalid move!")
                continue
        except ValueError:
            print("Enter a number!")
            continue
            
        board[move] = human_player
        
        if check_win(board, human_player):
            print_board(board)
            print("You win!")
            break
            
        if check_draw(board):
            print_board(board)
            print("Draw!")
            break
            
        # AI move
        start_time = time.time()
        count = [0]
        if algorithm == 'M':
            move = max(get_available_moves(board), 
                      key=lambda m: minimax(play_move(board, m, ai_player), 
                                           False, ai_player, human_player, count))
        else:
            move = max(get_available_moves(board), 
                      key=lambda m: alphabeta(play_move(board, m, ai_player), 
                                            False, ai_player, human_player, 
                                            -float('inf'), float('inf'), count))
        board[move] = ai_player
        print(f"AI evaluated {count[0]} nodes in {time.time()-start_time:.2f}s")
        
        if check_win(board, ai_player):
            print_board(board)
            print("AI wins!")
            break
            
        if check_draw(board):
            print_board(board)
            print("Draw!")
            break

def play_move(board, move, player):
    new_board = copy.deepcopy(board)
    new_board[move] = player
    return new_board

if __name__ == "__main__":
    compare_algorithms()
    
    while True:
        play_game()
        if input("Play again? (y/n): ").lower() != 'y':
            break