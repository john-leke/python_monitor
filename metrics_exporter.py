import os
import socket
import time
from datetime import datetime
import psutil
from prometheus_client import start_http_server, Gauge
import platform

# Create Prometheus Gauges for the metrics
hostname_gauge = Gauge('system_hostname', 'Hostname of the system')
network_gauge = Gauge('network_interface_info', 'Network interface and IP address', ['interface', 'address'])
cpu_usage_gauge = Gauge('cpu_usage_percent', 'Current CPU usage percentage')
memory_total_gauge = Gauge('memory_total_bytes', 'Total memory in bytes')
memory_used_gauge = Gauge('memory_used_bytes', 'Used memory in bytes')
disk_total_gauge = Gauge('disk_total_bytes', 'Total disk capacity in bytes', ['device'])
disk_used_gauge = Gauge('disk_used_bytes', 'Used disk capacity in bytes', ['device'])
uptime_gauge = Gauge('system_uptime_seconds', 'System uptime in seconds')
load_avg_gauge = Gauge('system_load_average', 'System load average', ['interval'])
datetime_gauge = Gauge('system_datetime', 'Current system date and time', ['timezone'])

def collect_metrics():
    # Collect hostname
    hostname = socket.gethostname()
    hostname_gauge.set(1)  # Dummy value for Prometheus (gauge doesn't handle strings)
    
    # Collect network interface information
    addrs = psutil.net_if_addrs()
    for interface, address_list in addrs.items():
        for address in address_list:
            if address.family == socket.AF_INET:  # IPv4 addresses
                network_gauge.labels(interface=interface, address=address.address).set(1)

    # Collect CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_usage_gauge.set(cpu_usage)

    # Collect memory statistics
    memory_info = psutil.virtual_memory()
    memory_total_gauge.set(memory_info.total)
    memory_used_gauge.set(memory_info.used)

    # Collect disk usage statistics
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_total_gauge.labels(device=partition.device).set(usage.total)
            disk_used_gauge.labels(device=partition.device).set(usage.used)
        except PermissionError:
            # Skip partitions that are not accessible
            continue

    # Collect system uptime
    uptime = time.time() - psutil.boot_time()
    uptime_gauge.set(uptime)

    # Collect system load average (only available on Unix-like systems)
    if hasattr(os, 'getloadavg'):  # This attribute is not available on Windows
        load_avg = os.getloadavg()  # returns a tuple with 1, 5, and 15-minute averages
        load_avg_gauge.labels(interval='1m').set(load_avg[0])
        load_avg_gauge.labels(interval='5m').set(load_avg[1])
        load_avg_gauge.labels(interval='15m').set(load_avg[2])

    # Collect date and time with timezone
    now = datetime.now()
    timezone = time.tzname[0]
    datetime_gauge.labels(timezone=timezone).set(now.timestamp())

def start_metrics_server():
    # Start the Prometheus metrics server
    start_http_server(5000)
    print("Metrics server started on http://localhost:5000/metrics")

    # Periodically collect metrics every 5 seconds
    while True:
        collect_metrics()
        time.sleep(5)

if __name__ == '__main__':
    # Start the metrics server
    start_metrics_server()

