buffers = { }

def reset ():
    global buffers
    buffers = { }
    
def append (buffname, s):
    global buffers
    if not buffname in buffers:
        buffers [buffname] = ""
    buffers [buffname] += (s + '\n')

def get ():
    return buffers
