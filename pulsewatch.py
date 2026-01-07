import time
import psutil
import socket
from datetime import datetime

LOG_FILE = "pulsewatch.log"
CHECK_INTERVAL = 10

CPU_ALERT = 85
RAM_ALERT = 90
DISK_ALERT = 90


def internet_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def get_stats():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "internet": internet_connected()
    }


def check_alerts(stats):
    alerts = []
    if stats["cpu"] > CPU_ALERT:
        alerts.append("⚠ HIGH CPU")
    if stats["ram"] > RAM_ALERT:
        alerts.append("⚠ HIGH RAM")
    if stats["disk"] > DISK_ALERT:
        alerts.append("⚠ LOW DISK SPACE")
    if not stats["internet"]:
        alerts.append("⚠ INTERNET DOWN")
    return alerts


def log(stats, alerts):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_text = " | ".join(alerts) if alerts else "OK"

    line = (
        f"[{ts}] CPU:{stats['cpu']}% "
        f"RAM:{stats['ram']}% "
        f"DISK:{stats['disk']}% "
        f"NET:{'ON' if stats['internet'] else 'OFF'} "
        f"STATUS:{alert_text}\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(line)

    print(line.strip())


def main():
    print("PulseWatch running… CTRL+C to stop")
    while True:
        stats = get_stats()
        alerts = check_alerts(stats)
        log(stats, alerts)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
