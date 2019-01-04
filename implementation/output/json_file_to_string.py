import json
from typeguard import typechecked
@typechecked
def json_file_to_string(name_file:str)->str:
    data = open(name_file, "rt").read()
    d = str(json.loads(data))
    return data

