import chess
import random
import sys
import time
SEARCH_DEPTH = 3
def evaluate_board(board):
    """
    Scores the board position. Positive values favor White, negative favor Black.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  
    }

    for piece_type, value in piece_values.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    return score
#minmax algo 
def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Recursive function to find the best move using minimax with alpha-beta pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move

def find_best_move(board):
    is_maximizing_player = board.turn == chess.WHITE
    _, best_move = minimax(board, SEARCH_DEPTH, -float('inf'), float('inf'), is_maximizing_player)
    
    return best_move

#logic
def get_player_move(board):
    """
    Gets a valid UCI move from the human player.
    """
    while True:
        try:
            move_str = input("Enter your move (e.g., e2e4): ").strip().lower()
            if move_str == 'quit':
                return None
            move = board.parse_uci(move_str)
            if move in board.legal_moves:
                return move
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid move format. Please use UCI (e.g., a1h8).")

def play_game():
    """
    Main function to run a chess game.
    """
    board = chess.Board()

    print("Chess game started!")
    print(f"You are playing as White against a level {SEARCH_DEPTH} bot.")
    print("Type 'quit' to exit the game.")
    print("-" * 25)

    while not board.is_game_over():
        print("\n" + board.unicode())

        if board.turn == chess.WHITE:
            print("Your turn (White):")
            player_move = get_player_move(board)
            if player_move is None:
                break
            board.push(player_move)
        else:
            print("Computer's turn (Black)...")
            start_time = time.time()
            ai_move = find_best_move(board)
            end_time = time.time()

            if ai_move:
                board.push(ai_move)
                print(f"Computer played: {ai_move.uci()} (took {end_time - start_time:.2f} seconds)")
            else:
                print("The AI could not find a move. This shouldn't happen.")
                break

    print("\n" + board.unicode())
    print("-" * 25)

    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        print(f"Checkmate! {winner} wins!")
    elif board.is_stalemate():
        print("Stalemate! Game is a draw.")
    else:
        print("Game over.")


if __name__ == "__main__":
    play_game()