from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

from utils.ai_utils import evaluate_board_state
from typeguard import typechecked
from webapi.api import start_api
from utils.macros import Macros


@typechecked
def main() -> None:
    start_api(Macros.SERVER_PORT)


if __name__ == '__main__':
    # main()
    print(evaluate_board_state())
