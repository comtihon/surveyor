from colorama import Fore

from tester.service.web_service import WebService
from tester.utils.http_utils import get


class Statistics(WebService):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)

    def check(self, answers: list):
        print('Checking statistics rest service', end=' ')
        for (q, a) in answers:
            statistics = self.fetch(q)
            if statistics is None:
                print(Fore.RED + 'No statistics for ' + q)
                return False
            if a not in statistics or statistics[a] != 1:
                print(Fore.RED + 'Wrong statistics')
                print(statistics)
        print(Fore.GREEN + 'OK')
        return True

    def fetch(self, question_id) -> dict or None:
        return get(self.url + '/question/' + question_id)
