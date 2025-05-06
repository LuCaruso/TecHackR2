# TecHackR2

## 1. Além do PortScan, quais são as 5 ferramentas mais úteis para reconhecimento em um pentest?

Além do PortScan, outras cinco ferramentas são: **DNS Enumeration, WHOIS Lookup, Wappalyzer, WAFW00F e Nikto**. Utilizando estas ferramentas, é possível realizar um pentest robusto e abranjente, analisando diversas rotas de ataque, cada qual com uma ferramenta mais apropriada.

- O **DNS Enumeration** mapeia registros de DNS, como A, MX, NS e CNAME, revelando subdomínios e serviços ocultos para ampliar a superfície de ataque, assim podendo identificar sites de desenvolvimento, ou paginas de login sucetíveis a atques de força bruta.  
- O **WHOIS Lookup** consulta bancos de dados de registro de domínios, obtendo informações sobre proprietário, registrar, datas de expiração e contatos administrativos para facilitar ataques de engenharia social e atribuição de domínio.  
- O **Wappalyzer** identifica tecnologias em uso em um site, como CMS, frameworks JavaScript, plataformas de e-commerce e ferramentas de análise, permitindo direcionar testes para vulnerabilidades específicas de cada componente, ou até ja reconhecer vulnerabilidades reconhecidas de certas versões dessas tecnologias.  
- O **WAFW00F** faz fingerprinting de Web Application Firewalls, detectando soluções como Cloudflare, F5 BIG-IP e AWS WAF, o que ajuda a ajustar técnicas de evasão e escolher payloads compatíveis.
- O **Nikto** é um scanner de vulnerabilidades web open-source que testa servidores HTTP contra mais de 6 700 arquivos e scripts perigosos, além de verificar versões desatualizadas de servidores e problemas de configuração.  
Apesar de eu julgar o Nikto uma ferramenta mais completa, no código do projeto, optei por usar o Nmap Vulnerability Scanner em vez do Nikto, pois o Nmap oferece integração nativa com sistemas Windows garantindo compatibilidade multiplataforma sem dependências de Linux.

----
## 2. Qual a diferença entre um scanner de portas SYN e um TCP Connect Scan? Explique em qual cenário cada um é mais eficiente

A diferença entre um scanner de portas TCP SYN e um TCP Connect Scan é que o SYN Scan envia apenas o pacote SYN e, ao receber um SYN/ACK, aborta o três-way handshake com um RST (half-open), tornando-se mais rápido e furtivo, mas exigindo privilégios de root. Por outro lado o Connect Scan usa a chamada de sistema connect(), completa o handshake inteiro (SYN→SYN/ACK→ACK) e depois encerra a conexão, não requerendo privilégios especiais,mas gera logs no alvo e sendo mais “barulhento” e lento.
Desta forma podemos o SYN Scan é melhor para os casos que é imprecindível não ser detectado (como é o caso de combate a crimes cibernéticos) e já se esta em uma etapa mais avançada, em que se tem permissões de administrador. Já o Connect Scan é mais indicado para os casos em que não tem problema gerar logs de acesso (como é o caso de pentests contratados, em que o cliente tem conhecimento da varredura), e que está em estagios mais iniciais da analise de vulnerabilidades, em que não se tem ainda permissões administrativas.

----
## 3. Como um pentester pode evitar ser detectado por sistemas de prevenção de intrusão (IPS) durante o reconhecimento? Liste técnicas e como elas impactam a eficácia do scan.

Algumas estratégias possíveis para evitar ser detectado durante o reconhecimento são:

- Uso de Delay entre as chamadas: diminuindo a frequência das requisições, podendo passar despercebido por sistemas de prevenção que verificam o volume de requisições em um intervalo curto de tempo, mas demorando mais para conseguir acessar o alvo;
- Uso de decoys: mascarando as requisições de forma a esconder o ip do host principal e evitando que ele seja bloqueado, mas pode acabar bloqueando por completo o host por conta do volume de acessos;
- Randomizar hosts atacados: embaralhando a ordem de alvos, de forma a diminuir a frequencia do ataque a um mesmo alvo, podendo passar despercebido, mas aumentando consideravelmente a duração do scan

-----------------
# Arquitetura e Decisões de Design
## Arquitetura do Projeto

O pentest em Python segue uma arquitetura modular e orientada a scripts, composta por:

- **Script principal (`target_recon.py`)**  
  Exibe um menu interativo, lê a opção do usuário e invoca, de forma sequencial, as funções de cada módulo de reconhecimento e varredura.

- **Módulos de Reconhecimento**  
  - `port_scan.py`: implementa scan TCP/UDP multithreaded, categorizando portas abertas, fechadas e filtradas.  
  - `dns_enumeration.py`: coleta registros DNS (A, MX, NS, CNAME, TXT, SOA) para descobrir subdomínios e serviços ocultos.  
  - `whois_lookup.py`: faz consulta WHOIS para extrair dados de registrante, registrar, datas e nameservers.  
  - `wappalyzer_scan.py`: invoca a CLI do Wappalyzer para identificar CMS, frameworks e versões de bibliotecas web, exibindo resultados via pandas.  
  - `wafw00f.py`: chama o utilitário WAFW00F para fingerprinting de Web Application Firewalls (Cloudflare, F5, AWS WAF etc.).  
  - `vuln_scan.py`: executa Nmap com scripts NSE “vuln”, captura a saída, processa CVEs em um DataFrame e permite filtragem de severidade.

- **Integração Externa**  
  Todos os módulos que dependem de ferramentas de terceiros (Nmap, WAFW00F, Wappalyzer) utilizam `subprocess` para invocar comandos de sistema, capturar stdout/stderr e tratar erros, garantindo compatibilidade com instalações padrão.

- **Apresentação e Filtros**  
  O uso de pandas em `vuln_scan.py` permite estruturar os dados de vulnerabilidade em tabelas, aplicar filtros de severidade e apresentar resumos concisos ao usuário.


## Decisões de Design
1. **Modularidade e Separação de Responsabilidades**  
   Cada funcionalidade (port scanning, DNS, WHOIS, WAF detection, tech fingerprinting, vulnerability scanning) vive em seu próprio módulo, facilitando manutenção, testes isolados e inclusão de novas ferramentas.

2. **Compatibilidade Multiplataforma**  
   A opção pelo **Nmap Vulnerability Scanner** foi motivada pelo desejo de rodar em Windows sem depender de ambiente Linux puro, mantendo a mesma interface de uso para todos os sistemas.

3. **Performance e Escalabilidade**  
   - O **PortScan** usa `threading` para paralelizar conexões e acelerar o processo em redes amplas.  
   - As consultas DNS e WHOIS são síncronas, mas limitadas ao escopo definido pelo usuário para evitar delays excessivos.

