from schema.insight_engine_response import InsightEngineResponse
from klee.cases import InsightEngineTestCase
from klee.consts import log
from klee import test
import pytest, time

@pytest.fixture(scope='module')
def run_engine():
    def closure(case: InsightEngineTestCase) -> InsightEngineResponse:
        test.run_full_query(test.new_dead_claim())

        for historic in case.request.history:
            test.run_full_query(historic.claim)
            time.sleep(1.25)

        response = test.run_full_query(case.request.claim)
        for key in ('commitSha', 'engineId', 'engineName', 'githubReleaseVersion'):
            del response[key]
        for item in response['insights']:
            item['defense']['referenceData'] = []

        return InsightEngineResponse.parse_obj(response)
    return closure

pytest.register_assert_rewrite("klee.pyt.shared")
from klee.pyt.shared import TestEngineV1 as TestStaging

log.info('Start smoke testing \n')
