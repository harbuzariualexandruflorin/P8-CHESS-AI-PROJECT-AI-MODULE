from typing import List, Callable

import chess
from typeguard import typechecked

from utils.macros import Macros


@typechecked
def get_board_pieces(board: chess.Board) -> List[chess.Piece]:
    piece_positions = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            piece_positions.append(piece)

    return piece_positions


@typechecked
def get_board_pieces_total_value(board_pieces: List[chess.Piece], check_color: Callable) -> float:
    total_value = 0

    for piece in board_pieces:
        if check_color(piece.color):
            total_value += Macros.PIECE_VALUES[piece.piece_type] / Macros.BOARD_INTERVAL_FIX

    return total_value


@typechecked
def evaluate_board_piece_score(board: chess.Board) -> (float, float):
    board_pieces = sorted(get_board_pieces(board), key=lambda piece: piece.piece_type)

    opponent = get_board_pieces_total_value(board_pieces, lambda color: color == board.turn)
    player = get_board_pieces_total_value(board_pieces, lambda color: color != board.turn)

    return player, opponent


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
def get_board_attack_total_value(board: chess.Board) -> float:
    total_value = 0
    for move in board.legal_moves:
        board.push_uci(str(move))
        total_value += evaluate_game_state(board, True)
        board.pop()

        if board.is_capture(move):
            piece = board.piece_at(Macros.UCI_TO_SQUARE[str(move)[2:4]])
            if piece is not None:
                total_value += Macros.PIECE_VALUES[piece.piece_type] / Macros.BOARD_INTERVAL_FIX

    return total_value


@typechecked
def evaluate_board_attack_score(board: chess.Board) -> (float, float):
    opponent = get_board_attack_total_value(board)
    board.turn = not board.turn
    player = get_board_attack_total_value(board)
    board.turn = not board.turn

    return player, opponent


@typechecked
def evaluate_board_state(board: chess.Board, move: str) -> float:
    board.push_uci(move)

    board_state_value = evaluate_game_state(board, False)
    if board.is_game_over():
        board.pop()
        return board_state_value

    player_piece_score, opponent_piece_score = evaluate_board_piece_score(board)
    player_attack_score, opponent_attack_score = evaluate_board_attack_score(board)

    board.pop()
    board_state_value += (player_piece_score - opponent_piece_score) + (player_attack_score - opponent_attack_score)

    if board_state_value > 1:
        return Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    elif board_state_value < -1:
        return -Macros.BOARD_POSSIBLE_CHECKMATE_VALUE
    return board_state_value
