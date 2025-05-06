import dns.resolver
import socket

# DNS Enumeration
def dns_enumeration():
    domain = input("Digite o domínio para DNS enumeration (google.com): ").strip()
    print(f"\n=== DNS Enumeration de {domain} ===\n")
    # Valida se o domínio é válido
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"Domínio inválido: {domain}")
        return
    registros = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
    for rec in registros:
        try:
            answers = dns.resolver.resolve(domain, rec)
            print(f"\n=== Registro {rec} de {domain} ===")
            for rdata in answers:
                print(rdata.to_text())
        except dns.resolver.NoAnswer:
            print(f"Nenhuma resposta para {rec}")
        except dns.resolver.NXDOMAIN:
            print(f"Domínio não existe: {domain}")
            break
        except Exception as e:
            print(f"Erro consultando {rec}: {e}")