import py0dws as zd
import output
import subprocess

import echo

def initialize_hard_coded_test (arg):
    palette = zd.initialize_component_palette ('.', '.', ['test.drawio.json'])
    return [palette, ['.', '.', 'main', ['test.drawio.json'], arg]]

def transpileDiagram (fname):
    ret = subprocess.run (['./das2json/mac/das2json', f'{fname}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.append ("stderr", ret.stderr)
        else:
            output.append ("stderr", f"error in shell_out {ret.returncode}")
    else:
        return output.append ("stdout", ret.stdout)

def interpretDiagram (arg):
    [palette, env] = initialize_hard_coded_test (arg)
    echo.install (palette)
    zd.start (palette, env)

def compile_and_run (filename, input_text):
    output.reset ()
    print (f'transpiling diagram {filename}')
    transpileDiagram (filename)
    print (f'running diagram {output.buffers}')
    interpretDiagram (input_text)
    return {
        "output" : output.get ("stdout"),
        "A" : output.get ("A"),
        "B": output.get ("B"),
        "C": output.get ("C"),
        }
