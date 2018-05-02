
from util import init_user,get_userlist,check_existence
import numpy as np

def is_homework(input_str, homeworkmark):
    #check if the str(string) has homeworkmark (set)
    #return the str without homeworkmark as well as whether the condition is true
    for wd in homeworkmark:
        if(input_str.find(wd)!=-1):
            return input_str[len(wd):],1
    return input_str,0

def is_namesmt(input_str):
    rt = input_str.split('-')
    if(len(rt)==1):
        rt = input_str.split('ー')
    if(len(rt)==1):
        rt = input_str.split(':')
    if(len(rt)==1):
        rt = input_str.split('：')
    if len(rt)!=2:
        return input_str,-1
    if rt[0]=='名前':
        return rt[1],1
    if rt[0]=='番号':
        return rt[1],1
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
    def msg_mng(self,info):
        rst,errid = is_homework(info, self.hwm_l)
        if errid==1:
            return rst,1#宿題
        rst,errid = is_namesmt(info)
        if errid==1:
            return rst,2#名前
        return info,0
