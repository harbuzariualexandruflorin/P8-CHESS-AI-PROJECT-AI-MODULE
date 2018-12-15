
import chess
from dependencies.dependencies_check import check_necessary_packages
import implementation.output.json_output as output
check_necessary_packages()

import utils.chess_utils as chess_functions
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros
from multiprocessing import Pool
from implementation.algorithms.negamax.negamax import negamax_root as negamax_algorithm
from implementation.algorithms.alfa_beta.alfabeta import alpha_beta_root as alphabeta_algorihm
from implementation.algorithms.minmax.minmax import min_max_root as minmax_algorithm
import time

@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)


def generate_response_case1(fen,color ) -> None:
    depth=1
    board=chess.Board(fen)
    negamax_board=board.copy()
    minmax_board=board.copy()
    alphabeta_bord=board.copy()
    list_for_min=[]
    list_for_alfa=[]
    list_for_nega=[]
    i=0
    while i<6:
        with Pool(processes=4) as pool:
            rminmax = pool.apply_async(minmax_algorithm, (depth, minmax_board, True,))
            rnegamax = pool.apply_async(negamax_algorithm, (depth + 1, negamax_board,))
            ralfabeta = pool.apply_async(alphabeta_algorihm, (depth, alphabeta_bord, True,))
            movealfa,valuealfa=ralfabeta.get()
            movemin,valuemin=rminmax.get()
            movenega,valuenega=rnegamax.get()
            list_for_alfa.append((str(movealfa),valuealfa))
            list_for_min.append((str(movemin),valuemin))
            list_for_nega.append((str(movenega),valuenega))
            negamax_board.push(movenega)
            minmax_board.push(movemin)
            alphabeta_bord.push(movealfa)
        i+=1
    color = ["w", "b"]
    color_pos = 0
    if "w" in fen:
        color_pos=0
    else:
        color_pos=1
    algorithms=[("MinMax",list_for_min,"PAWN_ADVANCE_STRATEGY"),("NegaMax",list_for_nega,"TAKE_PIECES_STRATEGY"),("AlfaBeta",list_for_alfa,"DEFEND_PIECES_STRATEGY")]
    list_moves=[]
    for algorithm in algorithms:
        #list_moves = []
        # variants.clear()
        variants = output.create_json_variants(algorithm[0],[algorithm[2]])
        # variants.clear()
        n=0
        for move,score in algorithm[1]:
            #while n!=6 :
            if color_pos%2==0:
                    n+=1
                    information_move=output.create_json_information_moves(color[color_pos]+move,score)
                    #output.add_variants(list_moves,variants,[information_move])
                    #if len(list_moves)==0:
                    if n==1 :
                        output.add_variants(list_moves, variants, [information_move])
                    else:
                        list_moves[-1]['moves'].append(information_move)
            else:
                    n+=1
                    information_move = output.create_json_information_moves(color[color_pos] + move, score)
                    #output.add_variants(list_moves, variants, [information_move])
                    # list_moves[-1]['moves'].append(information_move)
                    if n==1 :
                        output.add_variants(list_moves, variants, [information_move])
                    else:
                        list_moves[-1]['moves'].append(information_move)
                    #if len(list_moves)==0:
                     #   output.add_variants(list_moves, variants, [information_move])
                    #else:
                     #   list_moves[-1]['moves'].append(information_move)
            color_pos = 1-color_pos
                # print(variants)
    json_main_part=output.create_json_main_body(fen,list_moves)
    output.create_json_output(json_main_part)

if __name__ == '__main__':
    # main()

    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    generate_response_case1(fen,"w")