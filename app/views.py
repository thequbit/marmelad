from app import app

import json
import uuid
import os

import subprocess 

from flask import (
    request,
    render_template,
)

def exec(cmd):

    #lines = ''

    #with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, timeout=10) as p:
       	#for line in p.stdout:
            #print(line, end='')
            #lines += line.decode('utf-8') + '\r\n'
        #for line in p.stderr:
        #for line in iter(p.stderr.readline, ''):
            #print(line)
            #lines += line.decode('utf-8')

    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=10).decode('utf-8')

    #error_code = 0
    #if p.returncode != 0:
    #    raise subprocess.CalledProcessError(p.returncode, p.args)
        #error_code = p.returncode

    #return lines, error_code
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/python')
def python():
    return render_template('python.html')

@app.route('/run_script', methods=['POST'])
def run_script():

    payload = json.loads(request.get_data().decode('utf-8'))
    
    print(json.dumps(payload, indent=4))

    filename = str(uuid.uuid4()).encode('utf-8')

    with open(filename, 'w') as f:
        f.write(payload['code'])
    
    output = exec(['python', filename])
    
    #os.remove(filename)

    return json.dumps(
        dict(
            success=True,
            #filename=str(filename),
            output=output,
            #error_code=error_code,
        )
    )