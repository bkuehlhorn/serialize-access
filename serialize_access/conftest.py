# content of conftest.py
import pytest

from serialize_access import serialize_access

import logging


# logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )
    parser.addoption("--all", action="store", default=False, help="do all types")
    parser.addoption("--print", action="store", default=False, help="print all keys")


def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = 5
        else:
            end = 2
        metafunc.parametrize("param1", range(end))

    if "debug" in metafunc.fixturenames:
        if metafunc.config.getoption("debug"):
            serialize_access.logger.setLevel(serialize_access.logging.DEBUG)
        else:
            serialize_access.logger.setLevel(serialize_access.logging.INFO)
        # metafunc.parametrize("debug", metafunc.config.getoption('debug'))

    if "print" in metafunc.fixturenames:
        print = metafunc.config.getoption("print")

        # metafunc.parametrize("print", print)


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope="module")
def debug(request):
    serialize_access.logger.setLevel(serialize_access.logging.DEBUG) if request.config.getoption("--debug") else ""
    return request.config.getoption("--debug")


@pytest.fixture(scope="module")
def printKeys(request):
    return request.config.getoption("--print")
