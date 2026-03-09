import socket
import sys

host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

print(f"\nScanning {host} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((host, port))

    if result == 0:
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"

        print(f"Port {port} is OPEN ({service})")

    s.close()