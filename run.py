import py0dws as zd
import output
import subprocess
import json

import echo

def initialize_hard_coded_test (arg):
    palette = zd.initialize_component_palette ('.', '.', ['test.drawio.json'])
    return [palette, ['.', '.', 'main', ['test.drawio.json'], arg]]

def interpretDiagram (arg):
    [palette, env] = initialize_hard_coded_test (arg)
    echo.install (palette)
    zd.start (palette, env)
    return output.get ()

def run (filename, input_text):
    print (f'running diagram {filename} with input "{input_text}"')
    output.reset ()
    # must return dictionary containing outputs {output: ...string..., error:...string...}, i.e. JSON
    return json.dumps (interpretDiagram (input_text))
