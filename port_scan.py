import threading
import re
import socket
import ipaddress

#Validadores de padrões de entrada de portas e IPs
port_range_pattern = re.compile(r"^(\d+)-(\d+)$")
ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

known_ports =  {
        "echo": [7], "discard": [9], "systat": [11], "daytime": [13], "qotd": [17],
        "chargen": [19], "ftp-data": [20], "ftp": [21], "ssh": [22], "telnet": [23],
        "smtp": [25], "time": [37], "rlp": [39], "nameserver": [42], "nicname": [43],
        "domain": [53], "bootps": [67], "bootpc": [68], "tftp": [69], "gopher": [70],
        "finger": [79], "http": [80], "hosts2-ns": [81], "kerberos": [88], "hostname": [101],
        "iso-tsap": [102], "rtelnet": [107], "pop2": [109], "pop3": [110], "sunrpc": [111],
        "auth": [113], "uucp-path": [117], "sqlserv": [118], "nntp": [119], "ntp": [123],
        "epmap": [135], "netbios-ns": [137], "netbios-dgm": [138], "netbios-ssn": [139],
        "imap": [143], "sql-net": [150], "sqlsrv": [156], "pcmail-srv": [158], "snmp": [161],
        "snmptrap": [162], "print-srv": [170], "bgp": [179], "irc": [194], "ipx": [213],
        "rtsps": [322], "mftp": [349], "ldap": [389], "https": [443], "microsoft-ds": [445],
        "kpasswd": [464], "isakmp": [500]
    }

#Funções auxiliares
def get_ports(port_range):
    """
    Retorna a faixa de portas a ser escaneada.
    Se for apenas uma porta, retorna a mesma em ambas as posições.
    """
    if port_range_pattern.match(port_range):
        start_port, end_port = port_range.split("-")
        return int(start_port), int(end_port)
    else:
        port = int(port_range)
        return port, port

def get_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            banner = s.recv(1024).decode().strip()
            return banner if banner else "Não disponível"
    except:
        return "Não disponível"

#Funções de scan de portas
def scan_port(ip, port, protocol, open_ports, close_ports, filtered_ports):
    # Define a família de endereço com base no IP (IPv6 se conter ":", senão IPv4)
    if ':' in ip:
        family = socket.AF_INET6
    else:
        family = socket.AF_INET
        
    # Define o tipo de socket de acordo com o protocolo
    if protocol == "tcp":
        sock = socket.SOCK_STREAM
    elif protocol == "udp":
        sock = socket.SOCK_DGRAM
    # Tenta conectar ao IP e porta informados
    try:
        with socket.socket(family, sock) as s:
            s.settimeout(1)
            if protocol == "tcp":
                try:
                    s.connect((ip, port))  # Tenta conectar diretamente
                    state = 0 #OPEN
                except socket.timeout: 
                    state = -1 #FILTERED
                except ConnectionRefusedError: 
                    state = 111 #CLOSED
                except Exception:
                    state = 111 #CLOSED
            elif protocol == "udp":
                try:
                    s.sendto(b"\x00", (ip, port))
                    s.recvfrom(1024)  # Tenta receber dados da porta
                    state = 0 #OPEN
                except socket.timeout: 
                    state = -1 #FILTERED
                except Exception:
                    state = 111 #CLOSED
            
            try:
                #Descobre o serviço da porta usando o diretório de portas conhecidas, se não encontrar, usa a função getservbyport
                if port in known_ports.values():
                    service = list(known_ports.keys())[list(known_ports.values()).index(port)]
                else:
                    service = socket.getservbyport(port, protocol)
            except Exception:
                service = "unknown"
            
            if state == 0:
                os = get_banner(ip, port)
                open_ports[port] = [service, os]
            elif state == 111:
                close_ports[port] = service
            else:
                filtered_ports[port] = service
    except:
        pass

# Ferramentas do Target Recon
# Port Scanner
def port_scanner():
    # Solicita ao usuário o IP ou rede a ser escaneado.
    ip_input = input("Digite o IP(ipv4 ou ipv6) ou a rede que deseja escanear (ex.: 192.168.1.1 ou 2001:0db8:85a3:0000:0000:8a2e:0370:7334 ou 192.168.1.0/24): \n").strip()
    # Solicita ao usuário o range de portas a ser escaneado.
    port_range = input("\nDigite o range de portas(<int>-<int>), ou porta única(<int>), que deseja escanear (ex.: 80-443 ou 22): \n").strip()
    # Solicita ao usuário o protocolo a ser escaneado.
    protocol = input("\nDigite o protocolo que deseja escanear (TCP ou UDP): \n").strip()

    # Dicionário para armazenar as portas abertas
    ip_ports = {}
    # Obtém a faixa de portas a ser escaneada
    port_start, port_end= get_ports(port_range)
    # Lista de threads
    threads = []

    print(f"\n=== PortScan de {ip_input} ===\n")

    # Se for rede, escaneia todas as portas
    if "/" in ip_input:
        print(f"\nEscaneando todas as portas do IP {ip_input}...\n")
        ip_network = ipaddress.ip_network(ip_input, strict=False)
        for ip in ip_network.hosts():
            ip_str = str(ip)
            ip_ports[ip_str] = {"open": {}, "closed": {}, "filtered": {}}
            print(f"Escaneando IP {ip_str}...")
            for port in range(port_start, port_end + 1):
                #Criando uma thread para cada porta
                thread = threading.Thread(target=scan_port, args=(ip_str, port, protocol, ip_ports[ip_str]["open"], ip_ports[ip_str]["closed"], ip_ports[ip_str]["filtered"]))
                thread.start()
                threads.append(thread)

    # Se for IP, escaneia todas as portas
    elif ip_pattern.match(ip_input):
        ip_ports[ip_input] = {"open": {}, "closed": {}, "filtered": {}}
        print(f"\nEscaneando todas as portas do IP {ip_input}...\n")
        for port in range(port_start, port_end + 1):
            #Criando uma thread para cada porta
            thread = threading.Thread(target=scan_port, args=(ip_input, port, protocol, ip_ports[ip_input]["open"], ip_ports[ip_input]["closed"], ip_ports[ip_input]["filtered"]))
            thread.start()
            threads.append(thread)

    # Se for IPv6, escaneia todas as portas
    else:
        ip_ports[ip_input] = {"open": {}, "closed": {}, "filtered": {}}
        print(f"\nEscaneando todas as portas do IP {ip_input}...\n")
        for port in range(port_start, port_end + 1):
            #Criando uma thread para cada porta
            thread = threading.Thread(target=scan_port, args=(ip_input, port, protocol, ip_ports[ip_input]["open"], ip_ports[ip_input]["closed"], ip_ports[ip_input]["filtered"]))
            thread.start()
            threads.append(thread)

    # Aguarda todas as threads finalizarem
    for thread in threads:
        thread.join()

    # Imprime os resultados do escaneamento (somente portas abertas)
    print("_______________________________________________")
    for ip, data in ip_ports.items():
        if data["open"] or data["closed"]:
            print(f"IP: {ip}")
            print("  Open ports:")
            for port, service_os in data["open"].items():
                print(f"    - Porta {port} - open: {service_os[0]} - OS: {service_os[1]}")
            print("  Closed ports:")
            for port, service in data["closed"].items():
                print(f"    - Porta {port} - closed: {service}")
            print("  Filtered ports:")
            print(f"    - Portas filtradas: {data['filtered'].keys()}")
            print("_______________________________________________\n")
