import json

from typeguard import typechecked

import utils.chess_utils as chess_functions

import chess

from implementation.algorithms.minmax.minmax import min_max_root as min_max_algorithm

from implementation.algorithms.alfa_beta.alfabeta import alpha_beta_root as alfa_beta_algorithm

from implementation.algorithms.negamax.negamax import negamax_root as negamax_algorithm

@typechecked
def create_json_main_body(initial_state_FEN : str, variants : list) -> dict :
    return {"initialStateFEN" : initial_state_FEN, "variants" : variants}

@typechecked
def create_second_json_main_body(initial_state_FEN : str, mainVariant : dict) -> dict :
    return {"initialStateFEN" : initial_state_FEN, "mainVariant" : mainVariant}

@typechecked
def create_json_variants(algorithm_name : str, strategy_name: list) -> dict :
    return {"moves" : [], "algorithmName" : algorithm_name, "strategyNames" : strategy_name}

@typechecked
def create_json_information_moves(move : str, score : float) -> dict :
    return {"move" : move, "score" : score}

@typechecked
def create_json_information_moves_with_variants(move : str, score : float, variants : list) -> dict :
    return {"move" : move, "score" : score, "variants" : variants}

@typechecked
def create_json_moves(list_name: list) -> dict :
    return {"moves" : list_name}

@typechecked
def add_variants(list_of_moves : list, variants : dict, list_of_information_moves : list) -> None :
    list_of_moves.append(variants)
    list_of_moves[-1]["moves"] = list_of_information_moves

@typechecked
def add_moves(list_of_moves : list, moves : dict, list_of_information_moves : list) -> None :
    list_of_moves.append(moves)
    list_of_moves[-1]["variants"] = list_of_information_moves

@typechecked
def create_json_output(dictionary) -> None :
    text = json.dumps(dictionary, indent = 4)
    open("output.json","w").write(text)

@typechecked
def create_json_output2(dictionary) -> None :
    text = json.dumps(dictionary, indent = 4)
    open("second_output.json","w").write(text)

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
def game_algorithm(algorithm_name : str, depth : int, board : chess.Board, is_maximizing : bool, strategy : str) -> (chess.Move,float) :
    if algorithm_name == 'MinMax' :
        return min_max_algorithm(depth, board, is_maximizing, game_strategy(strategy))
    if algorithm_name == 'NegaMax' :
        return negamax_algorithm(depth, board, game_strategy(strategy))
    if algorithm_name == 'AlfaBeta' :
        return alfa_beta_algorithm(depth, board, is_maximizing, game_strategy(strategy))

@typechecked
def possible_variants(initial_state_FEN : str) -> None :
    list_of_algorithms = ['MinMax', 'NegaMax', 'AlfaBeta']
    strategy = choose_strategy()
    list_moves = list()
    for algorithm in list_of_algorithms :
        board = chess.Board(initial_state_FEN)
        print(board)
        variants = create_json_variants(algorithm, [strategy])
        print(algorithm)
        n = 0
        while n != 2 :
            if board.turn :
                n += 1
                move = game_algorithm(algorithm, 1, board, True, strategy)[0]
                score =  game_algorithm(algorithm, 1, board, True, strategy)[1]
                # score = chess_functions.evaluate_board_state(board, str(move), game_strategy(strategy))
                information_move = create_json_information_moves('w'+str(move), score)
                add_moves(list_moves, variants, [information_move])
                #print("You are advised to do this move",move)
                #move = input("Enter move:")
                move = chess.Move.from_uci(str(move))
                board.push(move)
            else :
                n += 1
                #print("Computer's Turn:")
                move = game_algorithm(algorithm, 1, board, True, strategy)[0]
                score =  game_algorithm(algorithm, 1, board, True, strategy)[1]
                # score = chess_functions.evaluate_board_state(board, str(move), game_strategy(strategy))
                information_move = create_json_information_moves('b'+str(move), score)
                list_moves[-1]['moves'].append(information_move)
                move = chess.Move.from_uci(str(move))
                board.push(move)
            print(board)
        json_main_part = create_json_main_body(initial_state_FEN, list_moves)
        create_json_output(json_main_part)

list_all_moves = list()
list_all_scores = list()

@typechecked
def play() -> None :
    global list_all_moves
    global list_all_scores
    board = chess.Board()
    print(board)
    n = 0
    while not board.is_game_over() :
        if board.turn :
            n += 1
            move,score = min_max_algorithm(1, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            # score = chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY])
            print(score)
            list_all_scores.append(score)
            print("You are advised to do this move",move)
            #move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            list_all_moves.append(str(move))
            board.push(move)
        else :
            n += 1
            print("Computer's Turn:")
            move,score = min_max_algorithm(1, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            # score = chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY])
            print(score)
            list_all_scores.append(score)
            move = chess.Move.from_uci(str(move))
            list_all_moves.append(str(move))
            board.push(move)
        print(board)
        print(list_all_scores,list_all_moves)
        print(n)
        #if n > 3 :
         #   break

@typechecked
def get_board(move_number_n : int ,initial_state_FEN : str) -> chess.Board :
    board = chess.Board(initial_state_FEN)
    for number_move in range(0, move_number_n-1) :
        move = chess.Move.from_uci(list_all_moves[number_move])
        board.push(move)
    return board

@typechecked
def possible_moves_instead_of_wrong_move(move_number_n : int ,initial_state_FEN : str, board_state : chess.Board) -> None:
    if move_number_n % 2 == 0 :
        first_color_piece, second_color_piece = 'w', 'b'
    else :
        first_color_piece, second_color_piece = 'b', 'w'
    first_move, second_move = first_color_piece+list_all_moves[move_number_n - 1], second_color_piece+list_all_moves[move_number_n]
    first_score, second_score = list_all_scores[move_number_n - 1], list_all_scores[move_number_n]
    list_of_algorithms = ['MinMax', 'NegaMax', 'AlfaBeta']
    strategy = choose_strategy()
    #strategy='PAWN_ADVANCE_STRATEGY'
    list_moves = list()
    for algorithm in list_of_algorithms :
        board = board_state
        print(board)
        variants = create_json_variants(algorithm, [strategy])
        print(algorithm)
        print(board.turn)
        n = 0
        while n != 2 :
            if not board.turn :
                n += 1
                move,score = game_algorithm(algorithm, 1, board, True, strategy)
                # score = chess_functions.evaluate_board_state(board, str(move), game_strategy(strategy))
                print(move, score)
                information_move = create_json_information_moves(first_color_piece+str(move), score)
                print(information_move)
                add_variants(list_moves, variants, [information_move])
                #print("You are advised to do this move",move)
                #move = input("Enter move:")
                move = chess.Move.from_uci(str(move))
                board.push(move)
            else :
                n += 1
                #print("Computer's Turn:")
                move,score = game_algorithm(algorithm, 1, board, True, strategy)
                # score = chess_functions.evaluate_board_state(board, str(move), game_strategy(strategy))
                information_move = create_json_information_moves(second_color_piece+str(move), score)
                list_moves[-1]['moves'].append(information_move)
                move = chess.Move.from_uci(str(move))
                board.push(move)
            print(board)
    d1=create_json_information_moves_with_variants(first_move,first_score,list_moves)
    d2=create_json_information_moves_with_variants(second_move,second_score,list_moves)
    dictionary=create_json_moves([d1,d2])
    json_main_part = create_second_json_main_body(initial_state_FEN, dictionary)
    create_json_output(json_main_part)

if __name__ == "__main__" :
    possible_variants("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    #play()
    #possible_moves_instead_of_wrong_move(2,"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",get_board(2,"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    #print(get_board(2,"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))