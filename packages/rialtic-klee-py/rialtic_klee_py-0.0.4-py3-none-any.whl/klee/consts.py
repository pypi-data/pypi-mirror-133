from pkg_resources import get_distribution
__version__ = get_distribution('rialtic-klee-py')

# Internal Constants
KLEE_FOLDER = "test_cases/.klee-internal/"
HISTORY_FILE = KLEE_FOLDER + '_history.json'
BINARY_FILE = KLEE_FOLDER + '_cases.klee'

# Logging Init
from logging import Logger as _Logger
log = _Logger('klee-logs', level = 0)

import datetime as _dt
INIT_TIME = int(_dt.datetime.utcnow().timestamp())

# Level	Numeric value
# CRITICAL	50
# ERROR	40
# WARNING	30
# INFO	20
# DEBUG	10
# NOTSET	0
