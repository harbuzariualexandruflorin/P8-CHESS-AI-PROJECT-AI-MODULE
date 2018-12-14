from typing import Callable, List

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
def get_board_piece_total_value(board: chess.Board) -> float:
    total_value = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None and piece.color == board.turn:
            total_value += Macros.PIECE_VALUES[piece.piece_type] / Macros.BOARD_INTERVAL_FIX

    return total_value


@typechecked
def get_board_attack_total_value(board: chess.Board) -> float:
    total_value = 0

    for move in board.legal_moves:
        captured_piece = board.is_capture(move)
        score_before = KEEP_PIECES_STRATEGY(board)[2] if captured_piece else 0

        board.push_uci(str(move))
        if captured_piece:
            total_value += score_before - KEEP_PIECES_STRATEGY(board)[1]

        total_value += evaluate_game_state(board, True)
        board.pop()

    return total_value


@typechecked
def get_board_piece_take_total_value(board: chess.Board) -> float:
    total_value = 0

    for move in board.legal_moves:
        if board.is_capture(move):
            total_value += Macros.BOARD_PIECE_TAKE_VALUE

    return total_value


@typechecked
def get_board_pawn_advance_total_value(board: chess.Board) -> float:
    total_value = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            row = 1 + square // Macros.BOARD_SIZE

            if piece.piece_type == chess.PAWN and piece.color == board.turn:
                if board.turn == chess.BLACK:
                    row = Macros.BOARD_SIZE - row + 1

                total_value += Macros.PAWN_ADVANCE_VALUES[row] / Macros.BOARD_INTERVAL_FIX

    return total_value


@typechecked
def get_board_defence_total_value(board: chess.Board) -> float:
    total_value = 0

    for square_defend in chess.SQUARES:
        piece_defend = board.piece_at(square_defend)
        if piece_defend is not None and piece_defend.color == board.turn:
            if board.is_attacked_by(not board.turn, square_defend):

                for square_defendant in chess.SQUARES:
                    piece_defendant = board.piece_at(square_defendant)
                    if piece_defendant is not None and piece_defendant.color == board.turn:

                        if square_defend in board.attacks(square_defendant):
                            total_value += Macros.PIECE_VALUES[piece_defend.piece_type] / Macros.BOARD_INTERVAL_FIX

    return total_value


@typechecked
def evaluate_strategy(board: chess.Board, strategy: Callable) -> (float, float, float):
    opponent = strategy(board)
    board.turn = not board.turn
    player = strategy(board)
    board.turn = not board.turn

    return player - opponent, player, opponent


@typechecked
def evaluate_board_state(board: chess.Board, move: str, algorithms: List[Callable]) -> float:
    board.push_uci(move)

    board_state_value = evaluate_game_state(board, False)
    if board.is_game_over():
        board.pop()
        return board_state_value

    for algorithm in algorithms:
        board_state_value += algorithm(board)[0]

    board.pop()
    if board_state_value > Macros.BOARD_CHECKMATE_VALUE:
        return Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    elif board_state_value < -Macros.BOARD_CHECKMATE_VALUE:
        return -Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    return board_state_value


PAWN_ADVANCE_STRATEGY: Callable = lambda board: evaluate_strategy(board, get_board_pawn_advance_total_value)
TAKE_PIECES_STRATEGY: Callable = lambda board: evaluate_strategy(board, get_board_piece_take_total_value)
ATTACK_PIECES_STRATEGY: Callable = lambda board: evaluate_strategy(board, get_board_attack_total_value)
DEFEND_PIECES_STRATEGY: Callable = lambda board: evaluate_strategy(board, get_board_defence_total_value)
KEEP_PIECES_STRATEGY: Callable = lambda board: evaluate_strategy(board, get_board_piece_total_value)
