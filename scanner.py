import socket
import sys

host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

if len(sys.argv) != 4:
    print("Usage: python3 scanner.py <host> <start_port> <end_port>\n")
    sys.exit()

# Determine the common service for a port
def get_service_name(port):
    try:
        service = socket.getservbyport(port)
        if service:
            return service # Sometimes lookup returns "None", we convert it to "unknown" so program doesn't crash
        else:
            return "unknown"
    except:
        return "unknown"

# Read data sent by the service.
def grab_banner(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP connection over IPv4
        s.settimeout(1) # Prevent socket from freezing by setting a timer 
        s.connect((host, port)) # This opens a TCP connection to perform a handshake

        # For web servers, send a basic HTTP request

        if port == 80:
            s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        
        banner = s.recv(1024).decode(errors="ignore").strip() # Receive and decode up to 1024 bytes to string
        s.close

        if banner: # We only read the first line so we dont get a long information for cleaner output
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
        service = get_service_name(port)
        banner = grab_banner(host, port)
        print(f"{port}/tcp{'':<3}{'open':<7}{service:<10}{banner}")
    
    s.close

        
    

    



