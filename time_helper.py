import time
 
def time2str(value):
    return value.strftime("%Y%m%d")

def str2time(value):
    return time.strptime(value,"%Y%m%d")
