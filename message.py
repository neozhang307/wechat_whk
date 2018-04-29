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

import numpy as np

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
            return 'error id',0
    except ValueError:
        username = unkown_str
        if username in user_d.values():
            return username,1
        else:
            return 'error name',0



def is_homework(input_str, homeworkmark):
    #check if the str(string) has homeworkmark (set)
    #return the str without homeworkmark as well as whether the condition is true
    for wd in homeworkmark:
        if(input_str.find(wd)!=-1):
            return input_str[len(wd):],1
    return input_str,0


def gen_hwmark(file):
    #generate hwmark from a specific file
    hwm_l = set()
    with open("hwmark") as hwmark:
        while(True):
            line = hwmark.readline()
            if(len(line)==0):
                break
            hwm_l.add(line.replace("\n",""))
    return list(hwm_l)

def get_hwmark():
    hwm_l = []
    try:
        hwm_l = np.load('data/hwmark.list.npy')
    except IOError:
        hwm_l = gen_hwmark("data/hwmark")
        np.save('data/hwmark.list.npy', hwm_l)
    return hwm_l

def splitname(inputstr, user_d):
    #split the string to two part, real homework and name
    rt = inputstr.split('-')
    if len(rt)==1:
        rt = inputstr.split('ー')
    if len(rt)!=2:
        return "nameformerr",None,-1
    name,errcode = check_existence(rt[1], user_d)
    if errcode==0:
        return "usernotfound",None,0
    return rt[0],name,1


def save(inputstr,name,filename):
    with open(filename,'a') as op:
        op.write(name+":\n\n")
        op.write(inputstr+"\n\n")
    return
    #if it's a home work. save it

class message:
    def __init__(self):
        self.user_d,self.user_d_rev = get_userlist()
        self.hwm_l = get_hwmark() 
    #generate return masage 
    def msg_mng(self,info,filename):
        rst,errid = is_homework(info, self.hwm_l)
        if errid==0:
            return "default",0
        msg,name,errid = splitname(rst, self.user_d)
        if(errid!=1):
            return msg,errid
        save(msg,name,filename)
        return name+'君、御宿題、承りました',1
