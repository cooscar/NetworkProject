import socket, threading, sys, ipaddress
from queue import Queue
from datetime import datetime

THREADS = 100
TIMEOUT = 2.0
print_lock = threading.Lock()

target_ip = None
start = None
end = None

SERVICE_SIGNATURES = {
    'SSH-': 'SSH Server',
    'HTTP/': 'HTTP Server',
    'FTP': 'FTP Server',
    'SMTP': 'SMTP Mail Server',
    '220': 'Mail/FTP Server',
    'MySQL': 'MySQL Database',
    'PostgreSQL': 'PostgreSQL Database',
    'Redis': 'Redis Database',
    'MongoDB': 'MongoDB Database',
    'RFB': 'VNC Server',
}

def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((ip, port))
        try:
            b = s.recv(1024).decode("utf-8", "ignore").strip()
        except:
            s.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            b = s.recv(1024).decode("utf-8", "ignore").strip()
        s.close()
        return b
    except:
        return None

def identify_service(banner, port):
    if not banner: return "Unknown Service"
    for s, n in SERVICE_SIGNATURES.items():
        if s in banner: return f"{n} | Banner: {banner[:100]}"
    fallback = {21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',
                143:'IMAP',443:'HTTPS',3306:'MySQL',5432:'PostgreSQL',6379:'Redis',
                8080:'HTTP-Alt',27017:'MongoDB',3389:'RDP',5900:'VNC'}
    return f"{fallback.get(port,'Unknown')} | Banner: {banner[:100]}"

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        r = s.connect_ex((ip, port))
        s.close()
        if r == 0:
            b = grab_banner(ip, port)
            return (port, identify_service(b, port) if b else "Open (No banner)")
        return None
    except:
        return None

def worker(ip, q, out):
    while True:
        p = q.get()
        if p is None: break
        r = scan_port(ip, p)
        if r:
            with print_lock:
                print(f"[+] Port {r[0]:5d} | {r[1]}")
                out.append(r)
        q.task_done()

def scan_host(ip, a=1, b=65535):
    print("\n" + "="*80)
    print("Scanning:", ip, "range", f"{a}-{b}")
    print("="*80, "\n")

    queue = Queue(); results = []; ts = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(ip, queue, results), daemon=True)
        t.start(); ts.append(t)
    for p in range(a, b+1): queue.put(p)
    queue.join()
    for _ in range(THREADS): queue.put(None)
    for t in ts: t.join()

    print("\n" + "="*80)
    print("Finished:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("="*80, "\n")

    if results:
        print(f"Found {len(results)} port(s):\n")
        for p, s in sorted(results): print(f"  {p:5d} - {s}")
    else:
        print("No open ports detected.")
    return results



def valid_ip(x):
    try:
        ipaddress.ip_address(x)
        return True
    except: return False

def valid_port(x):
    try:
        return 1 <= int(x) <= 65535
    except:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        i = 1
        while i < len(sys.argv):
            v = sys.argv[i]

            if v in ("-i", "-I"):
                if i+1 < len(sys.argv) and valid_ip(sys.argv[i+1]):
                    target_ip = sys.argv[i+1]
                    i += 1
                else:
                    print("Bad IP given.")
            elif v in ("-r", "-R"):
                if i+1 < len(sys.argv) and valid_port(sys.argv[i+1]):
                    start = int(sys.argv[i+1])
                    if i+2 < len(sys.argv) and valid_port(sys.argv[i+2]):
                        end = int(sys.argv[i+2]); i += 1
                    else:
                        end = 65535
                    i += 1
                else:
                    print("Bad starting port.")
            i += 1

    if not target_ip:
        print("Usage: luma scan -i <IP> [-r start end]")
        sys.exit(1)

    if start is None: start = 1
    if end is None: end = 65535

    try:
        socket.inet_aton(target_ip)
        scan_host(target_ip, start, end)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print("Err:", e)
        sys.exit(1)
