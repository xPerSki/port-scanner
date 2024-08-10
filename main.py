#!/usr/bin/env python3

from typing import Dict
import asyncio
import socket
import time
import json
import pyperclip


async def scan_single_port(ip: str, port: int) -> Dict:
    result: Dict = {
        "port": port,
        "status": "closed",
        "data": ""
    }
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=3)
        result["status"] = "open"
        data = await asyncio.wait_for(reader.read(1024), timeout=3)
        result["data"] = data.decode()
        writer.close()
        await writer.wait_closed()
    except (ConnectionRefusedError, asyncio.TimeoutError, asyncio.CancelledError, OSError, UnicodeDecodeError):
        pass

    return result


async def scan_multiple_ports(ip: str, ports: list) -> json:
    tasks = [scan_single_port(ip, port) for port in ports]
    results = list(await asyncio.gather(*tasks))
    output: Dict = {
        "Target": ip,
        "Scan Results": results
    }
    return json.dumps(output, indent=4)


start_time = time.perf_counter()

url = "scanme.nmap.org"
ipaddr = socket.gethostbyname(url)
ports_to_scan = [i for i in range(10000)]
scan_results = asyncio.run(scan_multiple_ports(ipaddr, ports_to_scan))
pyperclip.copy(scan_results)
print("Copied results to clipboard")
print(scan_results)

total_time = time.perf_counter() - start_time
print(f"Executed in {total_time:.2f} seconds")
