import psycopg2
from colorama import Fore

from tester.utils.model_utils import compare_surveys


class Postgres:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._conf = conf

    @property
    def conf(self) -> dict:
        return self._conf

    def check_survey(self, survey_id: str, survey_expected: dict) -> dict or None:
        print('Checking survey in postgres', end=' ')
        survey_from_db = self.get_survey(survey_id)
        if survey_from_db is None:
            return None
        if not compare_surveys(survey_expected, survey_from_db):
            print(Fore.RED + 'Survey mismatch.')
            print('Saved to manager' + str(survey_expected) + "\nGot from db " + str(survey_from_db))
            return None
        print(Fore.GREEN + 'OK')
        return survey_from_db

    def get_survey(self, survey_id: str) -> dict or None:
        try:
            conn = psycopg2.connect(host=self.conf['host'],
                                    port=self.conf['port'],
                                    database=self.conf['database'],
                                    user=self.conf['user'],
                                    password=self.conf['password'])
        except Exception as e:
            print(Fore.RED + 'Can\'t connect to postgres: ' + str(self.conf) + ' -> ' + e)
            return None
        cur = conn.cursor()
        survey = Postgres.find_survey(cur, survey_id)
        if survey is None:
            return None
        if not survey:
            print(Fore.RED + 'No survey for ' + survey_id)
            return None
        [(_, cc, _)] = survey
        questions = Postgres.find_questions(cur, survey_id)
        if questions is None:
            return None
        if not questions:
            print(Fore.RED + 'No questions for ' + survey_id)
            return None
        return Postgres.form_survey(cur, cc, questions)

    @staticmethod
    def form_survey(cur, cc, questions) -> dict or None:
        questions = [{'question_id': question_id, 'name': name} for (question_id, name, _) in questions]
        survey = {'name': 'test_survey', 'country_code': cc}
        qlist = []
        for q in questions:
            answers = Postgres.find_answers(cur, q['question_id'])
            if answers is None:
                return None
            answers = [{'answers_id': answer_id, 'name': name} for (answer_id, name, _) in answers]
            q['answers'] = answers
            qlist.append(q)
        survey['questions'] = qlist
        return survey

    @staticmethod
    def find_survey(cur, survey_id) -> list or None:
        try:
            cur.execute("SELECT * from survey where survey_id='" + survey_id + "'")
            return cur.fetchall()
        except Exception as e:
            print(Fore.RED + 'Can\'t query survey: ' + survey_id + ' -> ' + e)
            return None

    @staticmethod
    def find_questions(cur, survey_id) -> list or None:
        try:
            cur.execute("SELECT * from question where survey_id='" + survey_id + "'")
            return cur.fetchall()
        except Exception as e:
            print(Fore.RED + 'Can\'t query questions for survey_id ' + survey_id + ' -> ' + e)
            return None

    @staticmethod
    def find_answers(cur, question_id) -> list or None:
        try:
            cur.execute("SELECT * from answer where question_id='" + question_id + "'")
            return cur.fetchall()
        except Exception as e:
            print(Fore.RED + 'Can\'t query answers for question_id: ' + question_id + ' -> ' + e)
            return None
