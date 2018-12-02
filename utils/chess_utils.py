import chess
from typeguard import typechecked

from utils.macros import Macros


@typechecked
def evaluate_game_state(board: chess.Board, possible: bool) -> float:
    if board.is_checkmate():
        if possible:
            return Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
        return Macros.BOARD_CHECKMATE_VALUE

    if board.is_stalemate() or board.is_insufficient_material():
        return Macros.BOARD_STALEMATE_VALUE

    if board.is_check():
        if not possible:
            return Macros.BOARD_CHECK_VALUE

    return 0


@typechecked
def evaluate_board_piece_score(board: chess.Board, player_color: bool) -> (float, float, float):
    opponent, player = 0, 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == player_color:
                player += Macros.PIECE_VALUES[piece.piece_type] / Macros.BOARD_INTERVAL_FIX
            else:
                opponent += Macros.PIECE_VALUES[piece.piece_type] / Macros.BOARD_INTERVAL_FIX

    return player - opponent, player, opponent


@typechecked
def get_board_attack_total_value(board: chess.Board) -> float:
    total_value = 0

    for move in board.legal_moves:
        captured_piece = board.is_capture(move)
        score_before = evaluate_board_piece_score(board, not board.turn)[1] if captured_piece else 0

        board.push_uci(str(move))
        if captured_piece:
            total_value += score_before - evaluate_board_piece_score(board, board.turn)[1]

        total_value += evaluate_game_state(board, True)
        board.pop()

    return total_value


@typechecked
def evaluate_board_attack_score(board: chess.Board) -> (float, float, float):
    opponent = get_board_attack_total_value(board)
    board.turn = not board.turn
    player = get_board_attack_total_value(board)
    board.turn = not board.turn

    return player - opponent, player, opponent


@typechecked
def evaluate_board_state(board: chess.Board, move: str) -> float:
    board.push_uci(move)

    board_state_value = evaluate_game_state(board, False)
    if board.is_game_over():
        board.pop()
        return board_state_value

    piece_scores = evaluate_board_piece_score(board, not board.turn)
    board_state_value += piece_scores[0]

    attack_scores = evaluate_board_attack_score(board)
    board_state_value += attack_scores[0]
    board.pop()

    if board_state_value > Macros.BOARD_CHECKMATE_VALUE:
        return Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    elif board_state_value < -Macros.BOARD_CHECKMATE_VALUE:
        return -Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    return board_state_value
