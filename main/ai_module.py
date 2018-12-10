import random

import chess

from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

from utils.chess_utils import evaluate_board_state
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros


@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)


if __name__ == '__main__':
    # main()

    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    print(board)
    print("==============================================")

    print([str(x) for x in board.legal_moves])

    while not board.is_game_over():
        if board.turn:
            print("TURN -> WHITE")
        else:
            print("TURN -> BLACK")

        move = random.choice([str(x) for x in board.legal_moves])
        val = evaluate_board_state(board, move)

        board.push_uci(move)
        print(board)
        print(val)
        print(move)
        print("=================================================")