5. **Experiência Prática**  
   As ferramentas foram escolhidas com base na minha vivência no projeto:
   - **DNS Enumeration** revelou subdomínios de teste que escapavam ao escopo inicial, onde identifiquei possíveis alvos de brute-force.  
   - **WHOIS Lookup** me deu informações acerca de quem era administrador daquele domínio, que eu poderia explorar com engenharia social.  
   - **Wappalyzer** mapeou rapidamente versões vulneráveis de frameworks JavaScript, dos quais alguns estavam desatualizados.  
   - **WAFW00F** Não foi usado no projeto, mas caso eu continuasse trabalhando nele, provavelmente seria uma ferramenta que eu utilizaria  
   - **Nmap Vuln Scanner** Fez uma varredura das vulnerabilidades listadas que estavam presentes no site analisado no projeto.


## Resultados dos testes
A título de exemplo vamos executar os comandos para o **google.com**

Ao executar o programa ***target_recon.py***, temos no primeiro momento o menu para escolha da ferramenta a ser utilizada.

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

### Port Scanner
```bash
Escolha uma opção: 1
Digite o IP(ipv4 ou ipv6) ou a rede que deseja escanear (ex.: 192.168.1.1 ou 2001:0db8:85a3:0000:0000:8a2e:0370:7334 ou 192.168.1.0/24): 
8.8.8.8

Digite o range de portas(<int>-<int>), ou porta única(<int>), que deseja escanear (ex.: 80-443 ou 22):
0-3000 

Digite o protocolo que deseja escanear (TCP ou UDP):
tcp

=== PortScan de 8.8.8.8 ===


Escaneando todas as portas do IP 8.8.8.8...

_______________________________________________
IP: 8.8.8.8
  Open ports:
    - Porta 53 - open: domain - OS: Não disponível
    - Porta 443 - open: https - OS: Não disponível
    - Porta 853 - open: unknown - OS: Não disponível
  Closed ports:
    - Porta 0 - closed: unknown
  Filtered ports:
    - Portas filtradas: dict_keys([1, 3, 2, 11, 13, 9, 7, 17, 10, 6, 14, 4, 15, 8, 5, 12, 16, 25, 22, 20, 37, 27, 29, 28, 19, 31, 30, 24, 32, 26, 21, 23, 33, 35, 36, 34, 18, 43, 42, 38, 40, 46, 55, 41, 39, 45, 49, 50, 47, 48, 51, 54, 44, 70, 52, 65, 57, 68, 62, 66, 59, 56, 69, 67, 64, 72, 58, 81, 60, 79, 61, 71, 80, 63, 88, 95, 78, 101, 77, 102, 76, 74, 94, 75, 83, 87, 85, 84, 117, 93, 107, 82, 111, 110, 73, 86, 106, 92, 100, 90, 109, 113, 105, 104, 103, 91, 98, 114, 118, 89, 99, 115, 97, 108, 112, 116, 96, 120, 132, 124, 137, 122, 123, 131, 125, 139, 129, 135, 127, 119, 150, 128, 163, 121, 138, 130, 136, 126, 133, 152, 156, 158, 134, 179, 143, 149, 170, 162, 194, 160, 144, 174, 178, 151, 146, 142, 157, 147, 141, 159, 148, 140, 155, 154, 166, 175, 176, 153, 167, 173, 164, 168, 172, 200, 145, 171, 181, 161, 169, 180, 184, 182, 177, 202, 195, 220, 204, 215, 219, 192, 187, 183, 216, 196, 188, 212, 193, 190, 189, 186, 201, 217, 209, 198, 213, 199, 221, 208, 222, 197, 214, 206, 191, 207, 218, 210, 205, 223, 165, 224, 251, 211, 230, 185, 248, 257, 266, 233, 259, 238, 267, 242, 252, 227, 234, 245, 249, 231, 241, 261, 244, 254, 229, 243, 247, 237, 255, 265, 203, 263, 246, 253, 264, 250, 268, 260, 256, 236, 239, 270, 269, 262, 226, 235, 278, 240, 232, 273, 225, 288, 272, 279, 282, 228, 285, 287, 291, 280, 258, 277, 275, 289, 298, 271, 284, 297, 290, 283, 281, 276, 292, 274, 293, 286, 302, 316, 314, 294, 306, 299, 315, 308, 311, 322, 312, 307, 309, 301, 305, 303, 313, 304, 296, 310, 295, 317, 318, 320, 329, 333, 328, 321, 324, 323, 326, 327, 300, 336, 334, 319, 330, 325, 335, 332, 331, 342, 341, 345, 349, 351, 350, 352, 338, 346, 344, 337, 343, 339, 347, 348, 340, 370, 362, 369, 373, 354, 355, 368, 366, 374, 371, 367, 363, 372, 361, 359, 357, 358, 365, 353, 364, 356, 360, 389, 384, 375, 380, 383, 387, 388, 392, 377, 391, 378, 379, 382, 386, 381, 385, 376, 393, 394, 390, 400, 395, 404, 415, 397, 405, 410, 411, 409, 402, 398, 407, 412, 408, 401, 413, 396, 403, 414, 406, 399, 417, 418, 416, 419, 420, 422, 423, 424, 428, 426, 430, 431, 434, 421, 427, 425, 429, 433, 432, 445, 439, 435, 444, 449, 436, 441, 438, 455, 454, 452, 442, 446, 450, 447, 456, 451, 448, 437, 453, 440, 464, 463, 459, 476, 460, 466, 468, 472, 475, 457, 465, 471, 467, 458, 462, 470, 469, 477, 474, 473, 461, 483, 490, 485, 496, 479, 492, 499, 480, 500, 491, 481, 497, 494, 484, 495, 482, 487, 498, 478, 493, 488, 489, 486, 515, 512, 520, 507, 505, 514, 502, 508, 504, 503, 519, 511, 516, 506, 522, 518, 501, 509, 517, 513, 521, 510, 529, 531, 530, 524, 528, 537, 533, 535, 532, 536, 526, 538, 527, 525, 523, 534, 544, 543, 548, 556, 539, 540, 547, 554, 558, 546, 550, 557, 552, 551, 555, 545, 542, 553, 541, 549, 563, 565, 560, 569, 568, 575, 567, 564, 566, 562, 570, 571, 561, 574, 576, 577, 572, 573, 559, 578, 584, 585, 587, 579, 592, 580, 583, 588, 591, 593, 596, 595, 589, 590, 586, 594, 582, 581, 613, 608, 605, 604, 607, 615, 601, 600, 599, 603, 611, 606, 598, 610, 612, 616, 614, 617, 597, 602, 609, 623, 622, 618, 628, 627, 632, 634, 621, 619, 631, 633, 635, 629, 624, 630, 620, 625, 626, 636, 639, 642, 640, 638, 645, 651, 644, 654, 648, 647, 649, 643, 646, 655, 653, 637, 656, 641, 650, 652, 666, 671, 667, 672, 663, 661, 657, 669, 670, 665, 660, 659, 658, 662, 673, 668, 664, 674, 683, 678, 675, 691, 687, 676, 692, 694, 689, 688, 686, 684, 681, 685, 677, 679, 680, 690, 682, 693, 699, 703, 700, 695, 704, 709, 698, 713, 710, 702, 708, 712, 711, 707, 714, 701, 705, 706, 696, 697, 717, 720, 721, 719, 718, 723, 729, 722, 716, 724, 728, 732, 725, 726, 731, 730, 715, 727, 733, 749, 740, 736, 746, 741, 743, 735, 751, 744, 747, 748, 737, 734, 738, 752, 750, 745, 742, 739, 756, 764, 754, 753, 755, 759, 767, 758, 768, 772, 762, 765, 766, 773, 771, 761, 757, 770, 763, 769, 760, 780, 775, 781, 785, 777, 794, 793, 779, 784, 789, 791, 776, 787, 801, 783, 798, 778, 782, 788, 792, 805, 786, 797, 804, 803, 790, 795, 796, 774, 800, 806, 799, 815, 802, 809, 808, 814, 816, 807, 813, 810, 812, 811, 823, 817, 819, 820, 818, 824, 822, 831, 826, 829, 830, 828, 833, 832, 825, 827, 821, 834, 843, 851, 839, 848, 836, 838, 840, 842, 844, 845, 837, 846, 841, 835, 847, 850, 852, 849, 860, 863, 864, 859, 858, 868, 865, 866, 862, 855, 856, 854, 857, 861, 869, 867, 871, 870, 873, 877, 878, 885, 887, 874, 886, 879, 880, 888, 881, 889, 882, 872, 883, 875, 876, 884, 900, 892, 904, 895, 907, 890, 891, 897, 903, 899, 906, 898, 910, 909, 901, 908, 894, 902, 893, 905, 911, 896, 917, 914, 918, 926, 920, 927, 925, 921, 915, 924, 912, 923, 916, 928, 919, 922, 913, 931, 935, 930, 939, 944, 947, 940, 937, 943, 936, 929, 933, 934, 932, 938, 941, 946, 942, 945, 960, 956, 963, 949, 948, 964, 951, 954, 957, 950, 952, 955, 953, 958, 959, 961, 962, 971, 968, 975, 976, 965, 969, 973, 967, 979, 977, 972, 974, 978, 966, 970, 980, 992, 995, 989, 987, 988, 984, 981, 991, 993, 982, 986, 994, 997, 996, 990, 983, 985, 1003, 999, 998, 1004, 1005, 1012, 1000, 1007, 1009, 1001, 1008, 1015, 1013, 1014, 1006, 1016, 1011, 1002, 1010, 1023, 1020, 1025, 1028, 1022, 1017, 1021, 1030, 1018, 1031, 1026, 1027, 1019, 1029, 1024, 1034, 1033, 1043, 1032, 1040, 1039, 1035, 1038, 1037, 1041, 1042, 1036, 1044, 1053, 1046, 1056, 1049, 1052, 1048, 1045, 1055, 1047, 1051, 1050, 1057, 1054, 1059, 1061, 1068, 1072, 1070, 1075, 1058, 1065, 1066, 1064, 1067, 1074, 1063, 1062, 1073, 1069, 1071, 1060, 1082, 1077, 1083, 1076, 1086, 1080, 1087, 1088, 1091, 1084, 1081, 1079, 1089, 1085, 1078, 1094, 1092, 1090, 1093, 1098, 1109, 1105, 1106, 1102, 1110, 1095, 1101, 1097, 1096, 1100, 1108, 1099, 1107, 1103, 1104, 1111, 1115, 1120, 1116, 1114, 1119, 1124, 1123, 1113, 1112, 1118, 1121, 1122, 1126, 1125, 1117, 1131, 1127, 1128, 1133, 1135, 1129, 1136, 1139, 1142, 1138, 1141, 1132, 1137, 1130, 1140, 1134, 1155, 1148, 1143, 1144, 1152, 1149, 1150, 1147, 1146, 1157, 1151, 1156, 1154, 1153, 1145, 1166, 1167, 1168, 1158, 1161, 1160, 1170, 1169, 1165, 1164, 1172, 1163, 1159, 1162, 1171, 1173, 1183, 1176, 1184, 1180, 1187, 1188, 1182, 1177, 1174, 1181, 1186, 1185, 1178, 1175, 1189, 1208, 1203, 1207, 1204, 1199, 1211, 1191, 1195, 1206, 1215, 1212, 1192, 1216, 1179, 1213, 1205, 1209, 1196, 1218, 1226, 1223, 1198, 1219, 1197, 1217, 1210, 1220, 1228, 1200, 1190, 1221, 1225, 1201, 1214, 1222, 1193, 1194, 1224, 1202, 1227, 1229, 1230, 1233, 1232, 1231, 1234, 1237, 1235, 1236, 1239, 1241, 1240, 1238, 1242, 1245, 1244, 1246, 1243, 1247, 1249, 1248, 1251, 1250, 1252, 1253, 1254, 1256, 1255, 1258, 1257, 1265, 1259, 1263, 1260, 1262, 1264, 1261, 1266, 1267, 1269, 1268, 1270, 1272, 1271, 1279, 1275, 1278, 1277, 1273, 1276, 1287, 1282, 1288, 1283, 1285, 1286, 1281, 1274, 1280, 1284, 1289, 1292, 1299, 1296, 1290, 1291, 1295, 1300, 1293, 1294, 1298, 1297, 1303, 1307, 1304, 1311, 1306, 1309, 1305, 1301, 1312, 1302, 1310, 1308, 1318, 1316, 1315, 1314, 1317, 1313, 1322, 1321, 1320, 1319, 1323, 1326, 1327, 1325, 1329, 1324, 1328, 1332, 1337, 1333, 1339, 1334, 1338, 1330, 1336, 1331, 1335, 1347, 1343, 1341, 1342, 1340, 1344, 1345, 1346, 1356, 1360, 1352, 1350, 1355, 1351, 1363, 1353, 1357, 1354, 1349, 1361, 1348, 1358, 1362, 1359, 1369, 1365, 1367, 1366, 1375, 1379, 1376, 1370, 1372, 1374, 1378, 1371, 1373, 1381, 1364, 1368, 1380, 1377, 1387, 1392, 1388, 1384, 1389, 1386, 1382, 1383, 1385, 1390, 1393, 1391, 1394, 1397, 1396, 1395, 1399, 1402, 1403, 1400, 1405, 1404, 1406, 1398, 1401, 1408, 1407, 1413, 1412, 1409, 1411, 1414, 1410, 1422, 1419, 1421, 1415, 1416, 1418, 1417, 1420, 1423, 1424, 1425, 1427, 1426, 1428, 1433, 1434, 1432, 1429, 1430, 1439, 1442, 1441, 1437, 1431, 1435, 1440, 1444, 1438, 1436, 1443, 1451, 1452, 1447, 1459, 1460, 1455, 1456, 1449, 1457, 1453, 1446, 1458, 1450, 1448, 1445, 1461, 1454, 1477, 1462, 1466, 1465, 1472, 1474, 1470, 1471, 1467, 1469, 1473, 1464, 1463, 1468, 1478, 1475, 1476, 1482, 1481, 1479, 1480, 1483, 1484, 1488, 1506, 1487, 1507, 1492, 1504, 1508, 1491, 1496, 1500, 1489, 1490, 1494, 1501, 1505, 1493, 1485, 1499, 1498, 1497, 1495, 1486, 1502, 1503, 1512, 1524, 1523, 1510, 1515, 1519, 1511, 1530, 1520, 1513, 1516, 1529, 1527, 1518, 1521, 1509, 1525, 1517, 1522, 1514, 1526, 1528, 1535, 1544, 1536, 1534, 1533, 1540, 1541, 1531, 1532, 1542, 1537, 1538, 1539, 1543, 1545, 1558, 1557, 1554, 1549, 1546, 1550, 1547, 1548, 1560, 1559, 1556, 1551, 1555, 1552, 1561, 1553, 1584, 1567, 1571, 1580, 1564, 1572, 1576, 1563, 1579, 1568, 1566, 1582, 1574, 1562, 1577, 1578, 1573, 1599, 1588, 1583, 1575, 1587, 1591, 1592, 1595, 1602, 1598, 1585, 1570, 1581, 1596, 1589, 1590, 1594, 1614, 1586, 1565, 1607, 1593, 1597, 1569, 1625, 1626, 1609, 1618, 1622, 1621, 1620, 1600, 1619, 1624, 1613, 1629, 1631, 1640, 1644, 1643, 1639, 1623, 1632, 1612, 1628, 1636, 1615, 1604, 1603, 1635, 1634, 1641, 1617, 1637, 1610, 1633, 1606, 1630, 1638, 1627, 1608, 1601, 1664, 1679, 1672, 1659, 1655, 1656, 1652, 1669, 1662, 1665, 1647, 1666, 1661, 1658, 1616, 1657, 1673, 1670, 1642, 1731, 1660, 1663, 1651, 1687, 1683, 1692, 1691, 1688, 1668, 1667, 1676, 1696, 1675, 1700, 1704, 1671, 1699, 1686, 1650, 1653, 1678, 1677, 1649, 1646, 1690, 1705, 1694, 1689, 1693, 1697, 1701, 1674, 1702, 1698, 1723, 1719, 1711, 1742, 1722, 1707, 1703, 1713, 1714, 1710, 1709, 1749, 1748, 1752, 1712, 1743, 1744, 1654, 1715, 1681, 1751, 1605, 1745, 1741, 1738, 1721, 1718, 1746, 1717, 1737, 1726, 1725, 1730, 1695, 1648, 1611, 1753, 1684, 1680, 1747, 1728, 1724, 1740, 1735, 1732, 1739, 1682, 1733, 1755, 1729, 1685, 1734, 1750, 1720, 1727, 1736, 1764, 1706, 1801, 1768, 1708, 1645, 1781, 1776, 1771, 1775, 1759, 1756, 1760, 1763, 1784, 1767, 1772, 1780, 1807, 1800, 1796, 1803, 1808, 1799, 1792, 1716, 1804, 1754, 1762, 1798, 1777, 1761, 1766, 1793, 1785, 1769, 1805, 1802, 1782, 1765, 1786, 1758, 1810, 1863, 1836, 1791, 1849, 1878, 1859, 1851, 1857, 1774, 1826, 1814, 1790, 1778, 1818, 1825, 1789, 1830, 1817, 1853, 1845, 1877, 1862, 1816, 1819, 1820, 1811, 1823, 1809, 1787, 1783, 1835, 1828, 1795, 1812, 1815, 1824, 1832, 1847, 1788, 1864, 1860, 1848, 1869, 1839, 1861, 1842, 1858, 1794, 1833, 1829, 1821, 1773, 1834, 1770, 1838, 1854, 1855, 1841, 1865, 1779, 1827, 1856, 1831, 1813, 1852, 1844, 1840, 1843, 1797, 1757, 1806, 1846, 1822, 1866, 1837, 1898, 1902, 1871, 1904, 1924, 1914, 1913, 1910, 1905, 1893, 1931, 1917, 1874, 1870, 1900, 1923, 1886, 1903, 1944, 1879, 1918, 1906, 1909, 1911, 1868, 1882, 1930, 1880, 1933, 1881, 1920, 1872, 1884, 1867, 1915, 1875, 1895, 1897, 1947, 1907, 1939, 1955, 1887, 1932, 1954, 1896, 1908, 1890, 1922, 1925, 1935, 1916, 1928, 1929, 1894, 1949, 1945, 1950, 1891, 1876, 1927, 1883, 1892, 1899, 1919, 1912, 1948, 1888, 1936, 1921, 1926, 1885, 1934, 1889, 1953, 1938, 1999, 1850, 1937, 1991, 1988, 1943, 1993, 1986, 1952, 1963, 1979, 2000, 2006, 1942, 1970, 1983, 1987, 2009, 1992, 2014, 1998, 1965, 2003, 2010, 2001, 1960, 1959, 2033, 2012, 1962, 1901, 1873, 2023, 1973, 2015, 1995, 1971, 1964, 1974, 1940, 2004, 1980, 1941, 1978, 1989, 1957, 1997, 1994, 1982, 1985, 1972, 1946, 2021, 1981, 2005, 2030, 2028, 2020, 2007, 2024, 2053, 1990, 2029, 2026, 2019, 2031, 2078, 2040, 2089, 2090, 2034, 2073, 2060, 2044, 2076, 2051, 2048, 2091, 2052, 2068, 2056, 2080, 2093, 2042, 2081, 2038, 2072, 2055, 2071, 2050, 2075, 2066, 2063, 2054, 2046, 2057, 2058, 2065, 2087, 2103, 2094, 2101, 2096, 2095, 2084, 2083, 2086, 2085, 2016, 2082, 1968, 2047, 1984, 2032, 2002, 2011, 1951, 1961, 1966, 2013, 2022, 2027, 1975, 1977, 1967, 1956, 2025, 2102, 2036, 2079, 2067, 2092, 2049, 2045, 1976, 2064, 2061, 2074, 2077, 2062, 2070, 2059, 2069, 2088, 2035, 2100, 2097, 2098, 2099, 2043, 1996, 2104, 2037, 2041, 2039, 2018, 2017, 2008, 2121, 1958, 1969, 2109, 2106, 2108, 2120, 2110, 2117, 2105, 2118, 2112, 2122, 2107, 2115, 2111, 2119, 2123, 2116, 2125, 2135, 2162, 2155, 2160, 2129, 2133, 2182, 2169, 2142, 2173, 2149, 2113, 2150, 2126, 2153, 2157, 2158, 2140, 2143, 2127, 2128, 2131, 2161, 2165, 2124, 2130, 2177, 2137, 2134, 2138, 2146, 2114, 2141, 2175, 2170, 2159, 2132, 2148, 2147, 2156, 2136, 2144, 2151, 2179, 2242, 2234, 2166, 2180, 2194, 2183, 2168, 2192, 2196, 2164, 2224, 2220, 2181, 2193, 2189, 2186, 2201, 2225, 2198, 2217, 2197, 2213, 2230, 2202, 2238, 2206, 2222, 2229, 2185, 2152, 2139, 2261, 2176, 2171, 2191, 2184, 2188, 2172, 2215, 2203, 2207, 2204, 2227, 2216, 2233, 2200, 2195, 2226, 2212, 2245, 2154, 2247, 2219, 2252, 2249, 2248, 2174, 2178, 2253, 2237, 2209, 2210, 2218, 2236, 2221, 2235, 2255, 2256, 2260, 2231, 2243, 2163, 2208, 2167, 2199, 2228, 2187, 2244, 2232, 2251, 2239, 2205, 2241, 2259, 2264, 2190, 2258, 2223, 2263, 2240, 2214, 2301, 2145, 2211, 2246, 2254, 2299, 2319, 2307, 2329, 2288, 2291, 2271, 2276, 2394, 2311, 2267, 2266, 2272, 2275, 2300, 2280, 2287, 2320, 2309, 2315, 2295, 2279, 2312, 2283, 2296, 2304, 2313, 2302, 2317, 2274, 2306, 2322, 2310, 2294, 2314, 2289, 2284, 2305, 2292, 2297, 2321, 2293, 2318, 2285, 2316, 2308, 2282, 2342, 2345, 2281, 2265, 2350, 2349, 2340, 2347, 2278, 2332, 2257, 2341, 2290, 2326, 2268, 2250, 2298, 2328, 2343, 2339, 2270, 2269, 2334, 2325, 2323, 2351, 2331, 2337, 2303, 2286, 2344, 2262, 2277, 2336, 2330, 2324, 2387, 2453, 2383, 2348, 2447, 2386, 2346, 2352, 2335, 2353, 2392, 2372, 2376, 2415, 2443, 2427, 2384, 2327, 2395, 2388, 2396, 2422, 2361, 2393, 2418, 2438, 2273, 2338, 2333, 2382, 2504, 2414, 2380, 2421, 2363, 2360, 2391, 2371, 2455, 2419, 2412, 2416, 2357, 2446, 2379, 2420, 2403, 2424, 2378, 2417, 2411, 2425, 2430, 2381, 2441, 2454, 2456, 2389, 2367, 2355, 2408, 2356, 2358, 2405, 2406, 2439, 2398, 2433, 2445, 2374, 2364, 2397, 2440, 2390, 2423, 2431, 2413, 2464, 2426, 2434, 2435, 2399, 2359, 2354, 2365, 2368, 2475, 2377, 2429, 2407, 2400, 2442, 2370, 2432, 2452, 2437, 2477, 2465, 2409, 2459, 2451, 2483, 2402, 2444, 2478, 2375, 2448, 2428, 2385, 2450, 2480, 2366, 2472, 2468, 2525, 2410, 2449, 2492, 2495, 2500, 2487, 2404, 2401, 2553, 2473, 2462, 2369, 2460, 2436, 2362, 2373, 2458, 2551, 2479, 2565, 2532, 2490, 2560, 2511, 2531, 2512, 2508, 2471, 2561, 2573, 2581, 2507, 2585, 2519, 2580, 2543, 2541, 2502, 2540, 2535, 2474, 2516, 2524, 2514, 2489, 2527, 2536, 2488, 2491, 2529, 2579, 2542, 2521, 2520, 2510, 2522, 2548, 2497, 2547, 2523, 2550, 2582, 2546, 2476, 2499, 2559, 2567, 2503, 2470, 2484, 2482, 2554, 2493, 2496, 2533, 2466, 2552, 2467, 2463, 2526, 2557, 2562, 2494, 2575, 2498, 2578, 2505, 2481, 2549, 2569, 2555, 2587, 2457, 2528, 2589, 2539, 2600, 2611, 2620, 2619, 2563, 2616, 2485, 2501, 2534, 2538, 2603, 2558, 2571, 2576, 2612, 2583, 2506, 2509, 2515, 2461, 2544, 2584, 2607, 2604, 2530, 2537, 2577, 2586, 2598, 2574, 2469, 2517, 2594, 2518, 2545, 2486, 2593, 2590, 2608, 2614, 2615, 2556, 2596, 2513, 2606, 2701, 2703, 2702, 2711, 2704, 2725, 2694, 2564, 2668, 2572, 2632, 2588, 2659, 2623, 2675, 2647, 2640, 2651, 2635, 2655, 2624, 2667, 2628, 2610, 2656, 2652, 2643, 2669, 2664, 2595, 2601, 2670, 2650, 2657, 2663, 2622, 2658, 2629, 2617, 2625, 2690, 2609, 2613, 2654, 2665, 2597, 2566, 2636, 2662, 2660, 2642, 2602, 2644, 2631, 2646, 2591, 2621, 2570, 2648, 2630, 2639, 2666, 2649, 2645, 2671, 2689, 2672, 2691, 2699, 2638, 2634, 2680, 2686, 2605, 2637, 2697, 2709, 2712, 2641, 2695, 2633, 2679, 2673, 2626, 2684, 2674, 2599, 2681, 2714, 2727, 2677, 2708, 2618, 2729, 2713, 2707, 2685, 2723, 2592, 2688, 2735, 2719, 2683, 2568, 2687, 2696, 2676, 2732, 2740, 2715, 2627, 2700, 2726, 2710, 2653, 2716, 2692, 2722, 2682, 2678, 2706, 2661, 2693, 2734, 2736, 2751, 2724, 2731, 2743, 2748, 2777, 2752, 2733, 2720, 2758, 2738, 2763, 2741, 2755, 2756, 2761, 2759, 2769, 2750, 2767, 2762, 2705, 2739, 2765, 2771, 2784, 2744, 2753, 2747, 2746, 2760, 2775, 2766, 2737, 2698, 2754, 2717, 2764, 2728, 2742, 2773, 2770, 2730, 2779, 2768, 2757, 2783, 2778, 2788, 2749, 2721, 2793, 2745, 2800, 2798, 2786, 2796, 2790, 2781, 2801, 2830, 2792, 2816, 2825, 2780, 2820, 2831, 2812, 2718, 2822, 2821, 2844, 2806, 2824, 2834, 2797, 2853, 2794, 2807, 2804, 2802, 2846, 2810, 2809, 2791, 2855, 2817, 2837, 2813, 2782, 2826, 2805, 2772, 2774, 2795, 2803, 2799, 2845, 2811, 2835, 2787, 2833, 2819, 2827, 2785, 2848, 2815, 2789, 2818, 2849, 2829, 2850, 2776, 2856, 2854, 2814, 2839, 2860, 2851, 2847, 2823, 2842, 2836, 2840, 2852, 2859, 2872, 2838, 2832, 2808, 2841, 2866, 2865, 2843, 2828, 2868, 2878, 2871, 2876, 2875, 2879, 2857, 2864, 2869, 2861, 2858, 2886, 2870, 2881, 2867, 2883, 2897, 2884, 2900, 2896, 2874, 2894, 2863, 2880, 2901, 2895, 2889, 2898, 2891, 2862, 2885, 2892, 2893, 2882, 2877, 2887, 2873, 2888, 2899, 2912, 2914, 2917, 2890, 2904, 2911, 2918, 2903, 2908, 2916, 2905, 2910, 2907, 2906, 2902, 2915, 2913, 2909, 2919, 2923, 2928, 2920, 2931, 2922, 2927, 2932, 2929, 2925, 2934, 2926, 2921, 2924, 2930, 2936, 2933, 2944, 2939, 2942, 2940, 2943, 2945, 2946, 2941, 2938, 2950, 2935, 2949, 2937, 2948, 2947, 2953, 2955, 2959, 2952, 2951, 2956, 2954, 2957, 2958, 2961, 2964, 2963, 2967, 2962, 2960, 2968, 2965, 2966, 2969, 2972, 2978, 2971, 2970, 2973, 2976, 2974, 2977, 2979, 2975, 2981, 2983, 2980, 2995, 2991, 2986, 2982, 2989, 2996, 2992, 2993, 2984, 2990, 2994, 2987, 2985, 2988, 2997, 2998, 2999, 3000])
```

