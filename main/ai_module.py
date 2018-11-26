from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

from typeguard import typechecked
from webapi.api import start_api


@typechecked
def main() -> None:
    print(start_api('5002'))


if __name__ == '__main__':
    main()
