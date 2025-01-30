import codec_test
from types import ModuleType
import unittest


class TestRunner:
    def __init__(self) -> None:
        self.__test_modules: list[ModuleType] = []
        self.__test_suite: unittest.TestSuite = unittest.TestSuite()

    def add_test_module(self, test_module: ModuleType) -> None:
        if test_module not in self.__test_modules:
            self.__test_modules.append(test_module)

    def add_test_modules(self, test_modules: list[ModuleType]) -> None:
        for test_module in test_modules:
            self.add_test_module(test_module)

    def run(self) -> None:
        for test_module in self.__test_modules:
            self.__test_suite.addTests(
                unittest.defaultTestLoader.loadTestsFromModule(test_module)
            )

        unittest.TextTestRunner(verbosity=2).run(self.__test_suite)


if __name__ == '__main__':
    test_modules = [
        codec_test,
    ]

    test_runner = TestRunner()
    test_runner.add_test_modules(test_modules)
    test_runner.run()
