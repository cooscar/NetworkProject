import sys
from pythonping import ping
import time
import ipaddress

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
        while True:
            try:
                ping(ip, verbose=True, count=1)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n Test cancelled by user")
                break











