import socket
import re

def is_valid_ip(ip: str) -> bool:
    """Validate IPv4 address format"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    parts = ip.split('.')
    for part in parts:
        try:
            if int(part) < 0 or int(part) > 255:
                return False
        except ValueError:
            return False
    return True

def check_camera_status(ip: str) -> bool:
    """
    Check if a camera at the given IP address is online.
    Tries common ports: 80, 554, 8000, 81, 8080
    """
    # Validate IP format first
    if not is_valid_ip(ip):
        return False
    
    ports = [80, 554, 8000, 81, 8080]
    
    for port in ports:
        try:
            # Create socket and set timeout BEFORE connecting
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout per port
            
            # Try to connect
            result = sock.connect_ex((ip, port))
            sock.close()
            
            # If connection successful (result == 0), camera is online
            if result == 0:
                return True
        except socket.error as e:
            # Log the error for debugging
            print(f"Error checking {ip}:{port} - {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error checking {ip}:{port} - {str(e)}")
            continue
    
    return False