from colorama import Fore

from tester.service.kafka import Kafka
from tester.service.manager import Manager
from tester.service.mongodb import Mongo
from tester.service.postgres import Postgres
from tester.service.requests import Requests
from tester.service.statistics import Statistics
from tester.test.test import Test
from tester.utils.model_utils import compare_surveys


class FullTest(Test):
    def __init__(self, conf: dict) -> None:
        super().__init__(__name__)
        self._manager = Manager(conf['manager'])
        self._postgres = Postgres(conf['postgres'])
        self._requests = Requests(conf['requests'])
        self._kafka = Kafka(conf['kafka'])
        self._mongo = Mongo(conf['mongodb'])
        self._statistics = Statistics(conf['statistics'])

    @property
    def manager(self) -> Manager:
        return self._manager

    @property
    def postgres(self) -> Postgres:
        return self._postgres

    @property
    def requests(self) -> Requests:
        return self._requests

    @property
    def kafka(self) -> Kafka:
        return self._kafka

    @property
    def mongo(self) -> Mongo:
        return self._mongo

    @property
    def statistics(self) -> Statistics:
        return self._statistics

    def run(self) -> bool:
        survey = {'name': 'test_survey', 'country_code': 'en', 'questions': [
            {'name': 'question1', 'answers': [{'name': 'yes'}, {'name': 'no'}]},
            {'name': 'question2', 'answers': [{'name': 'yes'}, {'name': 'no'}]}
        ]}
        survey_id = self.manager.create(survey)
        if survey_id is None:
            return False
        print(Fore.GREEN + "OK")
        answers = self.check_survey(survey_id, survey)
        if answers is None:
            return False
        if not self.check_answers(survey_id, answers):
            return False
        return True

    def check_survey(self, survey_id, survey) -> list or None:
        survey_from_db = self.postgres.check_survey(survey_id, survey)
        if survey_from_db is None:
            return False
        survey_got = self.manager.get(survey_id)
        if survey_got is None:
            return None
        if not self.compare_surveys(survey_from_db, survey_got):
            return None
        answers = self.select_answers(survey_got)
        print(Fore.GREEN + 'OK')
        return answers

    def check_answers(self, survey_id: str, answers_selected: list) -> bool:
        unanswered = self.requests.answer(survey_id, answers_selected)
        if unanswered is None:
            return False
        if unanswered:
            print(Fore.RED + 'Some questions not anwered')
            print(unanswered)
            return False
        print(Fore.GREEN + "OK")
        if not self.kafka.check_answers(answers_selected):
            return False
        if not self.mongo.check_statistics(answers_selected):
            return False
        if not self.statistics.check(answers_selected):
            return False
        return True

    def compare_surveys(self, survey_from_db: dict, survey_got: dict) -> bool:
        if not compare_surveys(survey_from_db, survey_got):
            print(Fore.RED + 'Survey mismatch.')
            print('Got from db ' + str(survey_from_db) + "\nGot from manager " + str(survey_got))
            return False
        return True

    # select every first answer of a question
    def select_answers(self, survey: dict) -> list:
        questions = survey['questions']
        selected = []
        for q in questions:
            selected.append((q['id'], q['answers'][0]['id']))
        return selected
