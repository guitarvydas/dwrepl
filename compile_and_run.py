import py0dws as zd
import output
import subprocess
import json

import echo

def transpileDiagram (fname):
    ret = subprocess.run (['./das2json/mac/das2json', f'{fname}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.append ("stderr", ret.stderr)
        else:
            output.append ("stderr", f"error in shell_out {ret.returncode}")
    else:
        return output.append ("stdout", ret.stdout)




def initialize_hard_coded_test (arg):
    palette = zd.initialize_component_palette ('.', '.', ['test.drawio.json'])
    return [palette, ['.', '.', 'main', ['test.drawio.json'], arg]]

def interpretDiagram (arg):
    [palette, env] = initialize_hard_coded_test (arg)
    echo.install (palette)
    zd.start (palette, env)

def compile (filename):
    print (f'transpiling diagram {filename}')
    transpileDiagram (filename)
    
def run (filename, input_text):
    print (f'running diagram {filename} with input "{input_text}"')
    output.reset ()
    interpretDiagram (input_text)
    return output.buffers
    
def compile_and_run (filename, input_text):
    compile (filename)
    r = run (filename, input_text)
    return r
