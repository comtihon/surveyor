from colorama import Fore

from tester.test.full import FullTest


# Same as FullTest but without kafka
class TravisTest(FullTest):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self._name = __name__.split('.')[-1:][0]

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
