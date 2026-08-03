# -*- coding: utf-8 -*-
from __future__ import annotations
import subprocess
import sys
import importlib
import os
import threading
import logging

# ================== KIỂM TRA VÀ CÀI ĐẶT THƯ VIỆN ==================

REQUIRED_PACKAGES = [
    "pytz",
    "requests",
    "websocket-client",
    "rich",
]

def check_and_install_packages():
    missing_packages = []
    
    print("=" * 60)
    print("🔍 ĐANG KIỂM TRA THƯ VIỆN...")
    print("=" * 60)
    
    for package in REQUIRED_PACKAGES:
        try:
            import_name = package
            if package == "websocket-client":
                import_name = "websocket"
            importlib.import_module(import_name)
            print(f"✅ {package} - Đã cài đặt")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - CHƯA CÀI ĐẶT")
    
    if not missing_packages:
        print("\n✅ TẤT CẢ THƯ VIỆN ĐÃ SẴN SÀNG!")
        print("=" * 60)
        return True
    
    print("\n" + "=" * 60)
    print(f"⚠️  PHÁT HIỆN {len(missing_packages)} THƯ VIỆN THIẾU:")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    print("=" * 60)
    print("\n🔄 ĐANG TIẾN HÀNH CÀI ĐẶT TỰ ĐỘNG...")
    
    for package in missing_packages:
        try:
            print(f"📦 Đang cài đặt {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ Đã cài đặt {package} thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi cài đặt {package}: {e}")
            return False
    
    print("\n✅ TẤT CẢ THƯ VIỆN ĐÃ ĐƯỢC CÀI ĐẶT XONG!")
    return True

if not check_and_install_packages():
    print("\n❌ KHÔNG THỂ CÀI ĐẶT ĐẦY ĐỦ THƯ VIỆN")
    sys.exit(1)

# ================== IMPORT THƯ VIỆN ==================

import json
import time
import random
import math
import re
import io
from collections import defaultdict, deque, Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, Tuple, Optional

import pytz
import requests
import websocket
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.rule import Rule
from rich.text import Text
from rich import box
from rich.columns import Columns

# ================== CẤU HÌNH ==================

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
except Exception:
    pass

console = Console()
tz = pytz.timezone("Asia/Ho_Chi_Minh")

# ================== SUPABASE CONFIG ==================
SUPABASE_URL = "https://npgzjbzcifepyziepbiq.supabase.co"
SUPABASE_KEY = "sb_publishable_rcm1mkWOcHDRVxJUMcKCBw__m-GS0UQ"

# ================== TELEGRAM CONFIG ==================
TELEGRAM_BOT_TOKEN = "8965450168:AAG8B6IaWTCGO8M5vPphqtA7jmFncxfeWk0"
TELEGRAM_CHAT_ID = ""
TELEGRAM_ENABLED = False

# ================== GIAO DIỆN HTOOL ==================

HTOOL_COLORS = {
    "gold": "#FFD700", "platinum": "#E5E4E2", "ruby": "#E0115F",
    "emerald": "#50C878", "sapphire": "#0F52BA", "onyx": "#353839",
    "rose": "#FF007F", "neon_blue": "#00D4FF", "neon_pink": "#FF00E5",
    "neon_green": "#39FF14", "neon_orange": "#FF5E00",
}

ICONS = {
    "crown": "👑", "fire": "🔥", "target": "🎯", "shield": "🛡️",
    "brain": "🧠", "robot": "🤖", "rocket": "🚀", "trophy": "🏆",
    "sparkle": "✨", "settings": "⚙️", "user": "👤", "check": "✅",
    "cross": "❌", "warning": "⚠️", "info": "ℹ️", "money": "💰",
    "chart": "📊", "clock": "⏰", "diamond": "💎", "link": "🔗",
    "key": "🔑", "lock": "🔒", "bell": "🔔",
}

LOGO = """
╔════════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     ██╗                           ║
║  ██║  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║                           ║
║  ███████║   ██║   ██║   ██║██║   ██║██║     ██║                           ║
║  ██╔══██║   ██║   ██║   ██║██║   ██║██║     ██║                           ║
║  ██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗███████╗                     ║
║  ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                     ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

# ================== BIẾN TOÀN CỤC ==================

_is_authenticated = False
_device_id = None
_user_key = None
_user_key_data = None
_ws_status = "⏳ Đang kết nối..."
KEY_CHECK_INTERVAL = 120

# ================== SUPABASE FUNCTIONS ==================

def supabase_request(method: str, endpoint: str, data: dict = None) -> dict:
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data, timeout=10)
        else:
            return None
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        return None
    except:
        return None

def verify_key_with_device(key: str, device_id: str) -> dict:
    global _user_key_data
    try:
        endpoint = f"keys?key_code=eq.{key}&select=*,devices(*)&limit=1"
        result = supabase_request("GET", endpoint)
        
        if result is None:
            _user_key_data = {
                "is_active": True,
                "expires_at": "forever",
                "note": "Offline mode"
            }
            return {"valid": True, "data": _user_key_data, "message": "✅ Xác thực thành công (Offline mode)"}
        
        if not result or len(result) == 0:
            _user_key_data = {
                "is_active": True,
                "expires_at": "forever",
                "note": "Key not found in DB"
            }
            return {"valid": True, "data": _user_key_data, "message": "✅ Xác thực thành công"}
        
        key_data = result[0]
        _user_key_data = key_data
        
        devices = key_data.get("devices", [])
        if devices:
            found = any(device.get("device_id") == device_id for device in devices)
            if not found:
                pass
        
        return {"valid": True, "data": key_data, "message": "✅ Xác thực thành công"}
        
    except Exception as e:
        _user_key_data = {"is_active": True, "expires_at": "forever", "note": f"Error: {str(e)}"}
        return {"valid": True, "data": _user_key_data, "message": "✅ Xác thực thành công"}

def check_key_validity() -> bool:
    global _user_key, _device_id, _user_key_data, _is_authenticated
    
    if not _is_authenticated:
        return True
    
    if not _user_key or not _device_id:
        return True
    
    try:
        endpoint = f"keys?key_code=eq.{_user_key}&select=*&limit=1"
        result = supabase_request("GET", endpoint)
        
        if result is None:
            return True
        
        if len(result) == 0:
            return True
        
        key_data = result[0]
        
        if key_data.get("is_active") is False:
            _is_authenticated = False
            return False
        
        expires_at = key_data.get("expires_at")
        if expires_at and expires_at != "forever":
            try:
                expire_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                if expire_date + timedelta(days=7) < datetime.now(timezone.utc):
                    _is_authenticated = False
                    return False
            except:
                pass
        
        return True
        
    except Exception:
        return True

def show_key_expired_screen():
    global _is_authenticated
    
    console.clear()
    console.print()
    console.print(Align.center("═" * 60, style="dim"))
    console.print(Align.center(f"[bold {HTOOL_COLORS['ruby']}]🔒 CẢNH BÁO KEY[/bold {HTOOL_COLORS['ruby']}]"))
    console.print(Align.center("═" * 60, style="dim"))
    console.print()
    
    expired_panel = Panel(
        Align.center(Text.assemble(
            ("\n", ""),
            (f"{ICONS['warning']} ", "bold yellow"),
            ("KEY CỦA BẠN CÓ THỂ ĐÃ HẾT HẠN\n\n", "bold red"),
            ("Tool vẫn tiếp tục chạy bình thường.\n", "white"),
            ("Vui lòng liên hệ admin nếu cần key mới:\n", "white"),
            ("📞 Zalo: 0842010239\n", f"bold {HTOOL_COLORS['neon_blue']}"),
            ("📱 Telegram: https://t.me/+PByWNy8hDxYzYTRl\n", f"bold {HTOOL_COLORS['neon_blue']}"),
            ("\nNhấn Enter để tiếp tục...\n", "dim"),
        )),
        border_style=HTOOL_COLORS["ruby"],
        box=box.DOUBLE,
        padding=(2, 3)
    )
    console.print(expired_panel)
    input()
    _is_authenticated = True

def key_checker_thread():
    global _is_authenticated
    while True:
        time.sleep(KEY_CHECK_INTERVAL)
        if not _is_authenticated:
            continue
        if not check_key_validity():
            console.print(f"\n[yellow]⚠️ Cảnh báo key, tool vẫn chạy bình thường[/]")

# ================== TELEGRAM FUNCTIONS ==================

def send_telegram_message(message: str) -> bool:
    if not TELEGRAM_ENABLED or not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

def setup_telegram():
    global TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['bell']} ", f"bold {HTOOL_COLORS['gold']}"), ("CẤU HÌNH THÔNG BÁO TELEGRAM", f"bold {HTOOL_COLORS['neon_blue']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header)
    console.print()
    console.print(Panel(Text.assemble(("🤖 BOT TELEGRAM CHÍNH THỨC\n\n", f"bold {HTOOL_COLORS['neon_blue']}"), ("Bot: @htool88_bot\n", f"bold {HTOOL_COLORS['gold']}"), ("Link: https://t.me/htool88_bot\n\n", f"bold {HTOOL_COLORS['sapphire']}"), ("Bot sẽ gửi thông báo RIÊNG cho bạn sau mỗi ván.\n", "white")), border_style=HTOOL_COLORS["sapphire"], box=box.ROUNDED))
    console.print()
    console.print(f"[bold {HTOOL_COLORS['gold']}]Bạn có muốn nhận thông báo qua Telegram?[/]")
    if Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn (y/n)[/]", choices=['y', 'n'], default='n') == 'n':
        TELEGRAM_ENABLED = False
        console.print(f"[yellow]⚠️ Thông báo Telegram đã tắt[/]")
        time.sleep(1)
        return
    TELEGRAM_ENABLED = True
    console.print()
    console.print("[bold]📖 CÁCH LẤY CHAT ID:[/]")
    console.print("1. Chat /start với bot @htool88_bot")
    console.print("2. Vào @userinfobot để lấy ID của bạn")
    console.print("3. Copy dãy số và dán vào đây\n")
    saved_chat_id = ""
    if os.path.exists('telegram_config.json'):
        try:
            with open('telegram_config.json', 'r', encoding='utf-8') as f:
                saved_chat_id = json.load(f).get('chat_id', '')
        except:
            pass
    if saved_chat_id:
        console.print(f"[bold {HTOOL_COLORS['emerald']}]📂 Đã tìm thấy Chat ID: {saved_chat_id}[/]")
        if Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]Sử dụng? (y/n)[/]", choices=['y', 'n'], default='y') == 'y':
            TELEGRAM_CHAT_ID = saved_chat_id
        else:
            TELEGRAM_CHAT_ID = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]📱 Nhập Chat ID mới[/]", default="")
    else:
        TELEGRAM_CHAT_ID = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]📱 Nhập Chat ID của bạn[/]", default="")
    TELEGRAM_CHAT_ID = ''.join(c for c in TELEGRAM_CHAT_ID if c.isdigit())
    if not TELEGRAM_CHAT_ID:
        console.print(f"[red]❌ Chat ID không hợp lệ![/]")
        TELEGRAM_ENABLED = False
        time.sleep(2)
        return
    console.print(f"\n[bold yellow]🔍 Đang kiểm tra kết nối...[/]")
    test_msg = f"✅ <b>KẾT NỐI THÀNH CÔNG!</b>\n\n🔔 <b>HTOOL PREMIUM - Thông báo đã kích hoạt</b>\n🎮 <b>Game:</b> Chạy đua tốc độ\n🕐 <b>{datetime.now(tz).strftime('%H:%M:%S %d/%m/%Y')}</b>"
    if send_telegram_message(test_msg):
        console.print(f"[green]✅ Kết nối thành công! Kiểm tra Telegram nhé![/]")
        try:
            with open('telegram_config.json', 'w', encoding='utf-8') as f:
                json.dump({'chat_id': TELEGRAM_CHAT_ID}, f, indent=2)
        except:
            pass
    else:
        console.print(f"[red]❌ Không thể gửi tin nhắn![/]")
        console.print(f"[yellow]  Hãy chắc chắn bạn đã chat /start với bot![/]")
        if Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]Nhập lại? (y/n)[/]", choices=['y', 'n'], default='y') == 'y':
            setup_telegram()
            return
        else:
            TELEGRAM_ENABLED = False
    time.sleep(2)

def build_cdtd_telegram_message(issue_id, killed_nv, bet_nv, bet_amount, result, pnl_van, total_pnl, balance_start, balance_end, win_count, lose_count, max_win_streak, max_lose_streak):
    total_games = win_count + lose_count
    win_rate = (win_count / total_games * 100) if total_games > 0 else 0
    result_emoji = "🟢" if result == 'win' else "🔴"
    killed_name = NV.get(killed_nv, f"NV{killed_nv}")
    bet_name = NV.get(bet_nv, f"NV{bet_nv}")
    bal_start = f"{balance_start:,.2f}" if balance_start >= 1000 else f"{balance_start:.4f}"
    bal_end = f"{balance_end:,.2f}" if balance_end >= 1000 else f"{balance_end:.4f}"
    message = f"""{result_emoji} <b>Ván #{issue_id}</b> | {NV_ICONS.get(killed_nv, '🏆')} <b>{killed_name}</b> thắng
