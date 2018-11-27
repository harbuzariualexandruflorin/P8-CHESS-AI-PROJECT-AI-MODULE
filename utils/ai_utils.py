from typeguard import typechecked
from datetime import datetime
import logging
import chess
import os

from utils.macros import Macros


@typechecked
def get_logger(name: str) -> logging.Logger:
    log_file_name = "logfile_" + datetime.now().strftime("%d_%m_%Y.txt")
    log_directory = os.path.join("../logs", log_file_name)

    file_handler = logging.FileHandler(log_directory, 'a')
    file_formatter = logging.Formatter('**%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger(name)
    logger.handlers = []

    logger.addHandler(file_handler)
    return logger


@typechecked
def evaluate_board_state() -> float:
    board_state_value = 0

    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board.push_uci("f2f3")
    print(board)
    # for move in board.legal_moves:
    #     print(move)

    player, opponent = not board.turn, board.turn
    print(player, opponent)

    if board.is_checkmate():
        board_state_value = Macros.BOARD_WIN_VALUE
    else:

        pass

    return {
        chess.WHITE: board_state_value,
        chess.BLACK: -board_state_value
    }[player]
