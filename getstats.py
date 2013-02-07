import subprocess
import re
def uptime():
    # Returns `uptime` command info and up time as a list
    stats = subprocess.check_output("uptime").strip()
    uptm = re.findall('up\s+(.*),\s+\d+\s+user', stats)[0]
    data = [stats, uptm]
    return data

def cpu_load():
    # Returns cpu load data as a list
    data = re.findall('\d+\.\d+', subprocess.check_output("uptime").strip())
    return data

def mem_info():
    # Returns memory usage information as a dictionary
    mem = open('/proc/meminfo').read().split('\n')[:2]
    mem_total = float(re.findall(':\s+(\d+) kB', mem[0])[0])/1024
    mem_free = float(re.findall(':\s+(\d+) kB', mem[1])[0])/1024
    mem_used = mem_total-mem_free
    data = {'total':round(mem_total,2), 'free':round(mem_free,2),
            'used':round(mem_used,2), 'percent':round(mem_used/mem_total*100, 2)}
    return data

def temp():
    # Returns system temperature as string
    # Catching error since reading temperature during high load sometimes gives no response
    try:
        temp = subprocess.check_output("vcgencmd measure_temp", shell=True).split('=')[1].rstrip("'C\n")
        return temp
    except Exception as e:
        return e

def who():
    # Returns info of users connected to the system as a list of dictionary
    who = subprocess.check_output("who", shell=True).split('\n')
    data = []
    for session in who[:-1]:
        session = session.split()
        session_time = session[2] + ' ' + session[3]
        host = session[4]
        data.append({'time':session_time, 'host':host})
    return data

def network_usage(interface='wlan0'):
    # Returns network usage data as a dictionary
    usage = subprocess.check_output("ifconfig {0} | grep RX\ bytes".format(interface), shell=True).strip()
    usage = re.findall('s:(\d+)', usage)
    total = (float(usage[0]) + float(usage[1])) / (1024*1024)
    rx = float(usage[0]) / (1024*1024)
    tx = float(usage[1]) / (1024*1024)
    data = {'rx':rx, 'tx':tx, 'total':total}
    return data

def disk_info():
    # Returns disk usage statistics as dictionaries in a list
    disk_raw = subprocess.check_output("df -hT | grep -vE 'tmpfs|rootfs|mmcblk|Filesystem'", shell=True).strip()
    data = []
    for disk in disk_raw.split('\n'):
        disk = disk.split()
        data.append({
            'mount_device':disk[0],
            'file_sys':disk[1],
            'total':disk[2][:-1],
            'used':disk[3][:-1],
            'free':disk[4][:-1],
            'percent':disk[5][:-1],
            'mount_path':disk[6]
        })
    return data

def hdd_status():
    try:
        with open('/media/hdd/alive.txt') as f: hdd_status = True
    except IOError as e:
        hdd_status = False
    return hdd_status