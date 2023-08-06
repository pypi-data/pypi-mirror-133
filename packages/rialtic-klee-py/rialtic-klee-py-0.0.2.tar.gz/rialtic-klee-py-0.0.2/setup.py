# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klee', 'klee.plans', 'klee.pyt']

package_data = \
{'': ['*'], 'klee': ['resource/*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'fhir.resources>=6.1.0,<7.0.0',
 'insight-engine-schema-python==0.2.1',
 'pytest-html>=3.1.1,<4.0.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.26,<3.0']

entry_points = \
{'console_scripts': ['klee = klee:cli']}

setup_kwargs = {
    'name': 'rialtic-klee-py',
    'version': '0.0.2',
    'description': 'Internal workflow/testing utility',
    'long_description': "# Rialtic Klee Overview\n\nThis library should serve to replace our loose scripts `build_test_cases.python`, `test_engine.python`, `smoke_test.python` in almost all cases.\n\n_You are still be able to write an interim `test_engine` script using library calls, when new engines create yet unaddressed requirements. However, this should be kept to a minimum._\n\n## The Command Line Utility\nThis library provides a command line utility in order to conduct local tests (with automatic building), and remote (smoke) tests.\n- `klee build [<optional_test_cases>]`\n- `klee test [<optional_test_cases>]`\n- `klee smoke [<optional_test_cases>]`\n\nnote: could we perhaps reconcile the diverged logic of SPEs/MPEs?\n\n## The Library API\n\n### File: `klee.build`\n\n##### Command: `klee build [<optional_test_cases>]`\nWith the following arguments,\n- `-p <plan-type>`, default: `'default'`\n- `-c <claims-dir>`, default: `'test_claims'`\n- `-o <output-dir>`, default: `''`, suggested: `test_cases/json_cases`\n- `-h <history-dir>`, default: `''`, suggested: `test_cases/history`\n\n### File: `klee.plans`\n\n##### Class Interface\n```python\nclass <LegacyTestPlan|MPETestPlan>(EngineTestPlan):\n  def __init__(self, claims_dir = 'test_claims', output_dir = '', history_dir = ''):\n    ...\n  def build_all_cases(self) -> Dict[str, InsightEngineTestCase]:\n    ...\n  def build_test_case(self, node: Union[str, KleeTestClaim]) -> InsightEngineTestCase:\n    ...\n  def build_node_labels(self, node_labels: List[str]) -> Dict[str, InsightEngineTestCase]:\n    ...\n```\n\n### File: `klee.test`\n\n##### Command: `klee test [<optional_test_cases>]`\nWith the following arguments,\n- `-p <plan_type>`, default: `'default'`\n- `-c <claims_dir>`, default: `'test_claims'`\n\n##### Command: `klee smoke [<optional_test_cases>]`\nWith the following arguments,\n- `-p <plan_type>`, default: `'default'`\n- `-c <claims_dir>`, default: `'test_claims'`\n\n##### Class Interface\n```python\nclass PyTestUtility:\n    @staticmethod\n    def invoke_cases(test_cases: Dict[str, InsightEngineTestCase], style = 'local'):\n        ...\n    @staticmethod\n    def env_vars_present():\n        ...\n\n# todo: staging api functions\n```\n\n# Library Structure\n~~Functionality for competing logic within a step is separated into individual files. Within a module's `__init__` file there will be an exported function which will attempt the implementations for that particular step in the current preferred order.~~\n\n## Supported Test Plan Formats\n\n### File: `klee.plans.*`\nExposes\n```python\n@abstractclass\nclass EngineTestPlan(TestCaseBuilder):\n    def claim_line(self, claim: KleeTestClaim):\n        ...\n    def get_history(self, claim: KleeTestClaim):\n        ...\nclass LegacyTestPlan(EngineTestPlan):\n    ...\nclass MPETestPlan(EngineTestPlan):\n    ...\n```\n\n## Supported Test Claims Formats\n\n### File: `klee.claims`\nExposes\n```python\nclass ClaimsDirectory:\n    ...\n\nclass KleeTestClaim:\n    ...\n\n```\n\n[Test Claim/Tab Naming Conventions](http://community.rialtic.io/docs/spec/test_claims/)\n\n## Supported Insight/Defenses Formats\n\n### File: `klee.insights`\nExposes\n```python\nclass InsightDict(dict):\n    ...\nclass InsightText:\n    ...\n\ndef load_insights() -> InsightDict:\n    ...\ndef read_engine_result() -> InsightDict:\n    ...\ndef read_local_files() -> InsightDict:\n    ...\n```\n\nFlow:\n- `result.EngineResult.insight_<type|text|defense>` > `<insights_and_defenses|insights|defense>.csv` > `<insights|defense>.json` > `test_plan.csv + test_dataset.csv ???`\n\n## Library File Utils\n\n### File: `klee.files`\nExposes\n```python\nclass KleeFile:\n    ...\n\nclass Inspection:\n    ...\n\ndef read_claim(*paths) -> Claim:\n    ...\ndef read_csv(*paths) -> List[Rows]:\n    ...\ndef read_json(*paths) -> JSON/dict:\n    ...\ndef read_str(*paths) -> str:\n    ...\n\ndef save_json(object, *path):\n    ...\n```\n\n\n## Mass Testing\nWe could potentially create a [Github Action](https://docs.github.com/en/actions) to test (by a yet to be decided trigger) against a range of engine repos.\n\n## Versioning\nAs the design of this library evolves over time, engines will be written depending on certain assumptions made by this test suite. To address these,  we will be using semantic versioning (https://semver.org/).\nIf features/tests are removed, it should be considered a **major** breaking change.\nIf features/tests are added, it should be considered a **minor** api change.\nIf there is a bug introduced, a bugfix **patch** should be released.\n\nIn the format of `v<MAJOR>.<MINOR>.<PATCH>`, which can be used with Pipenv's compatibility operator to accept all non breaking changes as `rialtic-klee-python ~= <MAJOR>.<MINOR>`.\n\n## Repository Branches\nBranches:\n- `development` serves as our development/specification discussion head\n- `v<MAJOR>.<MINOR>` should be used for retroactive fixes\n\nTags:\n- `v<MAJOR>.<MINOR>.<PATCH>` for each release\n\n<hr>\n\n![ships in the dark](ships_in_the_dark.jpg)\n",
    'author': 'Rialtic',
    'author_email': 'engines.data@rialtic.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rialtic-community/rialtic-klee-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
