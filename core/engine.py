import argparse
import importlib
import threading
import time
from rich.console import Console
from rich.table import Table

console = Console()

def load_attack(attack_name):
    """بارگذاری پویای ماژول حمله"""
    try:
        module = importlib.import_module(f"attacks.{attack_name}")
        return module.run
    except ModuleNotFoundError:
        console.print(f"[red]❌ ماژول {attack_name} پیدا نشد.[/red]")
        return None

def show_banner():
    banner = """
[bold red]
    ╔═══════════════════════════════════════╗
    ║   🛡️  DDoS Simulation Toolkit  🛡️   ║
    ║     فقط برای تست نفوذ مجاز و آموزش    ║
    ╚═══════════════════════════════════════╝
[/bold red]
    """
    console.print(banner)

def main():
    show_banner()
    
    parser = argparse.ArgumentParser(description="ابزار شبیه‌سازی حملات DDoS - فقط آموزشی")
    parser.add_argument("--attack", required=True, help="نام حمله (مثلاً l7_http_flood)")
    parser.add_argument("--target", required=True, help="آدرس هدف (فقط سیستم‌های خودتان)")
    parser.add_argument("--port", type=int, default=443, help="پورت هدف")
    parser.add_argument("--threads", type=int, default=10, help="تعداد نخ‌های هم‌زمان")
    parser.add_argument("--duration", type=int, default=10, help="مدت زمان (ثانیه)")
    parser.add_argument("--rate", type=int, default=100, help="تعداد درخواست در ثانیه")

    args = parser.parse_args()

    console.print(f"\n[bold yellow]⚠️  هشدار:[/bold yellow] فقط روی سیستم‌های مجاز خودتان تست کنید!")
    console.print(f"[bold cyan]هدف:[/bold cyan] {args.target}:{args.port}")
    console.print(f"[bold cyan]حمله:[/bold cyan] {args.attack}")
    console.print(f"[bold cyan]مدت:[/bold cyan] {args.duration} ثانیه | [bold cyan]نخ‌ها:[/bold cyan] {args.threads}")

    # تأیید کاربر
    confirm = input("\n❓ آیا این سیستم تحت کنترل شماست؟ (yes/no): ")
    if confirm.lower() != 'yes':
        console.print("[red]❌ عملیات لغو شد.[/red]")
        return

    attack_func = load_attack(args.attack)
    if not attack_func:
        return

    console.print(f"\n[green]🚀 شروع شبیه‌سازی...[/green]")
    
    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=attack_func, args=(args.target, args.port, args.rate))
        t.daemon = True
        t.start()
        threads.append(t)

    time.sleep(args.duration)
    console.print("\n[bold green]✅ شبیه‌سازی پایان یافت.[/bold green]")
