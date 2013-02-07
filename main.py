from getstats import *
from flask import Flask, redirect, url_for, render_template
from flask.ext.bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

uptime_ = uptime()
cpu_load_ = cpu_load()
mem_info_ = mem_info()
temp_ = temp()
who_ = who()
network_usage_ = network_usage()
disk_info_ = disk_info()
hdd_status_ = hdd_status()

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_FONTAWESOME'] = True

@app.route('/')
def index():
    return redirect(url_for('stats'))

@app.route('/stats')
def stats():
    return render_template('statistics.html', **globals())

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)