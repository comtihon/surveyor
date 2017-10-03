from colorama import Fore

from tester.test.full import FullTest
from tester.test.test import Test


# Same as FullTest but without kafka
class TravisTest(Test, FullTest):
    def __init__(self, conf: dict) -> None:
        FullTest.__init__(__name__, conf)

    def check_answers(self, survey_id: str, answers_selected: list) -> bool:
        unanswered = self.requests.answer(survey_id, answers_selected)
        if unanswered is None:
            return False
        if unanswered:
            print(Fore.RED + 'Some questions not anwered')
            print(unanswered)
            return False
        print(Fore.GREEN + "OK")
        if not self.mongo.check_statistics(answers_selected):
            return False
        if not self.statistics.check(answers_selected):
            return False
        return True