### Whois
```bash
Escolha uma opção: 2
Digite o IP ou domínio para consulta WHOIS (ex.: 172.217.172.142 ou google.com): google.com

=== WHOIS de google.com ===

Domain Name      : GOOGLE.COM
Registrar        : MarkMonitor, Inc.
Whois Server     : whois.markmonitor.com
Updated Date     : [datetime.datetime(2019, 9, 9, 15, 39, 4), datetime.datetime(2024, 8, 2, 2, 17, 33, tzinfo=datetime.timezone.utc)]
Creation Date    : [datetime.datetime(1997, 9, 15, 4, 0), datetime.datetime(1997, 9, 15, 7, 0, tzinfo=datetime.timezone.utc)]
Expiration Date  : [datetime.datetime(2028, 9, 14, 4, 0), datetime.datetime(2028, 9, 13, 7, 0, tzinfo=datetime.timezone.utc)]
Name Servers     : ['NS1.GOOGLE.COM', 'NS2.GOOGLE.COM', 'NS3.GOOGLE.COM', 'NS4.GOOGLE.COM']
Status           : ['clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited', 'clientTransferProhibited https://icann.org/epp#clientTransferProhibited', 'clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited', 'serverDeleteProhibited https://icann.org/epp#serverDeleteProhibited', 'serverTransferProhibited https://icann.org/epp#serverTransferProhibited', 'serverUpdateProhibited https://icann.org/epp#serverUpdateProhibited', 'clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)', 'clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)', 'clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)', 'serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)', 'serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)', 'serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)']
Emails           : ['abusecomplaints@markmonitor.com', 'whoisrequest@markmonitor.com']
Dnssec           : unsigned
domain_name: GOOGLE.COM
registrar: MarkMonitor, Inc.
registrar_url: http://www.markmonitor.com
reseller: None
whois_server: whois.markmonitor.com
referral_url: None
updated_date: [datetime.datetime(2019, 9, 9, 15, 39, 4), datetime.datetime(2024, 8, 2, 2, 17, 33, tzinfo=datetime.timezone.utc)]
creation_date: [datetime.datetime(1997, 9, 15, 4, 0), datetime.datetime(1997, 9, 15, 7, 0, tzinfo=datetime.timezone.utc)]
expiration_date: [datetime.datetime(2028, 9, 14, 4, 0), datetime.datetime(2028, 9, 13, 7, 0, tzinfo=datetime.timezone.utc)]
name_servers: ['NS1.GOOGLE.COM', 'NS2.GOOGLE.COM', 'NS3.GOOGLE.COM', 'NS4.GOOGLE.COM']
status: ['clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited', 'clientTransferProhibited https://icann.org/epp#clientTransferProhibited', 'clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited', 'serverDeleteProhibited https://icann.org/epp#serverDeleteProhibited', 'serverTransferProhibited https://icann.org/epp#serverTransferProhibited', 'serverUpdateProhibited https://icann.org/epp#serverUpdateProhibited', 'clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)', 'clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)', 'clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)', 'serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)', 'serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)', 'serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)']
emails: ['abusecomplaints@markmonitor.com', 'whoisrequest@markmonitor.com']
dnssec: unsigned
name: None
org: Google LLC
address: None
city: None
state: CA
registrant_postal_code: None
country: US
```

