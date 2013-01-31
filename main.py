import subprocess
import re
from flask import Flask, redirect, url_for, render_template
from flask.ext.bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_FONTAWESOME'] = True

def gb(kb):
    return round(float(kb) / (1024*1024), 2)

def sysStat():
    # Gathers various system stats and return them ----
    # Checking `uptime`
    uptime = subprocess.check_output("uptime").strip()

    # Parsing out only uptime
    up = re.findall('up\s+(.*),\s+\d+\s+user', uptime)[0]

    # Checking Memory Usage
    mem = open('/proc/meminfo').read().split('\n')[:2]
    mem_total = float(re.findall(':\s+(\d+) kB', mem[0])[0])/1024
    mem_free = float(re.findall(':\s+(\d+) kB', mem[1])[0])/1024
    mem_used = mem_total-mem_free
    memory = {'total':round(mem_total,2), 'free':round(mem_free,2),
              'used':round(mem_used,2), 'percent':round(mem_used/mem_total*100, 2)}

    # Checking Disk Usage
    diskstats = subprocess.check_output("df", shell=True).split('\n')
    diskstats = [x for x in diskstats if 'rootfs' in x or 'hdd' in x]
    # sample -> ['/dev/sda2', '488179708', '76123108', '412056600', '16%', '/media/hdd']
    sd = diskstats[0].split()
    sd = {'total':gb(sd[1]), 'used':gb(sd[2]), 'free':gb(sd[3]), 'percent':sd[4][:-1]}
    hdd = diskstats[1].split()
    hdd = {'total':gb(hdd[1]), 'used':gb(hdd[2]), 'free':gb(hdd[3]), 'percent':hdd[4][:-1]}

    # Checking RPi Temperature
    temp = subprocess.check_output("vcgencmd measure_temp", shell=True).split('=')[1].rstrip("'C\n")

    # Checking HDD Status
    try:
        with open('/media/hdd/alive.txt') as f: hdd_status = True
    except IOError as e:
        hdd_status = False

    res = {'uptime':uptime, 'up':up, 'memory':memory, 'sd':sd, 'hdd':hdd, 'temp':temp, 'hdd_status':hdd_status}
    return res




@app.route('/')
def index():
    return redirect(url_for('stats'))

@app.route('/stats')
def stats():
    data = sysStat()
    return render_template('statistics.html', **data)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
