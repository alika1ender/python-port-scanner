import socket
import sys

host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

if len(sys.argv) != 4:
    print("Usage: python3 scanner.py <host> <start_port> <end_port>\n")
    sys.exit()

def get_service_name(port):
    try:
        service = socket.getservbyport(port)
        if service:
            return service
        else:
            return "unknown"
    except:
        return "unknown"

def grab_banner(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))

        # For web servers, send a basic HTTP request

        if port == 80:
            s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close

        if banner:
            first_line = banner.split("\n")[0]
            return first_line
        else:
            return "no banner"
        
    except:
        return "no banner"

print(f"Scanning {host} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((host, port))

    if result == 0:
        service = get_service_name(port)
        banner = grab_banner(host, port)
        print(f"{port}/tcp open  {service:<8} {banner}")
    
    s.close

        
    

    



