import random

import chess

from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

import utils.chess_utils as chess_functions
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
        val = chess_functions.evaluate_board_state(board, move, [
            chess_functions.PAWN_ADVANCE_STRATEGY,
            chess_functions.KEEP_PIECES_STRATEGY,
            chess_functions.ATTACK_PIECES_STRATEGY,
            chess_functions.DEFEND_PIECES_STRATEGY,
            chess_functions.TAKE_PIECES_STRATEGY
        ])

        board.push_uci(move)
        print(board)
        print(val)
        print(move)
        print("=================================================")

    ##caz 1
    #multiprocesare
    """
    r1 = mutare , scor, minmax, pown.strategi
    r2 = mutare scor, alpha , defece
    r3 =mutare scor , nega, attack
    create json 
     mutari 
        :r1
    mutari 
     r2
     mutari r3
     }}
     caz 2
     4 c213
    '"""




