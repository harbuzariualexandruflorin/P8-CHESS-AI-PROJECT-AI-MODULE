import json

from typeguard import typechecked

import utils.chess_utils as chess_functions

import chess

from implementation.algorithms.minmax.minmax import min_max_root as min_max_algorithm

@typechecked
def create_json_main_body(initial_state_FEN : str, variants : list) -> dict :
    return {"initialStateFEN" : initial_state_FEN, "variants" : variants}

@typechecked
def create_json_variants(algorithm_name : str, strategy_name: str) -> dict :
    return {"moves" : [], "algorithmName" : algorithm_name, "strategyNames" : strategy_name}

@typechecked
def create_json_information_moves(move : str, score : float) -> dict :
    return {"move" : move, "score" : score}

@typechecked
def add_variants(list_of_moves : list, variants : dict, list_of_information_moves : list) -> None :
    list_of_moves.append(variants)
    list_of_moves[-1]["moves"] = list_of_information_moves

@typechecked
def create_json_output(dictionary) -> None :
    text = json.dumps(dictionary, indent = 4)
    open("output.json","w").write(text)

@typechecked
def choose_algorithm() -> str :
    list_of_algorithms =  ['MinMax', 'NegaMax', 'AlfaBeta']
    print("Here is the list of all algorithms:",list_of_algorithms)
    algorithm = input("Choose one of them: ")
    return algorithm

@typechecked
def choose_strategy() -> str :
    list_of_strategies =  ['PAWN_ADVANCE_STRATEGY', 'TAKE_PIECES_STRATEGY', 'ATTACK_PIECES_STRATEGY', 'DEFEND_PIECES_STRATEGY', 'KEEP_PIECES_STRATEGY']
    print("Here is the list of all strategies:",list_of_strategies)
    algorithm = input("Choose one of them: ")
    return algorithm

@typechecked
def game_strategy(strategy_name : str) -> list :
    if strategy_name == 'PAWN_ADVANCE_STRATEGY' :
        return [chess_functions.PAWN_ADVANCE_STRATEGY]
    if strategy_name == 'TAKE_PIECES_STRATEGY' :
        return [chess_functions.TAKE_PIECES_STRATEGY]
    if strategy_name == 'ATTACK_PIECES_STRATEGY' :
        return [chess_functions.ATTACK_PIECES_STRATEGY]
    if strategy_name == 'DEFEND_PIECES_STRATEGY' :
        return [chess_functions.DEFEND_PIECES_STRATEGY]
    if strategy_name == 'KEEP_PIECES_STRATEGY' :
        return [chess_functions.KEEP_PIECES_STRATEGY]

@typechecked
def game_algorithm(algorithm_name : str, depth : int, board : chess.Board, is_maximizing : bool, strategy : str) -> chess.Move :
    if algorithm_name == 'MinMax' :
        return min_max_algorithm(depth, board, is_maximizing, game_strategy(strategy))

@typechecked
def play(initial_state_FEN : str) -> None :
    board = chess.Board()
    print(board)
    list_moves=list()
    while not board.is_game_over() :
        if board.turn :
            algorithm=choose_algorithm()
            strategy=choose_strategy()
            variants = create_json_variants(algorithm, strategy)
            move = game_algorithm(algorithm, 1, board, True, strategy)
            score = chess_functions.evaluate_board_state(board, str(move), game_strategy(strategy))
            information_move = create_json_information_moves('w'+str(move), score)
            add_variants(list_moves, variants, [information_move])
            print("You are advised to do this move",move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else :
            print("Computer's Turn:")
            variants = create_json_variants("MinMax", "PAWN_ADVANCE_STRATEGY")
            move = min_max_algorithm(1, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            score = chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY])
            information_move = create_json_information_moves('b'+str(move), score)
            add_variants(list_moves, variants, [information_move])
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        json_main_part = create_json_main_body(initial_state_FEN, list_moves)
        create_json_output(json_main_part)

if __name__ == "__main__" :
    play("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")