from flask import Flask, jsonify
import psutil
import socket

app = Flask(__name__)


def internet_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


@app.route("/api/status")
def status():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "internet": internet_connected()
    })


@app.route("/")
def index():
    return """
    <h1>PulseWatch Dashboard</h1>
    <pre id="data">Loading...</pre>
    <script>
    setInterval(async () => {
        const r = await fetch('/api/status');
        const d = await r.json();
        document.getElementById('data').innerText =
            JSON.stringify(d, null, 2);
    }, 2000);
    </script>
    """
    

app.run(host="0.0.0.0", port=5000)
