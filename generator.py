# import dependencies
import os
from flask import Flask
import psutil
import signal
import sys
# For CPU test
from multiprocessing import Pool
from multiprocessing import cpu_count

# bootstrap the app
app = Flask(__name__)

# set the port dynamically with a default of 3000 for local development
port = int(os.getenv('PORT', '3000'))

@app.route('/')
def hello_world():
    return 'Welcome to the bad app, never try it at home' 

@app.route('/memory_error')
def memory_error():
    print ("Generate memory error")
    a = ' ' * 1 * (10 ** 10)
    return None
@app.route('/overflow_error')
def overflow_error():
    print ("Generate overflow error")
    a = ' ' * 1 * (10 ** 24)
    return None
@app.route('/break')
def emulate_break():
    print ("Simulate break")
    try:
        a = ' ' * 1 * (10 ** 24)
    except OverflowError:
        print ("Overflow error")
        sys.exit(22) 

@app.route('/memory_load')
def memory_load():
    MEGA = 10 ** 6
    pid = os.getpid()
    i = 0
    while True:
        try:
            a = ' ' * (i * 10 * MEGA)
            del a
        except MemoryError:
            break
        i += 1
    max_i = i - 1

    _ = ' ' * (max_i * 10 * MEGA)
    py_process = psutil.Process(pid)                                                                                           
    used_memory = py_process.get_memory_info()[1] / MEGA
    print ("Used mem %s", used_memory)
    return used_memory


### CPU load

def f(x):
    while True:
        x*x

@app.route('/cpu_load')
def cpu_load():
    processes = cpu_count()
    print ('utilizing %d cores\n', processes)
    pool = Pool(processes)
    pool.map(f, range(processes))
    return "CPU load"

@app.route('/kill_itself')
def kill_itself():
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)
    print ("Kill signal recieved from user")
    return None 

# start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
