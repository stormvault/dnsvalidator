#!/usr/bin/env python3
#

import sys
import os
import asyncio
import geoip2
import geoip2.webservice

MAXMIND_KEY=os.environ.get('MAXMIND_KEY')


async def main(listfile):
    """Fetch MaxMind records from items in a file..
    """
    ips = [ip.strip() for ip in open(listfile, 'r').readlines()]
    for ip_addr in ips:
        ip_addr = ip_addr.strip()

        async with geoip2.webservice.AsyncClient(792098, MAXMIND_KEY) as client:
            response = await client.city(ip_address=ip_addr)
            yield {
                'ip': f"{ip_addr}",
                'city': f"{response.city.name}",
                'country': f"{response.country.iso_code}",
                'postal': f"{response.postal.code}",
            }


async def get_results(listfile):
    """Gather and show results.d
    """
    results = []
    async for res in main(listfile):
        results.append(res)

    for result in results:
        print(f"*** {result['ip']} ***")
        print(f" - city: {result['city']}")
        print(f" - country: {result['country']}")
        print(f" - postal: {result['postal']}")


if __name__ == "__main__":
    if not os.path.isfile(sys.argv[1]):
        print('error: {}: no such file'.format(sys.argv[1]))
        sys.exit(1)

    try:
        asyncio.run(get_results(sys.argv[1]))
    except KeyboardInterrupt as e:
        print(e)
        sys.exit(1)
