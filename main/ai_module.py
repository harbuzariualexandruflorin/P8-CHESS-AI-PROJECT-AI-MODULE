from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros


@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)


if __name__ == '__main__':
    main()
    # move_list = ["g1h3", "d7d6", "b2b3", "h7h6", "b3b4"]
    # fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # #aici ai string-ul pt cazul 1 : primesti fen-ul
    # print(generate_response_case1(fen))
    # #aici ai string-ul pt cazul 2 : primesti fen-ul si lista de mutari
    # #print(generate_response_case2(fen,move_list))
