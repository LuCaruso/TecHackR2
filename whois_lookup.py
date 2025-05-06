import ipaddress
import whois

# WHOIS Lookup
def whois_lookup():
    target = input("Digite o IP ou domínio para consulta WHOIS (ex.: 172.217.172.142 ou google.com): ").strip()

    # (Opcional) valida se é um IP; se for inválido, assume domínio
    try:
        ipaddress.ip_address(target)
    except ValueError:
        pass  # continua como domínio

    try:
        info = whois.whois(target)
        print(f"\n=== WHOIS de {target} ===\n")
        # Percorre os campos mais comuns
        for field in ("domain_name", "registrar", "whois_server",
                      "referral_url", "updated_date", "creation_date",
                      "expiration_date", "name_servers", "status",
                      "emails", "dnssec"):
            value = info.get(field)
            if value:
                print(f"{field.replace('_', ' ').title():17}: {value}")
        for k, v in info.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"WHOIS error inesperado: {e}")