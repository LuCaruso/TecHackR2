from port_scan import port_scanner
from whois_lookup import whois_lookup
from dns_enumeration import dns_enumeration
from wafw00f import wafw00f_scan
from vuln_scan import nmap_vuln_scan
from wappalyzer_scan import wappalyzer_scan

def main():
    print(r"""
  ______                           __     ____                          
 /_  __/____ _ _____ ____ _ ___   / /_   / __ \ ___   _____ ____   ____ 
  / /  / __ `// ___// __ `// _ \ / __/  / /_/ // _ \ / ___// __ \ / __ \
 / /  / /_/ // /   / /_/ //  __// /_   / _, _//  __// /__ / /_/ // / / /
/_/   \__,_//_/    \__, / \___/ \__/  /_/ |_| \___/ \___/ \____//_/ /_/ 
                  /____/                                                                                                                                                                                   
""")
    print("****************************************************************")
    print("* Desenvolvido por Luca Caruso                                 *")
    print("* Tecnologias Hacker                                           *")
    print("* Insper 2025.1                                                *")
    print("****************************************************************")

    while True:
        print("\n1) Port Scanner")
        print("2) WHOIS Lookup")
        print("3) DNS Enumeration")
        print("4) WAFW00F")
        print("5) Vulnerability Scan (Nmap)")
        print("6) Wappalyzer")
        print("0) Sair")

        choice = input("\nEscolha uma opção: ").strip()
        if choice == "1":
            port_scanner()
            print ("================================")
        elif choice == "2":
            whois_lookup()
            print ("================================")
        elif choice == "3":
            dns_enumeration()
            print ("================================")
        elif choice == "4":
            wafw00f_scan()
            print ("================================")
        elif choice == "5":
            nmap_vuln_scan()
            print ("================================")
        elif choice == "6":
            wappalyzer_scan()
            print ("================================")
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
