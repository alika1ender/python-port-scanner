import socket
import sys

if len(sys.argv) != 4:
    print("Usage: python3 scanner.py <host> <start_port> <end_port>\n")
    sys.exit()

host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
ports_open = 0

# Determine the common service for a port
def get_service_name(port):
    try:
        service = socket.getservbyport(port)
        if service:
            return service
        else:
            return "unknown"
    except:
        return "unknown"

# Read data sent by the service
def grab_banner(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP over IPv4
        s.settimeout(1)
        s.connect((host, port))

        # For web servers, send a basic HTTP request
        if port == 80:
            s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")

        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()

        if banner:
            first_line = banner.split("\n")[0]
            return first_line
        else:
            return "no banner"

    except:
        return "no banner"

print(f"Scanning {host} from port {start_port} to {end_port}...\n")
print(f"{'PORT':<9}{'STATE':<7}{'SERVICE':<10}BANNER")
print("-" * 50)

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((host, port))

    if result == 0:
        ports_open += 1
        service = get_service_name(port)
        banner = grab_banner(host, port)
        print(f"{port}/tcp{'':<3}{'open':<7}{service:<10}{banner}")

    s.close()

if ports_open == 0:
    print(f"No open ports between {start_port}-{end_port}")