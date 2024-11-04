buffers = { "stdout" : "", "stderr" : "", "A" : "", "B" : "", "C" : ""}

def reset ():
    global buffers
    buffers = { "stdout" : "", "stderr" : "", "A" : "", "B" : "", "C" : ""}
    
def append (buffname, s):
    global buffers
    buffers [buffname] += (s + '\n')

def get (buffname):
    global buffers
    return buffers [buffname]
