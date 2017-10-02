from tester.service.web_service import WebService
from tester.utils.http_utils import post


class Requests(WebService):
    def answer(self, survey_id: str, answers: list) -> list or None:
        print('Answering survey ', end='')
        body = [{'id': answer} for (_, answer) in answers]
        return post(self.url + '/respond/' + survey_id, body)
