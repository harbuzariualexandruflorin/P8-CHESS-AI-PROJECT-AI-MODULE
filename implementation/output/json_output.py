import json

from typeguard import typechecked

import utils.chess_utils as chess_functions

import chess

from implementation.algorithms.minmax.minmax import min_max_root as min_max_algorithm

@typechecked
def create_json_main_body(initial_state_FEN : str, variants : list) -> dict:
    return {"initialStateFEN" : initial_state_FEN, "variants" : variants}

@typechecked
def create_json_variants(algorithm_name : str, strategy_name: str) -> dict:
    return {"moves" : [], "algorithmName" : algorithm_name, "strategyNames" : strategy_name}

@typechecked
def create_json_information_moves(move : str, score : float) -> dict:
    return {"move" : move, "score" : score}

@typechecked
def add_variants(list_of_moves : list, variants : dict, list_of_information_moves : list) -> None:
    list_of_moves.append(variants)
    list_of_moves[-1]["moves"] = list_of_information_moves

@typechecked
def create_json_output(dictionary) -> None:
    text = json.dumps(dictionary, indent = 4)
    open("output.json","w").write(text)

@typechecked
def play(initial_state_FEN : str) -> None :
    board = chess.Board()
    print(board)
    list_moves=list()
    while not board.is_game_over() :
        if board.turn :
            variants = create_json_variants("MinMax", "PAWN_ADVANCE_STRATEGY")
            move = min_max_algorithm(2, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            score = chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY])
            information_move = create_json_information_moves('w'+str(move), score)
            add_variants(list_moves, variants, [information_move])
            print("You are advised to do this move",move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else :
            print("Computer's Turn:")
            variants = create_json_variants("MinMax", "PAWN_ADVANCE_STRATEGY")
            move = min_max_algorithm(2, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            score = chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY])
            information_move = create_json_information_moves('b'+str(move), score)
            add_variants(list_moves, variants, [information_move])
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        json_main_part=create_json_main_body(initial_state_FEN, list_moves)
        create_json_output(json_main_part)

if __name__ == "__main__" :
    play("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")