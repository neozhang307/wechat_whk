
from util import init_user,get_userlist,check_existence
import numpy as np

def is_homework(input_str, homeworkmark):
    #check if the str(string) has homeworkmark (set)
    #return the str without homeworkmark as well as whether the condition is true
    for wd in homeworkmark:
        if(input_str.find(wd)!=-1):
            return input_str,1
    return input_str,0

def is_namesmt(input_str):
    if input_str=='名前':
        return 1
    return 0

def is_numbersmt(input_str):
    if input_str=='番号':
        return 1
    return 0

def is_hwkstm(input_str):
    if input_str=='宿題':
        return 1
    return 0

def is_ilusstm(input_str):
    if input_str=='説明':
        return 1
    return 0
def is_mkhwkstm(input_str):
    if input_str=='宿題の指定':
        return 1
    return 0

#recommit sakubun
def is_rebunstm(input_str):
    if input_str=='补交作文':
        return 1
    return 0

#get sakubun statement
def is_getbunstm(input_str):
    if input_str=='作文':
        return 1
    return 0


def split_msg(input_str):
    rt = input_str.split('-',1)
    if(len(rt)==1):
        rt = input_str.split('ー',1)
    if(len(rt)==1):
        rt = input_str.split(':',1)
    if(len(rt)==1):
        rt = input_str.split('：',1)
    if len(rt)==1:
        return rt[0], "", 0
    
    return rt[0],rt[1],1

        
def gen_hwmark(file):
    #generate hwmark from a specific file
    hwm_l = set()
    with open("data/hwmark") as hwmark:
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
        
        stm,msg,errid = split_msg(info)
        
        if errid==-1:
            return info,0
        if(is_namesmt(stm)==1):
            return msg,2#名前
        if(is_numbersmt(stm)==1):
            return msg,3#bango
        if(is_hwkstm(stm)==1):
            return msg,4#query hwk
        if(is_hwkstm(stm)==1):
            return msg,5#
        if(is_rebunstm(stm)==1):
            return msg,6#
        if(is_getbunstm(stm)==1):
            return msg,8#query hwk
        if(is_mkhwkstm(stm)==1):
            return msg,9#set hwk
        return info,0
