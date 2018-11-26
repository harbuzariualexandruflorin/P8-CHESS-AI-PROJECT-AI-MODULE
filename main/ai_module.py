from dependencies.dependencies_check import check_necessary_packages

check_necessary_packages()

from webapi.api import start_api


def main():
    start_api('5002')


if __name__ == '__main__':
    main()
