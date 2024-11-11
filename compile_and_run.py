import compile
import run
    
def compile_and_run (filename, input_text):
    r = compile.compile (filename)
    print (f'compile --> {r}')
    if r != None and "error" in r:
        print (f'  {"error" in r}')
    else:
        r = run.run (filename, input_text)
    return r
