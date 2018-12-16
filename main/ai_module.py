from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()
from webapi.services import generate_response_case2
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros


@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)


if __name__ == '__main__':
    main()
    #move_list = ['g2g3', 'e7e6', 'f2f4', 'h7h6', 'e2e3', 'd7d5', 'e3e4', 'a7a6', 'e4d5', 'f8c5', 'c2c3', 'd8e7', 'd2d4',
    #            'g8f6', 'd4c5', 'b8d7', 'd5d6', 'e7f8', 'd6c7', 'h6h5', 'a2a3', 'f8e7', 'a1a2', 'a6a5', 'f1g2', 'd7f8',
    #            'c5c6', 'e6e5', 'c6b7', 'c8b7', 'c7c8q', 'a8c8', 'g2b7', 'e7b7', 'd1d7', 'f8d7', 'b2b4', 'b7h1',
    #            'b4a5', 'h1g1', 'e1e2', 'g1h2', 'e2e1', 'h2h1', 'e1e2', 'h1h2', 'e2d3', 'd7c5', 'd3e3', 'h2g3', 'e3e2',
    #            'g3g2', 'e2e3', 'f6d5']
    #fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # #aici ai string-ul pt cazul 1 : primesti fen-ul
    # print(generate_response_case1(fen))
    # #aici ai string-ul pt cazul 2 : primesti fen-ul si lista de mutari
    #print(generate_response_case2(fen,move_list))
