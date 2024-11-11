import compile
import run
    
def compile_and_run (filename, input_text):
    compile.compile (filename)
    r = run.run (filename, input_text)
    return r
