
import concurrent.futures
from datetime import datetime
from typing import List, Tuple
import asyncio
import concurrent.futures
import ipaddress
import datetime

from proxy_database import ProxyDatabase


async def scan_proxy(proxy_ip: str, port: int) -> bool:
    """Scan proxy for a given port."""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(proxy_ip, port), timeout=5)
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


def scan_range(range_ip: str, proxy_ports: List[int], proxy_db: ProxyDatabase):
    """Scan a range of IPs for open proxy ports and save to the database."""
    range_network = ipaddress.ip_network(range_ip, strict=False)
    for host_ip in range_network.hosts():
        proxy_ip = str(host_ip)
        port_scan_results = []
        for port in proxy_ports:
            result = asyncio.run(scan_proxy(proxy_ip, port))
            port_scan_results.append(result)
        proxy_alive = any(port_scan_results)
        last_checked = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        proxy_db.set_proxy_status(proxy_ip, proxy_alive)


def scan_ranges(ranges: List[Tuple[str, List[int]]], proxy_db: ProxyDatabase, num_threads: int = 5):
    """Scan multiple ranges of IPs for open proxy ports and save to the database."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for range_ip, proxy_ports in ranges:
            executor.submit(scan_range, range_ip, proxy_ports, proxy_db)


if __name__ == '__main__':
    # Load ranges from the ranges module
    from ranges import RU_RANGES, UA_RANGES, KZ_RANGES, EU_RANGES, AM_RANGES, CN_RANGES, TW_RANGES, TH_RANGES, JP_RANGES

    ranges = RU_RANGES + UA_RANGES + KZ_RANGES + EU_RANGES + AM_RANGES + CN_RANGES + TW_RANGES + TH_RANGES + JP_RANGES

    # Proxy ports to scan
    proxy_ports = [80, 8080, 3128]

    # Create a proxy database instance
    proxy_db = ProxyDatabase()

    # Scan the ranges for proxy ports and update the database
    scan_ranges(ranges, proxy_db)
