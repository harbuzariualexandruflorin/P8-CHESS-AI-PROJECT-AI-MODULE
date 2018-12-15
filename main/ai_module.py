import random

import chess

from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

import utils.chess_utils as chess_functions
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros
from multiprocessing import Pool
from multiprocessing import Process
from implementation.algorithms.negamax.negamax import negamax_root as negamax_algorithm
from implementation.algorithms.alfa_beta.alfabeta import alpha_beta_root as alphabeta_algorihm
from implementation.algorithms.minmax.minmax import min_max_root as minmax_algorithm
import time

@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)

@typechecked
def generate_response_case1(board:chess.Board,color : str) -> None:
    depth=1
    negamax_board=board.copy()
    minmax_board=board.copy()
    alphabeta_bord=board.copy()
    i=0
    while i<6:
        with Pool(processes=4) as pool:
            rminmax = pool.apply_async(minmax_algorithm, (depth, minmax_board, True,))
            rnegamax = pool.apply_async(negamax_algorithm, (depth + 1, negamax_board,))
            ralfabeta = pool.apply_async(alphabeta_algorihm, (depth, alphabeta_bord, True,))
            movealfa,valuealfa=ralfabeta.get()
            movemin,valuemin=rminmax.get()
            movenega,valuenega=rnegamax.get()

            negamax_board.push(movenega)
            minmax_board.push(movemin)
            alphabeta_bord.push(movealfa)
            print(valuealfa)
            print(valuemin)
            print(valuenega)
        i+=1


if __name__ == '__main__':
    # main()

    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    start=time.time()
    generate_response_case1(board)
    print(time.time()-start)