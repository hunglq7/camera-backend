import socket

def check_camera_status(ip: str) -> bool:
    ports = [80, 554, 8000, 81, 8080]

    for port in ports:
        try:
            socket.setdefaulttimeout(0.5)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex((ip, port)) == 0:
                    return True
        except:
            continue
    return False