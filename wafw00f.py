import subprocess
import re

# Wafw00f
def wafw00f_scan():
    raw_target = input("Digite a URL para análise de tecnologias (ex: https://www.example.com): ").strip()
    hostname = re.sub(r'^https?://', '', raw_target)
    hostname = re.sub(r'^www\.', '', hostname)
    hostname = hostname.rstrip('/')
    target = f"http://{hostname}"
    try:
        cmd = ["wafw00f", target]
        print(f"Executando: {' '.join(cmd)}")
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        print(f"\n=== WAFW00F Scan de {target} ===\n{out}")
    except FileNotFoundError:
        print("wafw00f não encontrado. Instale via 'pip install wafw00f' e garanta que o comando 'wafw00f' esteja no PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Erro WAFW00F: {e.output}")
    except Exception as e:
        print(f"WAFW00F error inesperado: {e}")

