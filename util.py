import json
import six

def to_text(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def get_text(filename):
    tmp = ""
    try:
        finput = open("./data/txt/"+filename)
        tmp = ""
        while True:
            line = finput.readline()
            if len(line) == 0:
                break
            tmp+=line
        return tmp
    except IOError:
        return "BAD INPUT"

def json_loads(s):
    s = to_text(s)
    return json.loads(s)


def json_dumps(d):
    return json.dumps(d)


