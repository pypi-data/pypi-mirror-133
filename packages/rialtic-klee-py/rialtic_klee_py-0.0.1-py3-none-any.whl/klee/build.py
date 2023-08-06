import sys

from klee.insights import InsightDict, load_insights
from klee.claims import ClaimsDirectory, KleeTestClaim
from klee.cases import InsightEngineTestCase
from typing import Dict, Union, List
from os import path

class TestCaseBuilder:
    def __init__(self, claims_dir: str, output_dir = '', history_dir = ''):
        self.claims_dir: ClaimsDirectory = ClaimsDirectory(claims_dir)
        self.output_dir = path.realpath(output_dir) if output_dir else ''
        self.history_dir = path.realpath(history_dir) if history_dir else ''

        self.insights: InsightDict = load_insights()
        self.claims_dir.load_claims()

        self.init_test_plan()

    def build_all_cases(self) -> Dict[str, InsightEngineTestCase]:
        all_cases = {}
        for node_label, kt_claim in self.claims_dir.claims.items():
            all_cases[node_label] = self.build_test_case(kt_claim)
        return all_cases

    def build_test_case(self, node: Union[str, KleeTestClaim]) -> InsightEngineTestCase:
        """accepts node label or a node itself"""
        kt_claim = self.claims_dir.claims[node] if isinstance(node, str) else node

        if kt_claim.node_id in self.insights:
            # noinspection PyTypeChecker
            kt_case = InsightEngineTestCase(self, kt_claim)
            if not kt_case.test_plan.validate_case(kt_case):
                print(f"Unable to verify that {kt_claim.label_id} has been correctly built.")
                sys.exit(0)
            if self.output_dir:
                kt_case.save_to_folder(self.output_dir)
            if self.history_dir:
                kt_case.save_to_history(self.history_dir)
            return kt_case
        else:
            print("Unable to find insights for ", kt_claim.label_id)

    def build_node_labels(self, node_labels: List[str]) -> Dict[str, InsightEngineTestCase]:
        test_cases = {}

        if not node_labels:
            test_cases.update(self.build_all_cases())

        for label in node_labels:
            kt_case = self.build_test_case(label.split('.')[0])
            test_cases[kt_case.claim.label_id] = kt_case

        return test_cases

    def init_test_plan(self):
        pass
