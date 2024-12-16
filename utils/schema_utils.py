import json
import os

CURRENT_FILE_PATH = os.path.abspath(__file__)
TEMP_PATH = os.path.dirname(CURRENT_FILE_PATH)
ROOT_PATH = os.path.dirname(TEMP_PATH)
SCHEMAS_DIR = os.path.join(ROOT_PATH, 'schemas')


def load_schema(method_schema):
    path = os.path.join(SCHEMAS_DIR, method_schema)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
