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
            elif package == "websocket":
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
    print("-" * 60)
    
    for package in missing_packages:
        try:
            print(f"📦 Đang cài đặt {package}...")
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                package,
                "--quiet"
            ])
            print(f"✅ Đã cài đặt {package} thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi cài đặt {package}: {e}")
            print(f"💡 Vui lòng cài đặt thủ công: pip install {package}")
            return False
    
    print("\n" + "=" * 60)
    print("✅ TẤT CẢ THƯ VIỆN ĐÃ ĐƯỢC CÀI ĐẶT XONG!")
    print("=" * 60)
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
from datetime import datetime, timezone
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

# ================== GIAO DIỆN HTOOL ==================

HTOOL_COLORS = {
    "gold": "#FFD700",
    "platinum": "#E5E4E2",
    "ruby": "#E0115F",
    "emerald": "#50C878",
    "sapphire": "#0F52BA",
    "onyx": "#353839",
    "rose": "#FF007F",
    "neon_blue": "#00D4FF",
    "neon_pink": "#FF00E5",
    "neon_green": "#39FF14",
    "neon_orange": "#FF5E00",
}

ICONS = {
    "crown": "👑",
    "fire": "🔥",
    "target": "🎯",
    "shield": "🛡️",
    "brain": "🧠",
    "robot": "🤖",
    "rocket": "🚀",
    "trophy": "🏆",
    "sparkle": "✨",
    "settings": "⚙️",
    "user": "👤",
    "check": "✅",
    "warning": "⚠️",
    "info": "ℹ️",
    "money": "💰",
    "chart": "📊",
    "clock": "⏰",
    "diamond": "💎",
    "link": "🔗",
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
_ws_status = "⏳ Đang kết nối..."

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
    try:
        endpoint = f"keys?key_code=eq.{key}&select=*,devices(*)&limit=1"
        result = supabase_request("GET", endpoint)
        if not result or len(result) == 0:
            return {"valid": False, "error": "Key không tồn tại"}
        key_data = result[0]
        if not key_data.get("is_active", False):
            return {"valid": False, "error": "Key đã bị vô hiệu hóa"}
        expires_at = key_data.get("expires_at")
        if expires_at and expires_at != "forever":
            if datetime.fromisoformat(expires_at.replace('Z', '+00:00')) < datetime.now(timezone.utc):
                return {"valid": False, "error": "Key đã hết hạn"}
        devices = key_data.get("devices", [])
        found = False
        for device in devices:
            if device.get("device_id") == device_id:
                found = True
                break
        if not found:
            return {"valid": False, "error": "Mã thiết bị không khớp với key này"}
        return {"valid": True, "data": key_data, "message": "Xác thực thành công"}
    except Exception as e:
        return {"valid": False, "error": f"Lỗi xác thực: {str(e)}"}

# ================== HÀM XÁC THỰC ==================

def show_auth_screen():
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
        time.sleep(0.5)
        result = verify_key_with_device(key, device_id)
    
    if result.get("valid"):
        console.print()
        console.print(Panel(
            Text.assemble(
                ("✅ ", "bold green"),
                ("Xác thực thành công!\n", "bold green"),
                (f"Key: {key}\n", f"bold {gold_color}"),
                (f"Thiết bị: {device_id}\n", "bold cyan"),
            ),
            title=f"[bold green]✅ XÁC THỰC THÀNH CÔNG[/bold green]",
            border_style="green",
            box=box.HEAVY
        ))
        console.print("\n[dim]Nhấn Enter để tiếp tục...[/dim]")
        input()
        return True, key, device_id
    else:
        console.print()
        console.print(Panel(
            Text.assemble(
                ("❌ ", "bold red"),
                ("Xác thực thất bại!\n", "bold red"),
                (f"Lỗi: {result.get('error', 'Không xác định')}\n", "red"),
            ),
            title=f"[bold red]❌ XÁC THỰC THẤT BẠI[/bold red]",
            border_style="red",
            box=box.HEAVY
        ))
        console.print("\n[dim]Nhấn Enter để thử lại...[/dim]")
        input()
        return False, None, None

# ================== TOOL VUA THOÁT HIỂM ==================

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('htool.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
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

# ================== 40 LOGIC VTH ==================

SELECTION_MODES = {
    "RANDOM": "1. PHẬT ĐỘ (Random)",
    "MIN_PLAYER_BET": "2. AN TOÀN (Min Players & Bet)",
    "PROBABILITY": "3. XÁC SUẤT (Probability)",
    "FOLLOW_KILLER": "4. THEO SÁT THỦ",
    "SEQUENTIAL": "5. TUẦN TỰ (1→2→3→...→8)",
    "KILLER_PERSONALITY": "6. TÍNH CÁCH SÁT THỦ",
    "SMART_SAFE": "7. THÔNG MINH (AI Smart)",
    "FOLLOW_KILLER_DELAYED": "8. THEO VẾT SÁT THỦ",
    "HIDE_SEEK_MASTER": "9. THÁNH TRỐN TÌM",
    "BALANCE": "10. CÂN BẰNG",
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
    h = {
        "accept": "*/*", "accept-language": "vi,en;q=0.9",
        "cache-control": "no-cache", "country-code": "vn",
        "origin": "https://xworld.info", "referer": "https://xworld.info/",
        "user-agent": "Mozilla/5.0",
        "user-login": "login_v2", "xb-language": "vi-VN"
    }
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

# ================== LOGIC CHỌN PHÒNG VTH ==================

def choose_random():
    return random.choice(ROOM_ORDER)

def choose_min_player_bet():
    if not any(rs.get('players', 0) > 0 or rs.get('bet', 0) > 0 for rs in room_state.values()):
        return choose_random()
    player_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['players'])
    bet_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['bet'])
    scores = defaultdict(int)
    for i, r in enumerate(player_ranks):
        scores[r] += i
    for i, r in enumerate(bet_ranks):
        scores[r] += i
    if last_killed_room in scores:
        scores[last_killed_room] += 0.5
    return min(scores, key=scores.get)

def choose_probability():
    scores = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        scores[r] = survival_rate
    return max(scores, key=scores.get)

def choose_follow_killer():
    if last_killed_room is not None and last_killed_room in ROOM_ORDER:
        return last_killed_room
    return random.choice(ROOM_ORDER)

def choose_sequential():
    global _sequential_bet_index
    room = ROOM_ORDER[_sequential_bet_index]
    _sequential_bet_index = (_sequential_bet_index + 1) % len(ROOM_ORDER)
    return room

def choose_killer_personality():
    if not killer_history:
        return choose_random()
    avg_players = sum(h['players'] for h in killer_history) / len(killer_history)
    avg_bet = sum(h['bet'] for h in killer_history) / len(killer_history)
    scores = {}
    for r in ROOM_ORDER:
        if r == last_killed_room:
            scores[r] = -999999
            continue
        player_dist = abs(room_state[r]['players'] - avg_players) / (avg_players + 1)
        bet_dist = abs(room_state[r]['bet'] - avg_bet) / (avg_bet + 1)
        scores[r] = player_dist + bet_dist
    return max(scores, key=scores.get)

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

def choose_hide_seek_master():
    danger_scores = {}
    max_players = max(rs['players'] for rs in room_state.values()) or 1
    max_bet = max(rs['bet'] for rs in room_state.values()) or 1
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        hist_danger = (kills + 1) / (kills + survives + 2)
        crowd_danger = room_state[r]['players'] / max_players
        money_danger = room_state[r]['bet'] / max_bet
        recency_penalty = 1.0 if r == last_killed_room else 0.0
        danger_scores[r] = (0.3 * hist_danger) + (0.2 * crowd_danger) + (0.2 * money_danger) + recency_penalty
    return min(danger_scores, key=danger_scores.get)

def choose_balance():
    total_players = sum(rs['players'] for rs in room_state.values())
    total_bet = sum(rs['bet'] for rs in room_state.values())
    avg_players = total_players / len(ROOM_ORDER) if total_players > 0 else 0
    avg_bet = total_bet / len(ROOM_ORDER) if total_bet > 0 else 0
    scores = {}
    for r in ROOM_ORDER:
        scores[r] = abs(room_state[r]['players'] - avg_players) / (avg_players + 1) + abs(room_state[r]['bet'] - avg_bet) / (avg_bet + 1)
    return min(scores, key=scores.get)

def choose_room_tn(mode: str) -> Tuple[int, str]:
    logic_map = {
        "RANDOM": choose_random,
        "MIN_PLAYER_BET": choose_min_player_bet,
        "PROBABILITY": choose_probability,
        "FOLLOW_KILLER": choose_follow_killer,
        "SEQUENTIAL": choose_sequential,
        "KILLER_PERSONALITY": choose_killer_personality,
        "SMART_SAFE": choose_smart_safe,
        "HIDE_SEEK_MASTER": choose_hide_seek_master,
        "BALANCE": choose_balance,
    }
    func = logic_map.get(mode, choose_random)
    return func(), mode

# ================== API VÀ WEBSOCKET VTH ==================

def api_headers():
    return {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0",
        "user-id": str(USER_ID) if USER_ID else "",
        "user-secret-key": SECRET_KEY if SECRET_KEY else ""
    }

def place_bet_http(issue: int, room_id: int, amount: float) -> dict:
    payload = {"asset_type": "BUILD", "user_id": USER_ID, "room_id": int(room_id), "bet_amount": float(amount)}
    try:
        r = requests.post(BET_API_URL, headers=api_headers(), json=payload, timeout=8)
        try:
            return r.json()
        except:
            return {"raw": r.text}
    except Exception as e:
        return {"error": str(e)}

def record_bet(issue: int, room_id: int, amount: float, resp: dict, algo_used=None):
    rec = {"issue": issue, "room": room_id, "amount": float(amount), "time": datetime.now(tz).strftime("%H:%M:%S"), "resp": resp, "result": "Đang", "algo": algo_used}
    bet_history.append(rec)
    return rec

def place_bet_async(issue: int, room_id: int, amount: float, algo_used=None):
    def worker():
        time.sleep(random.uniform(0.05, 0.45))
        res = place_bet_http(issue, room_id, amount)
        record_bet(issue, room_id, amount, res, algo_used=algo_used)
    threading.Thread(target=worker, daemon=True).start()

def lock_prediction_if_needed():
    global prediction_locked, predicted_room, ui_state, current_bet, stop_flag
    if stop_flag or prediction_locked or issue_id is None:
        return
    mode = settings.get("algo", "RANDOM")
    chosen, algo = choose_room_tn(mode)
    predicted_room = chosen
    prediction_locked = True
    ui_state = "PREDICTED"
    if run_mode == "AUTO":
        bld = current_build
        if bld is None:
            bld, _, _ = fetch_balances_3games(retries=1, timeout=3)
        if current_bet is None:
            current_bet = base_bet
        amt = float(current_bet)
        if bld and amt > bld:
            current_bet = base_bet
            amt = float(current_bet)
        place_bet_async(issue_id, predicted_room, amt, algo_used=algo)

def on_open(ws):
    _ws["ws"] = ws
    global _ws_status
    _ws_status = "✅ Đã kết nối"
    try:
        payload = {"msg_type": "handle_enter_game", "asset_type": "BUILD", "user_id": USER_ID, "user_secret_key": SECRET_KEY}
        ws.send(json.dumps(payload))
    except:
        pass

def on_message(ws, message):
    global issue_id, killed_room, round_index, ui_state, analysis_start_ts
    global prediction_locked, predicted_room, last_killed_room, current_bet
    global win_streak, lose_streak, max_win_streak, max_lose_streak, stop_flag
    
    try:
        if isinstance(message, bytes):
            message = message.decode("utf-8", errors="replace")
        data = json.loads(message)
        msg_type = str(data.get("msg_type", ""))
        
        if msg_type == "notify_enter_game":
            if data.get("last_killed_room_id"):
                last_killed_room = int(data["last_killed_room_id"])
            for rm in data.get("room_stat", []):
                if isinstance(rm, dict):
                    rid = int(rm.get("room_id", 0))
                    room_state[rid] = {"players": int(rm.get("user_cnt", 0)), "bet": int(rm.get("total_bet_amount", 0))}
        
        elif "issue_stat" in msg_type:
            rooms = data.get("rooms", [])
            for rm in rooms:
                if isinstance(rm, dict):
                    rid = int(rm.get("room_id", 0))
                    room_state[rid] = {"players": int(rm.get("user_cnt", 0)), "bet": int(rm.get("total_bet_amount", 0))}
            
            new_issue = data.get("issue_id")
            if new_issue and new_issue != issue_id:
                issue_id = new_issue
                round_index += 1
                killed_room = None
                prediction_locked = False
                predicted_room = None
                ui_state = "ANALYZING"
                analysis_start_ts = time.time()
        
        elif "count_down" in msg_type:
            count_down = data.get("count_down", 99)
            if int(count_down) <= 10 and not prediction_locked:
                lock_prediction_if_needed()
        
        elif "result" in msg_type:
            kr = data.get("killed_room") or data.get("killed_room_id")
            if kr:
                killed_room = int(kr)
                game_kill_log.append(killed_room)
                last_killed_room = killed_room
                for rid in ROOM_ORDER:
                    if rid == killed_room:
                        room_stats[rid]["kills"] += 1
                    else:
                        room_stats[rid]["survives"] += 1
                
                for b in reversed(bet_history):
                    if b.get("issue") == issue_id:
                        if int(b.get("room")) != killed_room:
                            b["result"] = "Thắng"
                            current_bet = base_bet
                            win_streak += 1
                            lose_streak = 0
                            max_win_streak = max(max_win_streak, win_streak)
                        else:
                            b["result"] = "Thua"
                            current_bet = current_bet * multiplier if current_bet else base_bet
                            lose_streak += 1
                            win_streak = 0
                            max_lose_streak = max(max_lose_streak, lose_streak)
                        break
            ui_state = "RESULT"
    except:
        pass

def on_close(ws, code, reason):
    global _ws_status
    _ws_status = f"⏳ Đã đóng ({code})"

def on_error(ws, err):
    global _ws_status
    _ws_status = f"❌ Lỗi"

def start_ws():
    global _ws_status
    while not stop_flag:
        try:
            _ws_status = "⏳ Đang kết nối..."
            ws_app = websocket.WebSocketApp(WS_URL, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            _ws["ws"] = ws_app
            ws_app.run_forever(ping_interval=15, ping_timeout=6)
        except:
            _ws_status = "❌ Lỗi kết nối"
        time.sleep(random.uniform(1, 5))

def monitor_loop():
    global last_msg_ts, stop_flag
    while not stop_flag:
        now = time.time()
        if now - last_msg_ts > 45:
            try:
                wsobj = _ws.get("ws")
                if wsobj:
                    wsobj.close()
            except:
                pass
        time.sleep(0.6)

# ================== GIAO DIỆN VTH ==================

def build_logo_with_gradient(logo_text: str) -> Text:
    lines = logo_text.split('\n')
    result = Text()
    for line in lines:
        if line.strip():
            chars = list(line)
            for i, char in enumerate(chars):
                if char in ['█', '╔', '╗', '║', '╚', '╝', '═']:
                    if i % 3 == 0:
                        style = HTOOL_COLORS["gold"]
                    elif i % 3 == 1:
                        style = HTOOL_COLORS["neon_blue"]
                    else:
                        style = HTOOL_COLORS["neon_pink"]
                    result.append(char, style=style)
                else:
                    result.append(char, style="dim")
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
    content = Group(Align.center(logo_text), info_table)
    return Panel(content, border_style=HTOOL_COLORS["gold"], box=box.HEAVY, padding=(1, 2))

def build_premium_rooms():
    room_panels = []
    for r in ROOM_ORDER:
        st = room_state.get(r, {})
        players = st.get("players", 0)
        bet_val = st.get('bet', 0) or 0
        is_predicted = predicted_room is not None and int(r) == int(predicted_room)
        is_killed = killed_room is not None and int(r) == int(killed_room)
        if is_killed and is_predicted:
            border = f"bold {HTOOL_COLORS['ruby']}"
            title_style = f"bold {HTOOL_COLORS['ruby']}"
        elif is_killed:
            border = HTOOL_COLORS["ruby"]
            title_style = HTOOL_COLORS["ruby"]
        elif is_predicted:
            border = f"bold {HTOOL_COLORS['emerald']}"
            title_style = f"bold {HTOOL_COLORS['emerald']}"
        else:
            border = HTOOL_COLORS["onyx"]
            title_style = "white"
        content = Text.assemble(("\n", ""), (f"👥 {players:3d} ", "white"), ("| ", "dim"), (f"💰 {int(bet_val):,}", HTOOL_COLORS["gold"]), ("\n", ""), justify="center")
        room_panels.append(Panel(Align.center(content, vertical="middle"), title=f"[{title_style}]{ROOM_NAMES.get(r, f'Room {r}')}[/{title_style}]", border_style=border, box=box.HEAVY, expand=True, height=5))
    return Panel(Columns(room_panels, equal=True, expand=True), title=f"[bold {HTOOL_COLORS['gold']}]🎮 PREMIUM BATTLE ARENA 🎮[/]", box=box.HEAVY, border_style=HTOOL_COLORS["gold"], expand=True)

def build_premium_mid():
    if ui_state == "ANALYZING":
        elapsed = time.time() - (analysis_start_ts or time.time())
        progress = min(1.0, elapsed / analysis_duration)
        bar_width = 40
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
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
        result_text = "⏳ WAITING"
        result_color = HTOOL_COLORS["gold"]
        if last_bet and last_bet.get('issue') == issue_id:
            if last_bet.get('result') == "Thắng":
                result_text = "🎉 WINNER 🎉"
                result_color = HTOOL_COLORS["emerald"]
            elif last_bet.get('result') == "Thua":
                result_text = "💀 LOSER 💀"
                result_color = HTOOL_COLORS["ruby"]
        content = Text.assemble(("\n", ""), (f"{result_text}\n\n", f"bold {result_color}"), (f"☠️ Killer: {k}\n", f"bold {HTOOL_COLORS['ruby']}"))
        return Panel(Align.center(content), border_style=result_color, box=box.HEAVY, expand=True)
    else:
        return Panel(Align.center(Text(f"⏳ Waiting for game data...", style=HTOOL_COLORS["gold"])), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_premium_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 BET HISTORY[/]", box=box.ROUNDED, expand=True)
    t.add_column("Round", style=HTOOL_COLORS["sapphire"])
    t.add_column("Room", style=HTOOL_COLORS["neon_blue"])
    t.add_column("Amount", justify="right", style=HTOOL_COLORS["gold"])
    t.add_column("Result")
    for b in list(bet_history)[-6:]:
        res = str(b.get('result', '⏳'))
        res_text = Text(f"✅" if "Thắng" in res else f"❌" if "Thua" in res else f"⏳")
        t.add_row(str(b.get('issue', '-')), ROOM_NAMES.get(b.get('room'), str(b.get('room', '-'))), f"{float(b.get('amount', 0)):,.2f}", res_text)
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def prompt_settings() -> bool:
    global base_bet, multiplier, current_bet, bet_rounds_before_skip, pause_after_losses, profit_target, stop_when_profit_reached, stop_loss_target, stop_when_loss_reached
    
    console.clear()
    console.print(Panel(Align.center(f"[bold {HTOOL_COLORS['gold']}]⚙️ PREMIUM CONFIGURATION[/]"), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
    
    console.print(f"\n[bold {HTOOL_COLORS['neon_blue']}]💰 Cược gốc:[/]")
    base_bet = FloatPrompt.ask("   >>", default=1.0)
    console.print(f"\n[bold {HTOOL_COLORS['neon_blue']}]📈 Hệ số nhân:[/]")
    multiplier = FloatPrompt.ask("   >>", default=2.0)
    current_bet = base_bet
    
    modes = list(SELECTION_MODES.items())
    algo_table = Table(box=box.ROUNDED)
    algo_table.add_column("STT", style=HTOOL_COLORS["gold"], width=4)
    algo_table.add_column("Thuật toán", style=HTOOL_COLORS["neon_blue"])
    for i, (key, label) in enumerate(modes, 1):
        algo_table.add_row(str(i), label)
    console.print(f"\n[bold {HTOOL_COLORS['neon_pink']}]🧠 Chọn AI:[/]")
    console.print(algo_table)
    
    choice = IntPrompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn[/]", choices=[str(i) for i in range(1, len(modes) + 1)], default=1)
    settings["algo"] = modes[choice - 1][0]
    
    console.print(f"\n[bold {HTOOL_COLORS['sapphire']}]🛡️ Chống soi (nghỉ 1 ván sau N ván):[/]")
    bet_rounds_before_skip = IntPrompt.ask("   >>", default=0)
    console.print(f"\n[bold {HTOOL_COLORS['sapphire']}]⏸️ Nghỉ sau khi thua (số ván):[/]")
    pause_after_losses = IntPrompt.ask("   >>", default=0)
    
    pt_str = Prompt.ask(f"\n[bold {HTOOL_COLORS['emerald']}]🎯 Mục tiêu lãi (Enter bỏ qua):[/]", default="")
    if pt_str.strip():
        try:
            profit_target = float(pt_str)
            stop_when_profit_reached = True
        except:
            pass
    
    sl_str = Prompt.ask(f"\n[bold {HTOOL_COLORS['ruby']}]💀 Cắt lỗ (Enter bỏ qua):[/]", default="")
    if sl_str.strip():
        try:
            stop_loss_target = float(sl_str)
            stop_when_loss_reached = True
        except:
            pass
    
    start = Prompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]>> Bắt đầu? (Enter/q)[/]", default="")
    if start.lower() == 'q':
        return False
    run_mode = "AUTO"
    return True

def load_accounts() -> list:
    acc_file = Path("accounts.json")
    if not acc_file.exists():
        return []
    try:
        return json.loads(acc_file.read_text())
    except:
        return []

def save_accounts(accounts: list):
    with Path("accounts.json").open("w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)

def add_new_account(accounts: list) -> bool:
    console.clear()
    link = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Paste link[/]")
    if not link:
        return False
    try:
        parsed = urlparse(link)
        params = parse_qs(parsed.query)
        if 'userId' in params and 'secretKey' in params:
            uid = int(params.get('userId')[0])
            skey = params.get('secretKey', [None])[0]
            accounts.append({"userId": uid, "secretKey": skey})
            save_accounts(accounts)
            console.print(f"[green]✅ Đã thêm: {uid}[/]")
            time.sleep(2)
            return True
    except:
        pass
    return False

def delete_account(accounts: list) -> bool:
    console.clear()
    if not accounts:
        return False
    table = Table(box=box.ROUNDED)
    table.add_column("STT", style=HTOOL_COLORS["gold"])
    table.add_column("User ID", style=HTOOL_COLORS["neon_blue"])
    for i, acc in enumerate(accounts, 1):
        table.add_row(str(i), str(acc.get('userId')))
    console.print(table)
    choice = Prompt.ask(f"[bold {HTOOL_COLORS['ruby']}]>> Chọn STT[/]", default="")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(accounts):
            removed = accounts.pop(idx)
            save_accounts(accounts)
            console.print(f"[green]✅ Đã xóa: {removed.get('userId')}[/]")
            time.sleep(2)
            return True
    except:
        pass
    return False

def select_account_premium() -> bool:
    global USER_ID, SECRET_KEY
    while True:
        console.clear()
        accounts = load_accounts()
        if not accounts:
            console.print("[yellow]⚠️ Chưa có tài khoản![/]")
            time.sleep(2)
            return False
        table = Table(title="📋 DANH SÁCH TÀI KHOẢN", box=box.HEAVY)
        table.add_column("STT", style=HTOOL_COLORS["gold"])
        table.add_column("User ID", style=HTOOL_COLORS["neon_blue"])
        table.add_column("Balance", justify="right")
        for i, acc in enumerate(accounts, 1):
            uid = acc.get('userId')
            build, _, _ = fetch_balances_3games(uid=uid, secret=acc.get('secretKey'))
            table.add_row(str(i), str(uid), f"[{HTOOL_COLORS['emerald']}]{build:,.4f}[/]" if build else "[red]❌[/]")
        console.print(table)
        choice = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn số[/]", choices=[str(i) for i in range(1, len(accounts) + 1)], default="")
        if not choice:
            return False
        idx = int(choice) - 1
        if 0 <= idx < len(accounts):
            selected = accounts[idx]
            USER_ID = selected['userId']
            SECRET_KEY = selected['secretKey']
            console.print(f"[green]✅ Đã chọn: {USER_ID}[/]")
            time.sleep(1.5)
            return True

def start_threads():
    threading.Thread(target=start_ws, daemon=True).start()
    threading.Thread(target=monitor_loop, daemon=True).start()

def start_game_flow():
    global stop_flag
    if USER_ID is None or SECRET_KEY is None:
        console.print("[red]❌ Chưa chọn tài khoản.[/]")
        time.sleep(2)
        return
    
    console.print(Rule("[bold green]🚀 KHỞI ĐỘNG...[/]", style="green"))
    start_threads()
    
    with console.status("[bold green]Đang kết nối...[/]", spinner="dots"):
        wait_start = time.time()
        while issue_id is None and (time.time() - wait_start) < 30:
            time.sleep(0.5)
        if issue_id is None:
            console.print("\n[bold red]❌ Không nhận được dữ liệu.[/]")
            time.sleep(3)
            return
    
    console.print("\n[bold green]✅ Kết nối thành công![/]")
    time.sleep(2)
    
    def generate_layout():
        main_grid = Table.grid(expand=True, pad_edge=False)
        main_grid.add_column("main", ratio=60)
        main_grid.add_column("side", ratio=40)
        right_grid = Table.grid(expand=True, pad_edge=False)
        right_grid.add_row(build_premium_mid())
        right_grid.add_row(build_premium_history())
        main_grid.add_row(build_premium_rooms(), right_grid)
        root = Table.grid(expand=True, pad_edge=False)
        root.add_row(build_premium_header())
        root.add_row(main_grid)
        return root
    
    with Live(generate_layout(), refresh_per_second=4, console=console, screen=True) as live:
        try:
            while not stop_flag:
                live.update(generate_layout())
                time.sleep(0.25)
        except KeyboardInterrupt:
            console.print("[yellow]Người dùng thoát.[/]")

def save_strategy_config():
    config_data = {"base_bet": base_bet, "multiplier": multiplier, "algo": settings.get("algo"), "bet_rounds_before_skip": bet_rounds_before_skip, "pause_after_losses": pause_after_losses}
    try:
        with open(STRATEGY_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        console.print(f"[green]✅ Config saved![/]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/]")

def load_strategy_config() -> bool:
    global base_bet, multiplier, current_bet, bet_rounds_before_skip, pause_after_losses
    if not Path(STRATEGY_CONFIG_FILE).exists():
        console.print(f"[yellow]⚠️ Config not found.[/]")
        return False
    try:
        with open(STRATEGY_CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        base_bet = config_data.get("base_bet", 1.0)
        multiplier = config_data.get("multiplier", 2.0)
        settings["algo"] = config_data.get("algo", "RANDOM")
        bet_rounds_before_skip = config_data.get("bet_rounds_before_skip", 0)
        pause_after_losses = config_data.get("pause_after_losses", 0)
        current_bet = base_bet
        run_mode = "AUTO"
        console.print(f"[green]✅ Config loaded![/]")
        time.sleep(2)
        return True
    except:
        return False

# ================== TOOL CHẠY ĐUA TỐC ĐỘ (ĐÃ SỬA) ==================

cdtd_session = requests.Session()
cdtd_headers = {}

NV = {
    1: 'Bậc thầy tấn công',
    2: 'Quyền sắt',
    3: 'Thợ lặn sâu',
    4: 'Cơn lốc sân cỏ',
    5: 'Hiệp sĩ phi nhanh',
    6: 'Vua home run'
}

NV_ICONS = {1: '🥋', 2: '👊', 3: '🤿', 4: '🌪️', 5: '🏇', 6: '⚾'}

CDTD_ALGORITHMS = {
    "RANDOM": "1. NGẪU NHIÊN",
    "AVOID_LAST": "2. TRÁNH KẾT QUẢ CUỐI",
    "HOT_STREAK": "3. THEO CHUỖI THẮNG",
    "COLD_STREAK": "4. BẮT ĐẢO CHIỀU",
    "BALANCE": "5. CÂN BẰNG LỊCH SỬ",
    "PATTERN": "6. NHẬN DIỆN MẪU",
    "PROBABILITY": "7. XÁC SUẤT THỐNG KÊ",
    "FOLLOW_WINNER": "8. THEO NGƯỜI THẮNG",
    "ANTI_WINNER": "9. CHỐNG NGƯỜI THẮNG",
    "SMART_ANALYSIS": "10. PHÂN TÍCH THÔNG MINH",
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

# ================== CDTD LOGIC ==================

def choose_nv_random(data_top10, data_top100):
    return random.randint(1, 6)

def choose_nv_avoid_last(data_top10, data_top100):
    last_winner = int(data_top10[1][0]) if data_top10 and data_top10[1] else None
    candidates = [i for i in range(1, 7) if i != last_winner]
    return random.choice(candidates) if candidates else random.randint(1, 6)

def choose_nv_hot_streak(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        max_wins = max(data_top100[1])
        hot_nvs = [i+1 for i, wins in enumerate(data_top100[1]) if wins == max_wins]
        return random.choice(hot_nvs)
    return random.randint(1, 6)

def choose_nv_cold_streak(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        min_wins = min(data_top100[1])
        cold_nvs = [i+1 for i, wins in enumerate(data_top100[1]) if wins == min_wins]
        return random.choice(cold_nvs)
    return random.randint(1, 6)

def choose_nv_balance(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        total_wins = sum(data_top100[1])
        avg_wins = total_wins / 6
        below_avg = [i+1 for i, wins in enumerate(data_top100[1]) if wins < avg_wins]
        if below_avg:
            return random.choice(below_avg)
    return random.randint(1, 6)

def choose_nv_pattern(data_top10, data_top100):
    if len(cdtd_bet_history) >= 4:
        recent_winners = [int(b.get('winner', 0)) for b in list(cdtd_bet_history)[-6:] if b.get('winner')]
        if len(recent_winners) >= 4:
            if recent_winners[-1] == recent_winners[-3] and recent_winners[-2] == recent_winners[-4]:
                return recent_winners[-2]
    return random.randint(1, 6)

def choose_nv_probability(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        weights = []
        for i, wins in enumerate(data_top100[1]):
            weight = 1.0 / (wins + 1)
            if i + 1 == int(data_top10[1][0]):
                weight *= 0.5
            weights.append(weight)
        total = sum(weights)
        if total > 0:
            probabilities = [w/total for w in weights]
            return random.choices(range(1, 7), weights=probabilities, k=1)[0]
    return random.randint(1, 6)

def choose_nv_follow_winner(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        return data_top100[1].index(max(data_top100[1])) + 1
    return random.randint(1, 6)

def choose_nv_anti_winner(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        max_idx = data_top100[1].index(max(data_top100[1])) + 1
        candidates = [i for i in range(1, 7) if i != max_idx]
        return random.choice(candidates) if candidates else random.randint(1, 6)
    return random.randint(1, 6)

def choose_nv_smart_analysis(data_top10, data_top100):
    if data_top100 and data_top100[1]:
        scores = {}
        total_wins = sum(data_top100[1])
        avg_wins = total_wins / 6
        for i in range(1, 7):
            wins = data_top100[1][i-1]
            score = 0
            if wins < avg_wins:
                score += (avg_wins - wins) * 2
            if i == int(data_top10[1][0]):
                score -= 1
            score += random.uniform(-0.5, 0.5)
            scores[i] = score
        return max(scores, key=scores.get)
    return random.randint(1, 6)

def choose_nv_cdtd(mode: str, data_top10, data_top100):
    logic_map = {
        "RANDOM": choose_nv_random,
        "AVOID_LAST": choose_nv_avoid_last,
        "HOT_STREAK": choose_nv_hot_streak,
        "COLD_STREAK": choose_nv_cold_streak,
        "BALANCE": choose_nv_balance,
        "PATTERN": choose_nv_pattern,
        "PROBABILITY": choose_nv_probability,
        "FOLLOW_WINNER": choose_nv_follow_winner,
        "ANTI_WINNER": choose_nv_anti_winner,
        "SMART_ANALYSIS": choose_nv_smart_analysis,
    }
    func = logic_map.get(mode, choose_nv_random)
    return func(data_top10, data_top100), mode

# ================== CDTD API ==================

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        use_saved = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]Sử dụng thông tin đã lưu? (y/n)[/]', choices=['y', 'n'], default='y')
        if use_saved == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
    
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]📋 NHẬP THÔNG TIN[/]", style=HTOOL_COLORS["gold"]))
    console.print("[bold]HƯỚNG DẪN:[/]")
    console.print("1. Truy cập xworld.io\n2. Đăng nhập\n3. Vào Chạy đua tốc độ\n4. Copy link và dán vào đây\n")
    
    link = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]📋 Nhập link[/]')
    
    try:
        user_id = link.split('&')[0].split('?userId=')[1]
        user_secretkey = link.split('&')[1].split('secretKey=')[1]
    except:
        user_id = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]👤 User ID[/]')
        user_secretkey = Prompt.ask(f'[bold {HTOOL_COLORS["gold"]}]🔑 Secret Key[/]')
    
    json_data = {'user-id': user_id, 'user-secret-key': user_secretkey}
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def setup_cdtd_headers(data: dict):
    global cdtd_headers
    cdtd_headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }

def top_100_cdtd():
    headers = {
        'accept': '*/*',
        'origin': 'https://sprintrun.win',
        'referer': 'https://sprintrun.win/',
        'user-agent': 'Mozilla/5.0',
    }
    try:
        response = cdtd_session.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers, timeout=10).json()
        kq = [response['data']['athlete_2_win_times'][str(i)] for i in range(1, 7)]
        return [1, 2, 3, 4, 5, 6], kq
    except:
        return [1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0]

def top_10_cdtd():
    try:
        response = cdtd_session.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=cdtd_headers, timeout=10).json()
        ki = [i['issue_id'] for i in response['data']['recent_10']]
        kq = [i['result'][0] for i in response['data']['recent_10']]
        return ki, kq
    except:
        return [0], [1]

def user_asset_cdtd():
    try:
        json_data = {'user_id': int(cdtd_headers['user-id']), 'source': 'home'}
        response = cdtd_session.post('https://wallet.3games.io/api/wallet/user_asset', headers=cdtd_headers, json=json_data, timeout=10).json()
        return {
            'USDT': float(response['data']['user_asset'].get('USDT', 0)),
            'WORLD': float(response['data']['user_asset'].get('WORLD', 0)),
            'BUILD': float(response['data']['user_asset'].get('BUILD', 0))
        }
    except:
        return {'USDT': 0, 'WORLD': 0, 'BUILD': 0}

def bet_cdtd(issue_id, nv_id, amount):
    try:
        json_data = {
            'issue_id': int(issue_id),
            'bet_group': 'not_winner',
            'asset_type': cdtd_coin,
            'athlete_id': nv_id,
            'bet_amount': float(amount),
        }
        response = cdtd_session.post('https://api.sprintrun.win/sprint/bet', headers=cdtd_headers, json=json_data, timeout=10).json()
        if response.get('code') == 0 and response.get('msg') == 'ok':
            return True, "ok"
        elif response.get('code') == 51010:
            return False, "Kỳ đã kết thúc"
        else:
            return False, response.get('msg', 'Unknown error')
    except Exception as e:
        return False, str(e)

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
    pnl_color = HTOOL_COLORS["emerald"] if pnl >= 0 else HTOOL_COLORS["ruby"]
    info_table.add_row(f"{ICONS['chart']} P&L:", f"[{pnl_color}]{pnl:+.4f} {cdtd_coin}[/]")
    
    streak_text = Text.assemble(
        ("🔥 ", f"bold {HTOOL_COLORS['neon_orange']}"),
        (f"{cdtd_win_streak}", f"bold {HTOOL_COLORS['emerald']}"),
        (" | ", "dim"),
        ("💀 ", f"bold {HTOOL_COLORS['ruby']}"),
        (f"{cdtd_lose_streak}", f"bold {HTOOL_COLORS['ruby']}")
    )
    info_table.add_row("📊 STREAK:", streak_text)
    info_table.add_row(f"{ICONS['brain']} AI:", f"[bold {HTOOL_COLORS['neon_pink']}]{CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')}[/]")
    info_table.add_row(f"{ICONS['clock']} TIME:", f"[{HTOOL_COLORS['sapphire']}]{datetime.now(tz).strftime('%H:%M:%S')}[/]")
    info_table.add_row(f"{ICONS['target']} ISSUE:", f"[bold {HTOOL_COLORS['gold']}]{cdtd_issue_id or 'Waiting...'}[/]")
    info_table.add_row(f"{ICONS['info']} STATUS:", f"[dim]{cdtd_ui_state}[/]")
    
    content = Group(Align.center(logo_text), info_table)
    return Panel(content, border_style=HTOOL_COLORS["gold"], box=box.HEAVY, padding=(1, 2))

def build_cdtd_racers():
    data_top100 = top_100_cdtd()
    data_top10 = top_10_cdtd()
    
    racer_panels = []
    for i in range(1, 7):
        wins = data_top100[1][i-1] if data_top100[1] else 0
        is_predicted = cdtd_predicted_nv == i
        is_last_winner = False
        if data_top10 and data_top10[1]:
            try:
                is_last_winner = int(data_top10[1][0]) == i
            except:
                pass
        
        if is_predicted:
            border = f"bold {HTOOL_COLORS['emerald']}"
            title_style = f"bold {HTOOL_COLORS['emerald']}"
            bg = "on #003300"
            glow = "✨⭐"
        elif is_last_winner:
            border = HTOOL_COLORS["gold"]
            title_style = HTOOL_COLORS["gold"]
            bg = "on #332200"
            glow = "🏆"
        else:
            border = HTOOL_COLORS["onyx"]
            title_style = "white"
            bg = ""
            glow = ""
        
        content = Text.assemble(
            ("\n", ""),
            (f"{glow} {NV_ICONS[i]}\n", "default"),
            (f"{NV[i]}\n", title_style),
            (f"🏆 {wins} wins", "dim"),
            ("\n", ""),
            justify="center"
        )
        
        panel = Panel(
            Align.center(content, vertical="middle"),
            title=f"[{title_style}]#{i}[/{title_style}]",
            border_style=border,
            box=box.HEAVY,
            expand=True,
            height=6,
            style=bg
        )
        racer_panels.append(panel)
    
    return Panel(
        Columns(racer_panels, equal=True, expand=True),
        title=f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ CHẠY ĐUA TỐC ĐỘ - SPRINT RUN 🏎️[/]",
        box=box.HEAVY,
        border_style=HTOOL_COLORS["neon_orange"],
        expand=True
    )

def build_cdtd_mid():
    if cdtd_ui_state == "ANALYZING":
        elapsed = time.time() - (cdtd_analysis_start_ts or time.time())
        progress = min(1.0, elapsed / cdtd_analysis_duration)
        bar_width = 30
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        remaining = max(0, int(cdtd_analysis_duration - elapsed))
        
        content = Text.assemble(
            ("\n🧠 ĐANG PHÂN TÍCH DỮ LIỆU...\n\n", f"bold {HTOOL_COLORS['neon_blue']}"),
            (f"[{HTOOL_COLORS['gold']}]{bar}[/{HTOOL_COLORS['gold']}]\n\n"),
            (f"Tiến độ: {progress*100:.0f}%\n", HTOOL_COLORS['neon_pink']),
            (f"⏱️ Còn {remaining}s sẽ đặt cược\n", "dim"),
            (f"📊 Đang xử lý kỳ #{cdtd_issue_id}\n", "dim"),
            justify="center"
        )
        return Panel(content, border_style=HTOOL_COLORS["neon_blue"], box=box.HEAVY, expand=True)
    
    elif cdtd_ui_state == "PREDICTED":
        bet_amt = cdtd_current_bet or cdtd_base_bet
        content = Text.assemble(
            ("\n", ""),
            ("╔══════════════════════════════╗\n", HTOOL_COLORS["gold"]),
            ("║  🎯 DỰ ĐOÁN CỦA BOT  🎯    ║\n", HTOOL_COLORS["gold"]),
            ("║                            ║\n", HTOOL_COLORS["gold"]),
            ("║  ", HTOOL_COLORS["gold"]),
            (f"{NV_ICONS.get(cdtd_predicted_nv, '🤖')} {NV.get(cdtd_predicted_nv, 'N/A'):^20}", f"bold {HTOOL_COLORS['emerald']}"),
            ("  ║\n", HTOOL_COLORS["gold"]),
            ("║                            ║\n", HTOOL_COLORS["gold"]),
            ("║  💰 Cược: ", HTOOL_COLORS["gold"]),
            (f"{bet_amt:.2f} {cdtd_coin:<10}", f"bold {HTOOL_COLORS['gold']}"),
            ("  ║\n", HTOOL_COLORS["gold"]),
            ("║  🎲 Kỳ: ", HTOOL_COLORS["gold"]),
            (f"{cdtd_issue_id + 1 if cdtd_issue_id else '?':<13}", "white"),
            ("  ║\n", HTOOL_COLORS["gold"]),
            ("╚══════════════════════════════╝\n", HTOOL_COLORS["gold"]),
            ("\n"),
            (f"📈 Chuỗi thắng: {cdtd_win_streak}  📉 Chuỗi thua: {cdtd_lose_streak}\n", "white"),
            justify="center"
        )
        return Panel(content, border_style=HTOOL_COLORS["emerald"], box=box.HEAVY, expand=True)
    
    elif cdtd_ui_state == "RESULT":
        last_bet = cdtd_bet_history[-1] if cdtd_bet_history else None
        if last_bet and last_bet.get('result') == 'win':
            result_text = "🎉 CHIẾN THẮNG! 🎉"
            result_color = HTOOL_COLORS["emerald"]
            border_color = HTOOL_COLORS["emerald"]
        elif last_bet and last_bet.get('result') == 'lose':
            result_text = "💀 THUA CUỘC! 💀"
            result_color = HTOOL_COLORS["ruby"]
            border_color = HTOOL_COLORS["ruby"]
        else:
            result_text = "⏳ ĐANG CHỜ..."
            result_color = HTOOL_COLORS["gold"]
            border_color = HTOOL_COLORS["gold"]
        
        content = Text.assemble(
            ("\n", ""),
            (f"{result_text}\n\n", f"bold {result_color}"),
            ("Người thắng: ", "white"),
            (f"{NV_ICONS.get(cdtd_last_winner, '🏆')} {NV.get(cdtd_last_winner, 'N/A')}\n\n", f"bold {HTOOL_COLORS['gold']}"),
            (f"📊 P&L: {user_asset_cdtd().get(cdtd_coin, 0) - cdtd_stats['asset_0']:+.4f} {cdtd_coin}\n", f"bold {result_color}"),
            ("\n⏳ Đang chờ kỳ mới...", "dim"),
            justify="center"
        )
        return Panel(content, border_style=border_color, box=box.HEAVY, expand=True)
    
    else:
        content = Text.assemble(
            ("\n⏳ ĐANG CHỜ DỮ LIỆU...\n\n", f"bold {HTOOL_COLORS['gold']}"),
            ("🔄 Đang kết nối đến server...\n", "dim"),
            ("\n💡 Tool sẽ tự động chạy khi có dữ liệu", "dim"),
            justify="center"
        )
        return Panel(content, border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_cdtd_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 LỊCH SỬ CƯỢC[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["onyx"])
    t.add_column("Kỳ", no_wrap=True, style=HTOOL_COLORS["sapphire"], width=6)
    t.add_column("Chọn", no_wrap=True, style=HTOOL_COLORS["neon_blue"])
    t.add_column("Cược", justify="right", no_wrap=True, style=HTOOL_COLORS["gold"], width=10)
    t.add_column("KQ", no_wrap=True)
    t.add_column("Thắng", no_wrap=True)
    
    for b in list(cdtd_bet_history)[-10:]:
        issue = str(b.get('issue', '-'))
        chosen = NV.get(b.get('chosen'), str(b.get('chosen', '-')))
        amount = f"{b.get('amount', 0):.2f}"
        winner = NV.get(b.get('winner'), '-')
        
        if b.get('result') == 'win':
            result_text = Text("✅ THẮNG", style=f"bold {HTOOL_COLORS['emerald']}")
            winner_text = Text(winner, style=HTOOL_COLORS["emerald"])
        elif b.get('result') == 'lose':
            result_text = Text("❌ THUA", style=f"bold {HTOOL_COLORS['ruby']}")
            winner_text = Text(winner, style=HTOOL_COLORS["ruby"])
        else:
            result_text = Text("⏳", style=HTOOL_COLORS["gold"])
            winner_text = Text("-", style="dim")
        
        t.add_row(issue, chosen, amount, result_text, winner_text)
    
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def build_cdtd_stats():
    data_top100 = top_100_cdtd()
    
    t = Table(title=f"[bold {HTOOL_COLORS['neon_blue']}]📊 THỐNG KÊ 100 VÁN[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["neon_blue"])
    t.add_column("NV", style=HTOOL_COLORS["gold"], width=4)
    t.add_column("Tên", style="white")
    t.add_column("Thắng", justify="right", style=HTOOL_COLORS["emerald"], width=8)
    t.add_column("Tỷ lệ", justify="right", style=HTOOL_COLORS["neon_pink"], width=8)
    
    total_wins = sum(data_top100[1]) if data_top100[1] else 1
    for i in range(6):
        wins = data_top100[1][i] if data_top100[1] else 0
        rate = (wins / total_wins * 100) if total_wins > 0 else 0
        t.add_row(f"{NV_ICONS.get(i+1, '🏆')}", NV.get(i+1, f'NV{i+1}'), str(wins), f"{rate:.1f}%")
    
    # Tổng kết tool
    summary = Table(box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["gold"])
    summary.add_column("Chỉ số", style=HTOOL_COLORS["gold"])
    summary.add_column("Giá trị", style="white")
    summary.add_row("Tổng ván", str(cdtd_stats['win'] + cdtd_stats['lose']))
    summary.add_row("Thắng", f"[green]{cdtd_stats['win']}[/]")
    summary.add_row("Thua", f"[red]{cdtd_stats['lose']}[/]")
    summary.add_row("Max thắng", str(cdtd_max_win_streak))
    summary.add_row("Max thua", str(cdtd_max_lose_streak))
    pnl = user_asset_cdtd().get(cdtd_coin, 0) - cdtd_stats['asset_0']
    summary.add_row("P&L", f"[{'green' if pnl >= 0 else 'red'}]{pnl:+.4f} {cdtd_coin}[/]")
    
    return Panel(Columns([t, summary], equal=True, expand=True), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_cdtd_marquee():
    messages = [
        f"⚡ CHẠY ĐUA TỐC ĐỘ - AUTO BET {ICONS['rocket']}",
        f"🧠 AI: {CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')} {ICONS['robot']}",
        f"💰 Coin: {cdtd_coin} | Cược gốc: {cdtd_base_bet} | Hệ số: x{cdtd_multiplier}",
        f"🎯 Thắng: {cdtd_stats['win']} | Thua: {cdtd_stats['lose']} {ICONS['chart']}",
    ]
    message = messages[int(time.time() / 5) % len(messages)]
    full_text = " " * 20 + message + " " * 20
    width = console.width or 80
    start_index = int(time.time() * 3) % len(full_text)
    display_text = (full_text * 3)[start_index : start_index + width]
    return Panel(Text(display_text, style=f"bold {HTOOL_COLORS['neon_blue']}", no_wrap=True), box=box.ROUNDED, border_style=HTOOL_COLORS["onyx"], padding=0, expand=True)

def cdtd_generate_layout():
    main_grid = Table.grid(expand=True, pad_edge=False)
    main_grid.add_column("main", ratio=55)
    main_grid.add_column("side", ratio=45)
    right_grid = Table.grid(expand=True, pad_edge=False)
    right_grid.add_row(build_cdtd_mid())
    right_grid.add_row(build_cdtd_history())
    main_grid.add_row(build_cdtd_racers(), right_grid)
    
    root_layout = Table.grid(expand=True, pad_edge=False)
    root_layout.add_row(build_cdtd_header())
    root_layout.add_row(build_cdtd_marquee())
    root_layout.add_row(main_grid)
    root_layout.add_row(build_cdtd_stats())
    return root_layout

def cdtd_prompt_settings():
    global cdtd_base_bet, cdtd_multiplier, cdtd_coin, cdtd_current_bet
    global cdtd_pause_rounds, cdtd_bet_rounds_before_skip, cdtd_settings
    
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['settings']} ", f"bold {HTOOL_COLORS['gold']}"), ("CẤU HÌNH CHẠY ĐUA TỐC ĐỘ", f"bold {HTOOL_COLORS['neon_blue']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header)
    console.print()
    
    console.print(f"[bold {HTOOL_COLORS['gold']}]💰 Chọn loại tiền:[/]")
    coin_choice = Prompt.ask("   [1] USDT  [2] BUILD  [3] WORLD", choices=['1', '2', '3'], default='2')
    cdtd_coin = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}[coin_choice]
    
    console.print(f"\n[bold {HTOOL_COLORS['gold']}]💵 Cấu hình cược:[/]")
    cdtd_base_bet = FloatPrompt.ask(f"   Cược gốc ({cdtd_coin})", default=1.0)
    cdtd_multiplier = FloatPrompt.ask("   Hệ số nhân khi thua", default=2.0)
    cdtd_current_bet = cdtd_base_bet
    
    console.print(f"\n[bold {HTOOL_COLORS['gold']}]🛡️ Bảo vệ:[/]")
    cdtd_bet_rounds_before_skip = IntPrompt.ask("   Nghỉ 1 ván sau bao nhiêu ván? (0 = không)", default=0)
    cdtd_pause_rounds = IntPrompt.ask("   Nghỉ bao nhiêu ván sau khi thua? (0 = không)", default=0)
    
    console.clear()
    console.print(header)
    console.print(f"\n[bold {HTOOL_COLORS['neon_pink']}]🧠 Chọn thuật toán AI:[/]\n")
    
    algo_table = Table(box=box.ROUNDED, border_style=HTOOL_COLORS["neon_pink"])
    algo_table.add_column("#", style=HTOOL_COLORS["gold"], width=3)
    algo_table.add_column("Thuật toán", style=HTOOL_COLORS["neon_blue"])
    algo_table.add_column("Mô tả", style="dim")
    
    algo_descriptions = {
        "RANDOM": "Chọn ngẫu nhiên",
        "AVOID_LAST": "Tránh người vừa thắng",
        "HOT_STREAK": "Theo người đang thắng nhiều",
        "COLD_STREAK": "Bắt đảo chiều",
        "BALANCE": "Cân bằng lịch sử",
        "PATTERN": "Nhận diện mẫu lặp",
        "PROBABILITY": "Xác suất thống kê",
        "FOLLOW_WINNER": "Theo người thắng nhiều nhất",
        "ANTI_WINNER": "Chống người thắng nhiều nhất",
        "SMART_ANALYSIS": "Phân tích thông minh",
    }
    
    for i, (key, label) in enumerate(CDTD_ALGORITHMS.items(), 1):
        algo_table.add_row(str(i), label, algo_descriptions.get(key, ""))
    
    console.print(algo_table)
    
    algo_choice = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]>> Chọn (1-10)[/]", choices=[str(i) for i in range(1, 11)], default=1)
    cdtd_settings["algo"] = list(CDTD_ALGORITHMS.keys())[algo_choice - 1]
    
    console.print(f'\n[green]✅ Đã chọn: {CDTD_ALGORITHMS[cdtd_settings["algo"]]}[/]')
    console.print(f'[green]✅ Cấu hình hoàn tất![/]')
    time.sleep(1.5)
    return True

def cdtd_game_loop():
    global cdtd_issue_id, cdtd_previous_issue, cdtd_last_winner
    global cdtd_predicted_nv, cdtd_ui_state, cdtd_analysis_start_ts
    global cdtd_current_bet, cdtd_win_streak, cdtd_lose_streak
    global cdtd_max_win_streak, cdtd_max_lose_streak, cdtd_stop_flag
    global cdtd_stats, cdtd_pause_remaining, cdtd_skip_next, cdtd_rounds_placed
    global cdtd_bet_placed_this_round, cdtd_checked_result
    
    # Reset biến
    cdtd_stop_flag = False
    cdtd_issue_id = None
    cdtd_previous_issue = None
    cdtd_last_winner = None
    cdtd_predicted_nv = None
    cdtd_ui_state = "WAITING"
    cdtd_analysis_start_ts = None
    cdtd_win_streak = 0
    cdtd_lose_streak = 0
    cdtd_max_win_streak = 0
    cdtd_max_lose_streak = 0
    cdtd_rounds_placed = 0
    cdtd_skip_next = False
    cdtd_pause_remaining = 0
    cdtd_bet_placed_this_round = False
    cdtd_checked_result = False
    cdtd_current_bet = cdtd_base_bet
    cdtd_bet_history.clear()
    cdtd_stats = {'win': 0, 'lose': 0, 'asset_0': 0}
    
    asset = user_asset_cdtd()
    cdtd_stats['asset_0'] = asset.get(cdtd_coin, 0)
    
    with Live(cdtd_generate_layout(), refresh_per_second=3, console=console, screen=True) as live:
        while not cdtd_stop_flag:
            try:
                data_top10 = top_10_cdtd()
                current_issue = data_top10[0][0]
                
                # ===== PHÁT HIỆN KỲ MỚI =====
                if current_issue != cdtd_previous_issue:
                    
                    # Kiểm tra kết quả kỳ trước
                    if cdtd_previous_issue is not None and cdtd_predicted_nv is not None and not cdtd_checked_result:
                        try:
                            winner = int(data_top10[1][0]) if data_top10[1] else None
                            if winner is not None:
                                cdtd_last_winner = winner
                                for b in cdtd_bet_history:
                                    if b.get('result') == 'pending':
                                        b['winner'] = winner
                                        if b['chosen'] != winner:
                                            b['result'] = 'win'
                                            cdtd_win_streak += 1
                                            cdtd_lose_streak = 0
                                            cdtd_max_win_streak = max(cdtd_max_win_streak, cdtd_win_streak)
                                            cdtd_current_bet = cdtd_base_bet
                                            cdtd_stats['win'] += 1
                                        else:
                                            b['result'] = 'lose'
                                            cdtd_lose_streak += 1
                                            cdtd_win_streak = 0
                                            cdtd_max_lose_streak = max(cdtd_max_lose_streak, cdtd_lose_streak)
                                            cdtd_current_bet *= cdtd_multiplier
                                            cdtd_stats['lose'] += 1
                                            if cdtd_pause_rounds > 0:
                                                cdtd_pause_remaining = cdtd_pause_rounds
                                cdtd_checked_result = True
                                cdtd_ui_state = "RESULT"
                                live.update(cdtd_generate_layout())
                                time.sleep(2)
                        except:
                            pass
                    
                    # Chuyển sang kỳ mới
                    cdtd_previous_issue = current_issue
                    cdtd_issue_id = current_issue
                    cdtd_predicted_nv = None
                    cdtd_bet_placed_this_round = False
                    cdtd_checked_result = False
                    cdtd_analysis_start_ts = time.time()
                    cdtd_ui_state = "ANALYZING"
                    live.update(cdtd_generate_layout())
                
                # ===== LOGIC ĐẶT CƯỢC =====
                if cdtd_ui_state == "ANALYZING":
                    elapsed = time.time() - (cdtd_analysis_start_ts or time.time())
                    
                    if elapsed >= cdtd_analysis_duration - 8 and not cdtd_bet_placed_this_round:
                        mode = cdtd_settings.get("algo", "RANDOM")
                        chosen, algo = choose_nv_cdtd(mode, data_top10, top_100_cdtd())
                        cdtd_predicted_nv = chosen
                        cdtd_ui_state = "PREDICTED"
                        live.update(cdtd_generate_layout())
                        
                        should_bet = True
                        if cdtd_pause_remaining > 0:
                            cdtd_pause_remaining -= 1
                            should_bet = False
                        if cdtd_skip_next:
                            cdtd_skip_next = False
                            should_bet = False
                        
                        if should_bet:
                            next_issue = cdtd_issue_id + 1
                            bet_amount = cdtd_current_bet if cdtd_current_bet else cdtd_base_bet
                            
                            asset = user_asset_cdtd()
                            if bet_amount > asset.get(cdtd_coin, 0):
                                cdtd_current_bet = cdtd_base_bet
                                bet_amount = cdtd_base_bet
                            
                            success, msg = bet_cdtd(next_issue, chosen, bet_amount)
                            if success:
                                cdtd_bet_history.append({
                                    'issue': next_issue, 'chosen': chosen,
                                    'amount': bet_amount, 'result': 'pending', 'algo': algo
                                })
                                cdtd_rounds_placed += 1
                                cdtd_bet_placed_this_round = True
                                if cdtd_bet_rounds_before_skip > 0 and cdtd_rounds_placed >= cdtd_bet_rounds_before_skip:
                                    cdtd_skip_next = True
                                    cdtd_rounds_placed = 0
                        
                        live.update(cdtd_generate_layout())
                    
                    elif elapsed >= cdtd_analysis_duration + 15:
                        cdtd_ui_state = "WAITING"
                        cdtd_issue_id = None
                        live.update(cdtd_generate_layout())
                
                live.update(cdtd_generate_layout())
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                cdtd_stop_flag = True
                break
            except:
                time.sleep(3)

def main_cdtd_v3():
    console.clear()
    
    header = Panel(Align.center(Text.assemble((f"{ICONS['rocket']} ", f"bold {HTOOL_COLORS['gold']}"), ("CHẠY ĐUA TỐC ĐỘ", f"bold {HTOOL_COLORS['neon_blue']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header)
    console.print(f"[dim]💬 Support: @htool88 | Version 3.0[/dim]\n")
    
    data = load_data_cdtd()
    setup_cdtd_headers(data)
    
    if not cdtd_prompt_settings():
        return
    
    console.clear()
    console.print(f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ KHỞI ĐỘNG CHẠY ĐUA TỐC ĐỘ...[/]")
    
    with console.status(f"[bold {HTOOL_COLORS['gold']}]🔍 Đang kiểm tra...[/]", spinner="dots"):
        asset = user_asset_cdtd()
        data_top10 = top_10_cdtd()
        time.sleep(1)
    
    if asset.get(cdtd_coin, 0) <= 0:
        console.print(f'[red]❌ Số dư {cdtd_coin} = 0![/]')
        time.sleep(2)
        return
    
    console.print(f'[green]✅ Kết nối thành công![/]')
    console.print(f'[green]✅ Số dư: {asset[cdtd_coin]:.4f} {cdtd_coin}[/]')
    console.print(f'[green]✅ Kỳ hiện tại: #{data_top10[0][0]}[/]')
    time.sleep(2)
    
    cdtd_game_loop()
    
    console.clear()
    final_asset = user_asset_cdtd()
    pnl = final_asset.get(cdtd_coin, 0) - cdtd_stats['asset_0']
    
    summary = Panel(Align.center(Text.assemble(
        ("\n📊 TỔNG KẾT\n\n", f"bold {HTOOL_COLORS['gold']}"),
        (f"Thắng: {cdtd_stats['win']} | Thua: {cdtd_stats['lose']}\n", "white"),
        (f"P&L: {pnl:+.4f} {cdtd_coin}\n", HTOOL_COLORS["gold"] if pnl >= 0 else HTOOL_COLORS["ruby"]),
    )), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(summary)
    console.print("\n[dim]Nhấn Enter để quay lại menu...[/]")
    input()

# ================== MAIN MENU ==================

def build_main_menu():
    console.clear()
    logo_text = build_logo_with_gradient(LOGO)
    console.print(Align.center(logo_text))
    
    console.print()
    menu_panel = Panel(Align.center(Text.assemble(
        ("\n", ""),
        (f"  {ICONS['crown']}  ", f"bold {HTOOL_COLORS['gold']}"),
        ("HTOOL VIP PREMIUM", f"bold {HTOOL_COLORS['neon_blue']}"),
        (f"  {ICONS['crown']}  ", f"bold {HTOOL_COLORS['gold']}"),
        ("\n\n", ""),
        ("  [1] 🎯 VUA THOÁT HIỂM\n", f"bold {HTOOL_COLORS['neon_green']}"),
        ("  [2] 🏎️  CHẠY ĐUA TỐC ĐỘ\n", f"bold {HTOOL_COLORS['neon_orange']}"),
        ("  [3] ➕ THÊM TÀI KHOẢN\n", f"bold {HTOOL_COLORS['sapphire']}"),
        ("  [4] 🗑️  XÓA TÀI KHOẢN\n", f"bold {HTOOL_COLORS['ruby']}"),
        ("  [5] ⚙️  LƯU CONFIG VTH\n", f"bold {HTOOL_COLORS['gold']}"),
        ("  [6] 🎮 CHƠI VTH (LOAD CONFIG)\n", f"bold {HTOOL_COLORS['neon_blue']}"),
        ("  [q] 👋 THOÁT\n", f"bold {HTOOL_COLORS['rose']}"),
        ("\n", ""),
    )), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE, padding=(1, 2))
    console.print(menu_panel)
    console.print()
    return Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Chọn[/]", choices=['1','2','3','4','5','6','q'], default='q').lower()

def main_vth():
    global _is_authenticated, _device_id, _user_key
    
    while not _is_authenticated:
        success, key, device_id = show_auth_screen()
        if success:
            _is_authenticated = True
            _user_key = key
            _device_id = device_id
            break
        else:
            retry = Prompt.ask("[bold yellow]Thử lại? (y/n)[/]", choices=['y', 'n'], default='y')
            if retry.lower() == 'n':
                console.print("[red]👋 Tạm biệt![/]")
                sys.exit(0)
    
    console.clear()
    welcome = Panel(Align.center(Text.assemble((f"{ICONS['crown']} ", f"bold {HTOOL_COLORS['gold']}"), ("WELCOME TO HTOOL VIP PREMIUM", "bold white"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(welcome)
    console.print(f"[dim]💬 Support: @htool88 | Version 3.0[/dim]")
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
            accounts = load_accounts()
            add_new_account(accounts)
        elif choice == '4':
            accounts = load_accounts()
            delete_account(accounts)
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
            console.print(Panel(Align.center(Text.assemble((f"{ICONS['crown']} ", "bold gold"), ("THANK YOU!", "bold white"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
            break

if __name__ == "__main__":
    try:
        main_vth()
    except KeyboardInterrupt:
        console.print(f"\n[bold {HTOOL_COLORS['gold']}]Đã dừng. {ICONS['crown']}[/]")
        sys.exit(0)
