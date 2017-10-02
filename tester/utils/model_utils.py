def compare_surveys(expected: dict, got: dict) -> bool:
    return expected['name'] == got['name'] \
           and expected['country_code'] == got['country_code'] \
           and compare_questions(expected['questions'], got['questions'])


def compare_questions(expected, got):
    if len(expected) != len(got):
        return False
    for e in range(0, len(expected)):
        if expected[e]['name'] != got[e]['name'] \
                or not compare_answers(expected[e]['answers'], got[e]['answers']):
            return False
    return True


def compare_answers(expected, got):
    if len(expected) != len(got):
        return False
    for e in range(0, len(expected)):
        if expected[e]['name'] != got[e]['name']:
            return False
    return True
