import json
import six
import numpy as np


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


def init_user(filename):
    ## int user from filename
    myl = []
    myl_rev = []
    with open(filename) as user_f:
        while(True):
            line = user_f.readline()
            if(len(line)==0):
                break
            tup = line.split('\t')
            myl.append((int(tup[1]),tup[0]))
    myl.sort()
    for k,v in myl:
        myl_rev.append((v,k))
    user_d = dict(myl)
    user_d_rev = dict(myl_rev)
    return user_d,user_d_rev



def get_userlist():
    ## simply init user
    user_d = {}
    user_d_rev = {}
    try:
        user_d = np.load("data/user.dic.npy").item()
        user_d_rev = np.load("data/user_rev.dic.npy").item()
    except IOError:
        user_d,user_d_rev = init_user("data/person")
        np.save('data/ser.dic.npy', user_d)
        np.save('data/user_rev.dic.npy', user_d_rev)
    return user_d,user_d_rev

def check_existence(unkown_str, user_d):
    ## check if a string is a user
    ## if is a user, return the username
    ## if is not a user, return 0
    try:
        tmp_val = int(unkown_str)
        if tmp_val<=517 and tmp_val>=501:
            return user_d[tmp_val],1
        else:
            return unkown_str,0
    except ValueError:
        username = unkown_str
        if username in user_d.values():
            return username,1
        else:
            return unkown_str,0




