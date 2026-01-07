import time
import psutil
import socket
from datetime import datetime

LOG_FILE = "pulsewatch.log"
CHECK_INTERVAL = 10  # seconds


def internet_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    online = internet_connected()

    return {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "internet": online
    }


def log_stats(stats):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "ONLINE" if stats["internet"] else "OFFLINE"

    log_entry = (
        f"[{timestamp}] "
        f"CPU: {stats['cpu']}% | "
        f"RAM: {stats['memory']}% | "
        f"Disk: {stats['disk']}% | "
        f"Internet: {status}\n"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

    print(log_entry.strip())


def main():
    print("PulseWatch started. Press CTRL+C to stop.")
    while True:
        stats = get_system_stats()
        log_stats(stats)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
