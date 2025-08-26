import socket
from datetime import datetime
from pathlib import Path
import csv
import argparse
import time

try:
    from pynput.mouse import Controller as MouseController, Button
    mouse = MouseController()
except ImportError:
    mouse = None
    print("pynput not installed -> mouse click simulation disabled.")

def log_message(log_file, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    row = {"timestamp": ts, "message": msg}

    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_exists = log_file.exists()

    with open(log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "message"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def simulate_click(x=70, y=800):
    """Simulate a left mouse click wherever the cursor is."""
    if mouse:
        mouse.position = (x, y)
        time.sleep(0.05)
        mouse.click(Button.left, 1)
    else:
        print("Mouse simulation not available (install pynput).")

def main(host="0.0.0.0", port=5005, simulate_ui=False):
    log_file = Path.cwd() / "logs" / "network_markers.csv"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for UDP packets on {host}:{port} ...")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            msg = data.decode("utf-8").strip() 
            simulate_click()
            print(f"[RECEIVED] {msg} from {addr}")

            # Log to CSV
            log_message(log_file, msg)

    except KeyboardInterrupt:
        print("\nExiting listener...")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brainsight Marker Listener")
    parser.add_argument("--port", type=int, default=5005, help="UDP port to listen on")
    parser.add_argument("--simulate-ui", action="store_true", help="Simulate mouse click in Brainsight")
    args = parser.parse_args()

    main(port=args.port, simulate_ui=args.simulate_ui)
