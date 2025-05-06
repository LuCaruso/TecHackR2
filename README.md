# Documentação Técnica e Manual do Usuário

## 1. Visão Geral  
Este projeto em Python automatiza a fase de reconhecimento em testes de invasão (pentest), reunindo em um único menu interativo as seguintes funcionalidades:  
- Port scanning (TCP/UDP)  
- DNS enumeration  
- WHOIS lookup  
- Fingerprinting de tecnologias web (Wappalyzer)  
- Fingerprinting de WAFs (WAFW00F)  
- Varredura de vulnerabilidades via Nmap NSE  

O script principal é o `target_recon.py`, que orquestra a execução de cada módulo e apresenta resultados consolidados.

---

## 2. Pré-requisitos  

- **Python** instalado.  
- **Nmap** instalado e acessível via linha de comando.    

---

## 3. Instalação  

1. **Clone** este repositório (ou faça download dos arquivos):  
   ```bash
   git clone https://seu-repositorio.git
   cd seu-repositorio

2. **Crie e ative** um ambiente virtual:
    - Linux/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    - Windows (PowerShell):
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3. Instale as dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Estrutura do Projeto
```bash
.
├── requirements.txt
├── target_recon.py       # script principal (menu interativo)
├── port_scan.py          # TCP/UDP port scanner multithreaded
├── dns_enumeration.py    # coleta registros DNS (A, MX, CNAME, etc.)
├── whois_lookup.py       # consulta WHOIS
├── wappalyzer_scan.py    # invoca Wappalyzer CLI
├── wafw00f.py            # invoca WAFW00F CLI
└── vuln_scan.py          # Nmap NSE “vuln” scanner e pós-processamento
```

---
### 5. Descrição dos Módulos
- port_scan.py

    Escaneia portas TCP e UDP, classifica estados (abertas, fechadas, filtradas) e exibe em tabela.

- dns_enumeration.py

    Recupera registros DNS padrão e faz tentativas de zone transfer em servidores autorizados.

- whois_lookup.py
    
    Consulta bancos WHOIS públicos para extrair dados do registrante, registrar, datas e nameservers.

- wappalyzer_scan.py
    
    Executa wappalyzer <url> --quiet --json e formata saída em DataFrame via pandas.

- wafw00f.py
    
    Executa wafw00f <url> e identifica Web Application Firewalls em uso.

- vuln_scan.py
    
    Executa nmap --script vuln, vulners -oX - <target>, carrega XML no pandas, filtra CVEs por severidade e exibe resumo.

---
### 6. Como Executar
Após ativar o ambiente e instalar dependências:

```bash
python target_recon.py
```
Você verá um menu numerado. Basta digitar o número da opção desejada e, quando solicitado, informar o IP ou domínio do alvo.

```bash
  ______                           __     ____
 /_  __/____ _ _____ ____ _ ___   / /_   / __ \ ___   _____ ____   ____ 
  / /  / __ `// ___// __ `// _ \ / __/  / /_/ // _ \ / ___// __ \ / __ \
 / /  / /_/ // /   / /_/ //  __// /_   / _, _//  __// /__ / /_/ // / / /
/_/   \__,_//_/    \__, / \___/ \__/  /_/ |_| \___/ \___/ \____//_/ /_/ 
                  /____/                                                                                                                                  


****************************************************************
* Desenvolvido por Luca Caruso                                 *
* Tecnologias Hacker                                           *
* Insper 2025.1                                                *
****************************************************************

1) Port Scanner
2) WHOIS Lookup
3) DNS Enumeration
4) WAFW00F
5) Vulnerability Scan (Nmap)
6) Wappalyzer
0) Sair

Escolha uma opção:
```
