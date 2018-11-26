from pip._internal import get_installed_distributions as get_installed_packages
from pip._internal import main as pipmain
from main.ai_utils import get_logger
from typeguard import typechecked
from logging import Logger
from typing import List
import os


@typechecked
def logger() -> Logger:
    return get_logger(__name__)


@typechecked
def get_necessary_packages(file_name: str) -> List[str]:
    location = os.path.realpath(os.path.join(".", os.path.dirname(__file__)))
    lines = []
    try:
        with open(os.path.join(location, file_name)) as file:
            lines = [line.rstrip('\n') for line in file if len(line.rstrip('\n')) > 0]
    except FileNotFoundError:
        logger().exception("Failed to open file %s", file_name)
    except:
        logger().exception("Something went wrong")

    return lines


@typechecked
def install_packages(packages: List[str]) -> None:
    for package in packages:
        try:
            pipmain(['install', package])
        except:
            logger().exception("Failed to install package %s", package)


@typechecked
def check_necessary_packages() -> None:
    packages = get_necessary_packages('dependencies.txt')
    installed_packages = [package.project_name.lower() for package in get_installed_packages()]

    packages_to_install = list(dict.fromkeys([package for package in packages if package not in installed_packages]))
    install_packages(packages_to_install)
