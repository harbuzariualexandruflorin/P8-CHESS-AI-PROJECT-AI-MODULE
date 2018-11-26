from pip._internal import main as pipmain
from main.ai_utils import get_logger
from importlib import util
import os


def logger():
    return get_logger(__name__)


def get_necessary_packages(file_name):
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


def is_package_installed(package):
    installed = util.find_spec(package)
    return installed is not None


def install_packages(packages):
    for package in packages:
        try:
            pipmain(['install', package])
        except:
            logger().exception("Failed to install package %s", package)


def check_necessary_packages():
    packages = get_necessary_packages('dependencies.txt')
    packages_to_install = list(dict.fromkeys([package for package in packages if not is_package_installed(package)]))
    install_packages(packages_to_install)
