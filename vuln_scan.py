import subprocess
import re
import pandas as pd

# Vulnerability Scan (Nmap)
def nmap_vuln_scan():
    target = input("Digite o alvo para Vulnerability Scan (IP-192.168.1.1 ou domínio-google.com): ").strip()
    port_range = input("Digite o range de portas (padrão all ports ou ex: 1-65535): ").strip() or None
    filter_input = input("Filtrar CVEs com severidade mínima (ex: 5.5). Pressione Enter para sem filtro: ").strip()
    try:
        severity_threshold = float(filter_input) if filter_input else None
    except:
        print("Entrada inválida para filtro. Ignorando filtro.")
        severity_threshold = None
    cmd = ["nmap", "-sV", "--script=vuln"]
    if port_range:
        cmd.extend(["-p", port_range]) #Parametro opcional de range de portas
    cmd.append(target)
    try:
        print(f"Executando: {' '.join(cmd)}")
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        print(f"\n=== Nmap Vulnerability Scan de {target} ===")
        print(out)
        
        # Processa a saída do Nmap em uma tabela
        lines = out.splitlines()
        data = []
        current_port = None
        port_regex = re.compile(r"^(\d+)/tcp")
        cve_regex = re.compile(r"CVE-\d{4}-\d+")
        sev_regex = re.compile(r"(\d+\.\d+)")
        for line in lines:
            # detecta nova seção de serviço
            m_port = port_regex.search(line)
            if m_port:
                current_port = m_port.group(1)
            if "vulners:" in line:
                continue
            # identifica CVEs
            if 'CVE-' in line:
                cves = cve_regex.findall(line)
                sevs = sev_regex.findall(line)
                for idx, cve in enumerate(cves):
                    sev = float(sevs[idx]) if idx < len(sevs) else None
                    data.append({'Port': current_port, 'CVE': cve, 'Severity': sev})
        # aplica filtro
        df = pd.DataFrame(data)
        if severity_threshold is not None:
            df = df[df['Severity'] >= severity_threshold] #Mostra apenas CVEs com severidade maior ou igual ao threshold
        resumo = input("Deseja visualizar resumo das vulnerabilidades? (s/n): ").strip().lower()
        if resumo == 's':
            if df.empty:
                print("Nenhuma vulnerabilidade atende ao filtro definido.")
            else:
                print(df.to_string(index=False))
    except subprocess.CalledProcessError as e:
        print(f"Erro Nmap: {e.output}")
    except Exception as e:
        print(f"Nmap error inesperado: {e}")