### DNS Enumeration
```bash
Escolha uma opção: 3
Digite o domínio para DNS enumeration (google.com): google.com

=== DNS Enumeration de google.com ===


=== Registro A de google.com ===
172.217.29.174

=== Registro AAAA de google.com ===
2800:3f0:4001:837::200e

=== Registro MX de google.com ===
10 smtp.google.com.

=== Registro NS de google.com ===
ns2.google.com.
ns1.google.com.
ns3.google.com.
ns4.google.com.
Erro consultando TXT: The resolution lifetime expired after 5.107 seconds: Server Do53:181.213.132.2@53 answered The DNS operation timed out.; Server Do53:181.213.132.3@53 answered The DNS operation timed out.; Server Do53:192.168.15.1@53 answered ; Server Do53:192.168.15.1@53 answered The DNS operation timed out.

=== Registro SOA de google.com ===
ns1.google.com. dns-admin.google.com. 754990191 900 900 1800 60
Nenhuma resposta para CNAME
```

### WAFW00F
```bash
Escolha uma opção: 4
Digite a URL para análise de tecnologias (ex: https://www.example.com): https://www.google.com/
Executando: wafw00f http://google.com

=== WAFW00F Scan de http://google.com ===

                   ______
                  /      \
                 (  Woof! )
                  \  ____/                      )
                  ,,                           ) (_
             .-. -    _______                 ( |__|
            ()``; |==|_______)                .)|__|
            / ('        /|\                  (  |__|
        (  /  )        / | \                  . |__|
         \(_)_))      /  |  \                   |__|

                    ~ WAFW00F : v2.3.1 ~
    The Web Application Firewall Fingerprinting Toolkit

[*] Checking http://google.com
[+] Generic Detection results:
[-] No WAF detected by the generic detection
[~] Number of requests: 7
```