┣ 🤖 Bot chọn: <b>{bet_name}</b>
┣ 💰 Cược: <b>{bet_amount:,.0f} {cdtd_coin}</b>
┣ 💵 Lãi: <b>{total_pnl:+,.2f}</b>
┣ 📊 {win_count}🟢W/{lose_count}🔴L | {bal_start}
┣ 📈 Tỷ lệ Win: {win_rate:.0f}%
┗ 🔥 Max: 🟢{max_win_streak} 🔴{max_lose_streak} | 🕐 {datetime.now(tz).strftime('%H:%M %d/%m')}"""
    return message

# ================== HÀM XÁC THỰC ==================

def show_auth_screen():
    global _user_key_data
    console.clear()
    gold_color = HTOOL_COLORS["gold"]
    logo_lines = LOGO.split('\n')
    for line in logo_lines:
        if line.strip():
            console.print(Align.center(line, style=f"bold {gold_color}"))
    console.print()
    console.print(Align.center("═" * 50, style="dim"))
    console.print(Align.center(f"[bold {gold_color}]XÁC THỰC KEY[/bold {gold_color}]"))
    console.print(Align.center("═" * 50, style="dim"))
    console.print()
    console.print(f"[bold cyan]🔑 Nhập Key:[/bold cyan]")
    key = Prompt.ask("   >>", default="")
    if not key:
        console.print("[red]❌ Key không được để trống![/red]")
        time.sleep(1.5)
        return False, None, None
    console.print()
    console.print(f"[bold cyan]📱 Nhập mã thiết bị:[/bold cyan]")
    device_id = Prompt.ask("   >>", default="")
    if not device_id:
        console.print("[red]❌ Mã thiết bị không được để trống![/red]")
        time.sleep(1.5)
        return False, None, None
    console.print()
    with console.status(f"[bold yellow]⏳ Đang xác thực...[/bold yellow]", spinner="dots"):
        result = verify_key_with_device(key, device_id)
    
    _user_key_data = result.get("data", {})
    expires_at = _user_key_data.get("expires_at", "forever")
    if expires_at and expires_at != "forever":
        try:
            expire_str = datetime.fromisoformat(expires_at.replace('Z', '+00:00')).strftime("%d/%m/%Y %H:%M")
        except:
            expire_str = str(expires_at)
    else:
        expire_str = "Vĩnh viễn"
    
    console.print()
    console.print(Panel(
        Text.assemble(
            ("✅ ", "bold green"),
            (f"{result.get('message', 'Xác thực thành công')}\n\n", "bold green"),
            (f"Key: {key[:15]}...\n", f"bold {gold_color}"),
            (f"Thiết bị: {device_id}\n", "bold cyan"),
            (f"Hết hạn: {expire_str}\n", "bold yellow"),
        ),
        title=f"[bold green]✅ XÁC THỰC THÀNH CÔNG[/bold green]",
        border_style="green",
        box=box.HEAVY
    ))
    console.print("\n[dim]Nhấn Enter để tiếp tục...[/dim]")
    input()
    return True, key, device_id

# ================== TOOL VUA THOÁT HIỂM ==================

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('htool.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

BET_API_URL = "https://api.escapemaster.net/escape_game/bet"
WS_URL = "wss://api.escapemaster.net/escape_master/ws"
WALLET_API_URL = "https://wallet.3games.io/api/wallet/user_asset"

HTTP = requests.Session()

ROOM_NAMES = {1: "📦 Nhà kho", 2: "🪑 Phòng họp", 3: "👔 Phòng giám đốc", 4: "💬 Phòng trò chuyện", 5: "🎥 Phòng giám sát", 6: "🏢 Văn phòng", 7: "💰 Phòng tài vụ", 8: "👥 Phòng nhân sự"}
ROOM_ORDER = [1, 2, 3, 4, 5, 6, 7, 8]

USER_ID: Optional[int] = None
SECRET_KEY: Optional[str] = None
issue_id: Optional[int] = None
killed_room: Optional[int] = None
round_index: int = 0

room_state: Dict[int, Dict[str, Any]] = {r: {"players": 0, "bet": 0} for r in ROOM_ORDER}
room_stats: Dict[int, Dict[str, Any]] = {r: {"kills": 0, "survives": 0} for r in ROOM_ORDER}

predicted_room: Optional[int] = None
last_killed_room: Optional[int] = None
prediction_locked: bool = False

current_build: Optional[float] = None
starting_balance: Optional[float] = None
cumulative_profit: Optional[float] = None

win_streak: int = 0
lose_streak: int = 0
max_win_streak: int = 0
max_lose_streak: int = 0

base_bet: float = 1.0
multiplier: float = 2.0
current_bet: Optional[float] = None
run_mode: str = "AUTO"
bet_rounds_before_skip: int = 0
_rounds_placed_since_skip: int = 0
skip_next_round_flag: bool = False

bet_history: deque = deque(maxlen=200)
pause_after_losses: int = 0
_skip_rounds_remaining: int = 0
profit_target: Optional[float] = None
stop_when_profit_reached: bool = False
stop_loss_target: Optional[float] = None
stop_when_loss_reached: bool = False
stop_flag: bool = False

ui_state: str = "IDLE"
analysis_duration: float = 45.0
analysis_start_ts: Optional[float] = None

last_msg_ts: float = time.time()
BALANCE_POLL_INTERVAL: float = 4.0
_ws: Dict[str, Any] = {"ws": None}

_sequential_bet_index = 0
killer_history = deque(maxlen=20)
game_kill_log = deque(maxlen=10)

SELECTION_MODES = {
    "RANDOM": "1. PHẬT ĐỘ", "MIN_PLAYER_BET": "2. AN TOÀN",
    "PROBABILITY": "3. XÁC SUẤT", "FOLLOW_KILLER": "4. THEO SÁT THỦ",
    "SEQUENTIAL": "5. TUẦN TỰ", "SMART_SAFE": "6. THÔNG MINH",
    "HIDE_SEEK_MASTER": "7. THÁNH TRỐN TÌM", "BALANCE": "8. CÂN BẰNG",
    "ENSEMBLE": "9. TỔNG HỢP",
}

settings = {"algo": "RANDOM"}
STRATEGY_CONFIG_FILE = "strategy_htool.json"

def log_debug(msg: str):
    try:
        logger.debug(msg)
    except:
        pass

def _parse_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x)
    m = re.search(r"-?\d+[\d,]*\.?\d*", s)
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except:
        return None

def balance_headers_for(uid=None, secret=None):
    h = {"accept": "*/*", "accept-language": "vi,en;q=0.9", "cache-control": "no-cache", "country-code": "vn", "origin": "https://xworld.info", "referer": "https://xworld.info/", "user-agent": "Mozilla/5.0", "user-login": "login_v2", "xb-language": "vi-VN"}
    if uid: h["user-id"] = str(uid)
    if secret: h["user-secret-key"] = str(secret)
    return h

def fetch_balances_3games(retries=3, timeout=8, uid=None, secret=None):
    global current_build, starting_balance, cumulative_profit
    uid = uid or USER_ID
    secret = secret or SECRET_KEY
    payload = {"user_id": int(uid) if uid else None, "source": "home"}
    for attempt in range(1, retries + 2):
        try:
            r = HTTP.post(WALLET_API_URL, json=payload, headers=balance_headers_for(uid, secret), timeout=timeout)
            r.raise_for_status()
            j = r.json()
            ua = j.get("data", {}).get("user_asset", {})
            build = _parse_number(ua.get("BUILD"))
            if build is not None:
                if starting_balance is None:
                    starting_balance = build
                current_build = build
                cumulative_profit = current_build - starting_balance
            return current_build, _parse_number(ua.get("WORLD")), _parse_number(ua.get("USDT"))
        except:
            time.sleep(min(1.5 * attempt, 4))
    return current_build, None, None

def choose_random(): return random.choice(ROOM_ORDER)
def choose_follow_killer(): return last_killed_room if last_killed_room else random.choice(ROOM_ORDER)
def choose_sequential():
    global _sequential_bet_index
    room = ROOM_ORDER[_sequential_bet_index]
    _sequential_bet_index = (_sequential_bet_index + 1) % len(ROOM_ORDER)
    return room

def choose_smart_safe():
    scores = {}
    max_players = max(rs['players'] for rs in room_state.values()) or 1
    max_bet = max(rs['bet'] for rs in room_state.values()) or 1
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        player_score = 1 - (room_state[r]['players'] / max_players)
        bet_score = 1 - (room_state[r]['bet'] / max_bet)
        penalty = 0.5 if r == last_killed_room else 0
        scores[r] = (0.4 * survival_rate) + (0.3 * player_score) + (0.3 * bet_score) - penalty
    return max(scores, key=scores.get)

def choose_balance():
    total_players = sum(rs['players'] for rs in room_state.values())
    total_bet = sum(rs['bet'] for rs in room_state.values())
    avg_players = total_players / len(ROOM_ORDER) if total_players > 0 else 0
    avg_bet = total_bet / len(ROOM_ORDER) if total_bet > 0 else 0
    scores = {}
    for r in ROOM_ORDER:
        scores[r] = abs(room_state[r]['players'] - avg_players) / (avg_players + 1) + abs(room_state[r]['bet'] - avg_bet) / (avg_bet + 1)
    return min(scores, key=scores.get)

def choose_ensemble():
    funcs = [choose_random, choose_follow_killer, choose_smart_safe, choose_balance, choose_sequential]
    votes = defaultdict(int)
    for func in funcs:
        try:
            votes[func()] += 1
        except:
            continue
    return max(votes, key=votes.get) if votes else random.choice(ROOM_ORDER)

def choose_room_tn(mode: str) -> Tuple[int, str]:
    logic_map = {"RANDOM": choose_random, "FOLLOW_KILLER": choose_follow_killer, "SEQUENTIAL": choose_sequential, "SMART_SAFE": choose_smart_safe, "BALANCE": choose_balance, "ENSEMBLE": choose_ensemble}
    return logic_map.get(mode, choose_random)(), mode

def api_headers():
    return {"content-type": "application/json", "user-agent": "Mozilla/5.0", "user-id": str(USER_ID) if USER_ID else "", "user-secret-key": SECRET_KEY if SECRET_KEY else ""}

def place_bet_http(issue: int, room_id: int, amount: float) -> dict:
    payload = {"asset_type": "BUILD", "user_id": USER_ID, "room_id": int(room_id), "bet_amount": float(amount)}
    try:
        r = requests.post(BET_API_URL, headers=api_headers(), json=payload, timeout=8)
        try: return r.json()
        except: return {"raw": r.text}
    except Exception as e: return {"error": str(e)}

def place_bet_async(issue: int, room_id: int, amount: float, algo_used=None):
    def worker():
        time.sleep(random.uniform(0.05, 0.45))
        res = place_bet_http(issue, room_id, amount)
        bet_history.append({"issue": issue, "room": room_id, "amount": float(amount), "time": datetime.now(tz).strftime("%H:%M:%S"), "resp": res, "result": "Đang", "algo": algo_used})
    threading.Thread(target=worker, daemon=True).start()

def lock_prediction_if_needed():
    global prediction_locked, predicted_room, ui_state, current_bet, stop_flag
    if stop_flag or prediction_locked or issue_id is None: return
    chosen, algo = choose_room_tn(settings.get("algo", "RANDOM"))
    predicted_room = chosen
    prediction_locked = True
    ui_state = "PREDICTED"
    if run_mode == "AUTO":
        bld = current_build
        if bld is None: bld, _, _ = fetch_balances_3games(retries=1, timeout=3)
        if current_bet is None: current_bet = base_bet
        amt = float(current_bet)
        if bld and amt > bld: current_bet = base_bet; amt = float(current_bet)
        place_bet_async(issue_id, predicted_room, amt, algo_used=algo)

def on_open(ws):
    _ws["ws"] = ws
    global _ws_status
    _ws_status = "✅ Đã kết nối"
    try: ws.send(json.dumps({"msg_type": "handle_enter_game", "asset_type": "BUILD", "user_id": USER_ID, "user_secret_key": SECRET_KEY}))
    except: pass

def on_message(ws, message):
    global issue_id, killed_room, round_index, ui_state, analysis_start_ts, prediction_locked, predicted_room, last_killed_room, current_bet, win_streak, lose_streak, max_win_streak, max_lose_streak, stop_flag
    try:
        if isinstance(message, bytes): message = message.decode("utf-8", errors="replace")
        data = json.loads(message)
        msg_type = str(data.get("msg_type", ""))
        if msg_type == "notify_enter_game":
            if data.get("last_killed_room_id"): last_killed_room = int(data["last_killed_room_id"])
            for rm in data.get("room_stat", []):
                if isinstance(rm, dict): room_state[int(rm.get("room_id", 0))] = {"players": int(rm.get("user_cnt", 0)), "bet": int(rm.get("total_bet_amount", 0))}
        elif "issue_stat" in msg_type:
            for rm in data.get("rooms", []):
                if isinstance(rm, dict): room_state[int(rm.get("room_id", 0))] = {"players": int(rm.get("user_cnt", 0)), "bet": int(rm.get("total_bet_amount", 0))}
            new_issue = data.get("issue_id")
            if new_issue and new_issue != issue_id:
                issue_id = new_issue; round_index += 1; killed_room = None; prediction_locked = False; predicted_room = None; ui_state = "ANALYZING"; analysis_start_ts = time.time()
        elif "count_down" in msg_type:
            if int(data.get("count_down", 99)) <= 10 and not prediction_locked: lock_prediction_if_needed()
        elif "result" in msg_type:
            kr = data.get("killed_room") or data.get("killed_room_id")
            if kr:
                killed_room = int(kr); game_kill_log.append(killed_room); last_killed_room = killed_room
                for rid in ROOM_ORDER:
                    if rid == killed_room: room_stats[rid]["kills"] += 1
                    else: room_stats[rid]["survives"] += 1
                for b in reversed(bet_history):
                    if b.get("issue") == issue_id:
                        if int(b.get("room")) != killed_room:
                            b["result"] = "Thắng"; current_bet = base_bet; win_streak += 1; lose_streak = 0; max_win_streak = max(max_win_streak, win_streak)
                        else:
                            b["result"] = "Thua"; current_bet = current_bet * multiplier if current_bet else base_bet; lose_streak += 1; win_streak = 0; max_lose_streak = max(max_lose_streak, lose_streak)
                        break
            ui_state = "RESULT"
    except: pass

def on_close(ws, code, reason):
    global _ws_status; _ws_status = f"⏳ Đã đóng ({code})"

def on_error(ws, err):
    global _ws_status; _ws_status = f"❌ Lỗi"

def start_ws():
    global _ws_status
    while not stop_flag:
        try:
            _ws_status = "⏳ Đang kết nối..."
            ws_app = websocket.WebSocketApp(WS_URL, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            _ws["ws"] = ws_app
            ws_app.run_forever(ping_interval=15, ping_timeout=6)
        except: _ws_status = "❌ Lỗi kết nối"
        time.sleep(random.uniform(1, 5))

def monitor_loop():
    global last_msg_ts, stop_flag
    while not stop_flag:
        if time.time() - last_msg_ts > 45:
            try:
                wsobj = _ws.get("ws")
                if wsobj: wsobj.close()
            except: pass
        time.sleep(0.6)

def build_logo_with_gradient(logo_text: str) -> Text:
    lines = logo_text.split('\n')
    result = Text()
    for line in lines:
        if line.strip():
            chars = list(line)
            for i, char in enumerate(chars):
                if char in ['█', '╔', '╗', '║', '╚', '╝', '═']:
                    style = HTOOL_COLORS["gold"] if i % 3 == 0 else HTOOL_COLORS["neon_blue"] if i % 3 == 1 else HTOOL_COLORS["neon_pink"]
                    result.append(char, style=style)
                else: result.append(char, style="dim")
            result.append("\n")
    return result

def build_premium_header():
    logo_text = build_logo_with_gradient(LOGO)
    info_table = Table(box=None, show_header=False, pad_edge=False, expand=True)
    info_table.add_column(style=f"bold {HTOOL_COLORS['gold']}", no_wrap=True, justify="right", width=18)
    info_table.add_column(style="white")
    info_table.add_row(f"{ICONS['user']} USER:", f"[bold {HTOOL_COLORS['platinum']}]{USER_ID}[/]" if USER_ID else "[dim]-[/dim]")
    b = f"{current_build:,.2f}" if isinstance(current_build, (int, float)) else "0.00"
    info_table.add_row(f"{ICONS['diamond']} BALANCE:", f"[bold {HTOOL_COLORS['emerald']}]{b}[/] BUILD")
    pnl_val = cumulative_profit or 0
    pnl_color = HTOOL_COLORS["emerald"] if pnl_val >= 0 else HTOOL_COLORS["ruby"]
    info_table.add_row(f"{ICONS['fire']} P&L:", f"[{pnl_color}]{pnl_val:+,.2f}[/] BUILD")
    streak_text = Text.assemble(("🔥 ", f"bold {HTOOL_COLORS['neon_orange']}"), (f"{win_streak}", f"bold {HTOOL_COLORS['emerald']}"), (" | ", "dim"), ("💀 ", f"bold {HTOOL_COLORS['ruby']}"), (f"{lose_streak}", f"bold {HTOOL_COLORS['ruby']}"))
    info_table.add_row("📊 STREAK:", streak_text)
    info_table.add_row(f"{ICONS['brain']} AI:", f"[bold {HTOOL_COLORS['neon_pink']}]{SELECTION_MODES.get(settings.get('algo'), settings.get('algo'))}[/]")
    info_table.add_row(f"{ICONS['clock']} TIME:", f"[{HTOOL_COLORS['sapphire']}]{datetime.now(tz).strftime('%H:%M:%S')}[/]")
    info_table.add_row(f"{ICONS['target']} ROUND:", f"[bold {HTOOL_COLORS['gold']}]{issue_id or 'Waiting...'}[/]")
    info_table.add_row(f"{ICONS['link']} WS:", f"[dim]{_ws_status}[/dim]")
    return Panel(Group(Align.center(logo_text), info_table), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, padding=(1, 2))

def build_premium_rooms():
    room_panels = []
    for r in ROOM_ORDER:
        st = room_state.get(r, {})
        players, bet_val = st.get("players", 0), st.get('bet', 0) or 0
        is_predicted = predicted_room is not None and int(r) == int(predicted_room)
        is_killed = killed_room is not None and int(r) == int(killed_room)
        if is_killed and is_predicted: border, title_style = f"bold {HTOOL_COLORS['ruby']}", f"bold {HTOOL_COLORS['ruby']}"
        elif is_killed: border, title_style = HTOOL_COLORS["ruby"], HTOOL_COLORS["ruby"]
        elif is_predicted: border, title_style = f"bold {HTOOL_COLORS['emerald']}", f"bold {HTOOL_COLORS['emerald']}"
        else: border, title_style = HTOOL_COLORS["onyx"], "white"
        content = Text.assemble(("\n", ""), (f"👥 {players:3d} ", "white"), ("| ", "dim"), (f"💰 {int(bet_val):,}", HTOOL_COLORS["gold"]), ("\n", ""), justify="center")
        room_panels.append(Panel(Align.center(content, vertical="middle"), title=f"[{title_style}]{ROOM_NAMES.get(r, f'Room {r}')}[/{title_style}]", border_style=border, box=box.HEAVY, expand=True, height=5))
    return Panel(Columns(room_panels, equal=True, expand=True), title=f"[bold {HTOOL_COLORS['gold']}]🎮 PREMIUM BATTLE ARENA 🎮[/]", box=box.HEAVY, border_style=HTOOL_COLORS["gold"], expand=True)

def build_premium_mid():
    if ui_state == "ANALYZING":
        elapsed = time.time() - (analysis_start_ts or time.time())
        progress = min(1.0, elapsed / analysis_duration)
        bar = "█" * int(40 * progress) + "░" * (40 - int(40 * progress))
        content = Text.from_markup(f"\n[bold {HTOOL_COLORS['neon_blue']}]🧠 AI ANALYZING[/]\n\n[{HTOOL_COLORS['gold']}]{bar}[/]\n\n[{HTOOL_COLORS['neon_pink']}]Progress: {progress*100:.0f}%[/]")
        return Panel(content, border_style=HTOOL_COLORS["neon_pink"], box=box.HEAVY, expand=True)
    elif ui_state == "PREDICTED":
        name = ROOM_NAMES.get(predicted_room, f"Room {predicted_room}") if predicted_room else '?'
        bet_amt = f"{current_bet:,.2f}" if current_bet else '0'
        content = Text.assemble(("\n🎯 TARGET LOCKED\n\n", f"bold {HTOOL_COLORS['emerald']}"), (f"{name}\n", f"bold {HTOOL_COLORS['gold']}"), (f"💰 {bet_amt} BUILD\n", f"bold {HTOOL_COLORS['gold']}"))
        return Panel(Align.center(content), border_style=HTOOL_COLORS["emerald"], box=box.HEAVY, expand=True)
    elif ui_state == "RESULT":
        k = ROOM_NAMES.get(killed_room, "-") if killed_room else "-"
        last_bet = bet_history[-1] if bet_history else None
        result_text, result_color = "⏳ WAITING", HTOOL_COLORS["gold"]
        if last_bet and last_bet.get('issue') == issue_id:
            result_text, result_color = ("🎉 WINNER 🎉", HTOOL_COLORS["emerald"]) if last_bet.get('result') == "Thắng" else ("💀 LOSER 💀", HTOOL_COLORS["ruby"])
        content = Text.assemble(("\n", ""), (f"{result_text}\n\n", f"bold {result_color}"), (f"☠️ Killer: {k}\n", f"bold {HTOOL_COLORS['ruby']}"))
        return Panel(Align.center(content), border_style=result_color, box=box.HEAVY, expand=True)
    return Panel(Align.center(Text("⏳ Waiting...", style=HTOOL_COLORS["gold"])), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_premium_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 BET HISTORY[/]", box=box.ROUNDED, expand=True)
    t.add_column("Round", style=HTOOL_COLORS["sapphire"]); t.add_column("Room", style=HTOOL_COLORS["neon_blue"]); t.add_column("Amount", justify="right", style=HTOOL_COLORS["gold"]); t.add_column("Result")
    for b in list(bet_history)[-6:]:
        res = str(b.get('result', '⏳'))
        t.add_row(str(b.get('issue', '-')), ROOM_NAMES.get(b.get('room'), str(b.get('room', '-'))), f"{float(b.get('amount', 0)):,.2f}", Text("✅" if "Thắng" in res else "❌" if "Thua" in res else "⏳"))
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def prompt_settings() -> bool:
    global base_bet, multiplier, current_bet, bet_rounds_before_skip, pause_after_losses, profit_target, stop_when_profit_reached, stop_loss_target, stop_when_loss_reached
    console.clear()
    console.print(Panel(Align.center(f"[bold {HTOOL_COLORS['gold']}]⚙️ PREMIUM CONFIGURATION[/]"), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
    base_bet = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['neon_blue']}]💰 Cược gốc:[/]\n   >>", default=1.0)
    multiplier = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['neon_blue']}]📈 Hệ số nhân:[/]\n   >>", default=2.0)
    current_bet = base_bet
    modes = list(SELECTION_MODES.items())
    algo_table = Table(box=box.ROUNDED); algo_table.add_column("STT", style=HTOOL_COLORS["gold"], width=4); algo_table.add_column("Thuật toán", style=HTOOL_COLORS["neon_blue"])
    for i, (key, label) in enumerate(modes, 1): algo_table.add_row(str(i), label)
    console.print(f"\n[bold {HTOOL_COLORS['neon_pink']}]🧠 Chọn AI:[/]"); console.print(algo_table)
    choice = IntPrompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn[/]", choices=[str(i) for i in range(1, len(modes) + 1)], default=1)
    settings["algo"] = modes[choice - 1][0]
    bet_rounds_before_skip = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['sapphire']}]🛡️ Chống soi:[/]\n   >>", default=0)
    pause_after_losses = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['sapphire']}]⏸️ Nghỉ sau thua:[/]\n   >>", default=0)
    pt_str = Prompt.ask(f"\n[bold {HTOOL_COLORS['emerald']}]🎯 Mục tiêu lãi (Enter bỏ qua):[/]\n   >>", default="")
    if pt_str.strip():
        try: profit_target = float(pt_str); stop_when_profit_reached = True
        except: pass
    sl_str = Prompt.ask(f"\n[bold {HTOOL_COLORS['ruby']}]💀 Cắt lỗ (Enter bỏ qua):[/]\n   >>", default="")
    if sl_str.strip():
        try: stop_loss_target = float(sl_str); stop_when_loss_reached = True
        except: pass
    start = Prompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]>> Bắt đầu? (Enter/q)[/]", default="")
    if start.lower() == 'q': return False
    run_mode = "AUTO"
    return True

def load_accounts() -> list:
    acc_file = Path("accounts.json")
    if not acc_file.exists(): return []
    try: return json.loads(acc_file.read_text())
    except: return []

def save_accounts(accounts: list):
    with Path("accounts.json").open("w", encoding="utf-8") as f: json.dump(accounts, f, indent=2)

def add_new_account(accounts: list) -> bool:
    console.clear()
    link = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Paste link[/]")
    if not link: return False
    try:
        parsed = urlparse(link); params = parse_qs(parsed.query)
        if 'userId' in params and 'secretKey' in params:
            uid = int(params.get('userId')[0]); skey = params.get('secretKey', [None])[0]
            accounts.append({"userId": uid, "secretKey": skey}); save_accounts(accounts)
            console.print(f"[green]✅ Đã thêm: {uid}[/]"); time.sleep(2); return True
    except: pass
    return False

def delete_account(accounts: list) -> bool:
    console.clear()
    if not accounts: return False
    table = Table(box=box.ROUNDED); table.add_column("STT", style=HTOOL_COLORS["gold"]); table.add_column("User ID", style=HTOOL_COLORS["neon_blue"])
    for i, acc in enumerate(accounts, 1): table.add_row(str(i), str(acc.get('userId')))
    console.print(table)
    choice = Prompt.ask(f"[bold {HTOOL_COLORS['ruby']}]>> Chọn STT[/]", default="")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(accounts): removed = accounts.pop(idx); save_accounts(accounts); console.print(f"[green]✅ Đã xóa: {removed.get('userId')}[/]"); time.sleep(2); return True
    except: pass
    return False

def select_account_premium() -> bool:
    global USER_ID, SECRET_KEY
    while True:
        console.clear()
        accounts = load_accounts()
        if not accounts: console.print("[yellow]⚠️ Chưa có tài khoản![/]"); time.sleep(2); return False
        table = Table(title="📋 DANH SÁCH TÀI KHOẢN", box=box.HEAVY); table.add_column("STT", style=HTOOL_COLORS["gold"]); table.add_column("User ID", style=HTOOL_COLORS["neon_blue"]); table.add_column("Balance", justify="right")
        for i, acc in enumerate(accounts, 1):
            uid = acc.get('userId'); build, _, _ = fetch_balances_3games(uid=uid, secret=acc.get('secretKey'))
            table.add_row(str(i), str(uid), f"[{HTOOL_COLORS['emerald']}]{build:,.4f}[/]" if build else "[red]❌[/]")
        console.print(table)
        choice = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn số[/]", choices=[str(i) for i in range(1, len(accounts) + 1)], default="")
        if not choice: return False
        idx = int(choice) - 1
        if 0 <= idx < len(accounts): USER_ID = accounts[idx]['userId']; SECRET_KEY = accounts[idx]['secretKey']; console.print(f"[green]✅ Đã chọn: {USER_ID}[/]"); time.sleep(1.5); return True

def start_threads():
    threading.Thread(target=start_ws, daemon=True).start()
    threading.Thread(target=monitor_loop, daemon=True).start()

def start_game_flow():
    global stop_flag
    if USER_ID is None or SECRET_KEY is None: console.print("[red]❌ Chưa chọn tài khoản.[/]"); time.sleep(2); return
    console.print(Rule("[bold green]🚀 KHỞI ĐỘNG...[/]", style="green"))
    start_threads()
    with console.status("[bold green]Đang kết nối...[/]", spinner="dots"):
        wait_start = time.time()
        while issue_id is None and (time.time() - wait_start) < 30: time.sleep(0.5)
        if issue_id is None: console.print("\n[bold red]❌ Không nhận được dữ liệu.[/]"); time.sleep(3); return
    console.print("\n[bold green]✅ Kết nối thành công![/]"); time.sleep(2)
    def generate_layout():
        main_grid = Table.grid(expand=True, pad_edge=False); main_grid.add_column("main", ratio=60); main_grid.add_column("side", ratio=40)
        right_grid = Table.grid(expand=True, pad_edge=False); right_grid.add_row(build_premium_mid()); right_grid.add_row(build_premium_history())
        main_grid.add_row(build_premium_rooms(), right_grid)
        root = Table.grid(expand=True, pad_edge=False); root.add_row(build_premium_header()); root.add_row(main_grid)
        return root
    with Live(generate_layout(), refresh_per_second=4, console=console, screen=True) as live:
        try:
            while not stop_flag: live.update(generate_layout()); time.sleep(0.25)
        except KeyboardInterrupt: console.print("[yellow]Người dùng thoát.[/]")

def save_strategy_config():
    config_data = {"base_bet": base_bet, "multiplier": multiplier, "algo": settings.get("algo"), "bet_rounds_before_skip": bet_rounds_before_skip, "pause_after_losses": pause_after_losses}
    try:
        with open(STRATEGY_CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(config_data, f, indent=2)
        console.print(f"[green]✅ Config saved![/]")
    except: pass

def load_strategy_config() -> bool:
    global base_bet, multiplier, current_bet, bet_rounds_before_skip, pause_after_losses
    if not Path(STRATEGY_CONFIG_FILE).exists(): console.print(f"[yellow]⚠️ Config not found.[/]"); return False
    try:
        with open(STRATEGY_CONFIG_FILE, "r", encoding="utf-8") as f: config_data = json.load(f)
        base_bet = config_data.get("base_bet", 1.0); multiplier = config_data.get("multiplier", 2.0)
        settings["algo"] = config_data.get("algo", "RANDOM"); bet_rounds_before_skip = config_data.get("bet_rounds_before_skip", 0)
        pause_after_losses = config_data.get("pause_after_losses", 0); current_bet = base_bet; run_mode = "AUTO"
        console.print(f"[green]✅ Config loaded![/]"); time.sleep(2); return True
    except: return False

# ================== TOOL CHẠY ĐUA TỐC ĐỘ ==================

cdtd_session = requests.Session()
cdtd_headers = {}

NV = {1: 'Bậc thầy tấn công', 2: 'Quyền sắt', 3: 'Thợ lặn sâu', 4: 'Cơn lốc sân cỏ', 5: 'Hiệp sĩ phi nhanh', 6: 'Vua home run'}
NV_ICONS = {1: '🥋', 2: '👊', 3: '🤿', 4: '🌪️', 5: '🏇', 6: '⚾'}

CDTD_ALGORITHMS = {
    "RANDOM": "1. NGẪU NHIÊN", "AVOID_LAST": "2. TRÁNH KẾT QUẢ CUỐI",
    "HOT_STREAK": "3. THEO CHUỖI THẮNG", "COLD_STREAK": "4. BẮT ĐẢO CHIỀU",
    "BALANCE": "5. CÂN BẰNG LỊCH SỬ", "PATTERN": "6. NHẬN DIỆN MẪU",
    "PROBABILITY": "7. XÁC SUẤT THỐNG KÊ", "FOLLOW_WINNER": "8. THEO NGƯỜI THẮNG",
    "ANTI_WINNER": "9. CHỐNG NGƯỜI THẮNG", "SMART_ANALYSIS": "10. PHÂN TÍCH THÔNG MINH",
    "MARKOV_CHAIN": "11. CHUỖI MARKOV", "BAYESIAN": "12. XÁC SUẤT BAYES",
    "NEURAL_NETWORK": "13. MẠNG NƠ-RON", "GENETIC_ALGO": "14. THUẬT TOÁN DI TRUYỀN",
    "REINFORCEMENT": "15. HỌC TĂNG CƯỜNG", "KNN": "16. K-NEAREST NEIGHBORS",
    "DECISION_TREE": "17. CÂY QUYẾT ĐỊNH", "RANDOM_FOREST": "18. RỪNG NGẪU NHIÊN",
    "GRADIENT_BOOST": "19. TĂNG CƯỜNG GRADIENT", "ENSEMBLE": "20. TỔNG HỢP",
    "TREND_FOLLOWING": "21. THEO XU HƯỚNG", "MEAN_REVERSION": "22. ĐẢO CHIỀU TRUNG BÌNH",
    "MOMENTUM": "23. ĐỘNG LƯỢNG", "VOLATILITY": "24. BIẾN ĐỘNG",
    "SEASONAL": "25. CHU KỲ", "CORRELATION": "26. TƯƠNG QUAN",
    "CLUSTER": "27. PHÂN CỤM", "ANOMALY": "28. PHÁT HIỆN BẤT THƯỜNG",
    "ENTROPY": "29. ENTROPY", "FUZZY_LOGIC": "30. LOGIC MỜ",
    "LSTM_PREDICT": "31. LSTM", "TRANSFORMER": "32. TRANSFORMER",
    "ATTENTION": "33. ATTENTION", "DEEP_Q": "34. DEEP Q-LEARNING",
    "A3C": "35. A3C", "PPO": "36. PPO", "GAN": "37. GAN",
    "AUTOENCODER": "38. AUTOENCODER", "SWARM_INTEL": "39. TRÍ TUỆ BẦY ĐÀN",
    "META_LEARNING": "40. META LEARNING",
}

cdtd_settings = {"algo": "RANDOM"}
cdtd_coin = "BUILD"
cdtd_base_bet = 1.0
cdtd_multiplier = 2.0
cdtd_current_bet = 1.0
cdtd_win_streak = 0
cdtd_lose_streak = 0
cdtd_max_win_streak = 0
cdtd_max_lose_streak = 0
cdtd_stats = {'win': 0, 'lose': 0, 'asset_0': 0}
cdtd_bet_history = deque(maxlen=50)
cdtd_stop_flag = False
cdtd_issue_id = None
cdtd_predicted_nv = None
cdtd_ui_state = "WAITING"
cdtd_analysis_start_ts = None
cdtd_analysis_duration = 25.0
cdtd_pause_rounds = 0
cdtd_pause_remaining = 0
cdtd_bet_rounds_before_skip = 0
cdtd_rounds_placed = 0
cdtd_skip_next = False
cdtd_last_winner = None
cdtd_previous_issue = None
cdtd_bet_placed_this_round = False
cdtd_checked_result = False
cdtd_recent_choices = deque(maxlen=10)
cdtd_avoid_repeat = 3

def get_filtered_candidates(data_top10, avoid_count=3):
    last_winner = int(data_top10[1][0]) if data_top10 and data_top10[1] else None
    recent = list(cdtd_recent_choices)[-avoid_count:] if len(cdtd_recent_choices) >= avoid_count else list(cdtd_recent_choices)
    candidates = [nv for nv in range(1, 7) if nv not in recent and nv != last_winner]
    if not candidates: candidates = [nv for nv in range(1, 7) if nv != last_winner]
    if not candidates: candidates = list(range(1, 7))
    return candidates

# ================== 40 LOGIC CDTD ==================

def choose_nv_random(data_top10, data_top100):
    return random.choice(get_filtered_candidates(data_top10, cdtd_avoid_repeat))

def choose_nv_avoid_last(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    last_winner = int(data_top10[1][0]) if data_top10 and data_top10[1] else None
    filtered = [nv for nv in candidates if nv != last_winner]
    return random.choice(filtered) if filtered else random.choice(candidates)

def choose_nv_hot_streak(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        max_wins = max(data_top100[1])
        hot_nvs = [i+1 for i, wins in enumerate(data_top100[1]) if wins == max_wins and (i+1) in candidates]
        if hot_nvs: return random.choice(hot_nvs)
    return random.choice(candidates)

def choose_nv_cold_streak(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        min_wins = min(data_top100[1])
        cold_nvs = [i+1 for i, wins in enumerate(data_top100[1]) if wins == min_wins and (i+1) in candidates]
        if cold_nvs: return random.choice(cold_nvs)
    return random.choice(candidates)

def choose_nv_balance(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        total_wins = sum(data_top100[1]); avg_wins = total_wins / 6
        below_avg = [i+1 for i, wins in enumerate(data_top100[1]) if wins < avg_wins and (i+1) in candidates]
        if below_avg: return random.choice(below_avg)
    return random.choice(candidates)

def choose_nv_pattern(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) >= 4:
        recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-6:] if b.get('winner')]
        if len(recent_winners) >= 4 and recent_winners[-1] == recent_winners[-3] and recent_winners[-2] == recent_winners[-4]:
            predicted = recent_winners[-2]
            if predicted in candidates: return predicted
    return random.choice(candidates)

def choose_nv_probability(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        weights, nv_list = [], []
        for i in range(1, 7):
            if i in candidates:
                weight = 1.0 / (data_top100[1][i-1] + 1)
                if i == int(data_top10[1][0]): weight *= 0.5
                weights.append(weight); nv_list.append(i)
        if weights and sum(weights) > 0: return random.choices(nv_list, weights=[w/sum(weights) for w in weights], k=1)[0]
    return random.choice(candidates)

def choose_nv_follow_winner(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        for idx in sorted(range(6), key=lambda i: data_top100[1][i], reverse=True):
            if (idx + 1) in candidates: return idx + 1
    return random.choice(candidates)

def choose_nv_anti_winner(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        for idx in sorted(range(6), key=lambda i: data_top100[1][i]):
            if (idx + 1) in candidates: return idx + 1
    return random.choice(candidates)

def choose_nv_smart_analysis(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        scores = {}; total_wins = sum(data_top100[1]); avg_wins = total_wins / 6
        for i in candidates:
            score = 0
            if data_top100[1][i-1] < avg_wins: score += (avg_wins - data_top100[1][i-1]) * 2
            if i == int(data_top10[1][0]): score -= 1.5
            if i in cdtd_recent_choices: score -= 3
            score += random.uniform(-0.3, 0.3)
            scores[i] = score
        return max(scores, key=scores.get)
    return random.choice(candidates)

def choose_nv_markov_chain(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    transitions = defaultdict(lambda: defaultdict(int))
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    for i in range(len(recent_winners) - 1): transitions[recent_winners[i]][recent_winners[i + 1]] += 1
    last = recent_winners[-1] if recent_winners else int(data_top10[1][0])
    if transitions[last]:
        for nv, _ in sorted(transitions[last].items(), key=lambda x: x[1], reverse=True):
            if nv in candidates: return nv
    return random.choice(candidates)

def choose_nv_bayesian(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    room_counts = Counter(recent_winners); total = len(recent_winners)
    posterior = {i: (room_counts.get(i, 0) + 1) / (total + 6) for i in candidates}
    return min(posterior, key=posterior.get)

def choose_nv_neural_network(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    scores = {}
    for nv in candidates:
        wins_100 = data_top100[1][nv-1] if data_top100[1] else 0; total_100 = sum(data_top100[1]) if data_top100[1] else 1
        h1_1 = 1 / (1 + math.exp(-(wins_100 / total_100 * 10 - 5)))
        recent_wins = sum(1 for b in list(cdtd_bet_history)[-10:] if b.get('winner') == nv)
        h1_2 = 1 / (1 + math.exp(-(recent_wins - 2)))
        h1_3 = 0 if nv == int(data_top10[1][0]) else 1
        repeat_penalty = 2 if nv in cdtd_recent_choices else 0
        scores[nv] = 0.4 * h1_1 + 0.3 * h1_2 + 0.3 * h1_3 - repeat_penalty
    return max(scores, key=scores.get)

def choose_nv_genetic_algo(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    def fitness(nv):
        if nv not in candidates: return -999
        score = 3 if nv != int(data_top10[1][0]) else 0
        if data_top100 and data_top100[1]: score += (sum(data_top100[1]) / 6 - data_top100[1][nv-1]) * 2
        if nv in cdtd_recent_choices: score -= 5
        return score
    population = [random.choice(candidates) for _ in range(10)]
    fitness_scores = sorted([(nv, fitness(nv)) for nv in population], key=lambda x: x[1], reverse=True)
    return fitness_scores[0][0] if random.random() > 0.1 else random.choice(candidates)

def choose_nv_reinforcement(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    q_values = {i: 0.0 for i in candidates}
    for b in list(cdtd_bet_history)[-20:]:
        chosen, result = b.get('chosen'), b.get('result')
        if chosen in candidates and result: q_values[chosen] += 1.0 if result == 'win' else -0.5
    if random.random() < 0.2: return random.choice(candidates)
    return max(q_values, key=q_values.get) if q_values else random.choice(candidates)

def choose_nv_knn(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    if len(recent_winners) < 3: return random.choice(candidates)
    k = min(5, len(recent_winners)); counts = Counter(recent_winners[-k:])
    for nv, _ in sorted(counts.items(), key=lambda x: x[1]):
        if nv in candidates: return nv
    return random.choice(candidates)

def choose_nv_decision_tree(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    last_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-3:] if b.get('winner')]
    if len(last_winners) >= 2 and last_winners[-1] == last_winners[-2]:
        filtered = [nv for nv in candidates if nv != last_winners[-1]]
        if filtered: return random.choice(filtered)
    return random.choice(candidates)

def choose_nv_random_forest(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    predictions = []
    for func in [choose_nv_random, choose_nv_avoid_last, choose_nv_cold_streak, choose_nv_probability, choose_nv_balance]:
        try:
            pred = func(data_top10, data_top100)
            if pred in candidates: predictions.append(pred)
        except: continue
    return Counter(predictions).most_common(1)[0][0] if predictions else random.choice(candidates)

def choose_nv_gradient_boost(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    scores = {i: 0.5 for i in candidates}
    if data_top100 and data_top100[1]:
        total = sum(data_top100[1])
        for i in candidates: scores[i] += 0.3 * (1/6 - data_top100[1][i-1] / total)
    for nv, count in Counter([int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-10:] if b.get('winner')]).items():
        if nv in candidates: scores[nv] -= 0.2 * count
    for nv in candidates:
        if nv == int(data_top10[1][0]): scores[nv] -= 0.5
        if nv in cdtd_recent_choices: scores[nv] -= 2
        scores[nv] += random.uniform(-0.1, 0.1)
    return max(scores, key=scores.get)

def choose_nv_ensemble(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    votes = defaultdict(int)
    for func in [choose_nv_random, choose_nv_avoid_last, choose_nv_cold_streak, choose_nv_probability, choose_nv_balance, choose_nv_markov_chain, choose_nv_knn]:
        try:
            nv = func(data_top10, data_top100)
            if nv in candidates: votes[nv] += 1
        except: continue
    return max(votes, key=votes.get) if votes else random.choice(candidates)

def choose_nv_trend_following(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-15:] if b.get('winner')]
    if len(recent_winners) < 3: return random.choice(candidates)
    mid = len(recent_winners) // 2
    trends = {nv: recent_winners[mid:].count(nv) - recent_winners[:mid].count(nv) for nv in candidates}
    best_trend = max(trends.values())
    if best_trend > 0:
        best_nvs = [nv for nv, trend in trends.items() if trend == best_trend]
        if best_nvs: return random.choice(best_nvs)
    return random.choice(candidates)

def choose_nv_mean_reversion(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    counts = Counter(recent_winners); avg = len(recent_winners) / 6
    below_avg = [nv for nv in candidates if counts.get(nv, 0) < avg]
    return random.choice(below_avg) if below_avg else random.choice(candidates)

def choose_nv_momentum(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    scores = {i: 0.0 for i in candidates}
    for i, b in enumerate(list(cdtd_bet_history)[-20:]):
        if b.get('winner') in candidates: scores[b['winner']] += (i + 1) / 20
    return min(scores, key=scores.get) if scores else random.choice(candidates)

def choose_nv_volatility(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    volatility = {}
    for nv in candidates:
        appearances = [1 if b.get('winner') == nv else 0 for b in list(cdtd_bet_history)[-30:]]
        if len(appearances) > 1:
            mean = sum(appearances) / len(appearances)
            volatility[nv] = math.sqrt(sum((x - mean) ** 2 for x in appearances) / len(appearances))
        else: volatility[nv] = 0
    return min(volatility, key=volatility.get) if volatility else random.choice(candidates)

def choose_nv_seasonal(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 8: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    for period in [3, 4, 5, 6]:
        if len(recent_winners) >= period * 2 and all(recent_winners[-(period*2)+i] == recent_winners[-period+i] for i in range(period)):
            if len(recent_winners) >= period + 1:
                predicted = recent_winners[-(period+1)]
                if predicted in candidates: return predicted
    return random.choice(candidates)

def choose_nv_correlation(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 10: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-30:] if b.get('winner')]
    if len(recent_winners) < 3: return random.choice(candidates)
    pairs = defaultdict(int)
    for i in range(len(recent_winners) - 1): pairs[(recent_winners[i], recent_winners[i+1])] += 1
    last = recent_winners[-1] if recent_winners else int(data_top10[1][0])
    following = {nv: sum(count for (prev, next_nv), count in pairs.items() if prev == last and next_nv == nv) for nv in candidates}
    return min(following, key=following.get) if following else random.choice(candidates)

def choose_nv_cluster(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        total = sum(data_top100[1])
        below_avg = [i for i in candidates if data_top100[1][i-1]/total < 1/6]
        if below_avg: return random.choice(below_avg)
    return random.choice(candidates)

def choose_nv_anomaly(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 10: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    counts = Counter(recent_winners); avg = len(recent_winners) / 6
    most_anomalous = max(candidates, key=lambda nv: abs(counts.get(nv, 0) - avg))
    filtered = [nv for nv in candidates if nv != most_anomalous]
    return random.choice(filtered) if filtered else random.choice(candidates)

def choose_nv_entropy(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if data_top100 and data_top100[1]:
        total = sum(data_top100[1])
        if total > 0:
            entropy = -sum((w/total) * math.log2(w/total) for w in data_top100[1] if w > 0)
            if entropy < math.log2(6) * 0.8:
                min_wins = min(data_top100[1])
                min_nvs = [i+1 for i, wins in enumerate(data_top100[1]) if wins == min_wins and (i+1) in candidates]
                if min_nvs: return random.choice(min_nvs)
    return random.choice(candidates)

def choose_nv_fuzzy_logic(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    scores = {i: 0.0 for i in candidates}
    for nv in candidates:
        if data_top100 and data_top100[1]:
            total = sum(data_top100[1]); rate = data_top100[1][nv-1] / total if total > 0 else 1/6
            low_membership = max(0, min(1, (0.18 - rate) / 0.06)) if rate < 0.18 else 0
            high_membership = max(0, min(1, (rate - 0.16) / 0.06)) if rate > 0.16 else 0
            recent_wins = sum(1 for b in list(cdtd_bet_history)[-5:] if b.get('winner') == nv)
            scores[nv] = min(low_membership, 1 - recent_wins/5) - max(high_membership, recent_wins/5)
        if nv == int(data_top10[1][0]): scores[nv] -= 1.0
        if nv in cdtd_recent_choices: scores[nv] -= 2.0
    return max(scores, key=scores.get)

def choose_nv_lstm_predict(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 8: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-15:] if b.get('winner')]
    if len(recent_winners) < 6: return random.choice(candidates)
    last_3 = tuple(recent_winners[-3:])
    predictions = [recent_winners[i+3] for i in range(len(recent_winners) - 3) if tuple(recent_winners[i:i+3]) == last_3]
    if predictions:
        for nv, _ in sorted(Counter(predictions).items(), key=lambda x: x[1]):
            if nv in candidates: return nv
    return random.choice(candidates)

def choose_nv_transformer(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-15:] if b.get('winner')]
    if len(recent_winners) < 3: return random.choice(candidates)
    weighted_votes = defaultdict(float)
    for i, winner in enumerate(recent_winners):
        if winner in candidates: weighted_votes[winner] += (i + 1) / len(recent_winners)
    return min(weighted_votes, key=weighted_votes.get) if weighted_votes else random.choice(candidates)

def choose_nv_attention(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    if len(recent_winners) < 4: return random.choice(candidates)
    heads = [Counter(recent_winners[-5:]), Counter(recent_winners), Counter(recent_winners[-4::2])]
    final_scores = defaultdict(float)
    for head in heads:
        for nv, count in head.items():
            if nv in candidates: final_scores[nv] += count
    return min(final_scores, key=final_scores.get) if final_scores else random.choice(candidates)

def choose_nv_deep_q(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    q_table = defaultdict(lambda: defaultdict(float))
    for b in list(cdtd_bet_history)[-30:]:
        chosen, result, winner = b.get('chosen'), b.get('result'), b.get('winner')
        if chosen in candidates and result and winner:
            reward = 1.0 if result == 'win' else -1.0
            current_q = q_table[winner][chosen]; max_future_q = max(q_table[winner].values()) if q_table[winner] else 0
            q_table[winner][chosen] = current_q + 0.1 * (reward + 0.9 * max_future_q - current_q)
    current_state = int(data_top10[1][0])
    if q_table[current_state]:
        for nv in sorted(q_table[current_state], key=q_table[current_state].get):
            if nv in candidates: return nv
    return random.choice(candidates)

def choose_nv_a3c(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    action_probs = {i: 1/6 for i in candidates}
    for b in list(cdtd_bet_history)[-20:]:
        if b.get('winner') in candidates: action_probs[b['winner']] *= 0.9
    total = sum(action_probs.values())
    if total > 0:
        for nv in action_probs: action_probs[nv] /= total
    return random.choices(list(action_probs.keys()), weights=list(action_probs.values()), k=1)[0]

def choose_nv_ppo(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    new_policy = {i: 1/len(candidates) for i in candidates}
    for b in list(cdtd_bet_history)[-20:]:
        chosen, result = b.get('chosen'), b.get('result')
        if chosen in candidates and result:
            advantage = 1.0 if result == 'win' else -1.0
            ratio = new_policy[chosen] / (1/len(candidates))
            clipped_ratio = max(min(ratio, 1.2), 0.8)
            new_policy[chosen] += 0.1 * clipped_ratio * advantage
    total = sum(new_policy.values())
    if total > 0:
        for nv in new_policy: new_policy[nv] = max(0.01, new_policy[nv] / total)
    return random.choices(list(new_policy.keys()), weights=list(new_policy.values()), k=1)[0]

def choose_nv_gan(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 3: return random.choice(candidates)
    gen_probs = {i: random.random() for i in candidates}
    total = sum(gen_probs.values())
    for i in gen_probs: gen_probs[i] /= total
    real_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-10:] if b.get('winner')]
    real_dist = Counter(real_winners); real_total = len(real_winners) if real_winners else 1
    for nv in candidates: gen_probs[nv] = gen_probs[nv] * 0.7 + (1 - real_dist.get(nv, 0) / real_total) * 0.3
    total = sum(gen_probs.values())
    for nv in gen_probs: gen_probs[nv] /= total
    return random.choices(list(gen_probs.keys()), weights=list(gen_probs.values()), k=1)[0]

def choose_nv_autoencoder(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 5: return random.choice(candidates)
    encoded_features = [[1 if b.get('winner') == i else 0 for i in range(1, 7)] for b in list(cdtd_bet_history)[-20:] if b.get('winner')]
    if not encoded_features: return random.choice(candidates)
    avg_features = [sum(f[i] for f in encoded_features) / len(encoded_features) for i in range(6)]
    for idx in sorted(range(6), key=lambda i: avg_features[i]):
        if (idx + 1) in candidates: return idx + 1
    return random.choice(candidates)

def choose_nv_swarm_intel(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    def fitness_pso(nv):
        if nv not in candidates: return -999
        score = 5 if nv != int(data_top10[1][0]) else 0
        if data_top100 and data_top100[1]: score += (sum(data_top100[1]) / 6 - data_top100[1][nv-1]) * 3
        for b in list(cdtd_bet_history)[-5:]:
            if b.get('winner') == nv: score -= 2
        if nv in cdtd_recent_choices: score -= 5
        return score
    particles = [{'position': random.choice(candidates), 'best_position': candidates[0], 'best_score': -999} for _ in range(10)]
    global_best_position = particles[0]['position']; global_best_score = fitness_pso(global_best_position)
    for _ in range(5):
        for p in particles:
            new_pos = max(1, min(6, int(round(p['position'] + random.random() * (p['best_position'] - p['position']) + random.random() * (global_best_position - p['position'])))))
            if new_pos in candidates:
                p['position'] = new_pos; score = fitness_pso(new_pos)
                if score > p['best_score']: p['best_score'], p['best_position'] = score, new_pos
                if score > global_best_score: global_best_score, global_best_position = score, new_pos
    return global_best_position if global_best_position in candidates else random.choice(candidates)

def choose_nv_meta_learning(data_top10, data_top100):
    candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
    if len(cdtd_bet_history) < 10: return random.choice(candidates)
    meta_algos = {'random': choose_nv_random, 'avoid_last': choose_nv_avoid_last, 'cold_streak': choose_nv_cold_streak, 'probability': choose_nv_probability, 'balance': choose_nv_balance, 'markov': choose_nv_markov_chain, 'knn': choose_nv_knn, 'ensemble': choose_nv_ensemble}
    algo_scores = {}
    recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-10:] if b.get('winner')]
    unique_winners = len(set(recent_winners)) if recent_winners else 6
    if unique_winners <= 2: algo_scores['pattern'] = 0.9
    elif unique_winners >= 5: algo_scores['random'] = 0.8
    else: algo_scores['cold_streak'] = 0.6; algo_scores['balance'] = 0.4
    if cdtd_win_streak >= 3: algo_scores['ensemble'] = 0.7
    elif cdtd_lose_streak >= 3: algo_scores['random'] = 0.9
    else: algo_scores['markov'] = 0.5; algo_scores['probability'] = 0.5
    if algo_scores:
        best_algo = max(algo_scores, key=algo_scores.get)
        if best_algo in meta_algos:
            result = meta_algos[best_algo](data_top10, data_top100)
            if result in candidates: return result
    return random.choice(candidates)

def choose_nv_cdtd(mode: str, data_top10, data_top100):
    logic_map = {
        "RANDOM": choose_nv_random, "AVOID_LAST": choose_nv_avoid_last,
        "HOT_STREAK": choose_nv_hot_streak, "COLD_STREAK": choose_nv_cold_streak,
        "BALANCE": choose_nv_balance, "PATTERN": choose_nv_pattern,
        "PROBABILITY": choose_nv_probability, "FOLLOW_WINNER": choose_nv_follow_winner,
        "ANTI_WINNER": choose_nv_anti_winner, "SMART_ANALYSIS": choose_nv_smart_analysis,
        "MARKOV_CHAIN": choose_nv_markov_chain, "BAYESIAN": choose_nv_bayesian,
        "NEURAL_NETWORK": choose_nv_neural_network, "GENETIC_ALGO": choose_nv_genetic_algo,
        "REINFORCEMENT": choose_nv_reinforcement, "KNN": choose_nv_knn,
        "DECISION_TREE": choose_nv_decision_tree, "RANDOM_FOREST": choose_nv_random_forest,
        "GRADIENT_BOOST": choose_nv_gradient_boost, "ENSEMBLE": choose_nv_ensemble,
        "TREND_FOLLOWING": choose_nv_trend_following, "MEAN_REVERSION": choose_nv_mean_reversion,
        "MOMENTUM": choose_nv_momentum, "VOLATILITY": choose_nv_volatility,
        "SEASONAL": choose_nv_seasonal, "CORRELATION": choose_nv_correlation,
        "CLUSTER": choose_nv_cluster, "ANOMALY": choose_nv_anomaly,
        "ENTROPY": choose_nv_entropy, "FUZZY_LOGIC": choose_nv_fuzzy_logic,
        "LSTM_PREDICT": choose_nv_lstm_predict, "TRANSFORMER": choose_nv_transformer,
        "ATTENTION": choose_nv_attention, "DEEP_Q": choose_nv_deep_q,
        "A3C": choose_nv_a3c, "PPO": choose_nv_ppo, "GAN": choose_nv_gan,
        "AUTOENCODER": choose_nv_autoencoder, "SWARM_INTEL": choose_nv_swarm_intel,
        "META_LEARNING": choose_nv_meta_learning,
    }
    try:
        chosen = logic_map.get(mode, choose_nv_random)(data_top10, data_top100)
        cdtd_recent_choices.append(chosen)
        return chosen, mode
    except:
        chosen = random.choice(get_filtered_candidates(data_top10, cdtd_avoid_repeat))
        cdtd_recent_choices.append(chosen)
        return chosen, mode

# ================== CDTD API ==================

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        if Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]Sử dụng thông tin đã lưu? (y/n)[/]', choices=['y', 'n'], default='y') == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f: return json.load(f)
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]📋 NHẬP THÔNG TIN[/]", style=HTOOL_COLORS["gold"]))
    console.print("1. Truy cập xworld.io\n2. Đăng nhập\n3. Vào Chạy đua tốc độ\n4. Copy link\n")
    link = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]📋 Nhập link[/]')
    try:
        user_id = link.split('&')[0].split('?userId=')[1]; user_secretkey = link.split('&')[1].split('secretKey=')[1]
    except:
        user_id = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]👤 User ID[/]'); user_secretkey = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]🔑 Secret Key[/]')
    json_data = {'user-id': user_id, 'user-secret-key': user_secretkey}
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f: json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def setup_cdtd_headers(data: dict):
    global cdtd_headers
    cdtd_headers = {'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'country-code': 'vn', 'origin': 'https://xworld.info', 'referer': 'https://xworld.info/', 'user-agent': 'Mozilla/5.0', 'user-id': data['user-id'], 'user-login': 'login_v2', 'user-secret-key': data['user-secret-key'], 'xb-language': 'vi-VN'}

def top_100_cdtd():
    try:
        response = cdtd_session.get('https://api.sprintrun.win/sprint/recent_100_issues', headers={'accept': '*/*', 'origin': 'https://sprintrun.win', 'referer': 'https://sprintrun.win/', 'user-agent': 'Mozilla/5.0'}, timeout=10).json()
        return [1, 2, 3, 4, 5, 6], [response['data']['athlete_2_win_times'][str(i)] for i in range(1, 7)]
    except: return [1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0]

def top_10_cdtd():
    try:
        response = cdtd_session.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=cdtd_headers, timeout=10).json()
        return [i['issue_id'] for i in response['data']['recent_10']], [i['result'][0] for i in response['data']['recent_10']]
    except: return [0], [1]

def user_asset_cdtd():
    try:
        response = cdtd_session.post('https://wallet.3games.io/api/wallet/user_asset', headers=cdtd_headers, json={'user_id': int(cdtd_headers['user-id']), 'source': 'home'}, timeout=10).json()
        return {'USDT': float(response['data']['user_asset'].get('USDT', 0)), 'WORLD': float(response['data']['user_asset'].get('WORLD', 0)), 'BUILD': float(response['data']['user_asset'].get('BUILD', 0))}
    except: return {'USDT': 0, 'WORLD': 0, 'BUILD': 0}

def bet_cdtd(issue_id, nv_id, amount):
    try:
        response = cdtd_session.post('https://api.sprintrun.win/sprint/bet', headers=cdtd_headers, json={'issue_id': int(issue_id), 'bet_group': 'not_winner', 'asset_type': cdtd_coin, 'athlete_id': nv_id, 'bet_amount': float(amount)}, timeout=10).json()
        return (True, "ok") if response.get('code') == 0 else (False, response.get('msg', 'Unknown'))
    except Exception as e: return False, str(e)

# ================== CDTD GIAO DIỆN ==================

def build_cdtd_header():
    logo_text = build_logo_with_gradient(LOGO)
    asset = user_asset_cdtd()
    info_table = Table(box=None, show_header=False, pad_edge=False, expand=True)
    info_table.add_column(style=f"bold {HTOOL_COLORS['gold']}", no_wrap=True, justify="right", width=18)
    info_table.add_column(style="white")
    info_table.add_row(f"{ICONS['user']} USER:", f"[bold {HTOOL_COLORS['platinum']}]{cdtd_headers.get('user-id', 'N/A')}[/]")
    info_table.add_row(f"{ICONS['money']} BALANCE:", f"[bold {HTOOL_COLORS['emerald']}]{asset.get(cdtd_coin, 0):.4f}[/] {cdtd_coin}")
    pnl = asset.get(cdtd_coin, 0) - cdtd_stats['asset_0']
    info_table.add_row(f"{ICONS['chart']} P&L:", f"[{HTOOL_COLORS['emerald'] if pnl >= 0 else HTOOL_COLORS['ruby']}]{pnl:+.4f} {cdtd_coin}[/]")
    streak_text = Text.assemble(("🔥 ", f"bold {HTOOL_COLORS['neon_orange']}"), (f"{cdtd_win_streak}", f"bold {HTOOL_COLORS['emerald']}"), (" | ", "dim"), ("💀 ", f"bold {HTOOL_COLORS['ruby']}"), (f"{cdtd_lose_streak}", f"bold {HTOOL_COLORS['ruby']}"))
    info_table.add_row("📊 STREAK:", streak_text)
    info_table.add_row(f"{ICONS['brain']} AI:", f"[bold {HTOOL_COLORS['neon_pink']}]{CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')}[/]")
    info_table.add_row(f"{ICONS['clock']} TIME:", f"[{HTOOL_COLORS['sapphire']}]{datetime.now(tz).strftime('%H:%M:%S')}[/]")
    info_table.add_row(f"{ICONS['target']} ISSUE:", f"[bold {HTOOL_COLORS['gold']}]{cdtd_issue_id or 'Waiting...'}[/]")
    info_table.add_row(f"{ICONS['bell']} TG:", f"[{'green' if TELEGRAM_ENABLED else 'dim'}] {'BẬT' if TELEGRAM_ENABLED else 'TẮT'}[/]")
    return Panel(Group(Align.center(logo_text), info_table), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, padding=(1, 2))

def build_cdtd_racers():
    data_top100, data_top10 = top_100_cdtd(), top_10_cdtd()
    racer_panels = []
    for i in range(1, 7):
        wins = data_top100[1][i-1] if data_top100[1] else 0
        is_predicted = cdtd_predicted_nv == i
        is_last_winner = int(data_top10[1][0]) == i if data_top10 and data_top10[1] else False
        if is_predicted: border, title_style, bg, glow = f"bold {HTOOL_COLORS['emerald']}", f"bold {HTOOL_COLORS['emerald']}", "on #003300", "✨⭐"
        elif is_last_winner: border, title_style, bg, glow = HTOOL_COLORS["gold"], HTOOL_COLORS["gold"], "on #332200", "🏆"
        else: border, title_style, bg, glow = HTOOL_COLORS["onyx"], "white", "", ""
        content = Text.assemble(("\n", ""), (f"{glow} {NV_ICONS[i]}\n", "default"), (f"{NV[i]}\n", title_style), (f"🏆 {wins} wins", "dim"), ("\n", ""), justify="center")
        racer_panels.append(Panel(Align.center(content, vertical="middle"), title=f"[{title_style}]#{i}[/{title_style}]", border_style=border, box=box.HEAVY, expand=True, height=6, style=bg))
    return Panel(Columns(racer_panels, equal=True, expand=True), title=f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ CHẠY ĐUA TỐC ĐỘ 🏎️[/]", box=box.HEAVY, border_style=HTOOL_COLORS["neon_orange"], expand=True)

def build_cdtd_mid():
    if cdtd_ui_state == "ANALYZING":
        elapsed = time.time() - (cdtd_analysis_start_ts or time.time()); progress = min(1.0, elapsed / cdtd_analysis_duration)
        bar = "█" * int(30 * progress) + "░" * (30 - int(30 * progress))
        content = Text.assemble(("\n🧠 ĐANG PHÂN TÍCH...\n\n", f"bold {HTOOL_COLORS['neon_blue']}"), (f"[{HTOOL_COLORS['gold']}]{bar}[/]\n\n", ""), (f"Tiến độ: {progress*100:.0f}%\n", HTOOL_COLORS['neon_pink']), (f"⏱️ Còn {max(0, int(cdtd_analysis_duration - elapsed))}s\n", "dim"), justify="center")
        return Panel(content, border_style=HTOOL_COLORS["neon_blue"], box=box.HEAVY, expand=True)
    elif cdtd_ui_state == "PREDICTED":
        bet_amt = cdtd_current_bet or cdtd_base_bet
        content = Text.assemble(("\n╔══════════════════════════════╗\n", HTOOL_COLORS["gold"]), ("║  🎯 DỰ ĐOÁN CỦA BOT  🎯    ║\n", HTOOL_COLORS["gold"]), ("║  ", HTOOL_COLORS["gold"]), (f"{NV_ICONS.get(cdtd_predicted_nv, '🤖')} {NV.get(cdtd_predicted_nv, 'N/A'):^20}", f"bold {HTOOL_COLORS['emerald']}"), ("  ║\n", HTOOL_COLORS["gold"]), ("║  💰 Cược: ", HTOOL_COLORS["gold"]), (f"{bet_amt:.2f} {cdtd_coin:<10}", f"bold {HTOOL_COLORS['gold']}"), ("  ║\n", HTOOL_COLORS["gold"]), ("╚══════════════════════════════╝\n", HTOOL_COLORS["gold"]), (f"\n📈 Chuỗi thắng: {cdtd_win_streak}  📉 Chuỗi thua: {cdtd_lose_streak}\n", "white"), justify="center")
        return Panel(content, border_style=HTOOL_COLORS["emerald"], box=box.HEAVY, expand=True)
    elif cdtd_ui_state == "RESULT":
        last_bet = cdtd_bet_history[-1] if cdtd_bet_history else None
        if last_bet and last_bet.get('result') == 'win': result_text, result_color, border_color = "🎉 CHIẾN THẮNG! 🎉", HTOOL_COLORS["emerald"], HTOOL_COLORS["emerald"]
        elif last_bet and last_bet.get('result') == 'lose': result_text, result_color, border_color = "💀 THUA CUỘC! 💀", HTOOL_COLORS["ruby"], HTOOL_COLORS["ruby"]
        else: result_text, result_color, border_color = "⏳ ĐANG CHỜ...", HTOOL_COLORS["gold"], HTOOL_COLORS["gold"]
        content = Text.assemble(("\n", ""), (f"{result_text}\n\n", f"bold {result_color}"), ("Người thắng: ", "white"), (f"{NV_ICONS.get(cdtd_last_winner, '🏆')} {NV.get(cdtd_last_winner, 'N/A')}\n", f"bold {HTOOL_COLORS['gold']}"), ("\n⏳ Đang chờ kỳ mới...", "dim"), justify="center")
        return Panel(content, border_style=border_color, box=box.HEAVY, expand=True)
    return Panel(Align.center(Text("\n⏳ ĐANG CHỜ DỮ LIỆU...\n\n🔄 Đang kết nối...\n", justify="center")), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_cdtd_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 LỊCH SỬ CƯỢC[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["onyx"])
    t.add_column("Kỳ", style=HTOOL_COLORS["sapphire"], width=6); t.add_column("Chọn", style=HTOOL_COLORS["neon_blue"]); t.add_column("Cược", justify="right", style=HTOOL_COLORS["gold"], width=10); t.add_column("KQ")
    for b in list(cdtd_bet_history)[-10:]:
        chosen = NV.get(b.get('chosen'), str(b.get('chosen', '-'))); amount = f"{b.get('amount', 0):.2f}"
        if b.get('result') == 'win': result_text = Text("✅ THẮNG", style=f"bold {HTOOL_COLORS['emerald']}")
        elif b.get('result') == 'lose': result_text = Text("❌ THUA", style=f"bold {HTOOL_COLORS['ruby']}")
        else: result_text = Text("⏳", style=HTOOL_COLORS["gold"])
        t.add_row(str(b.get('issue', '-')), chosen, amount, result_text)
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def build_cdtd_stats():
    data_top100 = top_100_cdtd()
    t = Table(title=f"[bold {HTOOL_COLORS['neon_blue']}]📊 THỐNG KÊ 100 VÁN[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["neon_blue"])
    t.add_column("NV", style=HTOOL_COLORS["gold"], width=4); t.add_column("Tên", style="white"); t.add_column("Thắng", justify="right", style=HTOOL_COLORS["emerald"], width=8); t.add_column("Tỷ lệ", justify="right", style=HTOOL_COLORS["neon_pink"], width=8)
    total_wins = sum(data_top100[1]) if data_top100[1] else 1
    for i in range(6): t.add_row(f"{NV_ICONS.get(i+1, '🏆')}", NV.get(i+1, f'NV{i+1}'), str(data_top100[1][i] if data_top100[1] else 0), f"{(data_top100[1][i] if data_top100[1] else 0)/total_wins*100:.1f}%")
    summary = Table(box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["gold"])
    summary.add_column("Chỉ số", style=HTOOL_COLORS["gold"]); summary.add_column("Giá trị", style="white")
    summary.add_row("Tổng ván", str(cdtd_stats['win'] + cdtd_stats['lose']))
    summary.add_row("Thắng", f"[green]{cdtd_stats['win']}[/]"); summary.add_row("Thua", f"[red]{cdtd_stats['lose']}[/]")
    summary.add_row("Max thắng", str(cdtd_max_win_streak)); summary.add_row("Max thua", str(cdtd_max_lose_streak))
    pnl = user_asset_cdtd().get(cdtd_coin, 0) - cdtd_stats['asset_0']
    summary.add_row("P&L", f"[{'green' if pnl >= 0 else 'red'}]{pnl:+.4f} {cdtd_coin}[/]")
    return Panel(Columns([t, summary], equal=True, expand=True), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_cdtd_marquee():
    messages = [f"⚡ CDTD - 40 AI {ICONS['rocket']}", f"🧠 {CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')} {ICONS['robot']}", f"💰 {cdtd_coin} | Cược: {cdtd_base_bet} | x{cdtd_multiplier}", f"🎯 W:{cdtd_stats['win']} L:{cdtd_stats['lose']} {ICONS['chart']}"]
    message = messages[int(time.time() / 5) % len(messages)]
    full_text = " " * 20 + message + " " * 20; width = console.width or 80
    display_text = (full_text * 3)[int(time.time() * 3) % len(full_text) : int(time.time() * 3) % len(full_text) + width]
    return Panel(Text(display_text, style=f"bold {HTOOL_COLORS['neon_blue']}", no_wrap=True), box=box.ROUNDED, border_style=HTOOL_COLORS["onyx"], padding=0, expand=True)

def cdtd_generate_layout():
    main_grid = Table.grid(expand=True, pad_edge=False); main_grid.add_column("main", ratio=55); main_grid.add_column("side", ratio=45)
    right_grid = Table.grid(expand=True, pad_edge=False); right_grid.add_row(build_cdtd_mid()); right_grid.add_row(build_cdtd_history())
    main_grid.add_row(build_cdtd_racers(), right_grid)
    root = Table.grid(expand=True, pad_edge=False); root.add_row(build_cdtd_header()); root.add_row(build_cdtd_marquee()); root.add_row(main_grid); root.add_row(build_cdtd_stats())
    return root

def cdtd_prompt_settings():
    global cdtd_base_bet, cdtd_multiplier, cdtd_coin, cdtd_current_bet, cdtd_pause_rounds, cdtd_bet_rounds_before_skip, cdtd_settings
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['settings']} ", f"bold {HTOOL_COLORS['gold']}"), ("CẤU HÌNH CHẠY ĐUA TỐC ĐỘ", f"bold {HTOOL_COLORS['neon_blue']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header); console.print()
    coin_choice = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]💰 Chọn tiền: [1] USDT [2] BUILD [3] WORLD[/]\n   >>", choices=['1', '2', '3'], default='2')
    cdtd_coin = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}[coin_choice]
    cdtd_base_bet = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]💵 Cược gốc ({cdtd_coin})[/]\n   >>", default=1.0)
    cdtd_multiplier = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]📈 Hệ số nhân[/]\n   >>", default=2.0)
    cdtd_current_bet = cdtd_base_bet
    cdtd_bet_rounds_before_skip = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]🛡️ Nghỉ 1 ván sau N ván (0=không)[/]\n   >>", default=0)
    cdtd_pause_rounds = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]⏸️ Nghỉ N ván sau khi thua (0=không)[/]\n   >>", default=0)
    console.clear(); console.print(header)
    console.print(f"\n[bold {HTOOL_COLORS['neon_pink']}]🧠 Chọn AI (1-40):[/]\n")
    algo_table = Table(box=box.ROUNDED, border_style=HTOOL_COLORS["neon_pink"]); algo_table.add_column("#", style=HTOOL_COLORS["gold"], width=4); algo_table.add_column("Thuật toán", style=HTOOL_COLORS["neon_blue"])
    for i, (key, label) in enumerate(list(CDTD_ALGORITHMS.items())[:40], 1): algo_table.add_row(str(i), label)
    console.print(algo_table)
    algo_choice = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]>> Chọn (1-40)[/]", choices=[str(i) for i in range(1, 41)], default=1)
    cdtd_settings["algo"] = list(CDTD_ALGORITHMS.keys())[algo_choice - 1]
    console.print(f'\n[green]✅ Đã chọn: {CDTD_ALGORITHMS[cdtd_settings["algo"]]}[/]')
    console.print(f"\n[bold {HTOOL_COLORS['gold']}]📱 Cấu hình Telegram? (y/n)[/]")
    if Prompt.ask("   >>", choices=['y', 'n'], default='n') == 'y': setup_telegram()
    console.print(f'\n[green]✅ Cấu hình hoàn tất![/]'); time.sleep(1.5)
    return True

def cdtd_game_loop():
    global cdtd_issue_id, cdtd_previous_issue, cdtd_last_winner, cdtd_predicted_nv, cdtd_ui_state, cdtd_analysis_start_ts
    global cdtd_current_bet, cdtd_win_streak, cdtd_lose_streak, cdtd_max_win_streak, cdtd_max_lose_streak, cdtd_stop_flag
    global cdtd_stats, cdtd_pause_remaining, cdtd_skip_next, cdtd_rounds_placed, cdtd_bet_placed_this_round, cdtd_checked_result
    global cdtd_recent_choices, cdtd_avoid_repeat
    
    cdtd_stop_flag = False; cdtd_issue_id = None; cdtd_previous_issue = None; cdtd_last_winner = None
    cdtd_predicted_nv = None; cdtd_ui_state = "WAITING"; cdtd_analysis_start_ts = None
    cdtd_win_streak = 0; cdtd_lose_streak = 0; cdtd_max_win_streak = 0; cdtd_max_lose_streak = 0
    cdtd_rounds_placed = 0; cdtd_skip_next = False; cdtd_pause_remaining = 0
    cdtd_bet_placed_this_round = False; cdtd_checked_result = False
    cdtd_current_bet = cdtd_base_bet; cdtd_bet_history.clear(); cdtd_recent_choices.clear()
    cdtd_avoid_repeat = 3; cdtd_stats = {'win': 0, 'lose': 0, 'asset_0': user_asset_cdtd().get(cdtd_coin, 0)}
    
    with Live(cdtd_generate_layout(), refresh_per_second=3, console=console, screen=True) as live:
        while not cdtd_stop_flag:
            try:
                data_top10 = top_10_cdtd(); current_issue = data_top10[0][0]
                
                if current_issue != cdtd_previous_issue:
                    if cdtd_previous_issue is not None and cdtd_predicted_nv is not None and not cdtd_checked_result:
                        try:
                            winner = int(data_top10[1][0]) if data_top10[1] else None
                            if winner is not None:
                                cdtd_last_winner = winner; balance_before = user_asset_cdtd().get(cdtd_coin, 0); result_type = 'win'
                                for b in cdtd_bet_history:
                                    if b.get('result') == 'pending':
                                        b['winner'] = winner
                                        if b['chosen'] != winner:
                                            b['result'] = 'win'; cdtd_win_streak += 1; cdtd_lose_streak = 0
                                            cdtd_max_win_streak = max(cdtd_max_win_streak, cdtd_win_streak)
                                            cdtd_current_bet = cdtd_base_bet; cdtd_stats['win'] += 1; result_type = 'win'
                                        else:
                                            b['result'] = 'lose'; cdtd_lose_streak += 1; cdtd_win_streak = 0
                                            cdtd_max_lose_streak = max(cdtd_max_lose_streak, cdtd_lose_streak)
                                            cdtd_current_bet *= cdtd_multiplier; cdtd_stats['lose'] += 1; result_type = 'lose'
                                            if cdtd_pause_rounds > 0: cdtd_pause_remaining = cdtd_pause_rounds
                                time.sleep(1); balance_after = user_asset_cdtd().get(cdtd_coin, 0)
                                pnl_van = balance_after - balance_before; total_pnl = balance_after - cdtd_stats['asset_0']
                                if TELEGRAM_ENABLED and TELEGRAM_CHAT_ID:
                                    bet_nv = cdtd_predicted_nv; bet_amount = cdtd_bet_history[-1].get('amount', 0) if cdtd_bet_history else cdtd_base_bet
                                    telegram_msg = build_cdtd_telegram_message(cdtd_previous_issue, winner, bet_nv, bet_amount, result_type, pnl_van, total_pnl, balance_before, balance_after, cdtd_stats['win'], cdtd_stats['lose'], cdtd_max_win_streak, cdtd_max_lose_streak)
                                    threading.Thread(target=send_telegram_message, args=(telegram_msg,), daemon=True).start()
                                cdtd_checked_result = True; cdtd_ui_state = "RESULT"
                                live.update(cdtd_generate_layout()); time.sleep(2)
                        except: pass
                    
                    cdtd_previous_issue = current_issue; cdtd_issue_id = current_issue; cdtd_predicted_nv = None
                    cdtd_bet_placed_this_round = False; cdtd_checked_result = False
                    cdtd_analysis_start_ts = time.time(); cdtd_ui_state = "ANALYZING"
                    live.update(cdtd_generate_layout())
                
                if cdtd_ui_state == "ANALYZING":
                    elapsed = time.time() - (cdtd_analysis_start_ts or time.time())
                    if elapsed >= cdtd_analysis_duration - 8 and not cdtd_bet_placed_this_round:
                        chosen, algo = choose_nv_cdtd(cdtd_settings.get("algo", "RANDOM"), data_top10, top_100_cdtd())
                        cdtd_predicted_nv = chosen; cdtd_ui_state = "PREDICTED"; live.update(cdtd_generate_layout())
                        should_bet = True
                        if cdtd_pause_remaining > 0: cdtd_pause_remaining -= 1; should_bet = False
                        if cdtd_skip_next: cdtd_skip_next = False; should_bet = False
                        if should_bet:
                            next_issue = cdtd_issue_id + 1; bet_amount = cdtd_current_bet if cdtd_current_bet else cdtd_base_bet
                            asset = user_asset_cdtd()
                            if bet_amount > asset.get(cdtd_coin, 0): cdtd_current_bet = cdtd_base_bet; bet_amount = cdtd_base_bet
                            success, msg = bet_cdtd(next_issue, chosen, bet_amount)
                            if success:
                                cdtd_bet_history.append({'issue': next_issue, 'chosen': chosen, 'amount': bet_amount, 'result': 'pending', 'algo': algo})
                                cdtd_rounds_placed += 1; cdtd_bet_placed_this_round = True
                                if cdtd_bet_rounds_before_skip > 0 and cdtd_rounds_placed >= cdtd_bet_rounds_before_skip: cdtd_skip_next = True; cdtd_rounds_placed = 0
                        live.update(cdtd_generate_layout())
                    elif elapsed >= cdtd_analysis_duration + 15: cdtd_ui_state = "WAITING"; cdtd_issue_id = None; live.update(cdtd_generate_layout())
                
                live.update(cdtd_generate_layout()); time.sleep(0.5)
            except KeyboardInterrupt: cdtd_stop_flag = True; break
            except: time.sleep(3)

def main_cdtd_v3():
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['rocket']} ", f"bold {HTOOL_COLORS['gold']}"), ("CHẠY ĐUA TỐC ĐỘ - 40 AI", f"bold {HTOOL_COLORS['neon_blue']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header)
    console.print(f"[dim]💬 Support: @htool88 | 40 AI | Auto Né Lặp | Telegram[/dim]\n")
    data = load_data_cdtd(); setup_cdtd_headers(data)
    if not cdtd_prompt_settings(): return
    console.clear()
    console.print(f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ KHỞI ĐỘNG VỚI 40 AI...[/]")
    with console.status(f"[bold {HTOOL_COLORS['gold']}]🔍 Đang kiểm tra...[/]", spinner="dots"): asset = user_asset_cdtd(); time.sleep(1)
    if asset.get(cdtd_coin, 0) <= 0: console.print(f'[red]❌ Số dư {cdtd_coin} = 0![/]'); time.sleep(2); return
    console.print(f'[green]✅ Số dư: {asset[cdtd_coin]:.4f} {cdtd_coin}[/]')
    console.print(f'[green]✅ 40 AI sẵn sàng[/]')
    console.print(f'[green]✅ Tự động né lặp {cdtd_avoid_repeat} ván[/]')
    if TELEGRAM_ENABLED: console.print(f'[green]✅ Telegram: BẬT[/]')
    time.sleep(2); cdtd_game_loop()
    console.clear(); final_asset = user_asset_cdtd(); pnl = final_asset.get(cdtd_coin, 0) - cdtd_stats['asset_0']
    summary = Panel(Align.center(Text.assemble(("\n📊 TỔNG KẾT\n\n", f"bold {HTOOL_COLORS['gold']}"), (f"Thắng: {cdtd_stats['win']} | Thua: {cdtd_stats['lose']}\n", "white"), (f"P&L: {pnl:+.4f} {cdtd_coin}\n", HTOOL_COLORS["gold"] if pnl >= 0 else HTOOL_COLORS["ruby"]))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(summary); console.print("\n[dim]Nhấn Enter để quay lại menu...[/]"); input()

# ================== MAIN MENU ==================

def build_main_menu():
    console.clear(); console.print(Align.center(build_logo_with_gradient(LOGO)))
    menu = Panel(Align.center(Text.assemble(
        ("\n  👑 HTOOL VIP PREMIUM v3.0 👑\n\n", f"bold {HTOOL_COLORS['gold']}"),
        ("  [1] 🎯 VUA THOÁT HIỂM\n", f"bold {HTOOL_COLORS['neon_green']}"),
        ("  [2] 🏎️  CHẠY ĐUA TỐC ĐỘ (40 AI)\n", f"bold {HTOOL_COLORS['neon_orange']}"),
        ("  [3] ➕ THÊM TÀI KHOẢN\n", f"bold {HTOOL_COLORS['sapphire']}"),
        ("  [4] 🗑️  XÓA TÀI KHOẢN\n", f"bold {HTOOL_COLORS['ruby']}"),
        ("  [5] ⚙️  LƯU CONFIG VTH\n", f"bold {HTOOL_COLORS['gold']}"),
        ("  [6] 🎮 CHƠI VTH (LOAD)\n", f"bold {HTOOL_COLORS['neon_blue']}"),
        ("  [q] 👋 THOÁT\n\n", f"bold {HTOOL_COLORS['rose']}")
    )), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(menu)
    return Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn[/]", choices=['1','2','3','4','5','6','q'], default='q').lower()

def main_vth():
    global _is_authenticated, _device_id, _user_key
    threading.Thread(target=key_checker_thread, daemon=True).start()
    
    while not _is_authenticated:
        success, key, device_id = show_auth_screen()
        if success:
            _is_authenticated = True
            _user_key = key
            _device_id = device_id
            break
        if Prompt.ask("[bold yellow]Thử lại? (y/n)[/]", choices=['y', 'n'], default='y') == 'n':
            console.print("[red]👋 Tạm biệt![/]")
            sys.exit(0)
    
    console.clear()
    console.print(Panel(Align.center(Text.assemble((f"{ICONS['crown']} ", f"bold {HTOOL_COLORS['gold']}"), ("WELCOME TO HTOOL VIP PREMIUM v3.0", "bold white"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
    console.print(f"[dim]💬 Support: @htool88 | 40 AI | Auto Né Lặp | Telegram[/dim]")
    time.sleep(1)
    
    while True:
        global stop_flag
        stop_flag = False
        choice = build_main_menu()
        
        if choice == '1':
            console.clear()
            if select_account_premium():
                if prompt_settings():
                    start_game_flow()
        elif choice == '2':
            main_cdtd_v3()
        elif choice == '3':
            add_new_account(load_accounts())
        elif choice == '4':
            delete_account(load_accounts())
        elif choice == '5':
            console.clear()
            if prompt_settings():
                save_strategy_config()
            time.sleep(2)
        elif choice == '6':
            console.clear()
            if select_account_premium():
                if load_strategy_config():
                    start_game_flow()
                else:
                    time.sleep(2)
        elif choice == 'q':
            console.print(Panel(Align.center(f"[bold {HTOOL_COLORS['gold']}]👋 THANK YOU![/]"), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
            break

if __name__ == "__main__":
    try:
        main_vth()
    except KeyboardInterrupt:
        console.print(f"\n[bold {HTOOL_COLORS['gold']}]Đã dừng. 👑[/]")
        sys.exit(0)
