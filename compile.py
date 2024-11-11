import subprocess
import output

def transpileDiagram (fname):
    ret = subprocess.run (['./das2json/mac/das2json', f'{fname}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.append ("error", ret.stderr)
        else:
            output.append ("error", f"error in shell_out {ret.returncode}")
    else:
        return output.append ("output", ret.stdout)

def compile (filename):
    print (f'transpiling diagram {filename}')
    return transpileDiagram (filename)
    