### Nmap Vulnerability Scan
```bash
Escolha uma opção: 5
Digite o alvo para Vulnerability Scan (IP-192.168.1.1 ou domínio-google.com): google.com
Digite o range de portas (padrão all ports ou ex: 1-65535):
Filtrar CVEs com severidade mínima (ex: 5.5). Pressione Enter para sem filtro: 7
Executando: nmap -sV --script=vuln google.com

=== Nmap Vulnerability Scan de google.com ===
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-05 21:48 Hora oficial do Brasil
Pre-scan script results:
| broadcast-avahi-dos:
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Nmap scan report for google.com (172.217.29.174)
Host is up (0.046s latency).
Other addresses for google.com (not scanned): 2800:3f0:4001:837::200e
rDNS record for 172.217.29.174: pngrua-ae-in-f14.1e100.net
Not shown: 997 filtered tcp ports (no-response), 1 filtered tcp ports (net-unreach)
PORT    STATE SERVICE   VERSION
80/tcp  open  http      gws
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.0 200 OK
|     Date: Tue, 06 May 2025 00:49:36 GMT
|     Expires: -1
|     Cache-Control: private, max-age=0
|     Content-Type: text/html; charset=ISO-8859-1
|     Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-hGOlI6qf-5SGmF4CPysvEw' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
|     P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
|     Server: gws
|     X-XSS-Protection: 0
|     X-Frame-Options: SAMEORIGIN
|     Set-Cookie: AEC=AVcja2fPFfHv2IErujbEn5CVaUxgLqev1avNdZEv_VoubW3h2ASKa4n2kA; expires=Sun, 02-Nov-2025 00:49:36 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
|     Set-Cookie: NID=523=eexbZ3U_cSjeSPx-OomoXrJ8zadmVJBTUSPv3p894l1BRAbpCk0r8Zq7xQ2Fz0jjevgY5MnxtB-59hFoaVEmo47kvak_NuJyR9E52OQMRzHc8zaBHFg7pGAyO_nQuqNcsN-0TPLXLg_MOuemABfy7XQEuIFYX7d1V9a3lMHaDUanMB0lLFeYS
|   HTTPOptions:
|     HTTP/1.0 405 Method Not Allowed
|     Content-Type: text/html; charset=UTF-8
|     Referrer-Policy: no-referrer
|     Content-Length: 1592
|     Date: Tue, 06 May 2025 00:49:36 GMT
|     <!DOCTYPE html>
|     <html lang=en>
|     <meta charset=utf-8>
|     <meta name=viewport content="initial-scale=1, minimum-scale=1, width=device-width">
|     <title>Error 405 (Method Not Allowed)!!1</title>
|     <style>
|_    *{margin:0;padding:0}html,code{font:15px/22px arial,sans-serif}html{background:#fff;color:#222;padding:15px}body{margin:7% auto 0;max-width:390px;min-height:180px;padding:30px 0 15px}* > body{background:url(//www.google.com/images/errors/robot.png) 100% 5px no-repeat;padding-right:205px}p{margin:11px 0 22px;overflow:hidden}ins{color:#777;text-decoration:none}a img{border:0}@media screen and (max-width:772px){body{background:none;margin-top:0;max-width:none;padding-right:0}}#logo{background:url(//www.google.com/images/branding
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-csrf:
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=google.com
|   Found the following possible CSRF vulnerabilities:
|
|     Path: http://www.google.com:80/
|     Form id: tsuid_4lwzalzuo9325oup1eosmai_1
|     Form action: /search
|
|     Path: http://www.google.com:80/webhp
|     Form id: tsuid_5lwzapkmkmyy5oupr4an-ak_1
|     Form action: /search
|
|     Path: http://www.google.com:80/
|     Form id: tsuid_4lwzalzuo9325oup1eosmai_1
|     Form action: /search
|
|     Path: http://www.google.com:80/
|     Form id: tsuid_4lwzalzuo9325oup1eosmai_1
|_    Form action: /search
|_http-server-header: gws
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
443/tcp open  ssl/https gws
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.0 200 OK
|     Date: Tue, 06 May 2025 00:49:42 GMT
|     Expires: -1
|     Cache-Control: private, max-age=0
|     Content-Type: text/html; charset=ISO-8859-1
|     Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-yCsGkDCroiZtjtrwktOOQA' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
|     Accept-CH: Sec-CH-Prefers-Color-Scheme
|     P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
|     Server: gws
|     X-XSS-Protection: 0
|     X-Frame-Options: SAMEORIGIN
|     Set-Cookie: AEC=AVcja2colmV6Xmb-xrJ2SNKf2AGlZ88jWxOee6-47Crlpx6d_7pULCAYmA; expires=Sun, 02-Nov-2025 00:49:42 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
|_    Set-Cookie: NID=523=dMgKOpucZDK_0v6Sp-kHr5dRm9bMVN7-Djlf0sqCx-spcQ8TgO5vJc9QzxNMffUSeEC8j-rQFmY8IdGGKDEuWL1Kkv5VbaPvnleeWVCRO6HQqjMUwOIdRlg0qBMqmvhxMjtUygVc6Y-rP
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-csrf:
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=google.com
|   Found the following possible CSRF vulnerabilities:
|
|     Path: https://www.google.com:443/
|     Form id: tsuid_4vwzainhmkjd5oup1moi4qu_1
|     Form action: /search
|
|     Path: https://www.google.com:443/
|     Form id: tsuid_4vwzainhmkjd5oup1moi4qu_1
|     Form action: /search
|
|     Path: https://www.google.com:443/webhp
|     Form id: tsuid_5vwzanlhc8c65oupqeer2ag_1
|     Form action: /search
|
|     Path: https://www.google.com:443/preferences?hl=pt-BR
|     Form id: k8h6ob
|     Form action: /setprefs
|
|     Path: https://www.google.com:443/imghp?hl=pt-BR&tab=wi
|     Form id: tsuid_6vwzaixhjjly5oupzla3sqm_1
|_    Form action: https://www.google.com/search
|_http-server-header: gws
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port80-TCP:V=7.95%I=7%D=5/5%Time=68195CA0%P=i686-pc-windows-windows%r(G
SF:etRequest,3728,"HTTP/1\.0\x20200\x20OK\r\nDate:\x20Tue,\x2006\x20May\x2
SF:02025\x2000:49:36\x20GMT\r\nExpires:\x20-1\r\nCache-Control:\x20private
SF:,\x20max-age=0\r\nContent-Type:\x20text/html;\x20charset=ISO-8859-1\r\n
SF:Content-Security-Policy-Report-Only:\x20object-src\x20'none';base-uri\x
SF:20'self';script-src\x20'nonce-hGOlI6qf-5SGmF4CPysvEw'\x20'strict-dynami
SF:c'\x20'report-sample'\x20'unsafe-eval'\x20'unsafe-inline'\x20https:\x20
SF:http:;report-uri\x20https://csp\.withgoogle\.com/csp/gws/other-hp\r\nP3
SF:P:\x20CP=\"This\x20is\x20not\x20a\x20P3P\x20policy!\x20See\x20g\.co/p3p
SF:help\x20for\x20more\x20info\.\"\r\nServer:\x20gws\r\nX-XSS-Protection:\
SF:x200\r\nX-Frame-Options:\x20SAMEORIGIN\r\nSet-Cookie:\x20AEC=AVcja2fPFf
SF:Hv2IErujbEn5CVaUxgLqev1avNdZEv_VoubW3h2ASKa4n2kA;\x20expires=Sun,\x2002
SF:-Nov-2025\x2000:49:36\x20GMT;\x20path=/;\x20domain=\.google\.com;\x20Se
SF:cure;\x20HttpOnly;\x20SameSite=lax\r\nSet-Cookie:\x20NID=523=eexbZ3U_cS
SF:jeSPx-OomoXrJ8zadmVJBTUSPv3p894l1BRAbpCk0r8Zq7xQ2Fz0jjevgY5MnxtB-59hFoa
SF:VEmo47kvak_NuJyR9E52OQMRzHc8zaBHFg7pGAyO_nQuqNcsN-0TPLXLg_MOuemABfy7XQE
SF:uIFYX7d1V9a3lMHaDUanMB0lLFeYS")%r(HTTPOptions,6DC,"HTTP/1\.0\x20405\x20
SF:Method\x20Not\x20Allowed\r\nContent-Type:\x20text/html;\x20charset=UTF-
SF:8\r\nReferrer-Policy:\x20no-referrer\r\nContent-Length:\x201592\r\nDate
SF::\x20Tue,\x2006\x20May\x202025\x2000:49:36\x20GMT\r\n\r\n<!DOCTYPE\x20h
SF:tml>\n<html\x20lang=en>\n\x20\x20<meta\x20charset=utf-8>\n\x20\x20<meta
SF:\x20name=viewport\x20content=\"initial-scale=1,\x20minimum-scale=1,\x20
SF:width=device-width\">\n\x20\x20<title>Error\x20405\x20\(Method\x20Not\x
SF:20Allowed\)!!1</title>\n\x20\x20<style>\n\x20\x20\x20\x20\*{margin:0;pa
SF:dding:0}html,code{font:15px/22px\x20arial,sans-serif}html{background:#f
SF:ff;color:#222;padding:15px}body{margin:7%\x20auto\x200;max-width:390px;
SF:min-height:180px;padding:30px\x200\x2015px}\*\x20>\x20body{background:u
SF:rl\(//www\.google\.com/images/errors/robot\.png\)\x20100%\x205px\x20no-
SF:repeat;padding-right:205px}p{margin:11px\x200\x2022px;overflow:hidden}i
SF:ns{color:#777;text-decoration:none}a\x20img{border:0}@media\x20screen\x
SF:20and\x20\(max-width:772px\){body{background:none;margin-top:0;max-widt
SF:h:none;padding-right:0}}#logo{background:url\(//www\.google\.com/images
SF:/branding");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port443-TCP:V=7.95%T=SSL%I=7%D=5/5%Time=68195CA6%P=i686-pc-windows-wind
SF:ows%r(GetRequest,2094,"HTTP/1\.0\x20200\x20OK\r\nDate:\x20Tue,\x2006\x2
SF:0May\x202025\x2000:49:42\x20GMT\r\nExpires:\x20-1\r\nCache-Control:\x20
SF:private,\x20max-age=0\r\nContent-Type:\x20text/html;\x20charset=ISO-885
SF:9-1\r\nContent-Security-Policy-Report-Only:\x20object-src\x20'none';bas
SF:e-uri\x20'self';script-src\x20'nonce-yCsGkDCroiZtjtrwktOOQA'\x20'strict
SF:-dynamic'\x20'report-sample'\x20'unsafe-eval'\x20'unsafe-inline'\x20htt
SF:ps:\x20http:;report-uri\x20https://csp\.withgoogle\.com/csp/gws/other-h
SF:p\r\nAccept-CH:\x20Sec-CH-Prefers-Color-Scheme\r\nP3P:\x20CP=\"This\x20
SF:is\x20not\x20a\x20P3P\x20policy!\x20See\x20g\.co/p3phelp\x20for\x20more
SF:\x20info\.\"\r\nServer:\x20gws\r\nX-XSS-Protection:\x200\r\nX-Frame-Opt
SF:ions:\x20SAMEORIGIN\r\nSet-Cookie:\x20AEC=AVcja2colmV6Xmb-xrJ2SNKf2AGlZ
SF:88jWxOee6-47Crlpx6d_7pULCAYmA;\x20expires=Sun,\x2002-Nov-2025\x2000:49:
SF:42\x20GMT;\x20path=/;\x20domain=\.google\.com;\x20Secure;\x20HttpOnly;\
SF:x20SameSite=lax\r\nSet-Cookie:\x20NID=523=dMgKOpucZDK_0v6Sp-kHr5dRm9bMV
SF:N7-Djlf0sqCx-spcQ8TgO5vJc9QzxNMffUSeEC8j-rQFmY8IdGGKDEuWL1Kkv5VbaPvnlee
SF:WVCRO6HQqjMUwOIdRlg0qBMqmvhxMjtUygVc6Y-rP");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 390.31 seconds

Deseja visualizar resumo das vulnerabilidades? (s/n): s
Nenhuma vulnerabilidade atende ao filtro definido.
```

### Wappalyzer
```bash
Escolha uma opção: 6
Digite a URL para análise de tecnologias (ex: https://www.example.com): https://www.google.com/

=== Wappalyzer Scan de http://google.com ===
       Tecnologia Versão    Categorias   Grupos
Google Web Server          Web servers  Servers
             HSTS             Security Security
           HTTP/2        Miscellaneous    Other
           HTTP/3        Miscellaneous    Other
```