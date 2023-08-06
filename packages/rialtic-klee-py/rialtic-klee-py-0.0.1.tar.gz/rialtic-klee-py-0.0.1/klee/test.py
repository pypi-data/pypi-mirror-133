import pathlib, time, uuid, pytest, requests, os

from fhir.resources.claim import Claim
from typing import Dict

from klee.files import fhir_to_json, KleeFile
from klee.cases import InsightEngineTestCase
from klee.consts import *


class PyTestUtility:
    @staticmethod
    def invoke_cases(test_cases: Dict[str, InsightEngineTestCase], style = 'local'):
        log.info(f"Found {len(test_cases)} test cases to be run")
        os.environ['RIALTIC_HISTORY_FILE'] = HISTORY_FILE

        with KleeFile(BINARY_FILE, 'wb') as file:
            file.write_and_flush(test_cases)
            pytest.main(["-vvv", "-s", "--pyargs", "klee.pyt." + style])

        print(f"Klee ran a total of {len(test_cases)} test cases.")

    @staticmethod
    def env_vars_present():
        for var in ('RIALTIC_DATA_ENV', 'RIALTIC_REF_DB', 'APIKEY'):
            if not os.getenv(var):
                print(f"Please set '{var}' on your environment")
                return False
        return True

def url_for(text):
    return "/".join(["https://ommunitystaging-api.dev.rialtic.dev",
        "0666ef1a-9f9a-4e68-b262-a3634006d88b", text])

def run_full_query(claim: Claim):
    print("Uploading claim", claim.id)
    log.info('uploading claim: %s', claim.json())
    result = submit_transaction(claim).json()

    time.sleep(1.25)
    if result['status'] != 'ok':
        output = "%s :: %s" % (result['status'], result['statusDetails'])
        log.error(output); raise Exception(f"API Respone: {output}")
    print(f"Transaction <{result['transactionId']}> submission ok!")

    time.sleep(1.25)
    result = request_insights(result['transactionId']).json()
    executions = result.get('insights', [])
    print("===="*16+f">> Found {len(executions)} engine executions")
    for name in {x['engineName'] for x in executions}:
        print(
            "    [+] ID:", {v['engineId'] for v in executions if v['engineName'] == name}.pop().split(':')[0].ljust(24),
            "    [+] Engine:", name.split('/')[1].ljust(32),
            "    [+] Versions:", ", ".join(v['githubReleaseVersion'] for v in executions if v['engineName'] == name).ljust(48),
        )

    selected = sorted(executions, key = lambda x: x['githubReleaseVersion']).pop()
    log.info("using result: %s %s %s", selected['engineId'], selected['engineName'],
             selected['githubReleaseVersion']); return selected

def request_insights(tx_id: str):
    engine_name = "rialtic-community/"+get_engine_info()
    print("Requesting insights from", engine_name)
    return requests.post(url_for('insights'), json = {
        "insightEngineNames": engine_name,
        "transactionId": tx_id,
    })

def submit_transaction(claim: Claim):
    return requests.post(url_for('claims'), json = {
        "clientId": "rialtic-klee-py",
        "context": "<nocontext>",
        "claim": fhir_to_json(claim),
        "timeout": 450,
    })

def get_engine_info():
    repo, version = pathlib.Path.cwd().stem, ''
    return ":".join([x for x in (repo, version) if x])

def new_dead_claim():
    no_patient = str(uuid.uuid4())
    return Claim.parse_obj({
        "id": "72-6961-6c74-6963",
        "contained": [{"id": f"{no_patient}", "resourceType": "Patient"}],
        "billablePeriod": {"end": "1970-04-30", "start": "1970-04-30"}, "created": "1900-01-01",
        "insurance": [{"coverage": {"reference": "#No-Coverage"}, "focal": True, "sequence": 1}],
        "patient": {"reference": f"#{no_patient}"}, "priority": {"coding": [{"code": "normal"}]},
        "provider": {"reference": "#No-Provider"}, "status": "active",
        "type": {"coding": [{"code": "professional"}]}, "use": "claim",
        "identifier": [{"value": "dead claim"}],
        "resourceType": "Claim",
    })