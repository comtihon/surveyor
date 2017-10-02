from tester.service.web_service import WebService
from tester.utils.http_utils import get
from tester.utils.http_utils import post


class Manager(WebService):
    def get(self, survey_id: str) -> dict or None:
        print('Getting survey ', end='')
        return get(self.url + '/survey/' + survey_id)

    def create(self, survey: dict) -> str or None:
        print('Creating survey ', end='')
        return post(self.url + '/survey', survey)
