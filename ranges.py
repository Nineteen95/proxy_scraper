
import ipaddress

# Диапазоны IP-адресов для стран
RANGES = {
    'RU': ['31.0.0.0/8', '46.0.0.0/8', '62.0.0.0/8'],
    'UA': ['77.0.0.0/8', '93.0.0.0/8', '213.0.0.0/8'],
    'KZ': ['2.0.0.0/8', '5.0.0.0/8', '37.0.0.0/8'],
    'EU': ['31.0.0.0/8', '46.0.0.0/8', '62.0.0.0/8', '77.0.0.0/8', '93.0.0.0/8', '213.0.0.0/8'],
    'US': ['23.0.0.0/8', '34.0.0.0/8', '52.0.0.0/8', '54.0.0.0/8', '104.0.0.0/8', '198.0.0.0/8'],
    'CN': ['1.0.0.0/8', '27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8', '42.0.0.0/8', '43.0.0.0/8'],
    'TW': ['27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8', '42.0.0.0/8', '43.0.0.0/8', '49.0.0.0/8'],
    'TH': ['1.0.0.0/8', '14.0.0.0/8', '27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8', '42.0.0.0/8'],
    'JP': ['1.0.0.0/8', '27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8', '42.0.0.0/8', '43.0.0.0/8', '49.0.0.0/8']
}

# Список часто используемых портов
PORTS = [80, 8080, 3128, 8888]