import subprocess
import output

def run (filename, input_text):
    output.reset ()
    print (f'running diagram {filename} with input "{input_text}"')
    ret = subprocess.run (['python3', 'subprocess_run.py', f'{filename}', f'{input_text}'], capture_output=True, encoding='utf-8')
    if  not (ret.returncode == 0):
        if ret.stderr != None:
            output.append ("error", ret.stderr)
        else:
            output.append ("error", f"error in shell_out {ret.returncode}")
    else:
        output.append ("output", ret.stdout)
    return output.get ()
