import argparse
import asyncio


from proxy_scanner import scan_ranges
from ranges import RANGES
from proxy_database import ProxyDatabase
from proxy_checker import check_proxy
from proxy_api import start_api_server
from dotenv import load_dotenv



import os




def parse_args():
    parser = argparse.ArgumentParser(description='Proxy Scanner and Checker')

    parser.add_argument('--database-uri', dest='database_uri', type=str, default='postgresql://localhost/proxy_database',
                        help='URI for the database (default: postgresql://localhost/proxy_database)')

    parser.add_argument('--proxy-ranges', dest='proxy_ranges', type=str, default='',
                        help='Comma-separated list of IP ranges for scanning (e.g. "192.168.1.0/24,10.0.0.0/8")')

    parser.add_argument('--proxy-scan-threads', dest='proxy_scan_threads', type=int, default=10,
                        help='Number of threads for scanning ports (default: 10)')

    parser.add_argument('--proxy-check-threads', dest='proxy_check_threads', type=int, default=10,
                        help='Number of threads for checking proxies (default: 10)')

    parser.add_argument('--api-host', dest='api_host', type=str, default='localhost',
                        help='API server host (default: localhost)')

    parser.add_argument('--api-port', dest='api_port', type=int, default=8080,
                        help='API server port (default: 8080)')

    parser.add_argument('--scan', dest='scan', action='store_true', default=False,
                        help='Run port scanning')

    parser.add_argument('--check', dest='check', action='store_true', default=False,
                        help='Run proxy checking')

    args = parser.parse_args()
    return args


async def run_scanner(database_uri, proxy_ranges, proxy_scan_threads):
    async with ProxyDatabase(database_uri) as db:
        scanner = scan_ranges(proxy_ranges, proxy_scan_threads, db)
        await scanner.scan()


async def run_checker(database_uri, proxy_check_threads):
    async with ProxyDatabase(database_uri) as db:
        tasks = [check_proxy(proxy) for proxy in db.get_all_proxies()]
        await asyncio.gather(*tasks)



def main():
    args = parse_args()

    if args.scan:
        asyncio.run(run_scanner(args.database_uri, args.proxy_ranges, args.proxy_scan_threads))

    if args.check:
        asyncio.run(run_checker(args.database_uri, args.proxy_check_threads))

    if not args.scan and not args.check:
        async def start_services():
            async with ProxyDatabase(args.database_uri) as db:
                tasks = [
                    start_api_server(args.api_host, args.api_port),
                    scan_ranges(args.proxy_ranges, args.proxy_scan_threads, db).scan(),
                    check_proxy(db).check_proxy(args.proxy_check_threads)
                ]
                await asyncio.gather(*tasks)
        asyncio.run(start_services())


if __name__ == '__main__':
    load_dotenv()
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')
    main()

