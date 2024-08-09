#!/usr/bin/env python3

import asyncio
import socket
import time
import sys


async def scan_single_port(ip: str, port: int) -> dict:
    result: dict = {
        "port": port,
        "status": "closed",
        "data": ""
    }
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        result["status"] = "open"
        result["data"] = await asyncio.wait_for(reader.read(1024), timeout=3)
        writer.close()
        await writer.wait_closed()
    except (ConnectionRefusedError, asyncio.TimeoutError, OSError):
        pass

    print(f"port {result['port']} is {result['status']}")

    return result


async def scan_multiple_ports(ip: str, ports: list) -> list[dict]:
    print("Target IP:", ip)
    print("Ports:", ports)

    tasks = [scan_single_port(ip, port) for port in ports]
    results = list(await asyncio.gather(*tasks))
    return results


start_time = time.perf_counter()

url = "scanme.nmap.org"
ipaddr = socket.gethostbyname(url)
ports_to_scan = [i for i in range(100)]
scan_results = asyncio.run(scan_multiple_ports(ipaddr, ports_to_scan))
print(scan_results)

total_time = time.perf_counter() - start_time
print(f"Executed in {total_time:.2f} seconds")
