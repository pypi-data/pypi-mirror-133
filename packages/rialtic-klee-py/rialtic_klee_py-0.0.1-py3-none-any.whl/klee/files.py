import csv, json, shutil, pickle, os, sys

from klee.consts import *
from klee.consts import __version__
from fhir.resources import domainresource
from fhir.resources.claim import Claim
from typing import Dict, Any

def save_json(data, *paths):
    target = os.path.join(*paths)
    log.debug('saving json: %s', target)
    os.makedirs(os.path.dirname(target), exist_ok = True)
    with open(target, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 2)

def read_claim(*paths) -> Claim:
    return Claim.parse_obj(read_json(*paths))

def read_json(*paths) -> Dict[Any, Any]:
    target = os.path.join(*paths)
    log.debug('reading json: %s', target)
    with open(target) as file:
        return json.load(file)

def read_str(*paths) -> str:
    target = os.path.join(*paths)
    log.debug('reading str: %s', target)
    with open(target) as file:
        return file.read()

def read_csv(*paths, normalize = False, **kwargs):
    target = os.path.join(*paths)
    log.debug('reading csv: %s', target)
    with open(target) as file:
        reader = csv.DictReader(file, **kwargs)
        new_list = []
        if normalize:
            for row in reader:
                new_row = {}
                for col in row:
                    new_col = col.lower()
                    new_col = new_col.replace(" ", "")
                    new_col = new_col.replace("-", "")
                    new_col = new_col.replace("_", "")
                    new_row[new_col] = row[col]
                new_list.append(new_row)
        else:
            new_list.extend(reader)
        return new_list

class KleeFile:
    def __init__(self, filename, mode, **kwargs):
        self.path = os.path.join(os.getcwd(), filename)
        self.file = open(self.path, mode, **kwargs)
        self.mode = mode

    def read_data(self):
        if self.mode == 'rb':
            return pickle.load(self.file)
        else:
            return json.load(self.file)

    def write_and_flush(self, data):
        if self.mode == 'wb':
            pickle.dump(data, self.file)
        else:
            json.dump(data, self.file)

        self.file.flush()

    def delete_file(self):
        self.file.close()
        if os.path.exists(self.file.name):
            os.remove(self.file.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete_file()

    def __del__(self):
        self.delete_file()

class Inspection:
    def __enter__(self):
        sys.path.append(os.getcwd())

    def __exit__(self, type, value, traceback):
        sys.path.pop()

def fhir_to_json(obj: domainresource.DomainResource) -> Dict:
    return json.loads(obj.json())

# Private functions
import logging, dotenv

def _init_structure():
    root = os.path.dirname(__file__)
    os.makedirs(KLEE_FOLDER, exist_ok=True)

    def copy_file(full_name, hard_copy = False):
        src = os.path.join(root, 'resource', full_name)
        dest = os.path.join('test_cases', full_name)

        if not os.path.exists(dest) or hard_copy:
            parent = os.path.dirname(dest)
            os.makedirs(parent, exist_ok=True)
            shutil.copy2(src, dest)

    copy_file('.gitignore', True)

def _configure_log():
    log_file = logging.FileHandler(filename = KLEE_FOLDER + "klee.log", mode="w")
    log_file.setFormatter(logging.Formatter("%(asctime)s: [%(levelname)s] %(message)s"))
    log.addHandler(log_file)

    std_err = logging.StreamHandler(stream=sys.stderr)
    std_err.setLevel(os.getenv('KLEE_LOG_LEVEL', 'WARNING'))
    std_err.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    log.addHandler(std_err)

    log.info("klee version: %s", __version__)

# ensure directories exists
# this might be better suited elsewhere as a klee_init('repo_directory')
_init_structure()
dotenv.load_dotenv()
_configure_log()

