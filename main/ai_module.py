import chess
from dependencies.dependencies_check import check_necessary_packages
import implementation.output.json_output as output
check_necessary_packages()

import implementation.algorithms.tree.tree_gen
import utils.chess_utils as chess_functions
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros
from multiprocessing import Pool
from implementation.algorithms.negamax.negamax import negamax_root as negamax_algorithm
from implementation.algorithms.alfa_beta.alfabeta import alpha_beta_root as alphabeta_algorihm
from implementation.algorithms.minmax.minmax import min_max_root as minmax_algorithm
import time
from implementation.algorithms.tree.tree_gen import mistake_checker as mistake_move
from implementation.output.json_file_to_string import json_file_to_string as convert_json_to_string

@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)

@typechecked
def generate_response_case1(fen : str) -> str:
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
    return convert_json_to_string('output.json')

@typechecked
def generate_response_case2(fen : str ,list : list) -> str:
    depth=1
    board=chess.Board(fen)
    bad_move=mistake_move(list.copy(),len(list)%2+1,0)
    list_for_min=[]
    list_for_alfa=[]
    list_for_nega=[]
    for index in range (0, len(list)):
        if index==bad_move[1]:
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
    list_all_moves=[]
    list_all_variants = []
    list_strategies=[chess_functions.PAWN_ADVANCE_STRATEGY,chess_functions.DEFEND_PIECES_STRATEGY,chess_functions.TAKE_PIECES_STRATEGY,chess_functions.ATTACK_PIECES_STRATEGY,chess_functions.KEEP_PIECES_STRATEGY]
    for move in list :
        if move in bad_move :
            n = 0
            for algorithm in algorithms:
                variants = output.create_json_variants(algorithm[0],[algorithm[2]])
                n += 1
                m=0
                for move_algorithm,score in algorithm[1]:
                    if color_pos%2==0:
                        m+=1
                        information_move=output.create_json_information_moves(color[color_pos]+move_algorithm,score)
                        #print("Info White",information_move)
                        #                       output.add_variants(list_moves,variants,[information_move])
                        if m==1 :
                            output.add_variants(list_moves, variants, [information_move])
                        else:
                            list_moves[-1]['moves'].append(information_move)

                    else:
                        m+=1
                        information_move=output.create_json_information_moves(color[color_pos]+move_algorithm,score)
                        #list_moves[-1]['moves'].append(information_move)
                        if m==1 :
                            output.add_variants(list_moves, variants, [information_move])
                        else:
                            list_moves[-1]['moves'].append(information_move)
                        #print("Info Black",information_move)
                    color_pos = 1-color_pos

                list_all_variants.append(variants)
                #print(list_all_variants)
                if n == 3 :
                    d=output.create_json_moves(list_all_variants)
                    list_all_moves.append(output.create_json_information_moves_with_variants(move,chess_functions.evaluate_board_state(board, move, list_strategies),list_moves))

        else:
            list_all_moves.append(output.create_json_information_moves(move,chess_functions.evaluate_board_state(board, move, list_strategies)))
        board.push_uci(move)
    #d2=output.create_json_information_moves_with_variants(second_move,second_score,list_moves)
    #print(list_all_moves)
    dictionary=output.create_json_moves(list_all_moves)
    #dictionary={"moves":list_all_moves}
    json_main_part = output.create_second_json_main_body(fen, dictionary)
    output.create_json_output2(json_main_part)
    return convert_json_to_string('second_output.json')

if __name__ == '__main__':
    # main()
    move_list = ["g1h3", "d7d6", "b2b3", "h7h6", "b3b4"]
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    #aici ai string-ul pt cazul 1 : primesti fen-ul
    print(generate_response_case1(fen))
    #aici ai string-ul pt cazul 2 : primesti fen-ul si lista de mutari
    #print(generate_response_case2(fen,move_list))
