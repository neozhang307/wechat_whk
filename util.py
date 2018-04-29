def get_text(filename):
    
    with open("./data/txt/"+filename) as finput:
        tmp = ""
        while True:
            line = finput.readline()
            if len(line) == 0:
                break
            tmp+=line
        return tmp
    return "BAD CODE"
