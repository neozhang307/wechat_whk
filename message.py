
from util import init_user,get_userlist,check_existence,is_homework,gen_hwmark,get_hwmark

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
