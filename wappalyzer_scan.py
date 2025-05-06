import pandas as pd
from wappalyzer import analyze
import subprocess
import re

# Wappalyzer Scan
def wappalyzer_scan():
    raw_target = input(
        "Digite a URL para análise de tecnologias (ex: https://www.example.com): "
    ).strip()
    hostname = re.sub(r'^https?://', '', raw_target)
    hostname = re.sub(r'^www\.', '', hostname)
    hostname = hostname.rstrip('/')
    target = f"http://{hostname}"
    try:
        results = analyze(target, scan_type='full', threads=3)
        rows = []
        if isinstance(results, dict) and target in results and isinstance(
                results[target], dict):
            tech_items = results[target].items()
        else:
            tech_items = results.items()

        for tech, meta in tech_items:
            if isinstance(meta, dict) and 'version' in meta:
                vers = meta.get('version', '')
                cats = ", ".join(meta.get('categories', []))
                grps = ", ".join(meta.get('groups', []))
                rows.append({
                    "Tecnologia": tech,
                    "Versão": vers,
                    "Categorias": cats,
                    "Grupos": grps
                })
            elif isinstance(meta, dict):
                vers = meta.get('version', '')
                cats = ", ".join(meta.get('categories', []))
                grps = ", ".join(meta.get('groups', []))
                rows.append({
                    "Tecnologia": tech,
                    "Versão": vers,
                    "Categorias": cats,
                    "Grupos": grps
                })
            else:
                # Caso meta não siga o formato esperado
                rows.append({
                    "Tecnologia": tech,
                    "Versão": str(meta),
                    "Categorias": "",
                    "Grupos": ""
                })

        df = pd.DataFrame(rows)

        print(f"\n=== Wappalyzer Scan de {target} ===")
        print(df.to_string(index=False))

    except subprocess.CalledProcessError as e:
        print(f"Erro Wappalyzer: {e.output}")
    except Exception as e:
        print(f"Wappalyzer error inesperado: {e}")
