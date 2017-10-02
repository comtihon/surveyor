from time import sleep
from urllib.parse import quote_plus

import pymongo
from colorama import Fore


class Mongo:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        uri = "mongodb://%s:%s@%s:%s" % (
            quote_plus(conf['username']),
            quote_plus(conf['password']),
            conf['host'],
            str(conf['port']))
        self._client = pymongo.MongoClient(uri)
        self._database = conf['database']

    @property
    def database(self) -> str:
        return self._database

    @property
    def client(self):
        return self._client

    def check_statistics(self, answers_selected: list) -> bool:
        print('Checking statistics in mongo', end=' ')
        for (q, a) in answers_selected:
            if not self.check_mongo(q, a):
                return False
        print(Fore.GREEN + 'OK')
        return True

    def check_mongo(self, question_id, answer_id, result=1):
        statistics = self.fetch_question(question_id)
        if statistics is None:
            print(Fore.RED + 'Fail, no data in mongodb for' + question_id)
            return False
        if statistics.get(answer_id, -1) != result:
            print(Fore.RED + 'Metric mismatch')
            print(statistics)
            return False
        return True

    def fetch_question(self, question_id: str, retry=True) -> dict:
        db = self.client[self.database]
        res = db.statistics.find_one({'question_id': question_id})
        if res is None and retry:  # test can run faster than collector. Should wait for data
            sleep(1)
            return self.fetch_question(question_id, False)
        return res
