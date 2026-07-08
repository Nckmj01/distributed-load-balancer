import os
import asyncio
import aiohttp
import csv

URL = "http://localhost:5001/home"
TOTAL_REQUESTS = 10000

server_counts = {}


async def send_request(session):
    try:
        async with session.get(URL) as response:
            data = await response.json()
            message = data.get("message", "")
            server = message.split(":")[-1].strip()
            server_counts[server] = server_counts.get(server, 0) + 1
    except Exception:
        pass


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(TOTAL_REQUESTS):
            tasks.append(send_request(session))
        await asyncio.gather(*tasks)
asyncio.run(main())

print("\nRequest Distribution\n")

for server, count in sorted(server_counts.items()):
    print(f"Server {server}: {count}")

results_path = os.path.join(os.path.dirname(__file__), "modified_results_6_servers.csv")

with open(results_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Server", "Requests"])
    for server, count in sorted(server_counts.items()):
        writer.writerow([server, count])

print("\nResults saved to modified results.csv")