import os

from colorama import Fore

from tester.test.test import Test


def get_all_tests(tests: list) -> ['class']:
    import_all_tests()
    tests_available = Test.__subclasses__()
    if tests == ['all']:
        return tests_available
    return [t for t in tests_available if t.name in tests]


def import_all_tests():
    modules = os.listdir('tester/test')
    for t in modules:
        if t.endswith('.py'):
            print(Fore.CYAN + 'import ' + 'tester.test.' + t[:-3])
            __import__('tester.test.' + t[:-3], globals(), locals(), [], 0)
