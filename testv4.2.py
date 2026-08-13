# -*- coding: utf-8 -*-
from __future__ import annotations
import subprocess
import sys
import importlib
import os
import threading
import logging
import json
import time
import random
import math
import re
import hashlib
import hmac
import base64
import socket
import ipaddress
import platform
import uuid
from collections import defaultdict, deque, Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Tuple, Optional, List
from urllib.parse import urlparse, parse_qs

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
    print("\n" + "=" * 60)
    print("❌ KHÔNG THỂ CÀI ĐẶT ĐẦY ĐỦ THƯ VIỆN")
    print("💡 VUI LÒNG CÀI ĐẶT THỦ CÔNG:")
    print("   pip install pytz requests websocket-client rich")
    print("=" * 60)
    sys.exit(1)

# ================== IMPORT THƯ VIỆN ==================

import pytz
import requests
import websocket
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.rule import Rule
from rich.text import Text
from rich import box
from rich.columns import Columns

# ================== CẤU HÌNH ==================

console = Console()
tz = pytz.timezone("Asia/Ho_Chi_Minh")

# ================== SUPABASE CONFIG ==================
SUPABASE_URL = "https://ebviepssggyyrdeedpnz.supabase.co"
SUPABASE_KEY = "sb_publishable_B3VF2kG0260fFrOtWBJi1g_ylklAm1_"

# ================== TELEGRAM CONFIG ==================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = ""
TELEGRAM_ENABLED = False

# ================== GIAO DIỆN HTOOL ==================

HTOOL_COLORS = {
    "gold": "#FFD700",
    "gold_dark": "#B8860B",
    "platinum": "#E5E4E2",
    "diamond": "#B9F2FF",
    "ruby": "#E0115F",
    "emerald": "#50C878",
    "sapphire": "#0F52BA",
    "amethyst": "#9966CC",
    "onyx": "#353839",
    "rose": "#FF007F",
    "neon_blue": "#00D4FF",
    "neon_pink": "#FF00E5",
    "neon_green": "#39FF14",
    "neon_orange": "#FF5E00",
    "crimson": "#DC143C",
    "turquoise": "#40E0D0",
    "lavender": "#E6E6FA",
}

ICONS = {
    "crown": "👑",
    "diamond": "💎",
    "star": "⭐",
    "fire": "🔥",
    "lightning": "⚡",
    "target": "🎯",
    "shield": "🛡️",
    "sword": "⚔️",
    "brain": "🧠",
    "robot": "🤖",
    "rocket": "🚀",
    "trophy": "🏆",
    "medal": "🏅",
    "gem": "💠",
    "sparkle": "✨",
    "settings": "⚙️",
    "user": "👤",
    "key": "🔑",
    "lock": "🔒",
    "unlock": "🔓",
    "check": "✅",
    "cross": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "money": "💰",
    "chart": "📊",
    "clock": "⏰",
    "link": "🔗",
    "wifi": "📶",
    "globe": "🌐",
    "plus": "➕",
    "minus": "➖",
    "arrow": "➡️",
    "heart": "❤️",
    "bell": "🔔",
    "gift": "🎁",
    "magic": "🔮",
    "phone": "📞",
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
_ws_status = "⏳ Đang kết nối..."
_is_authenticated = False
_user_key = None
_key_type = "free"
_heartbeat_running = False
_heartbeat_thread = None
_in_menu = False
_ip_info = {}
AI_PERFORMANCE = defaultdict(lambda: {"wins": 0, "losses": 0, "total": 0})
_secure_mode = False
_secure_tool = None

# ================== HỆ THỐNG CHỐNG SOI ==================

class IPRotator:
    """Quản lý xoay IP tự động để tránh bị phát hiện"""
    
    def __init__(self):
        self.proxy_list = []
        self.current_proxy = None
        self.last_rotation = time.time()
        self.rotation_interval = 300
        self.max_requests_per_ip = 50
        self.used_ips = []
        self.ip_history = deque(maxlen=100)
        self.request_count = 0
        self.load_proxy_list()
    
    def load_proxy_list(self):
        try:
            if os.path.exists('proxy_list.txt'):
                with open('proxy_list.txt', 'r') as f:
                    proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    self.proxy_list.extend(proxies)
            
            if not self.proxy_list:
                self.proxy_list = [None]
            
            safe_console_print(f"[green]✅ Đã tải {len(self.proxy_list)} proxy[/green]")
        except Exception as e:
            safe_console_print(f"[yellow]⚠️ Lỗi tải proxy: {e}[/yellow]")
            self.proxy_list = [None]
    
    def get_proxy(self) -> Optional[dict]:
        if self.should_rotate():
            self.rotate_ip()
        
        if self.current_proxy:
            return {"http": self.current_proxy, "https": self.current_proxy}
        return None
    
    def rotate_ip(self):
        available_proxies = [p for p in self.proxy_list if p not in self.used_ips]
        
        if available_proxies:
            self.current_proxy = random.choice(available_proxies)
            self.used_ips.append(self.current_proxy)
        else:
            self.used_ips = []
            self.current_proxy = random.choice(self.proxy_list)
        
        self.last_rotation = time.time()
        self.request_count = 0
        
        ip_display = self.current_proxy if self.current_proxy else "IP thật"
        safe_console_print(f"[dim]🔄 Đã xoay IP: {ip_display}[/dim]")
        
        self.ip_history.append({
            "ip": ip_display,
            "time": datetime.now().isoformat()
        })
    
    def should_rotate(self) -> bool:
        if time.time() - self.last_rotation > self.rotation_interval:
            return True
        if self.request_count >= self.max_requests_per_ip:
            return True
        return False
    
    def increment_request(self):
        self.request_count += 1
    
    def get_random_user_agent(self) -> str:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        ]
        return random.choice(user_agents)

class RequestRandomizer:
    def __init__(self):
        self.min_delay = 0.5
        self.max_delay = 3.0
        self.last_request_time = 0
    
    def get_random_delay(self) -> float:
        delay = random.uniform(self.min_delay, self.max_delay)
        if random.random() < 0.3:
            delay *= random.uniform(0.5, 1.5)
        return delay
    
    def wait_before_request(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_delay:
            wait_time = self.get_random_delay() - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def get_random_headers(self) -> dict:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
        ]
        
        accept_languages = ['vi-VN,vi;q=0.9,en;q=0.8', 'en-US,en;q=0.9', 'vi;q=0.9,en;q=0.8']
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': random.choice(accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }

class AntiDetectionSystem:
    def __init__(self):
        self.ip_rotator = IPRotator()
        self.request_randomizer = RequestRandomizer()
        self.is_stealth_mode = False
        self.detection_risk = 0
        self.last_check = time.time()
        self.request_history = []
        self.stealth_session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    
    def enable_stealth_mode(self):
        self.is_stealth_mode = True
        safe_console_print("[bold green]🛡️ Đã bật chế độ tàng hình![/bold green]")
        self.ip_rotator.rotate_ip()
        self.stealth_session_id = hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:8]
    
    def make_stealth_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        self.request_randomizer.wait_before_request()
        proxy = self.ip_rotator.get_proxy()
        headers = self.request_randomizer.get_random_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        if proxy:
            kwargs['proxies'] = proxy
        if 'timeout' not in kwargs:
            kwargs['timeout'] = random.uniform(8, 15)
        
        try:
            response = requests.request(method, url, **kwargs)
            self.ip_rotator.increment_request()
            self.request_history.append({
                'url': url,
                'time': time.time(),
                'status': response.status_code,
                'ip': self.ip_rotator.current_proxy
            })
            self.check_detection_risk()
            return response
        except Exception as e:
            safe_console_print(f"[yellow]⚠️ Request error: {e}[/yellow]")
            return None
    
    def check_detection_risk(self):
        recent_requests = [r for r in self.request_history 
                          if time.time() - r['time'] < 60]
        
        if len(recent_requests) > 30:
            self.detection_risk += 10
        elif len(recent_requests) > 20:
            self.detection_risk += 5
        elif len(recent_requests) > 10:
            self.detection_risk += 2
        
        if self.detection_risk > 70:
            safe_console_print(f"[red]⚠️ Phát hiện rủi ro cao ({self.detection_risk}%)[/red]")
            self.ip_rotator.rotate_ip()
            self.detection_risk = 0
    
    def get_status(self) -> dict:
        return {
            'stealth_mode': self.is_stealth_mode,
            'detection_risk': self.detection_risk,
            'current_ip': self.ip_rotator.current_proxy,
            'request_count': len(self.request_history),
            'ip_history': list(self.ip_rotator.ip_history),
            'session_id': self.stealth_session_id,
        }
    
    def display_status(self):
        status = self.get_status()
        safe_console_print("\n" + "="*50)
        safe_console_print("🛡️ ANTI-DETECTION STATUS")
        safe_console_print("="*50)
        safe_console_print(f"🔒 Stealth Mode: {'✅ BẬT' if status['stealth_mode'] else '❌ TẮT'}")
        safe_console_print(f"🌐 Current IP: {status['current_ip'] or 'IP thật'}")
        safe_console_print(f"⚠️ Detection Risk: {status['detection_risk']}%")
        safe_console_print(f"📊 Total Requests: {status['request_count']}")
        safe_console_print(f"🔑 Session ID: {status['session_id']}")
        safe_console_print("="*50)

class SecureHTOOL:
    def __init__(self):
        self.anti_detection = AntiDetectionSystem()
        self.is_stealth = False
    
    def start_stealth_mode(self):
        safe_console_print("\n[bold]🛡️ KHỞI ĐỘNG CHẾ ĐỘ CHỐNG SOI[/bold]")
        safe_console_print("="*50)
        self.anti_detection.enable_stealth_mode()
        self.is_stealth = True
        self.anti_detection.display_status()
        safe_console_print("\n[green]✅ Đã sẵn sàng chống soi![/green]")
        time.sleep(2)
    
    def make_secure_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        if self.is_stealth:
            return self.anti_detection.make_stealth_request(url, **kwargs)
        else:
            return requests.request('GET', url, **kwargs)
    
    def secure_post(self, url: str, **kwargs) -> Optional[requests.Response]:
        if self.is_stealth:
            return self.anti_detection.make_stealth_request(url, method='POST', **kwargs)
        else:
            return requests.post(url, **kwargs)
    
    def get_status(self) -> dict:
        if self.is_stealth:
            return self.anti_detection.get_status()
        return {'stealth_mode': False}
    
    def display_status(self):
        if self.is_stealth:
            self.anti_detection.display_status()

# ================== SCAN IP ==================

def get_public_ip() -> Optional[str]:
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    try:
        response = requests.get('https://ip-api.com/json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('query')
    except:
        pass
    return None

def get_local_ip() -> Optional[str]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def get_device_fingerprint() -> str:
    try:
        info = []
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            info.append(mac)
        except:
            pass
        try:
            info.append(socket.gethostname())
        except:
            pass
        info.append(platform.platform())
        info.append(platform.processor())
        info.append(platform.machine())
        fingerprint_str = ''.join(info)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
    except:
        return hashlib.md5(str(time.time()).encode()).hexdigest()[:16]

def scan_ip_ban_list() -> bool:
    try:
        ip = get_public_ip()
        if not ip:
            return False
        
        blacklist_file = "ip_blacklist.txt"
        if not os.path.exists(blacklist_file):
            with open(blacklist_file, 'w', encoding='utf-8') as f:
                f.write("# Blacklisted IPs\n")
            return False
        
        with open(blacklist_file, 'r', encoding='utf-8') as f:
            blacklist = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if ip in blacklist:
            safe_console_print(f"[red]❌ IP {ip} đã bị cấm![/red]")
            return True
        return False
    except:
        return False

def check_ip_whitelist() -> bool:
    try:
        ip = get_public_ip()
        if not ip:
            return False
        
        whitelist_file = "ip_whitelist.txt"
        if not os.path.exists(whitelist_file):
            return True
        
        with open(whitelist_file, 'r', encoding='utf-8') as f:
            whitelist = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not whitelist:
            return True
        
        if ip in whitelist:
            return True
        
        for entry in whitelist:
            if '/' in entry:
                try:
                    network = ipaddress.ip_network(entry, strict=False)
                    if ipaddress.ip_address(ip) in network:
                        return True
                except:
                    pass
        
        safe_console_print(f"[red]❌ IP {ip} không có trong whitelist![/red]")
        return False
    except:
        return True

class IPScanner:
    def __init__(self):
        self.public_ip = None
        self.local_ip = None
        self.device_fingerprint = None
        self.location_info = None
        self._scanned = False
    
    def scan(self) -> bool:
        try:
            self.public_ip = get_public_ip()
            self.local_ip = get_local_ip()
            self.device_fingerprint = get_device_fingerprint()
            
            if self.public_ip:
                try:
                    response = requests.get(f'http://ip-api.com/json/{self.public_ip}', timeout=5)
                    if response.status_code == 200:
                        self.location_info = response.json()
                except:
                    pass
            
            self._scanned = True
            
            if scan_ip_ban_list():
                return False
            
            if not check_ip_whitelist():
                return False
            
            self.log_scan_info()
            return True
        except Exception as e:
            safe_console_print(f"[yellow]⚠️ Lỗi scan IP: {e}[/yellow]")
            return False
    
    def log_scan_info(self):
        log_data = {
            "timestamp": datetime.now(tz).isoformat(),
            "public_ip": self.public_ip,
            "local_ip": self.local_ip,
            "fingerprint": self.device_fingerprint,
            "location": self.location_info,
        }
        
        try:
            with open("ip_scan_log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
        except:
            pass
        
        safe_console_print("[dim]📡 SCAN IP:[/dim]")
        if self.public_ip:
            safe_console_print(f"  🌐 Public IP: [bold]{self.public_ip}[/bold]")
        if self.local_ip:
            safe_console_print(f"  🏠 Local IP: [bold]{self.local_ip}[/bold]")
        if self.location_info:
            city = self.location_info.get('city', 'N/A')
            country = self.location_info.get('country', 'N/A')
            safe_console_print(f"  📍 Location: [bold]{city}, {country}[/bold]")
        safe_console_print(f"  🔑 Fingerprint: [dim]{self.device_fingerprint}[/dim]")
        safe_console_print("")
    
    def get_status(self) -> dict:
        return {
            "scanned": self._scanned,
            "public_ip": self.public_ip,
            "local_ip": self.local_ip,
            "fingerprint": self.device_fingerprint,
            "location": self.location_info,
        }
    
    def is_ip_safe(self) -> bool:
        if not self._scanned:
            self.scan()
        if scan_ip_ban_list():
            return False
        if not check_ip_whitelist():
            return False
        return True

def enhanced_auth_check():
    global _ip_info
    ip_scanner = IPScanner()
    if not ip_scanner.scan():
        safe_console_print("[red]❌ Scan IP thất bại! Tool sẽ không chạy.[/red]")
        return False
    if not ip_scanner.is_ip_safe():
        safe_console_print("[red]❌ IP không an toàn! Tool sẽ không chạy.[/red]")
        return False
    _ip_info = ip_scanner.get_status()
    return True

# ================== CHỐNG DEBUG ==================

def detect_debugger() -> bool:
    try:
        if sys.gettrace() is not None:
            return True
        if 'PYCHARM_HOSTED' in os.environ:
            return True
        return False
    except:
        return False

def anti_crack_check() -> bool:
    if detect_debugger():
        console.print("[red]❌ Phát hiện debugger! Tool sẽ không chạy.[/red]")
        return False
    return True

# ================== HÀM XÁC THỰC KEY ==================

def verify_key_with_device(key: str) -> dict:
    if detect_debugger():
        return {"valid": False, "error": "Phát hiện debugger! Không thể xác thực."}
    
    url = f"{SUPABASE_URL}/rest/v1/keys?key_code=eq.{key}"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "HTOOL-Secure/3.0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return {"valid": False, "error": f"HTTP {response.status_code}"}
        
        data = response.json()
        
        if not data:
            return {"valid": False, "error": "Key không tồn tại"}
        
        keyData = data[0]
        
        if keyData.get('status') != 'active':
            return {"valid": False, "error": "Key đã bị vô hiệu hóa"}
        
        if keyData.get('expires_at'):
            try:
                from datetime import datetime
                expiry = datetime.fromisoformat(keyData['expires_at'].replace('Z', '+00:00'))
                if datetime.now().astimezone() > expiry:
                    return {"valid": False, "error": "Key đã hết hạn"}
            except:
                pass
        
        used_count = keyData.get('used_count', 0)
        max_uses = keyData.get('max_uses')
        if max_uses and used_count >= max_uses:
            return {"valid": False, "error": "Key đã đạt giới hạn sử dụng"}
        
        new_count = used_count + 1
        update_url = f"{SUPABASE_URL}/rest/v1/keys?key_code=eq.{key}"
        update_data = {"used_count": new_count}
        
        requests.patch(update_url, json=update_data, headers=headers, timeout=10)
        
        return {
            "valid": True,
            "data": {
                "key": key,
                "key_type": keyData.get('key_type', 'free'),
                "max_ai": keyData.get('max_ai', 10),
                "expires_at": keyData.get('expires_at', 'forever'),
                "note": keyData.get('note', ''),
                "used_count": new_count,
                "max_uses": keyData.get('max_uses')
            }
        }
        
    except Exception as e:
        return {"valid": False, "error": f"Lỗi: {str(e)}"}

def parse_datetime_safe(date_str):
    if not date_str or date_str == 'forever':
        return None
    try:
        if 'Z' in date_str or '+' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.astimezone(timezone.utc)
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None

# ================== HEARTBEAT ==================

def heartbeat_worker():
    global _is_authenticated, _user_key, _heartbeat_running
    
    while _heartbeat_running:
        time.sleep(30)
        
        if _user_key and _is_authenticated:
            result = verify_key_with_device(_user_key)
            if not result.get("valid"):
                _is_authenticated = False
                safe_console_print("[bold red]🔒 KEY ĐÃ BỊ KHÓA HOẶC HẾT HẠN![/bold red]")
                safe_console_print("[bold red]Tool sẽ tự động thoát sau 5 giây...[/bold red]")
                time.sleep(5)
                os._exit(0)

def start_heartbeat():
    global _heartbeat_thread, _heartbeat_running
    _heartbeat_running = True
    _heartbeat_thread = threading.Thread(target=heartbeat_worker, daemon=True)
    _heartbeat_thread.start()

def stop_heartbeat():
    global _heartbeat_running
    _heartbeat_running = False

# ================== MÀN HÌNH XÁC THỰC ==================

def show_auth_screen():
    global _key_type, _secure_mode
    
    if not anti_crack_check():
        return False, None, "free"
    
    if not enhanced_auth_check():
        console.print("[red]❌ Xác thực IP thất bại![/red]")
        time.sleep(2)
        return False, None, "free"
    
    console.clear()
    gold_color = HTOOL_COLORS["gold"]
    logo_lines = LOGO.split('\n')
    for line in logo_lines:
        if line.strip():
            console.print(Align.center(line, style=f"bold {gold_color}"))
    
    console.print()
    console.print(Align.center("═" * 50, style="dim"))
    console.print(Align.center(f"[bold {gold_color}]XÁC THỰC KEY[/bold {gold_color}]", style=f"bold {gold_color}"))
    console.print(Align.center("═" * 50, style="dim"))
    console.print()
    
    console.print(Panel(
        Text.assemble(
            ("🔑 KEY FREE: ", "bold white"),
            ("Sử dụng 12 AI cơ bản\n", "dim"),
            ("👑 KEY VIP: ", "bold gold"),
            ("Sử dụng toàn bộ 42 AI\n", "bold gold"),
            ("\n", ""),
            ("🔒 Anti-Crack Active", "bold green"),
            ("\n", ""),
            ("🌐 IP Security Active", "bold green"),
            ("\n", ""),
            ("🛡️ Anti-Detection Active", "bold green"),
        ),
        title="[bold]THÔNG TIN KEY[/bold]",
        border_style=HTOOL_COLORS["gold"],
        box=box.ROUNDED
    ))
    console.print()
    
    console.print(f"[bold cyan]🔑 Nhập Key:[/bold cyan]")
    console.print("[dim]   (Key có dạng: HTOOL_XXXXX hoặc FREE_XXXXX)[/dim]")
    key = Prompt.ask("   >>", default="")
    
    if not key:
        console.print("[red]❌ Key không được để trống![/red]")
        time.sleep(1.5)
        return False, None, "free"
    
    console.print()
    console.print("[bold]🛡️ BẬT CHẾ ĐỘ CHỐNG SOI?[/bold]")
    console.print("[dim]  - Giúp tránh bị phát hiện khi dùng tool[/dim]")
    console.print("[dim]  - Tự động xoay IP và fake headers[/dim]")
    console.print("[dim]  - Giảm nguy cơ bị ban[/dim]")
    stealth_choice = Prompt.ask("[bold cyan]>> Bật chế độ chống soi? (y/n)[/bold cyan]", 
                                 choices=['y', 'n'], default='y')
    
    if stealth_choice == 'y':
        _secure_mode = True
    else:
        _secure_mode = False
        console.print("[dim]⚠️ Chế độ chống soi đã tắt[/dim]")
    
    console.print()
    with console.status(f"[bold yellow]⏳ Đang xác thực...[/bold yellow]", spinner="dots") as status:
        time.sleep(0.5)
        result = verify_key_with_device(key)
    
    if result.get("valid"):
        console.print()
        data = result.get("data", {})
        key_type = data.get("key_type", "free")
        max_ai = data.get("max_ai", 10)
        
        expiry_info = ""
        expires_at = data.get('expires_at')
        if expires_at and expires_at != 'forever':
            try:
                expiry_dt = parse_datetime_safe(expires_at)
                if expiry_dt:
                    now_utc = datetime.now(timezone.utc)
                    time_left = expiry_dt - now_utc
                    days = time_left.days
                    hours = time_left.seconds // 3600
                    minutes = (time_left.seconds % 3600) // 60
                    if days > 0:
                        expiry_info = f"Còn {days} ngày {hours} giờ"
                    elif hours > 0:
                        expiry_info = f"Còn {hours} giờ {minutes} phút"
                    else:
                        expiry_info = f"Còn {minutes} phút"
            except:
                expiry_info = expires_at
        
        key_icon = "👑" if key_type == "vip" else "🔑"
        key_color = "bold gold" if key_type == "vip" else "bold white"
        
        if _secure_mode:
            global _secure_tool
            _secure_tool = SecureHTOOL()
            _secure_tool.start_stealth_mode()
        
        console.print(Panel(
            Text.assemble(
                ("✅ ", "bold green"),
                ("Xác thực thành công!\n", "bold green"),
                (f"Key: ", "white"),
                (f"{key}\n", f"bold {gold_color}"),
                (f"Loại: ", "white"),
                (f"{key_icon} {key_type.upper()}\n", key_color),
                (f"AI: ", "white"),
                (f"{max_ai}/42 AI\n", "bold cyan"),
                (f"Trạng thái: ", "white"),
                (f"Hoạt động\n", "bold green"),
                (f"Hạn: ", "white"),
                (f"{expiry_info}\n", "yellow"),
                (f"Ghi chú: ", "white"),
                (f"{data.get('note', 'N/A')}\n", "dim"),
                (f"Lượt sử dụng: ", "white"),
                (f"{data.get('used_count', 0)}/{data.get('max_uses', '∞')}", "dim"),
                ("\n", ""),
                ("🔒 Anti-Crack: Đã kích hoạt", "bold green"),
                ("\n", ""),
                (f"🌐 IP: {_ip_info.get('public_ip', 'N/A')}", "dim"),
                ("\n", ""),
                (f"🛡️ Anti-Detection: {'✅ BẬT' if _secure_mode else '❌ TẮT'}", "bold green" if _secure_mode else "dim"),
            ),
            title=f"[bold green]✅ XÁC THỰC THÀNH CÔNG[/bold green]",
            border_style="green",
            box=box.HEAVY
        ))
        
        console.print()
        console.print("[dim]Nhấn Enter để tiếp tục...[/dim]")
        input()
        
        return True, key, key_type
    else:
        console.print()
        console.print(Panel(
            Text.assemble(
                ("❌ ", "bold red"),
                ("Xác thực thất bại!\n", "bold red"),
                (f"Lỗi: ", "white"),
                (f"{result.get('error', 'Không xác định')}\n", "red"),
                ("\nVui lòng kiểm tra lại Key.", "dim")
            ),
            title=f"[bold red]❌ XÁC THỰC THẤT BẠI[/bold red]",
            border_style="red",
            box=box.HEAVY
        ))
        console.print()
        console.print("[dim]Nhấn Enter để thử lại...[/dim]")
        input()
        return False, None, "free"

def require_valid_auth() -> bool:
    global _is_authenticated
    return _is_authenticated

def safe_console_print(*args, **kwargs):
    try:
        console.print(*args, **kwargs)
    except:
        pass

def safe_console_status(message, spinner="dots"):
    return console.status(message, spinner=spinner)

# ================== TELEGRAM ==================

def send_telegram_message(message: str) -> bool:
    if not TELEGRAM_ENABLED or not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
        
        if _secure_tool and _secure_tool.is_stealth:
            response = _secure_tool.make_secure_request(url, method='POST', json=payload, timeout=10)
            return response.status_code == 200 if response else False
        else:
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
    test_msg = f"✅ <b>KẾT NỐI THÀNH CÔNG!</b>\n\n🔔 <b>HTOOL PREMIUM - Thông báo đã kích hoạt</b>\n🕐 <b>{datetime.now(tz).strftime('%H:%M:%S %d/%m/%Y')}</b>"
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

# ================== CÁC HÀM AI ==================

def choose_random() -> int:
    return random.choice(ROOM_ORDER)

def choose_min_player_bet() -> int:
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

def choose_probability() -> int:
    scores = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        scores[r] = survival_rate
    return max(scores, key=scores.get)

def choose_follow_killer() -> int:
    if last_killed_room is not None and last_killed_room in ROOM_ORDER:
        return last_killed_room
    return random.choice(ROOM_ORDER)

def choose_sequential() -> int:
    global _sequential_bet_index
    room_to_bet = ROOM_ORDER[_sequential_bet_index]
    _sequential_bet_index = (_sequential_bet_index + 1) % len(ROOM_ORDER)
    return room_to_bet

def choose_killer_personality_enhanced() -> int:
    if len(killer_history) < 3:
        return choose_random()
    
    recent_killers = killer_history[-15:] if len(killer_history) > 15 else killer_history
    avg_players = sum(h['players'] for h in recent_killers) / len(recent_killers)
    avg_bet = sum(h['bet'] for h in recent_killers) / len(recent_killers)
    player_var = sum((h['players'] - avg_players) ** 2 for h in recent_killers) / len(recent_killers)
    bet_var = sum((h['bet'] - avg_bet) ** 2 for h in recent_killers) / len(recent_killers)
    stability_factor = 1.5 if player_var < 2 and bet_var < 100 else 0.8
    
    avoidance_scores = {}
    for r in ROOM_ORDER:
        if r == last_killed_room:
            avoidance_scores[r] = -999999
            continue
        
        current_players = room_state[r]['players']
        current_bet = room_state[r]['bet']
        player_dist = abs(current_players - avg_players) / (avg_players + 1)
        bet_dist = abs(current_bet - avg_bet) / (avg_bet + 1)
        base_score = (player_dist + bet_dist) * stability_factor
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        base_score += survival_rate * 0.3
        avoidance_scores[r] = base_score
    
    return max(avoidance_scores, key=avoidance_scores.get)

def choose_smart_safe_enhanced() -> int:
    scores = {}
    max_players = max(rs['players'] for rs in room_state.values()) or 1
    max_bet = max(rs['bet'] for rs in room_state.values()) or 1
    recent_kills = list(game_kill_log)[-10:] if game_kill_log else []
    
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        player_score = 1 - (room_state[r]['players'] / max_players)
        bet_score = 1 - (room_state[r]['bet'] / max_bet)
        
        cycle_score = 0
        if recent_kills:
            if r in recent_kills:
                last_kill_idx = len(recent_kills) - 1 - max([i for i, x in enumerate(recent_kills) if x == r], default=-1)
                cycle_score = min(0.3, last_kill_idx * 0.05)
            else:
                cycle_score = -0.2
        
        killer_score = 0
        if killer_history:
            avg_players_killed = sum(h['players'] for h in killer_history) / len(killer_history)
            avg_bet_killed = sum(h['bet'] for h in killer_history) / len(killer_history)
            player_diff = abs(room_state[r]['players'] - avg_players_killed) / (avg_players_killed + 1)
            bet_diff = abs(room_state[r]['bet'] - avg_bet_killed) / (avg_bet_killed + 1)
            killer_score = (player_diff + bet_diff) * 0.15
        
        kill_penalty = 0.5 if r == last_killed_room else 0
        final_score = (0.30 * survival_rate + 0.20 * player_score + 0.15 * bet_score + 0.20 * cycle_score + 0.15 * killer_score - kill_penalty)
        final_score += random.uniform(-0.05, 0.05)
        scores[r] = final_score
    
    return max(scores, key=scores.get)

def choose_follow_killer_delayed() -> int:
    global last_killed_room_delayed
    if last_killed_room_delayed is not None and last_killed_room_delayed in ROOM_ORDER:
        return last_killed_room_delayed
    return random.choice(ROOM_ORDER)

def choose_hide_seek_master() -> int:
    danger_scores = {}
    max_players = max(rs['players'] for rs in room_state.values()) or 1
    max_bet = max(rs['bet'] for rs in room_state.values()) or 1
    avg_players_killed = 0
    avg_bet_killed = 0
    if killer_history:
        avg_players_killed = sum(h['players'] for h in killer_history) / len(killer_history)
        avg_bet_killed = sum(h['bet'] for h in killer_history) / len(killer_history)
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        hist_danger = (kills + 1) / (kills + survives + 2)
        crowd_danger = room_state[r]['players'] / max_players
        money_danger = room_state[r]['bet'] / max_bet
        personality_danger = 0
        if killer_history:
            player_sim = 1 - (abs(room_state[r]['players'] - avg_players_killed) / (avg_players_killed + max_players + 1))
            bet_sim = 1 - (abs(room_state[r]['bet'] - avg_bet_killed) / (avg_bet_killed + max_bet + 1))
            personality_danger = (player_sim + bet_sim) / 2
        recency_penalty = 1.0 if r == last_killed_room else 0.0
        total_danger = (0.3 * hist_danger) + (0.2 * crowd_danger) + (0.2 * money_danger) + (0.3 * personality_danger) + recency_penalty
        danger_scores[r] = total_danger
    return min(danger_scores, key=danger_scores.get)

def choose_balance() -> int:
    scores = {}
    total_players = sum(rs['players'] for rs in room_state.values())
    total_bet = sum(rs['bet'] for rs in room_state.values())
    avg_players = total_players / len(ROOM_ORDER) if total_players > 0 else 0
    avg_bet = total_bet / len(ROOM_ORDER) if total_bet > 0 else 0
    for r in ROOM_ORDER:
        players = room_state[r]['players']
        bet = room_state[r]['bet']
        score = abs(players - avg_players) / (avg_players + 1) + abs(bet - avg_bet) / (avg_bet + 1)
        scores[r] = score
    return min(scores, key=scores.get)

def choose_most_players() -> int:
    return max(ROOM_ORDER, key=lambda r: room_state[r]['players'])

def choose_least_players() -> int:
    return min(ROOM_ORDER, key=lambda r: room_state[r]['players'])

def choose_richest() -> int:
    return max(ROOM_ORDER, key=lambda r: room_state[r]['bet'])

def choose_poorest() -> int:
    return min(ROOM_ORDER, key=lambda r: room_state[r]['bet'])

def choose_alternate() -> int:
    if len(bet_history) < 2:
        return random.choice(ROOM_ORDER)
    last_rooms = [b.get('room') for b in list(bet_history)[-3:] if b.get('room')]
    candidates = [r for r in ROOM_ORDER if r not in last_rooms]
    if candidates:
        return random.choice(candidates)
    return random.choice(ROOM_ORDER)

def choose_avoid_result() -> int:
    if last_killed_room is None:
        return random.choice(ROOM_ORDER)
    candidates = [r for r in ROOM_ORDER if r != last_killed_room]
    if not candidates:
        return random.choice(ROOM_ORDER)
    return random.choice(candidates)

def choose_cold() -> int:
    player_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['players'])
    bet_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['bet'])
    scores = defaultdict(int)
    for i, r in enumerate(reversed(player_ranks)):
        scores[r] += i
    for i, r in enumerate(reversed(bet_ranks)):
        scores[r] += i
    return min(scores, key=scores.get)

def choose_hot() -> int:
    player_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['players'])
    bet_ranks = sorted(ROOM_ORDER, key=lambda r: room_state[r]['bet'])
    scores = defaultdict(int)
    for i, r in enumerate(player_ranks):
        scores[r] += i
    for i, r in enumerate(bet_ranks):
        scores[r] += i
    return max(scores, key=scores.get)

def choose_median() -> int:
    if not any(rs['players'] > 0 for rs in room_state.values()):
        return random.choice(ROOM_ORDER)
    players_list = sorted(ROOM_ORDER, key=lambda r: room_state[r]['players'])
    bet_list = sorted(ROOM_ORDER, key=lambda r: room_state[r]['bet'])
    median_players = players_list[len(players_list) // 2]
    median_bet = bet_list[len(bet_list) // 2]
    if median_players == median_bet:
        return median_players
    scores = {}
    for r in ROOM_ORDER:
        dist_players = abs(room_state[r]['players'] - room_state[median_players]['players'])
        dist_bet = abs(room_state[r]['bet'] - room_state[median_bet]['bet'])
        scores[r] = dist_players + dist_bet
    return min(scores, key=scores.get)

def choose_pattern() -> int:
    if len(game_kill_log) < 3:
        return random.choice(ROOM_ORDER)
    last_3 = list(game_kill_log)[-3:]
    if len(last_3) == 3 and last_3[0] == last_3[2]:
        return last_3[1]
    return random.choice(ROOM_ORDER)

def choose_cycle_analysis() -> int:
    if len(game_kill_log) < 6:
        return choose_random()
    
    history = list(game_kill_log)
    best_cycle = None
    best_score = -1
    
    for cycle_len in range(2, 11):
        if len(history) >= cycle_len * 2:
            matches = 0
            total = len(history) - cycle_len
            for i in range(total):
                if history[i] == history[i + cycle_len]:
                    matches += 1
            score = matches / max(1, total)
            if score > best_score:
                best_score = score
                best_cycle = cycle_len
    
    if best_cycle and best_score > 0.6:
        last_cycle_start = len(history) - best_cycle
        if last_cycle_start >= 0:
            predicted = history[last_cycle_start]
            if predicted in ROOM_ORDER:
                if predicted == last_killed_room:
                    alternatives = [r for r in ROOM_ORDER if r != predicted]
                    if alternatives:
                        return random.choice(alternatives)
                return predicted
    
    return choose_smart_safe_enhanced()

def choose_trend_analysis() -> int:
    if len(killer_history) < 5:
        return choose_random()
    
    player_trends = []
    bet_trends = []
    for h in killer_history[-10:]:
        player_trends.append(h['players'])
        bet_trends.append(h['bet'])
    
    if len(player_trends) >= 3:
        player_slope = (player_trends[-1] - player_trends[0]) / max(1, len(player_trends))
        bet_slope = (bet_trends[-1] - bet_trends[0]) / max(1, len(bet_trends))
        next_players = player_trends[-1] + player_slope * 1.5
        next_bet = bet_trends[-1] + bet_slope * 1.5
        
        scores = {}
        for r in ROOM_ORDER:
            if r == last_killed_room:
                scores[r] = -999999
                continue
            players = room_state[r]['players']
            bet = room_state[r]['bet']
            player_dist = abs(players - next_players) / (next_players + 1)
            bet_dist = abs(bet - next_bet) / (next_bet + 1)
            scores[r] = player_dist + bet_dist
        
        return max(scores, key=scores.get)
    
    return choose_random()

def choose_vip_random() -> int:
    logic_list = [
        choose_random, choose_min_player_bet, choose_probability,
        choose_follow_killer, choose_sequential, choose_killer_personality_enhanced,
        choose_smart_safe_enhanced, choose_follow_killer_delayed, choose_hide_seek_master,
        choose_balance, choose_most_players, choose_least_players,
        choose_richest, choose_poorest, choose_alternate,
        choose_avoid_result, choose_cold, choose_hot, choose_median, choose_pattern,
        choose_cycle_analysis, choose_trend_analysis
    ]
    sys_random = random.SystemRandom()
    chosen_func = sys_random.choice(logic_list)
    return chosen_func()

def choose_killer_wave() -> int:
    if len(game_kill_log) < 4:
        return choose_random()
    last_4 = list(game_kill_log)[-4:]
    for i in range(1, 4):
        if len(last_4) >= i*2 and last_4[-i:] == last_4[-i*2:-i]:
            predicted = last_4[-i-1] if len(last_4) > i else last_4[-1]
            return predicted
    return choose_smart_safe_enhanced()

def choose_psycho_analysis() -> int:
    max_players_room = max(ROOM_ORDER, key=lambda r: room_state[r]['players'])
    max_bet_room = max(ROOM_ORDER, key=lambda r: room_state[r]['bet'])
    crowd_favorite = max_players_room if room_state[max_players_room]['players'] > room_state[max_bet_room]['players'] else max_bet_room
    candidates = [r for r in ROOM_ORDER if r != crowd_favorite]
    if candidates:
        return min(candidates, key=lambda r: room_state[r]['players'] + room_state[r]['bet'] * 0.01)
    return choose_random()

def choose_markov_chain() -> int:
    if len(game_kill_log) < 5:
        return choose_random()
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(game_kill_log) - 1):
        current = game_kill_log[i]
        next_room = game_kill_log[i + 1]
        transitions[current][next_room] += 1
    last = game_kill_log[-1]
    if transitions[last]:
        predicted = max(transitions[last].items(), key=lambda x: x[1])[0]
        return predicted
    return choose_smart_safe_enhanced()

def choose_deep_learning_enhanced() -> int:
    if len(killer_history) < 5:
        return choose_random()
    
    weights = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        
        recent_boost = 0
        if r in game_kill_log:
            recent_count = list(game_kill_log).count(r)
            recent_boost = -0.3 * min(1, recent_count / 3)
        
        trend_boost = 0
        if len(game_kill_log) >= 5:
            last_5 = list(game_kill_log)[-5:]
            if r in last_5:
                recent_appear = last_5.count(r)
                trend_boost = -0.2 * recent_appear
            else:
                trend_boost = 0.1
        
        max_players = max(rs['players'] for rs in room_state.values()) or 1
        max_bet = max(rs['bet'] for rs in room_state.values()) or 1
        crowd_boost = 1 - (room_state[r]['players'] / max_players)
        money_boost = 1 - (room_state[r]['bet'] / max_bet)
        
        killer_pattern_boost = 0
        if len(game_kill_log) >= 3:
            last_3 = list(game_kill_log)[-3:]
            if len(last_3) == 3 and last_3[0] == last_3[2] and last_3[0] == r:
                killer_pattern_boost = -0.4
        
        weights[r] = (0.25 * survival_rate + 0.20 * recent_boost + 0.15 * trend_boost + 0.15 * crowd_boost + 0.10 * money_boost + 0.15 * killer_pattern_boost)
        weights[r] += random.uniform(-0.08, 0.08)
    
    return max(weights, key=weights.get)

def choose_reinforcement() -> int:
    if len(bet_history) < 3:
        return choose_random()
    action_scores = {r: 0 for r in ROOM_ORDER}
    for b in list(bet_history)[-10:]:
        room = b.get('room')
        result = b.get('result')
        if room in ROOM_ORDER and result:
            if result == "Thắng":
                action_scores[room] += 1
            else:
                action_scores[room] -= 0.5
    max_score = max(action_scores.values())
    if max_score <= 0:
        return choose_random()
    best_rooms = [r for r, s in action_scores.items() if s == max_score]
    return random.choice(best_rooms)

def choose_bayesian() -> int:
    if len(game_kill_log) < 3:
        return choose_random()
    room_counts = Counter(game_kill_log)
    total_kills = len(game_kill_log)
    prior = {r: 1/len(ROOM_ORDER) for r in ROOM_ORDER}
    likelihood = {}
    for r in ROOM_ORDER:
        count = room_counts.get(r, 0)
        likelihood[r] = (count + 1) / (total_kills + len(ROOM_ORDER))
    posterior = {}
    for r in ROOM_ORDER:
        posterior[r] = prior[r] * likelihood[r]
    total = sum(posterior.values())
    for r in ROOM_ORDER:
        posterior[r] /= total
    return min(posterior, key=posterior.get)

def choose_k_means() -> int:
    if len(game_kill_log) < 6:
        return choose_random()
    from collections import defaultdict
    room_features = defaultdict(lambda: [0, 0])
    for i, room in enumerate(list(game_kill_log)[-10:]):
        room_features[room][0] += 1
        room_features[room][1] = i
    cluster_1 = set()
    cluster_2 = set()
    for room, features in room_features.items():
        if features[0] < 2:
            cluster_1.add(room)
        else:
            cluster_2.add(room)
    if cluster_1:
        return random.choice(list(cluster_1))
    return choose_random()

def choose_neural() -> int:
    if len(killer_history) < 3:
        return choose_random()
    scores = {}
    for r in ROOM_ORDER:
        players = room_state[r]['players']
        bet = room_state[r]['bet']
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        layer1 = (0.3 * survives) - (0.5 * kills) + (0.2 * players) - (0.3 * bet)
        layer2 = (0.4 * layer1) + (0.2 * (survives - kills))
        layer3 = (0.5 * layer2) + (0.3 * (1 - players/max(1, max(rs['players'] for rs in room_state.values()))))
        output = 1 / (1 + math.exp(-layer3))
        scores[r] = output
    return max(scores, key=scores.get)

def choose_fuzzy() -> int:
    if len(killer_history) < 2:
        return choose_random()
    scores = {}
    for r in ROOM_ORDER:
        players = room_state[r]['players']
        bet = room_state[r]['bet']
        players_young = max(0, 1 - players/2) if players < 2 else 0
        players_mid = max(0, 1 - abs(players-3)/2) if 1 < players < 5 else 0
        players_old = max(0, (players-4)/2) if players > 4 else 0
        bet_low = max(0, 1 - bet/100) if bet < 100 else 0
        bet_mid = max(0, 1 - abs(bet-300)/200) if 100 < bet < 500 else 0
        bet_high = max(0, (bet-400)/200) if bet > 400 else 0
        rule1 = min(players_young, bet_low)
        rule2 = min(players_old, bet_high)
        rule3 = min(players_mid, bet_mid)
        safety_score = (rule1 * 1.0 + rule2 * 0.0 + rule3 * 0.5) / (rule1 + rule2 + rule3 + 0.01)
        scores[r] = safety_score
    return max(scores, key=scores.get)

def choose_genetic() -> int:
    if len(killer_history) < 5:
        return choose_random()
    population = list(game_kill_log)[-10:]
    if not population:
        return choose_random()
    fitness = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        fitness[r] = (survives + 1) / (kills + survives + 2)
    return max(fitness, key=fitness.get)

def choose_ant_colony() -> int:
    if len(game_kill_log) < 3:
        return choose_random()
    pheromone = {}
    for r in ROOM_ORDER:
        count = list(game_kill_log).count(r)
        pheromone[r] = count / len(game_kill_log) if game_kill_log else 0
    return min(pheromone, key=pheromone.get)

def choose_particle_swarm() -> int:
    if len(killer_history) < 3:
        return choose_random()
    scores = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        recent_trend = 0.3 if r in list(game_kill_log)[-3:] else 0
        scores[r] = survival_rate + recent_trend
    return max(scores, key=scores.get)

def choose_knn() -> int:
    if len(game_kill_log) < 3:
        return choose_random()
    k = min(3, len(game_kill_log))
    nearest = list(game_kill_log)[-k:]
    counts = Counter(nearest)
    min_count = min(counts.values())
    candidates = [r for r, c in counts.items() if c == min_count]
    if candidates:
        return random.choice(candidates)
    return choose_random()

def choose_decision_tree() -> int:
    if len(killer_history) < 5:
        return choose_random()
    if last_killed_room:
        if room_state[last_killed_room]['players'] > 5:
            candidates = [r for r in ROOM_ORDER if r != last_killed_room]
            if candidates:
                return random.choice(candidates)
        elif room_state[last_killed_room]['bet'] > 1000:
            candidates = [r for r in ROOM_ORDER if r != last_killed_room]
            if candidates:
                return random.choice(candidates)
        return choose_probability()
    return choose_random()

def choose_random_forest() -> int:
    if len(killer_history) < 3:
        return choose_random()
    predictions = []
    for _ in range(5):
        if random.random() > 0.5:
            predictions.append(choose_probability())
        else:
            predictions.append(choose_min_player_bet())
    counts = Counter(predictions)
    return max(counts, key=counts.get)

def choose_gradient_boost() -> int:
    if len(killer_history) < 3:
        return choose_random()
    scores = {}
    for r in ROOM_ORDER:
        base_score = 0.5
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        survival_rate = (survives + 1) / (kills + survives + 2)
        base_score += 0.3 * survival_rate
        base_score -= 0.1 * (room_state[r]['players'] / max(1, max(rs['players'] for rs in room_state.values())))
        base_score -= 0.1 * (room_state[r]['bet'] / max(1, max(rs['bet'] for rs in room_state.values())))
        scores[r] = base_score
    return max(scores, key=scores.get)

def choose_lstm() -> int:
    if len(game_kill_log) < 4:
        return choose_random()
    last_5 = list(game_kill_log)[-5:]
    if len(last_5) == 5 and last_5[0] == last_5[3] and last_5[1] == last_5[4]:
        return last_5[2]
    return choose_markov_chain()

def choose_transformer() -> int:
    if len(game_kill_log) < 4:
        return choose_random()
    attention_scores = {}
    for r in ROOM_ORDER:
        kills = room_stats[r].get('kills', 0)
        survives = room_stats[r].get('survives', 0)
        recency = 1 - (list(game_kill_log).count(r) / max(1, len(game_kill_log)))
        attention_scores[r] = (0.4 * recency) + (0.3 * (survives / max(1, kills + survives))) + (0.3 * (1 - room_state[r]['players'] / max(1, max(rs['players'] for rs in room_state.values()))))
    return max(attention_scores, key=attention_scores.get)

def choose_ensemble_enhanced() -> int:
    if len(killer_history) < 3:
        return choose_random()
    
    ai_weights = {
        'choose_smart_safe_enhanced': 1.0,
        'choose_killer_personality_enhanced': 0.9,
        'choose_deep_learning_enhanced': 0.85,
        'choose_probability': 0.7,
        'choose_hide_seek_master': 0.6,
        'choose_balance': 0.5,
        'choose_cycle_analysis': 0.8,
        'choose_trend_analysis': 0.7,
    }
    
    votes = defaultdict(float)
    for ai_name, weight in ai_weights.items():
        try:
            func = globals().get(ai_name)
            if func:
                room = func()
                votes[room] += weight
        except:
            continue
    
    if len(game_kill_log) >= 4:
        last = game_kill_log[-1]
        transitions = defaultdict(lambda: defaultdict(int))
        for i in range(len(game_kill_log) - 1):
            transitions[game_kill_log[i]][game_kill_log[i + 1]] += 1
        if last in transitions and transitions[last]:
            predicted = max(transitions[last].items(), key=lambda x: x[1])[0]
            votes[predicted] += 0.7
    
    if not votes:
        return choose_random()
    return max(votes, key=votes.get)

# ================== ENHANCED LOGIC MAP ==================

ENHANCED_LOGIC_MAP = {
    "RANDOM": choose_random,
    "MIN_PLAYER_BET": choose_min_player_bet,
    "PROBABILITY": choose_probability,
    "FOLLOW_KILLER": choose_follow_killer,
    "SEQUENTIAL": choose_sequential,
    "KILLER_PERSONALITY": choose_killer_personality_enhanced,
    "SMART_SAFE": choose_smart_safe_enhanced,
    "FOLLOW_KILLER_DELAYED": choose_follow_killer_delayed,
    "HIDE_SEEK_MASTER": choose_hide_seek_master,
    "BALANCE": choose_balance,
    "MOST_PLAYERS": choose_most_players,
    "LEAST_PLAYERS": choose_least_players,
    "RICHEST": choose_richest,
    "POOREST": choose_poorest,
    "ALTERNATE": choose_alternate,
    "AVOID_RESULT": choose_avoid_result,
    "COLD": choose_cold,
    "HOT": choose_hot,
    "MEDIAN": choose_median,
    "PATTERN": choose_pattern,
    "VIP_RANDOM": choose_vip_random,
    "KILLER_WAVE": choose_killer_wave,
    "PSYCHO_ANALYSIS": choose_psycho_analysis,
    "MARKOV_CHAIN": choose_markov_chain,
    "DEEP_LEARNING": choose_deep_learning_enhanced,
    "REINFORCEMENT": choose_reinforcement,
    "BAYESIAN": choose_bayesian,
    "K_MEANS": choose_k_means,
    "NEURAL": choose_neural,
    "FUZZY": choose_fuzzy,
    "GENETIC": choose_genetic,
    "ANT_COLONY": choose_ant_colony,
    "PARTICLE_SWARM": choose_particle_swarm,
    "KNN": choose_knn,
    "DECISION_TREE": choose_decision_tree,
    "RANDOM_FOREST": choose_random_forest,
    "GRADIENT_BOOST": choose_gradient_boost,
    "LSTM": choose_lstm,
    "TRANSFORMER": choose_transformer,
    "ENSEMBLE": choose_ensemble_enhanced,
    "CYCLE_ANALYSIS": choose_cycle_analysis,
    "TREND_ANALYSIS": choose_trend_analysis,
}

# ================== HÀM CHỌN PHÒNG ==================

def choose_room_tn(mode: str) -> Tuple[int, str]:
    global _key_type
    mode = mode.upper()
    if not is_ai_available(mode, _key_type):
        safe_console_print(f"[yellow]⚠️ AI {mode} không khả dụng với key {_key_type}. Chuyển sang RANDOM.[/yellow]")
        mode = "RANDOM"
    func = ENHANCED_LOGIC_MAP.get(mode, choose_random)
    chosen_room = func()
    return chosen_room, mode

# ================== THEO DÕI HIỆU SUẤT AI ==================

def update_ai_performance(algo_name: str, is_win: bool):
    if is_win:
        AI_PERFORMANCE[algo_name]["wins"] += 1
    else:
        AI_PERFORMANCE[algo_name]["losses"] += 1
    AI_PERFORMANCE[algo_name]["total"] += 1
    try:
        with open('ai_performance.json', 'w', encoding='utf-8') as f:
            json.dump(dict(AI_PERFORMANCE), f, indent=2)
    except:
        pass

def get_best_ai() -> str:
    best_ai = "RANDOM"
    best_rate = 0
    for ai_name, stats in AI_PERFORMANCE.items():
        if stats["total"] >= 5:
            rate = stats["wins"] / stats["total"]
            if rate > best_rate:
                best_rate = rate
                best_ai = ai_name
    return best_ai

# ================== SMART MARTINGALE ==================

def calculate_smart_bet(base_bet: float, multiplier: float, lose_streak: int, current_balance: float, max_bet_percent: float = 0.2) -> float:
    bet = base_bet * (multiplier ** lose_streak)
    max_allowed = current_balance * max_bet_percent
    if bet > max_allowed:
        safe_console_print(f"[yellow]⚠️ Cược {bet:.2f} vượt quá {max_bet_percent*100}% số dư. Reset về {base_bet:.2f}.[/yellow]")
        bet = base_bet
    if lose_streak > 5:
        bet = min(bet, current_balance * 0.05)
    return round(bet, 2)

# ================== BIẾN TOÀN CỤC GAME ==================

ROOM_NAMES = {1: "📦 Nhà kho", 2: "🪑 Phòng họp", 3: "👔 Phòng giám đốc", 4: "💬 Phòng trò chuyện", 5: "🎥 Phòng giám sát", 6: "🏢 Văn phòng", 7: "💰 Phòng tài vụ", 8: "👥 Phòng nhân sự"}
ROOM_ORDER = [1, 2, 3, 4, 5, 6, 7, 8]

USER_ID: Optional[int] = None
SECRET_KEY: Optional[str] = None
issue_id: Optional[int] = None
issue_start_ts: Optional[float] = None
issue_end_ts: Optional[float] = None
count_down: Optional[int] = None
killed_room: Optional[int] = None
round_index: int = 0

room_state: Dict[int, Dict[str, Any]] = {r: {"players": 0, "bet": 0} for r in ROOM_ORDER}
room_stats: Dict[int, Dict[str, Any]] = {r: {"kills": 0, "survives": 0, "last_kill_round": None, "last_players": 0, "last_bet": 0} for r in ROOM_ORDER}

predicted_room: Optional[int] = None
last_killed_room: Optional[int] = None
last_killed_room_delayed: Optional[int] = None
prediction_locked: bool = False

current_build: Optional[float] = None
current_usdt: Optional[float] = None
current_world: Optional[float] = None
last_balance_ts: Optional[float] = None
last_balance_val: Optional[float] = None
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
bet_sent_for_issue: set = set()

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
last_balance_fetch_ts: float = 0.0
BALANCE_POLL_INTERVAL: float = 4.0
_ws: Dict[str, Any] = {"ws": None}

_sequential_bet_index = 0
killer_history = deque(maxlen=20)
game_kill_log = deque(maxlen=10)

# ================== AI LIST ==================

FREE_AI_LIST = [
    "RANDOM", "MIN_PLAYER_BET", "PROBABILITY", "FOLLOW_KILLER", 
    "SEQUENTIAL", "KILLER_PERSONALITY", "SMART_SAFE", 
    "FOLLOW_KILLER_DELAYED", "HIDE_SEEK_MASTER", "BALANCE",
    "CYCLE_ANALYSIS", "TREND_ANALYSIS"
]

VIP_AI_LIST = [
    "MOST_PLAYERS", "LEAST_PLAYERS", "RICHEST", "POOREST",
    "ALTERNATE", "AVOID_RESULT", "COLD", "HOT", "MEDIAN", "PATTERN",
    "VIP_RANDOM", "KILLER_WAVE", "PSYCHO_ANALYSIS", "MARKOV_CHAIN",
    "DEEP_LEARNING", "REINFORCEMENT", "BAYESIAN", "K_MEANS",
    "NEURAL", "FUZZY", "GENETIC", "ANT_COLONY", "PARTICLE_SWARM",
    "KNN", "DECISION_TREE", "RANDOM_FOREST", "GRADIENT_BOOST",
    "LSTM", "TRANSFORMER", "ENSEMBLE"
]

SELECTION_MODES = {
    "RANDOM": "1. PHẬT ĐỘ (Random)",
    "MIN_PLAYER_BET": "2. AN TOÀN (Min Players & Bet)",
    "PROBABILITY": "3. XÁC SUẤT (Probability)",
    "FOLLOW_KILLER": "4. THEO SÁT THỦ (Follow Killer)",
    "SEQUENTIAL": "5. TUẦN TỰ (1→2→3→...→8)",
    "KILLER_PERSONALITY": "6. TÍNH CÁCH SÁT THỦ (AI Enhanced)",
    "SMART_SAFE": "7. THÔNG MINH (AI Smart Enhanced)",
    "FOLLOW_KILLER_DELAYED": "8. THEO VẾT SÁT THỦ (Delay 1 ván)",
    "HIDE_SEEK_MASTER": "9. THÁNH TRỐN TÌM (Master AI)",
    "BALANCE": "10. CÂN BẰNG (Balance)",
    "MOST_PLAYERS": "11. ĐÔNG NHẤT (Most Players)",
    "LEAST_PLAYERS": "12. ÍT NHẤT (Least Players)",
    "RICHEST": "13. GIÀU NHẤT (Richest)",
    "POOREST": "14. NGHÈO NHẤT (Poorest)",
    "ALTERNATE": "15. XEN KẼ (Alternate)",
    "AVOID_RESULT": "16. TRÁNH KẾT QUẢ (Avoid Result)",
    "COLD": "17. PHÒNG LẠNH (Cold Room)",
    "HOT": "18. PHÒNG NÓNG (Hot Room)",
    "MEDIAN": "19. TRUNG VỊ (Median)",
    "PATTERN": "20. MẪU LẶP (Pattern)",
    "VIP_RANDOM": "21. VIP RANDOM (Random 22 logic)",
    "KILLER_WAVE": "22. BẮT SÓNG SÁT THỦ",
    "PSYCHO_ANALYSIS": "23. PHÂN TÍCH TÂM LÝ",
    "MARKOV_CHAIN": "24. CHUỖI MARKOV",
    "DEEP_LEARNING": "25. HỌC SÂU (Enhanced)",
    "REINFORCEMENT": "26. HỌC TĂNG CƯỜNG",
    "BAYESIAN": "27. XÁC SUẤT BAYES",
    "K_MEANS": "28. PHÂN CỤM K-MEANS",
    "NEURAL": "29. MẠNG NƠ-RON",
    "FUZZY": "30. LOGIC MỜ",
    "GENETIC": "31. THUẬT TOÁN DI TRUYỀN",
    "ANT_COLONY": "32. KIẾN BÒ",
    "PARTICLE_SWARM": "33. BẦY ĐÀN",
    "KNN": "34. K-NEAREST NEIGHBORS",
    "DECISION_TREE": "35. CÂY QUYẾT ĐỊNH",
    "RANDOM_FOREST": "36. RỪNG NGẪU NHIÊN",
    "GRADIENT_BOOST": "37. TĂNG CƯỜNG GRADIENT",
    "LSTM": "38. LSTM",
    "TRANSFORMER": "39. TRANSFORMER",
    "ENSEMBLE": "40. TỔNG HỢP (Enhanced)",
    "CYCLE_ANALYSIS": "41. PHÂN TÍCH CHU KỲ (Mới)",
    "TREND_ANALYSIS": "42. PHÂN TÍCH XU HƯỚNG (Mới)",
}

settings = {"algo": "ENSEMBLE"}
STRATEGY_CONFIG_FILE = "strategy_htool.json"

def get_available_ai_list(key_type: str = "free") -> List[str]:
    if key_type == "vip":
        return FREE_AI_LIST + VIP_AI_LIST
    else:
        return FREE_AI_LIST

def is_ai_available(ai_key: str, key_type: str = "free") -> bool:
    available = get_available_ai_list(key_type)
    return ai_key in available

# ================== HÀM HỖ TRỢ ==================

def _parse_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x)
    _num_re = re.compile(r"-?\d+[\d,]*\.?\d*")
    m = _num_re.search(s)
    if not m:
        return None
    token = m.group(0).replace(",", "")
    try:
        return float(token)
    except Exception:
        return None

def human_ts() -> str:
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def balance_headers_for(uid: Optional[int] = None, secret: Optional[str] = None) -> Dict[str, str]:
    h = {"accept": "*/*", "accept-language": "vi,en;q=0.9", "cache-control": "no-cache", "country-code": "vn", "origin": "https://xworld.info", "pragma": "no-cache", "referer": "https://xworld.info/", "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36", "user-login": "login_v2", "xb-language": "vi-VN"}
    if uid is not None:
        h["user-id"] = str(uid)
    if secret:
        h["user-secret-key"] = str(secret)
    return h

def fetch_balances_3games(retries=3, timeout=8, params=None, uid=None, secret=None):
    global current_build, current_usdt, current_world, last_balance_ts, starting_balance, last_balance_val, cumulative_profit
    uid = uid or USER_ID
    secret = secret or SECRET_KEY
    WALLET_API_URL = "https://wallet.3games.io/api/wallet/user_asset"
    payload = {"user_id": int(uid) if uid is not None else None, "source": "home"}
    attempt = 0
    while attempt <= retries:
        attempt += 1
        try:
            HTTP = requests.Session()
            r = HTTP.post(WALLET_API_URL, json=payload, headers=balance_headers_for(uid, secret), timeout=timeout)
            r.raise_for_status()
            j = r.json()
            data = j.get("data", {}) if isinstance(j, dict) else {}
            ua = data.get("user_asset", {}) if isinstance(data, dict) else {}
            build = _parse_number(ua.get("BUILD"))
            world = _parse_number(ua.get("WORLD"))
            usdt = _parse_number(ua.get("USDT"))
            if build is not None:
                if last_balance_val is None:
                    starting_balance = build
                    last_balance_val = build
                else:
                    last_balance_val = build
                current_build = build
                if starting_balance is not None:
                    cumulative_profit = current_build - starting_balance
            if usdt is not None:
                current_usdt = usdt
            if world is not None:
                current_world = world
            last_balance_ts = time.time()
            return current_build, current_world, current_usdt
        except Exception as e:
            time.sleep(min(1.5 * attempt, 4))
    return current_build, current_world, current_usdt

def api_headers() -> Dict[str, str]:
    return {"content-type": "application/json", "user-agent": "Mozilla/5.0", "user-id": str(USER_ID) if USER_ID else "", "user-secret-key": SECRET_KEY if SECRET_KEY else ""}

def place_bet_http(issue: int, room_id: int, amount: float) -> dict:
    BET_API_URL = "https://api.escapemaster.net/escape_game/bet"
    payload = {"asset_type": "BUILD", "user_id": USER_ID, "room_id": int(room_id), "bet_amount": float(amount)}
    try:
        if _secure_tool and _secure_tool.is_stealth:
            response = _secure_tool.make_secure_request(BET_API_URL, method='POST', json=payload, timeout=8)
            if response:
                try:
                    return response.json()
                except:
                    return {"raw": response.text, "http_status": response.status_code}
            return {"error": "Request failed"}
        else:
            r = requests.post(BET_API_URL, headers=api_headers(), json=payload, timeout=8)
            try:
                return r.json()
            except Exception:
                return {"raw": r.text, "http_status": r.status_code}
    except Exception as e:
        return {"error": str(e)}

def record_bet(issue: int, room_id: int, amount: float, resp: dict, algo_used: Optional[str] = None) -> dict:
    now = datetime.now(tz).strftime("%H:%M:%S")
    rec = {"issue": issue, "room": room_id, "amount": float(amount), "time": now, "resp": resp, "result": "Đang", "algo": algo_used, "delta": 0.0, "win_streak": win_streak, "lose_streak": lose_streak}
    bet_history.append(rec)
    return rec

def place_bet_async(issue: int, room_id: int, amount: float, algo_used: Optional[str] = None):
    def worker():
        safe_console_print(f"[cyan]Đang đặt {amount} BUILD -> PHÒNG_{room_id} (v{issue}) — Thuật toán: {algo_used}[/]")
        time.sleep(random.uniform(0.05, 0.45))
        res = place_bet_http(issue, room_id, amount)
        rec = record_bet(issue, room_id, amount, res, algo_used=algo_used)
        if isinstance(res, dict) and (res.get("msg") == "ok" or res.get("code") == 0 or res.get("status") in ("ok", 1)):
            bet_sent_for_issue.add(issue)
            safe_console_print(f"[green]✅ Đặt thành công {amount} BUILD vào PHÒNG_{room_id} (v{issue}).[/]")
        else:
            safe_console_print(f"[red]❌ Đặt lỗi v{issue}: {res}[/]")
    threading.Thread(target=worker, daemon=True).start()

def lock_prediction_if_needed(force: bool = False):
    global prediction_locked, predicted_room, ui_state, current_bet, _rounds_placed_since_skip, skip_next_round_flag, _skip_rounds_remaining, stop_flag
    
    if stop_flag:
        return
    if prediction_locked and not force:
        return
    if issue_id is None:
        return
    
    mode = settings.get("algo", "ENSEMBLE")
    chosen, algo_used = choose_room_tn(mode)
    predicted_room = chosen
    prediction_locked = True
    ui_state = "PREDICTED"
    
    if _skip_rounds_remaining > 0:
        safe_console_print(f"[yellow]⏸️ Đang nghỉ {_skip_rounds_remaining} ván theo cấu hình sau khi thua.[/]")
        _skip_rounds_remaining -= 1
        return
    if skip_next_round_flag:
        safe_console_print("[yellow]⏸️ TẠM DỪNG THEO DÕI SÁT THỦ[/]")
        skip_next_round_flag = False
        return
    if run_mode == "AUTO":
        bld = current_build
        if bld is None:
            bld, _, _ = fetch_balances_3games(retries=1, timeout=3)
            if bld is None:
                safe_console_print("[yellow]⚠️ Không lấy được số dư, không thể đặt cược. Sẽ thử lại...[/]")
                prediction_locked = False
                ui_state = "ANALYZING"
                return
        if current_bet is None:
            current_bet = base_bet
        amt = float(current_bet)
        if amt <= 0:
            safe_console_print("[yellow]⚠️ Số tiền đặt không hợp lệ (<=0). Bỏ qua.[/]")
            return
        if amt > bld:
            safe_console_print(f"[red]🔥 VỐN KHÔNG ĐỦ ĐỂ GẤP THẾP! Cần {amt:,.2f} nhưng chỉ có {bld:,.2f}. Reset về cược gốc.[/red]")
            current_bet = base_bet
            amt = float(current_bet)
            if amt > bld:
                safe_console_print(f"[red]💀 Vốn không đủ để đặt cược gốc ({amt:,.2f}). Dừng tool.[/red]")
                stop_flag = True
                return
        place_bet_async(issue_id, predicted_room, amt, algo_used=algo_used)
        _rounds_placed_since_skip += 1
        if bet_rounds_before_skip > 0 and _rounds_placed_since_skip >= bet_rounds_before_skip:
            skip_next_round_flag = True
            _rounds_placed_since_skip = 0

def enhanced_result_processing(killed_room: int, issue_id: int):
    global win_streak, lose_streak, max_win_streak, max_lose_streak, current_bet
    
    rec = None
    for b in reversed(bet_history):
        if b.get("issue") == issue_id:
            rec = b
            break
    
    if rec is None:
        return
    
    placed_room = int(rec.get("room"))
    
    if placed_room != killed_room:
        rec["result"] = "Thắng"
        win_streak += 1
        lose_streak = 0
        max_win_streak = max(max_win_streak, win_streak)
        
        if win_streak >= 3:
            current_bet = base_bet * (1 + min(win_streak * 0.05, 0.3))
        else:
            current_bet = base_bet
        
        algo_used = rec.get('algo')
        if algo_used:
            update_ai_performance(algo_used, True)
        
    else:
        rec["result"] = "Thua"
        lose_streak += 1
        win_streak = 0
        max_lose_streak = max(max_lose_streak, lose_streak)
        
        current_balance = current_build or 0
        current_bet = calculate_smart_bet(
            base_bet, 
            multiplier, 
            lose_streak,
            current_balance
        )
        
        algo_used = rec.get('algo')
        if algo_used:
            update_ai_performance(algo_used, False)
    
    rec["win_streak"] = win_streak
    rec["lose_streak"] = lose_streak

# ================== WEBSOCKET ==================

def safe_send_enter_game(ws):
    if not ws:
        return
    try:
        payload = {"msg_type": "handle_enter_game", "asset_type": "BUILD", "user_id": USER_ID, "user_secret_key": SECRET_KEY}
        ws.send(json.dumps(payload))
    except Exception:
        pass

def _extract_issue_id(d: Dict[str, Any]) -> Optional[int]:
    if not isinstance(d, dict):
        return None
    possible = []
    for key in ("issue_id", "issueId", "issue", "id"):
        v = d.get(key)
        if v is not None:
            possible.append(v)
    if isinstance(d.get("data"), dict):
        for key in ("issue_id", "issueId", "issue", "id"):
            v = d["data"].get(key)
            if v is not None:
                possible.append(v)
    for p in possible:
        try:
            return int(p)
        except Exception:
            try:
                return int(str(p))
            except Exception:
                continue
    return None

def on_open(ws):
    _ws["ws"] = ws
    global _ws_status
    _ws_status = "✅ Đã kết nối"
    safe_send_enter_game(ws)

def on_message(ws, message):
    global issue_id, count_down, killed_room, round_index, ui_state, analysis_start_ts, issue_start_ts, issue_end_ts
    global prediction_locked, predicted_room, last_killed_room, last_killed_room_delayed, last_msg_ts, current_bet
    global win_streak, lose_streak, max_win_streak, max_lose_streak, cumulative_profit, _skip_rounds_remaining, stop_flag
    
    last_msg_ts = time.time()
    try:
        if isinstance(message, bytes):
            try:
                message = message.decode("utf-8", errors="replace")
            except Exception:
                message = str(message)
        data = None
        try:
            data = json.loads(message)
        except Exception:
            try:
                data = json.loads(message.replace("'", '"'))
            except Exception:
                return
        if isinstance(data, dict) and isinstance(data.get("data"), str):
            try:
                inner = json.loads(data.get("data"))
                merged = dict(data)
                merged.update(inner)
                data = merged
            except Exception:
                pass
        msg_type = data.get("msg_type") or data.get("type") or ""
        msg_type = str(msg_type)
        new_issue = _extract_issue_id(data)
        if msg_type == "notify_enter_game":
            info = data.get("info", {})
            if isinstance(info, dict):
                if info.get("start_time"):
                    st = float(info.get("start_time"))
                    if st > time.time() * 500: st /= 1000.0
                    issue_start_ts = st
                if info.get("end_time"):
                    et = float(info.get("end_time"))
                    if et > time.time() * 500: et /= 1000.0
                    issue_end_ts = et
            if data.get("last_killed_room_id"):
                last_killed_room = int(data["last_killed_room_id"])
            room_stat = data.get("room_stat", [])
            if isinstance(room_stat, list):
                for rm in room_stat:
                    _process_room_update(rm)
        if msg_type == "notify_issue_stat" or "issue_stat" in msg_type:
            rooms = data.get("rooms") or []
            if not rooms and isinstance(data.get("data"), dict):
                rooms = data["data"].get("rooms", [])
            for rm in (rooms or []):
                _process_room_update(rm)
                try:
                    rid = int(rm.get("room_id") or rm.get("roomId") or rm.get("id"))
                except Exception:
                    continue
                players = int(rm.get("user_cnt") or rm.get("userCount") or 0) or 0
                bet = int(rm.get("total_bet_amount") or rm.get("totalBet") or rm.get("bet") or 0) or 0
                room_state[rid] = {"players": players, "bet": bet}
                room_stats[rid]["last_players"] = players
                room_stats[rid]["last_bet"] = bet
            if new_issue is not None and new_issue != issue_id:
                issue_id = new_issue
                if data.get("start_time"):
                    st = float(data.get("start_time"))
                    if st > time.time() * 500: st /= 1000.0
                    issue_start_ts = st
                else:
                    issue_start_ts = time.time()
                issue_end_ts = issue_start_ts + 60.0
                round_index += 1
                killed_room = None
                prediction_locked = False
                predicted_room = None
                ui_state = "ANALYZING"
                analysis_start_ts = time.time()
        elif msg_type == "notify_count_down" or "count_down" in msg_type:
            count_down = data.get("count_down") or data.get("countDown") or data.get("count") or count_down
            try:
                count_val = int(count_down)
            except Exception:
                count_val = None
            if count_val is not None and count_val <= 10 and not prediction_locked:
                lock_prediction_if_needed()
        elif msg_type == "notify_result" or "result" in msg_type:
            kr = None
            possible_keys = ["killed_room", "killed_room_id", "killedRoom", "killedRoomId", "kill_room"]
            for key in possible_keys:
                if data.get(key) is not None:
                    kr = data.get(key)
                    break
            if kr is None and isinstance(data.get("data"), dict):
                for key in possible_keys:
                    if data["data"].get(key) is not None:
                        kr = data["data"].get(key)
                        break
            if kr is not None:
                try:
                    krid = int(kr)
                except Exception:
                    krid = kr
                killed_room = krid
                game_kill_log.append(krid)
                update_killer_history(krid)
                last_killed_room = krid
                if last_killed_room_delayed is None:
                    last_killed_room_delayed = krid
                else:
                    last_killed_room_delayed = krid
                for rid in ROOM_ORDER:
                    if rid == krid:
                        room_stats[rid]["kills"] += 1
                        room_stats[rid]["last_kill_round"] = round_index
                    else:
                        room_stats[rid]["survives"] += 1
                balance_before_payout = current_build
                rec = None
                for b in reversed(bet_history):
                    if b.get("issue") == issue_id:
                        rec = b
                        break
                if rec is not None:
                    try:
                        placed_room = int(rec.get("room"))
                        if placed_room != int(killed_room):
                            rec["result"] = "Thắng"
                            current_bet = base_bet
                            win_streak += 1
                            lose_streak = 0
                            if win_streak > max_win_streak:
                                max_win_streak = win_streak
                        else:
                            rec["result"] = "Thua"
                            try:
                                if current_bet is not None:
                                    current_bet = calculate_smart_bet(base_bet, multiplier, lose_streak, current_build or 0)
                            except Exception:
                                current_bet = base_bet
                            lose_streak += 1
                            win_streak = 0
                            if lose_streak > max_lose_streak:
                                max_lose_streak = lose_streak
                            if pause_after_losses > 0:
                                _skip_rounds_remaining = pause_after_losses
                        threading.Thread(target=_background_update_balance_after_result, args=(rec, balance_before_payout), daemon=True).start()
                        rec["win_streak"] = win_streak
                        rec["lose_streak"] = lose_streak
                    except Exception:
                        pass
            ui_state = "RESULT"
            try:
                if stop_when_profit_reached and profit_target is not None and isinstance(current_build, (int, float)) and current_build >= profit_target and not stop_flag:
                    safe_console_print(f"[bold green]🎉 MỤC TIÊU LÃI ĐẠT: {current_build} >= {profit_target}. Dừng tool.[/]")
                    stop_flag = True
                    try:
                        wsobj = _ws.get("ws")
                        if wsobj:
                            wsobj.close()
                    except Exception:
                        pass
                if stop_when_loss_reached and stop_loss_target is not None and isinstance(current_build, (int, float)) and current_build <= stop_loss_target and not stop_flag:
                    safe_console_print(f"[bold red]💀 CẮT LỖ: {current_build:,.2f} <= {stop_loss_target:,.2f}. Dừng tool.[/]")
                    stop_flag = True
                    try:
                        wsobj = _ws.get("ws")
                        if wsobj:
                            wsobj.close()
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        pass

def _background_update_balance_after_result(rec: dict, balance_before: Optional[float]):
    global cumulative_profit
    try:
        time.sleep(2.5)
        new_balance, _, _ = fetch_balances_3games(retries=2, timeout=5)
        if rec and isinstance(new_balance, (int, float)):
            if isinstance(balance_before, (int, float)):
                delta = new_balance - balance_before
                rec['delta'] = delta
            else:
                if rec.get('result') == 'Thắng':
                    rec['delta'] = float(rec.get('amount', 0)) * 7
                elif rec.get('result') == 'Thua':
                    rec['delta'] = -float(rec.get('amount', 0))
    except Exception:
        pass

def update_killer_history(killed_room_id):
    if killed_room_id in room_state:
        killer_history.append({'players': room_state[killed_room_id].get('players', 0), 'bet': room_state[killed_room_id].get('bet', 0)})

def _process_room_update(room_data: dict):
    if not isinstance(room_data, dict):
        return
    try:
        rid = int(room_data.get("room_id") or room_data.get("roomId") or room_data.get("id"))
        players = int(room_data.get("user_cnt") or room_data.get("userCount") or 0) or 0
        bet = _parse_number(room_data.get("total_bet_amount") or room_data.get("totalBet") or room_data.get("bet") or 0) or 0
        room_state[rid] = {"players": players, "bet": bet}
        room_stats[rid]["last_players"] = players
        room_stats[rid]["last_bet"] = bet
    except (ValueError, TypeError):
        pass

def on_close(ws, code, reason):
    global _ws_status
    _ws_status = f"⏳ Đã đóng ({code})"

def on_error(ws, err):
    global _ws_status
    _ws_status = f"❌ Lỗi: {str(err)[:30]}"

def start_ws():
    WS_URL = "wss://api.escapemaster.net/escape_master/ws"
    backoff = 1.0
    global _ws_status
    while not stop_flag:
        try:
            _ws_status = "⏳ Đang kết nối..."
            ws_app = websocket.WebSocketApp(WS_URL, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            _ws["ws"] = ws_app
            ws_app.run_forever(ping_interval=15, ping_timeout=6)
        except Exception:
            _ws_status = f"❌ Lỗi kết nối"
        t = min(backoff + random.random() * 0.8, 30)
        if not stop_flag:
            time.sleep(t)
            backoff = min(backoff * 1.8, 30)

class BalancePoller(threading.Thread):
    def __init__(self, uid: Optional[int], secret: Optional[str], poll_seconds: int = 2, on_balance=None, on_error=None, on_status=None):
        super().__init__(daemon=True)
        self.uid = uid
        self.secret = secret
        self.poll_seconds = max(1, int(poll_seconds))
        self._running = True
        self._last_balance_local: Optional[float] = None
        self.on_balance = on_balance
        self.on_error = on_error
        self.on_status = on_status

    def stop(self):
        self._running = False

    def run(self):
        if self.on_status:
            self.on_status("Kết nối...")
        while self._running and not stop_flag:
            try:
                build, world, usdt = fetch_balances_3games(params={"userId": str(self.uid)} if self.uid else None, uid=self.uid, secret=self.secret)
                if build is None:
                    raise RuntimeError("Không đọc được balance từ response")
                delta = 0.0 if self._last_balance_local is None else (build - self._last_balance_local)
                first_time = (self._last_balance_local is None)
                if first_time or abs(delta) > 0:
                    self._last_balance_local = build
                    if self.on_balance:
                        self.on_balance(float(build), float(delta), {"ts": human_ts()})
                    if self.on_status:
                        self.on_status("Đang theo dõi")
                else:
                    if self.on_status:
                        self.on_status("Đang theo dõi (không đổi)")
            except Exception as e:
                if self.on_error:
                    self.on_error(str(e))
                if self.on_status:
                    self.on_status("Lỗi kết nối (thử lại...)")
            for _ in range(max(1, int(self.poll_seconds * 5))):
                if not self._running or stop_flag:
                    break
                time.sleep(0.2)
        if self.on_status:
            self.on_status("Đã dừng")

def monitor_loop():
    global last_balance_fetch_ts, last_msg_ts, stop_flag
    while not stop_flag:
        now = time.time()
        if now - last_balance_fetch_ts >= BALANCE_POLL_INTERVAL:
            last_balance_fetch_ts = now
            try:
                fetch_balances_3games(params={"userId": str(USER_ID)} if USER_ID else None)
            except Exception:
                pass
        if now - last_msg_ts > 12:
            try:
                safe_send_enter_game(_ws.get("ws"))
            except Exception:
                pass
        if now - last_msg_ts > 45:
            try:
                wsobj = _ws.get("ws")
                if wsobj:
                    try:
                        wsobj.close()
                    except Exception:
                        pass
            except Exception:
                pass
        try:
            if analysis_start_ts and (time.time() - analysis_start_ts >= analysis_duration) and not prediction_locked:
                lock_prediction_if_needed()
        except Exception:
            pass
        time.sleep(0.6)

# ================== GIAO DIỆN ==================

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
    info_table.add_row(f"{ICONS['user']} USER:", f"[bold {HTOOL_COLORS['platinum']}]{USER_ID}[/bold {HTOOL_COLORS['platinum']}]" if USER_ID else "[dim]-[/dim]")
    b = f"{current_build:,.2f}" if isinstance(current_build, (int, float)) else "0.00"
    info_table.add_row(f"{ICONS['diamond']} BALANCE:", f"[bold {HTOOL_COLORS['emerald']}]{b}[/bold {HTOOL_COLORS['emerald']}] BUILD")
    pnl_val = cumulative_profit if cumulative_profit is not None else 0
    if pnl_val > 0:
        pnl_color = HTOOL_COLORS["emerald"]
        pnl_icon = "📈"
    elif pnl_val < 0:
        pnl_color = HTOOL_COLORS["ruby"]
        pnl_icon = "📉"
    else:
        pnl_color = HTOOL_COLORS["gold"]
        pnl_icon = "➖"
    info_table.add_row(f"{ICONS['fire']} P&L:", f"[{pnl_color}]{pnl_icon} {pnl_val:+,.2f}[/{pnl_color}] BUILD")
    streak_text = Text.assemble(("🔥 ", f"bold {HTOOL_COLORS['neon_orange']}"), (f"{win_streak}", f"bold {HTOOL_COLORS['emerald']}"), (" | ", "dim"), ("💀 ", f"bold {HTOOL_COLORS['ruby']}"), (f"{lose_streak}", f"bold {HTOOL_COLORS['ruby']}"))
    info_table.add_row("📊 STREAK:", streak_text)
    algo_label = SELECTION_MODES.get(settings.get('algo'), settings.get('algo'))
    key_type_display = f"🔑 {_key_type.upper()}" if _key_type else "🔑 FREE"
    info_table.add_row(f"{ICONS['key']} KEY:", f"[bold {HTOOL_COLORS['gold'] if _key_type == 'vip' else 'white'}]{key_type_display}[/bold {HTOOL_COLORS['gold'] if _key_type == 'vip' else 'white'}]")
    info_table.add_row(f"{ICONS['brain']} AI:", f"[bold {HTOOL_COLORS['neon_pink']}]{algo_label}[/bold {HTOOL_COLORS['neon_pink']}]")
    now_str = datetime.now(tz).strftime("%H:%M:%S")
    info_table.add_row(f"{ICONS['clock']} TIME:", f"[{HTOOL_COLORS['sapphire']}]{now_str}[/{HTOOL_COLORS['sapphire']}]")
    info_table.add_row(f"{ICONS['target']} ROUND:", f"[bold {HTOOL_COLORS['gold']}]{issue_id or 'Waiting...'}[/bold {HTOOL_COLORS['gold']}]")
    info_table.add_row(f"🔗 WS:", f"[dim]{_ws_status}[/dim]")
    info_table.add_row(f"🌐 IP:", f"[dim]{_ip_info.get('public_ip', 'N/A')}[/dim]")
    info_table.add_row(f"🛡️ Anti-Detection:", f"[{'green' if _secure_mode else 'dim'}] {'ON' if _secure_mode else 'OFF'}[/]")
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
            bg = "on #330000"
            glow = "💀⚡🔥"
        elif is_killed:
            border = HTOOL_COLORS["ruby"]
            title_style = HTOOL_COLORS["ruby"]
            bg = "on #1a0000"
            glow = "💀"
        elif is_predicted:
            border = f"bold {HTOOL_COLORS['emerald']}"
            title_style = f"bold {HTOOL_COLORS['emerald']}"
            bg = "on #003300"
            glow = "✨⭐"
        else:
            border = HTOOL_COLORS["onyx"]
            title_style = "white"
            bg = ""
            glow = ""
        content = Text.assemble(("\n", ""), (f"{glow} ", "default"), (f"👥 {players:3d} ", "white"), ("| ", "dim"), (f"💰 {int(bet_val):,}", HTOOL_COLORS["gold"]), ("\n", ""), justify="center")
        room_panel = Panel(Align.center(content, vertical="middle"), title=f"[{title_style}]{ROOM_NAMES.get(r, f'Room {r}')}[/{title_style}]", border_style=border, box=box.HEAVY, expand=True, height=5, style=bg)
        room_panels.append(room_panel)
    return Panel(Columns(room_panels, equal=True, expand=True), title=f"[bold {HTOOL_COLORS['gold']}]🎮 PREMIUM BATTLE ARENA 🎮[/bold {HTOOL_COLORS['gold']}]", box=box.HEAVY, border_style=HTOOL_COLORS["gold"], expand=True)

def build_premium_mid():
    global analysis_start_ts
    if ui_state == "ANALYZING":
        now = time.time()
        elapsed = now - (analysis_start_ts or now)
        progress = min(1.0, elapsed / analysis_duration)
        neurons = ["⚪", "🟢", "🔵", "🟣", "🟡"]
        active_neurons = int(progress * len(neurons))
        neural_net = " ".join(neurons[:active_neurons] + ["◯"] * (len(neurons) - active_neurons))
        lines = [f"\n[bold {HTOOL_COLORS['neon_blue']}]🧠 AI NEURAL NETWORK ANALYZING[/bold {HTOOL_COLORS['neon_blue']}]", f"\n[{HTOOL_COLORS['gold']}]{neural_net}[/{HTOOL_COLORS['gold']}]", f"\n[{HTOOL_COLORS['neon_pink']}]Progress: {progress*100:3.0f}%[/{HTOOL_COLORS['neon_pink']}]"]
        bar_width = 40
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        lines.append(f"[{HTOOL_COLORS['gold']}]├[/{HTOOL_COLORS['gold']}] {bar}")
        if issue_end_ts and now < issue_end_ts:
            remaining = int(issue_end_ts - now)
            lines.append(f"\n⏳ [bold {HTOOL_COLORS['gold']}]Time remaining: {remaining}s[/bold {HTOOL_COLORS['gold']}]")
        return Panel(Text.from_markup("\n".join(lines)), border_style=HTOOL_COLORS["neon_pink"], box=box.HEAVY, padding=(1, 2), expand=True)
    elif ui_state == "PREDICTED":
        name = ROOM_NAMES.get(predicted_room, f"Room {predicted_room}") if predicted_room else '?'
        bet_amt = f"{current_bet:,.2f}" if current_bet is not None else '0'
        content = Text.assemble(("\n", ""), ("╔══════════════════════════════════════════╗\n", HTOOL_COLORS["gold"]), ("║  🎯  TARGET LOCKED  🎯                  ║\n", HTOOL_COLORS["gold"]), ("║  ", HTOOL_COLORS["gold"]), (f"{name:^28}", f"bold {HTOOL_COLORS['emerald']}"), ("  ║\n", HTOOL_COLORS["gold"]), ("║  💰 ", HTOOL_COLORS["gold"]), (f"{bet_amt:^26}", f"bold {HTOOL_COLORS['gold']}"), (" BUILD  ║\n", HTOOL_COLORS["gold"]), ("╚══════════════════════════════════════════╝\n", HTOOL_COLORS["gold"]), ("\n", ""), ("☠️ Last Kill: ", ""), (f"{ROOM_NAMES.get(last_killed_room, '-')}", f"bold {HTOOL_COLORS['ruby']}"), ("  |  📈 Win: ", ""), (f"{win_streak}", f"bold {HTOOL_COLORS['emerald']}"), ("  |  📉 Lose: ", ""), (f"{lose_streak}", f"bold {HTOOL_COLORS['ruby']}"))
        return Panel(Align.center(content), border_style=HTOOL_COLORS["emerald"], box=box.HEAVY, padding=1, expand=True)
    elif ui_state == "RESULT":
        k = ROOM_NAMES.get(killed_room, "-") if killed_room else "-"
        last_bet = bet_history[-1] if bet_history else None
        result_text = "⏳ WAITING"
        result_color = HTOOL_COLORS["gold"]
        border = HTOOL_COLORS["gold"]
        if last_bet and last_bet.get('issue') == issue_id:
            if last_bet.get('result') == "Thắng":
                result_text = f"🎉 {ICONS['trophy']} WINNER {ICONS['trophy']}"
                result_color = HTOOL_COLORS["emerald"]
                border = HTOOL_COLORS["emerald"]
            elif last_bet.get('result') == "Thua":
                result_text = f"💀 {ICONS['fire']} LOSER {ICONS['fire']}"
                result_color = HTOOL_COLORS["ruby"]
                border = HTOOL_COLORS["ruby"]
        content = Text.assemble(("\n", ""), ("╔═══════════════════════════════════╗\n", border), ("║  ", border), (f"{result_text:^31}", f"bold {result_color}"), ("  ║\n", border), ("╚═══════════════════════════════════╝\n", border), ("\n", ""), ("☠️ Killer: ", ""), (f"{k}", f"bold {HTOOL_COLORS['ruby']}"), ("\n", ""), ("📊 P&L: ", ""), (f"{cumulative_profit:+,.2f}", f"bold {HTOOL_COLORS['gold']}"), (" BUILD", ""))
        return Panel(Align.center(content), border_style=border, box=box.HEAVY, padding=1, expand=True)
    else:
        return Panel(Align.center(Text(f"⏳ {ICONS['sparkle']} Waiting for game data... {ICONS['sparkle']}", style=HTOOL_COLORS["gold"])), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, expand=True)

def build_premium_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 BET HISTORY[/bold {HTOOL_COLORS['gold']}]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["onyx"])
    t.add_column("Round", no_wrap=True, style=HTOOL_COLORS["sapphire"])
    t.add_column("Room", no_wrap=True, style=HTOOL_COLORS["neon_blue"])
    t.add_column("Amount", justify="right", no_wrap=True, style=HTOOL_COLORS["gold"])
    t.add_column("Result", no_wrap=True)
    t.add_column("AI", no_wrap=True, style=HTOOL_COLORS["neon_pink"])
    last_n = list(bet_history)[-6:]
    for b in reversed(last_n):
        amt = b.get('amount') or 0
        res = str(b.get('result') or '⏳')
        algo = str(b.get('algo') or '-')
        if "Thắng" in res:
            res_text = Text(f"✅ {ICONS['trophy']}", style=HTOOL_COLORS["emerald"])
        elif "Thua" in res:
            res_text = Text(f"❌ {ICONS['fire']}", style=HTOOL_COLORS["ruby"])
        else:
            res_text = Text(f"⏳ {ICONS['sparkle']}", style=HTOOL_COLORS["gold"])
        t.add_row(str(b.get('issue') or '-'), ROOM_NAMES.get(b.get('room'), str(b.get('room') or '-')), f"{float(amt):,.2f}", res_text, algo[:1] if algo else '-')
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def build_premium_marquee():
    messages = [
        f"⚡ {ICONS['lightning']} HTOOL VIP PREMIUM - Best AI Tool {ICONS['crown']}",
        f"🧠 {ICONS['brain']} AI Powered Prediction System v3.0 {ICONS['robot']}",
        f"💰 {ICONS['diamond']} Play Smart, Win Big with HTOOL {ICONS['trophy']}",
        f"🔥 {ICONS['fire']} Don't Gamble - Let AI Decide {ICONS['shield']}",
        f"🎯 {ICONS['target']} Enhanced AI with Cycle & Trend Analysis {ICONS['sparkle']}",
        f"👑 {ICONS['crown']} Premium Features: Auto Martingale, Stop Loss, Take Profit",
        f"🤖 {ICONS['robot']} 42 AI Strategies: Choose the Best for You",
        f"💎 {ICONS['gem']} VIP Support: @htool88 - 24/7 Assistance",
        f"🌐 {ICONS['globe']} IP Security Active - Anti Crack {ICONS['shield']}",
        f"🛡️ {ICONS['shield']} Anti-Detection Mode: {'ON' if _secure_mode else 'OFF'}",
    ]
    message = messages[int(time.time() / 8) % len(messages)]
    full_text = " " * 30 + message + " " * 30
    width = console.width or 80
    start_index = int(time.time() * 3) % len(full_text)
    display_text = (full_text * 3)[start_index : start_index + width]
    return Panel(Text(display_text, style=f"bold {HTOOL_COLORS['neon_blue']}", no_wrap=True), box=box.ROUNDED, border_style=HTOOL_COLORS["onyx"], padding=0, expand=True)

# ================== CẤU HÌNH ==================

def save_strategy_config():
    config_data = {"base_bet": base_bet, "multiplier": multiplier, "algo": settings.get("algo"), "bet_rounds_before_skip": bet_rounds_before_skip, "pause_after_losses": pause_after_losses, "profit_target": profit_target, "stop_when_profit_reached": stop_when_profit_reached, "stop_loss_target": stop_loss_target, "stop_when_loss_reached": stop_when_loss_reached}
    try:
        with open(STRATEGY_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        safe_console_print(f"[green]✅ Config saved to '{STRATEGY_CONFIG_FILE}'[/green]")
    except Exception as e:
        safe_console_print(f"[red]❌ Error saving config: {e}[/red]")

def load_strategy_config() -> bool:
    global base_bet, multiplier, run_mode, bet_rounds_before_skip, current_bet, pause_after_losses, profit_target, stop_when_profit_reached, stop_loss_target, stop_when_loss_reached
    if not Path(STRATEGY_CONFIG_FILE).exists():
        safe_console_print(f"[yellow]⚠️ Config file '{STRATEGY_CONFIG_FILE}' not found.[/yellow]")
        safe_console_print("[yellow]➜ Please use option [5] to save config first.[/yellow]")
        return False
    try:
        with open(STRATEGY_CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        base_bet = config_data.get("base_bet", 1.0)
        multiplier = config_data.get("multiplier", 2.0)
        settings["algo"] = config_data.get("algo", "ENSEMBLE")
        bet_rounds_before_skip = config_data.get("bet_rounds_before_skip", 0)
        pause_after_losses = config_data.get("pause_after_losses", 0)
        profit_target = config_data.get("profit_target", None)
        stop_when_profit_reached = config_data.get("stop_when_profit_reached", False)
        stop_loss_target = config_data.get("stop_loss_target", None)
        stop_when_loss_reached = config_data.get("stop_when_loss_reached", False)
        current_bet = base_bet
        run_mode = "AUTO"
        safe_console_print(f"[green]✅ Config loaded from '{STRATEGY_CONFIG_FILE}'[/green]")
        safe_console_print()
        summary = build_config_summary()
        safe_console_print(Panel(summary, title="[bold]LOADED CONFIG[/bold]", box=box.HEAVY, border_style=HTOOL_COLORS["emerald"], expand=False))
        time.sleep(2)
        return True
    except Exception as e:
        safe_console_print(f"[red]❌ Error loading config: {e}[/red]")
        return False

def build_config_summary():
    summary = Table(box=box.ROUNDED, show_header=False, border_style=HTOOL_COLORS["gold"])
    summary.add_column(style=f"bold {HTOOL_COLORS['sapphire']}", width=20)
    summary.add_column(style="white")
    config_items = [
        (f"{ICONS['money']} Cược gốc:", f"[bold {HTOOL_COLORS['emerald']}]{base_bet:,.2f} BUILD[/bold {HTOOL_COLORS['emerald']}]"),
        (f"{ICONS['chart']} Hệ số nhân:", f"[bold {HTOOL_COLORS['gold']}]x{multiplier}[/bold {HTOOL_COLORS['gold']}]"),
        (f"{ICONS['key']} Loại Key:", f"[bold {HTOOL_COLORS['gold'] if _key_type == 'vip' else 'white'}]{_key_type.upper()}[/bold {HTOOL_COLORS['gold'] if _key_type == 'vip' else 'white'}]"),
        (f"{ICONS['brain']} Thuật toán:", f"[bold {HTOOL_COLORS['neon_pink']}]{SELECTION_MODES.get(settings['algo'], settings['algo'])}[/bold {HTOOL_COLORS['neon_pink']}]"),
        (f"{ICONS['shield']} Chống soi:", f"[bold {HTOOL_COLORS['sapphire']}]Nghỉ 1 ván sau {bet_rounds_before_skip} ván[/bold {HTOOL_COLORS['sapphire']}]" if bet_rounds_before_skip > 0 else "[dim]Không kích hoạt[/dim]"),
        (f"{ICONS['clock']} Nghỉ khi thua:", f"[bold {HTOOL_COLORS['sapphire']}]Nghỉ {pause_after_losses} ván[/bold {HTOOL_COLORS['sapphire']}]" if pause_after_losses > 0 else "[dim]Không kích hoạt[/dim]"),
        (f"{ICONS['target']} Mục tiêu lãi:", f"[bold {HTOOL_COLORS['emerald']}]Dừng khi đạt {profit_target:,.2f} BUILD[/bold {HTOOL_COLORS['emerald']}]" if profit_target else "[dim]Chạy vô hạn[/dim]"),
        (f"{ICONS['shield']} Cắt lỗ:", f"[bold {HTOOL_COLORS['ruby']}]Dừng khi còn {stop_loss_target:,.2f} BUILD[/bold {HTOOL_COLORS['ruby']}]" if stop_loss_target else "[dim]Không kích hoạt[/dim]"),
        (f"{ICONS['shield']} Anti-Detection:", f"[bold {HTOOL_COLORS['emerald']}]{'✅ BẬT' if _secure_mode else '❌ TẮT'}[/bold {HTOOL_COLORS['emerald']}]"),
    ]
    for label, value in config_items:
        summary.add_row(label, value)
    return summary

def build_config_header():
    return Panel(Align.center(Text.assemble((f"{ICONS['settings']} ", f"bold {HTOOL_COLORS['gold']}"), ("PREMIUM CONFIGURATION", f"bold {HTOOL_COLORS['neon_blue']}"), (f" {ICONS['settings']}", f"bold {HTOOL_COLORS['gold']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)

def build_step_indicator(current_step: int, total_steps: int):
    steps = ["💰 VỐN", "🧠 AI", "🛡️ RỦI RO", "🎯 MỤC TIÊU"]
    step_indicators = []
    for i, step in enumerate(steps, 1):
        if i < current_step:
            step_indicators.append(f"[bold {HTOOL_COLORS['emerald']}]✅ {step}[/bold {HTOOL_COLORS['emerald']}]")
        elif i == current_step:
            step_indicators.append(f"[bold {HTOOL_COLORS['gold']}]▶️ {step}[/bold {HTOOL_COLORS['gold']}]")
        else:
            step_indicators.append(f"[dim]◻️ {step}[/dim]")
    return "  →  ".join(step_indicators)

def prompt_settings():
    global base_bet, multiplier, run_mode, bet_rounds_before_skip, current_bet, pause_after_losses, profit_target, stop_when_profit_reached, stop_loss_target, stop_when_loss_reached, _key_type
    
    console.clear()
    console.print(build_config_header())
    console.print()
    
    key_info = Panel(
        Text.assemble(
            (f"🔑 Loại Key: ", "white"),
            (f"{_key_type.upper()}\n", "bold gold" if _key_type == "vip" else "bold white"),
            (f"📊 Số AI có thể dùng: ", "white"),
            (f"{len(get_available_ai_list(_key_type))}/42\n", "bold cyan"),
            (f"{'⭐ Bạn đang sử dụng KEY VIP - Full 42 AI' if _key_type == 'vip' else '🔓 Bạn đang sử dụng KEY FREE - 12 AI cơ bản'}", 
             "bold gold" if _key_type == "vip" else "dim"),
            ("\n", ""),
            (f"🌐 IP Security: Active", "bold green"),
            (f"\n🛡️ Anti-Detection: {'✅ BẬT' if _secure_mode else '❌ TẮT'}", "bold green" if _secure_mode else "dim"),
        ),
        title="[bold]THÔNG TIN KEY[/bold]",
        border_style=HTOOL_COLORS["gold"],
        box=box.ROUNDED
    )
    console.print(key_info)
    console.print()
    
    console.print(build_step_indicator(1, 4))
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]💎 BƯỚC 1: QUẢN LÝ VỐN[/bold {HTOOL_COLORS['gold']}]", style=HTOOL_COLORS["gold"]))
    
    info_panel = Panel(Text.assemble((f"{ICONS['info']} ", "bold yellow"), ("Hãy thiết lập số vốn và mức cược phù hợp với túi tiền của bạn", "white"), ("\n", ""), (f"{ICONS['warning']} ", "bold red"), ("Không nên đặt quá 5-10% tổng vốn mỗi ván", "yellow")), border_style=HTOOL_COLORS["sapphire"], box=box.ROUNDED)
    console.print(info_panel)
    console.print()
    console.print(f"[bold {HTOOL_COLORS['neon_blue']}]💰 Cược gốc:[/bold {HTOOL_COLORS['neon_blue']}]")
    console.print("[dim]➜ Số BUILD sẽ đặt mỗi ván (tối thiểu 1.0)[/dim]")
    base_bet = FloatPrompt.ask("   >>", default=1.0)
    console.print(f"\n[bold {HTOOL_COLORS['neon_blue']}]📈 Hệ số nhân (Gấp thếp):[/bold {HTOOL_COLORS['neon_blue']}]")
    console.print("[dim]➜ Số lần nhân khi thua (khuyến nghị 2.0 - 10.0)[/dim]")
    multiplier = FloatPrompt.ask("   >>", default=2.0)
    current_bet = base_bet
    
    console.clear()
    console.print(build_config_header())
    console.print()
    
    console.print(build_step_indicator(2, 4))
    console.print(Rule(f"[bold {HTOOL_COLORS['neon_pink']}]🧠 BƯỚC 2: CHỌN THUẬT TOÁN AI[/bold {HTOOL_COLORS['neon_pink']}]", style=HTOOL_COLORS["neon_pink"]))
    
    available_ai_list = get_available_ai_list(_key_type)
    modes = list(SELECTION_MODES.items())
    available_modes = [(key, label) for key, label in modes if key in available_ai_list]
    
    algo_table = Table(box=box.ROUNDED, border_style=HTOOL_COLORS["neon_pink"])
    algo_table.add_column("STT", style=f"bold {HTOOL_COLORS['gold']}", width=4)
    algo_table.add_column("Tên thuật toán", style=HTOOL_COLORS["neon_blue"])
    algo_table.add_column("Loại", style="dim")
    algo_table.add_column("Mô tả", style="dim")
    
    algo_descriptions = {
        "RANDOM": "Ngẫu nhiên, không suy nghĩ",
        "MIN_PLAYER_BET": "Chọn phòng ít người & ít tiền nhất",
        "PROBABILITY": "Dựa trên xác suất thống kê",
        "FOLLOW_KILLER": "Theo dấu sát thủ vừa xuất hiện",
        "SEQUENTIAL": "Đặt theo thứ tự 1→2→3→...→8",
        "KILLER_PERSONALITY": "Học thói quen của sát thủ (Enhanced)",
        "SMART_SAFE": "Tính toán an toàn thông minh (Enhanced)",
        "FOLLOW_KILLER_DELAYED": "Theo vết sát thủ (delay 1 ván)",
        "HIDE_SEEK_MASTER": "Thuật toán trốn tìm cao cấp",
        "BALANCE": "Chọn phòng cân bằng nhất",
        "MOST_PLAYERS": "Chọn phòng đông người nhất",
        "LEAST_PLAYERS": "Chọn phòng ít người nhất",
        "RICHEST": "Chọn phòng giàu nhất",
        "POOREST": "Chọn phòng nghèo nhất",
        "ALTERNATE": "Xen kẽ giữa các phòng",
        "AVOID_RESULT": "Tránh phòng vừa bị kill",
        "COLD": "Chọn phòng lạnh (ít chọn)",
        "HOT": "Chọn phòng nóng (nhiều chọn)",
        "MEDIAN": "Chọn phòng trung vị",
        "PATTERN": "Tìm mẫu lặp trong kết quả",
        "VIP_RANDOM": "Random 1 trong 22 logic mỗi ván",
        "KILLER_WAVE": "Bắt sóng sát thủ theo chu kỳ",
        "PSYCHO_ANALYSIS": "Phân tích tâm lý đám đông",
        "MARKOV_CHAIN": "Dùng xác suất Markov",
        "DEEP_LEARNING": "Học sâu với nhiều lớp (Enhanced)",
        "REINFORCEMENT": "Học tăng cường từ kết quả",
        "BAYESIAN": "Xác suất Bayes có điều kiện",
        "K_MEANS": "Phân cụm K-Means",
        "NEURAL": "Mạng nơ-ron nhân tạo",
        "FUZZY": "Logic mờ fuzzy",
        "GENETIC": "Thuật toán di truyền",
        "ANT_COLONY": "Tối ưu hóa kiến bò",
        "PARTICLE_SWARM": "Tối ưu bầy đàn",
        "KNN": "K-Nearest Neighbors",
        "DECISION_TREE": "Cây quyết định",
        "RANDOM_FOREST": "Rừng ngẫu nhiên",
        "GRADIENT_BOOST": "Gradient Boosting",
        "LSTM": "Long Short-Term Memory",
        "TRANSFORMER": "Transformer Attention",
        "ENSEMBLE": "Tổng hợp tất cả logic (Enhanced)",
        "CYCLE_ANALYSIS": "Phân tích chu kỳ ẩn (Mới)",
        "TREND_ANALYSIS": "Phân tích xu hướng (Mới)",
    }
    
    for i, (key, label) in enumerate(available_modes, 1):
        desc = algo_descriptions.get(key, "")
        ai_type = "🆓 FREE" if key in FREE_AI_LIST else "👑 VIP"
        algo_table.add_row(str(i), label, ai_type, desc)
    
    console.print(algo_table)
    console.print()
    
    if _key_type == "free":
        console.print("[dim]🔓 Key Free: 12 AI cơ bản (đánh dấu 🆓)[/dim]")
    else:
        console.print("[bold gold]👑 Key VIP: Sử dụng toàn bộ 42 AI[/bold gold]")
    
    choice = IntPrompt.ask(
        f"[bold {HTOOL_COLORS['gold']}]>> Chọn số thứ tự[/bold {HTOOL_COLORS['gold']}]",
        choices=[str(i) for i in range(1, len(available_modes) + 1)]
    )
    selected_key = available_modes[choice - 1][0]
    settings["algo"] = selected_key
    
    console.print(f"[green]✅ Đã chọn: {SELECTION_MODES.get(settings['algo'])}[/green]")
    
    console.clear()
    console.print(build_config_header())
    console.print()
    
    console.print(build_step_indicator(3, 4))
    console.print(Rule(f"[bold {HTOOL_COLORS['sapphire']}]🛡️ BƯỚC 3: QUẢN LÝ RỦI RO[/bold {HTOOL_COLORS['sapphire']}]", style=HTOOL_COLORS["sapphire"]))
    
    risk_panel = Panel(Text.assemble((f"{ICONS['shield']} ", "bold cyan"), ("Các tính năng bảo vệ giúp giảm thiểu rủi ro khi chơi", "white"), ("\n", ""), (f"{ICONS['info']} ", "dim"), ("Nhập 0 để bỏ qua tính năng", "dim")), border_style=HTOOL_COLORS["sapphire"], box=box.ROUNDED)
    console.print(risk_panel)
    console.print()
    console.print(f"[bold {HTOOL_COLORS['neon_blue']}]🛡️ Chống soi:[/bold {HTOOL_COLORS['neon_blue']}]")
    console.print("[dim]➜ Nghỉ 1 ván sau mỗi N ván đặt (tránh bị phát hiện)[/dim]")
    bet_rounds_before_skip = IntPrompt.ask("   >> Nhập số ván", default=0)
    console.print(f"\n[bold {HTOOL_COLORS['neon_blue']}]⏸️ Nghỉ khi thua liên tiếp:[/bold {HTOOL_COLORS['neon_blue']}]")
    console.print("[dim]➜ Nghỉ N ván sau khi thua (giảm cảm xúc)[/dim]")
    pause_after_losses = IntPrompt.ask("   >> Nhập số ván nghỉ", default=0)
    
    console.clear()
    console.print(build_config_header())
    console.print()
    
    console.print(build_step_indicator(4, 4))
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]🎯 BƯỚC 4: ĐẶT MỤC TIÊU[/bold {HTOOL_COLORS['gold']}]", style=HTOOL_COLORS["gold"]))
    
    target_panel = Panel(Text.assemble((f"{ICONS['target']} ", "bold yellow"), ("Đặt mục tiêu lãi và cắt lỗ để bảo vệ tài khoản", "white"), ("\n", ""), (f"{ICONS['info']} ", "dim"), ("Để trống để chạy vô hạn", "dim")), border_style=HTOOL_COLORS["gold"], box=box.ROUNDED)
    console.print(target_panel)
    console.print()
    console.print(f"[bold {HTOOL_COLORS['emerald']}]🎯 Mục tiêu lãi:[/bold {HTOOL_COLORS['emerald']}]")
    console.print("[dim]➜ Dừng tool khi đạt số BUILD này (nhập số dư mong muốn)[/dim]")
    pt_str = Prompt.ask("   >> Nhập số BUILD (Enter để bỏ qua)", default="")
    if pt_str.strip():
        try:
            profit_target = float(pt_str)
            stop_when_profit_reached = True
            console.print(f"[green]✅ Đã đặt mục tiêu lãi: {profit_target:,.2f} BUILD[/green]")
        except ValueError:
            profit_target = None
            stop_when_profit_reached = False
            console.print("[dim]⏭️ Bỏ qua mục tiêu lãi[/dim]")
    else:
        profit_target = None
        stop_when_profit_reached = False
        console.print("[dim]⏭️ Bỏ qua mục tiêu lãi[/dim]")
        console.print()
    console.print(f"[bold {HTOOL_COLORS['ruby']}]💀 Cắt lỗ:[/bold {HTOOL_COLORS['ruby']}]")
    console.print("[dim]➜ Dừng tool khi số dư còn lại là N BUILD[/dim]")
    sl_str = Prompt.ask("   >> Nhập số BUILD tối thiểu (Enter để bỏ qua)", default="")
    if sl_str.strip():
        try:
            stop_loss_target = float(sl_str)
            stop_when_loss_reached = True
            console.print(f"[green]✅ Đã đặt cắt lỗ: còn {stop_loss_target:,.2f} BUILD[/green]")
        except ValueError:
            stop_loss_target = None
            stop_when_loss_reached = False
            console.print("[dim]⏭️ Bỏ qua cắt lỗ[/dim]")
    else:
        stop_loss_target = None
        stop_when_loss_reached = False
        console.print("[dim]⏭️ Bỏ qua cắt lỗ[/dim]")
    console.print()
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]📋 TỔNG KẾT CẤU HÌNH[/bold {HTOOL_COLORS['gold']}]", style=HTOOL_COLORS["gold"]))
    console.print(build_config_summary())
    console.print()
    console.print(Panel(Align.center(Text.assemble((f"{ICONS['check']} ", "bold green"), ("Cấu hình đã hoàn tất! ", "bold white"), (f"{ICONS['sparkle']}", "bold gold"))), border_style=HTOOL_COLORS["emerald"], box=box.ROUNDED))
    start_choice = Prompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]>> Bắt đầu chơi ngay? (Enter để bắt đầu / q để thoát)[/bold {HTOOL_COLORS['gold']}]", default="")
    if start_choice.lower() == 'q':
        return False
    console.clear()
    run_mode = "AUTO"
    return True

# ================== QUẢN LÝ TÀI KHOẢN ==================

def load_accounts() -> list:
    acc_file = Path("accounts.json")
    if not acc_file.exists():
        return []
    try:
        return json.loads(acc_file.read_text())
    except (json.JSONDecodeError, IOError):
        return []

def save_accounts(accounts: list):
    acc_file = Path("accounts.json")
    with acc_file.open("w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)

def add_new_account(accounts: list) -> bool:
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['user']} ", f"bold {HTOOL_COLORS['gold']}"), ("ADD NEW ACCOUNT", f"bold {HTOOL_COLORS['neon_blue']}"), (f" {ICONS['user']}", f"bold {HTOOL_COLORS['gold']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(header)
    console.print()
    console.print(Panel(Text.assemble((f"{ICONS['info']} ", "bold yellow"), ("Dán link trò chơi vào bên dưới", "white"), ("\n", ""), ("Ví dụ: ", "dim"), ("https://xworld.info/?userId=12345&secretKey=abc123", "dim cyan")), border_style=HTOOL_COLORS["sapphire"], box=box.ROUNDED))
    console.print()
    link = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Paste link[/bold {HTOOL_COLORS['gold']}]")
    if not link:
        console.print("[yellow]Cancelled.[/yellow]")
        time.sleep(1)
        return False
    try:
        parsed = urlparse(link)
        params = parse_qs(parsed.query)
        if 'userId' in params and 'secretKey' in params:
            uid = int(params.get('userId')[0])
            skey = params.get('secretKey', [None])[0]
            if any(acc.get('userId') == uid for acc in accounts):
                console.print(f"[yellow]⚠️ Account userId: {uid} already exists.[/yellow]")
                time.sleep(2)
                return False
            accounts.append({"userId": uid, "secretKey": skey})
            save_accounts(accounts)
            console.print(Panel(Align.center(Text.assemble((f"{ICONS['check']} ", "bold green"), (f"Added account: ", "bold white"), (f"{uid}", f"bold {HTOOL_COLORS['gold']}"))), border_style=HTOOL_COLORS["emerald"], box=box.ROUNDED))
            time.sleep(2)
            return True
        else:
            console.print("[red]❌ Invalid link! Missing 'userId' or 'secretKey'.[/red]")
            time.sleep(2)
            return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        time.sleep(2)
        return False

def delete_account(accounts: list) -> bool:
    console.clear()
    header = Panel(Align.center(Text.assemble((f"{ICONS['fire']} ", f"bold {HTOOL_COLORS['ruby']}"), ("DELETE ACCOUNT", f"bold {HTOOL_COLORS['neon_blue']}"), (f" {ICONS['fire']}", f"bold {HTOOL_COLORS['ruby']}"))), border_style=HTOOL_COLORS["ruby"], box=box.DOUBLE)
    console.print(header)
    console.print()
    if not accounts:
        console.print("[yellow]No accounts to delete.[/yellow]")
        time.sleep(2)
        return False
    table = Table(box=box.ROUNDED, border_style=HTOOL_COLORS["ruby"])
    table.add_column("STT", style=f"bold {HTOOL_COLORS['gold']}", width=6)
    table.add_column("User ID", style=HTOOL_COLORS["neon_blue"])
    for i, acc in enumerate(accounts, 1):
        table.add_row(str(i), str(acc.get('userId')))
    console.print(table)
    console.print()
    choice_str = Prompt.ask(f"[bold {HTOOL_COLORS['ruby']}]>> Select account to delete[/bold {HTOOL_COLORS['ruby']}]", default="")
    if not choice_str:
        console.print("[yellow]Cancelled.[/yellow]")
        time.sleep(1)
        return False
    try:
        choice_idx = int(choice_str) - 1
        if 0 <= choice_idx < len(accounts):
            removed_acc = accounts.pop(choice_idx)
            save_accounts(accounts)
            console.print(f"[green]✅ Deleted account: {removed_acc.get('userId')}[/green]")
            time.sleep(2)
            return True
        else:
            console.print("[red]❌ Invalid selection.[/red]")
            time.sleep(1)
            return False
    except ValueError:
        console.print("[red]❌ Invalid input.[/red]")
        time.sleep(1)
        return False

def select_account_premium() -> bool:
    global USER_ID, SECRET_KEY
    while True:
        console.clear()
        header = Panel(Align.center(Text.assemble((f"{ICONS['user']} ", f"bold {HTOOL_COLORS['gold']}"), ("SELECT ACCOUNT", f"bold {HTOOL_COLORS['neon_blue']}"), (f" {ICONS['user']}", f"bold {HTOOL_COLORS['gold']}"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
        console.print(header)
        console.print()
        accounts = load_accounts()
        if not accounts:
            console.print(Panel(Align.center(Text.assemble((f"{ICONS['warning']} ", "bold yellow"), ("Không có tài khoản nào!", "bold white"), ("\n", ""), ("Vui lòng dùng tùy chọn [3] để thêm tài khoản", "dim"))), border_style=HTOOL_COLORS["ruby"], box=box.ROUNDED))
            time.sleep(2)
            return False
        table = Table(title=f"[bold {HTOOL_COLORS['gold']}]📋 ACCOUNT LIST[/bold {HTOOL_COLORS['gold']}]", box=box.HEAVY, border_style=HTOOL_COLORS["sapphire"])
        table.add_column("STT", style=f"bold {HTOOL_COLORS['gold']}", width=6)
        table.add_column("User ID", style=HTOOL_COLORS["neon_blue"])
        table.add_column("Balance", justify="right")
        table.add_column("Status", justify="center")
        with console.status(f"[bold {HTOOL_COLORS['neon_blue']}]🔍 Checking balances...[/bold {HTOOL_COLORS['neon_blue']}]", spinner="dots") as status:
            for i, acc in enumerate(accounts, 1):
                uid = acc.get('userId')
                skey = acc.get('secretKey')
                status.update(f"[{HTOOL_COLORS['neon_blue']}]Checking account {uid}...[/{HTOOL_COLORS['neon_blue']}]")
                build, _, _ = fetch_balances_3games(uid=uid, secret=skey)
                if build is not None:
                    balance_str = f"[bold {HTOOL_COLORS['emerald']}]{build:,.4f}[/bold {HTOOL_COLORS['emerald']}]"
                    status_str = f"[{HTOOL_COLORS['emerald']}]✅ Online[/{HTOOL_COLORS['emerald']}]"
                else:
                    balance_str = f"[{HTOOL_COLORS['ruby']}]❌ Error[/{HTOOL_COLORS['ruby']}]"
                    status_str = f"[{HTOOL_COLORS['ruby']}]❌ Offline[/{HTOOL_COLORS['ruby']}]"
                table.add_row(str(i), str(uid), balance_str, status_str)
        console.print(table)
        console.print()
        choices = [str(i) for i in range(1, len(accounts) + 1)]
        choice_str = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Select account number[/bold {HTOOL_COLORS['gold']}]", choices=choices, default="")
        if not choice_str:
            return False
        try:
            choice_idx = int(choice_str) - 1
            if 0 <= choice_idx < len(accounts):
                selected_account = accounts[choice_idx]
                USER_ID = selected_account['userId']
                SECRET_KEY = selected_account['secretKey']
                console.print(Panel(Align.center(Text.assemble((f"{ICONS['check']} ", "bold green"), (f"Đã chọn tài khoản: ", "bold white"), (f"{USER_ID}", f"bold {HTOOL_COLORS['gold']}"))), border_style=HTOOL_COLORS["emerald"], box=box.ROUNDED))
                time.sleep(1.5)
                return True
            else:
                console.print("[red]❌ Invalid selection![/red]")
                time.sleep(1)
                return False
        except ValueError:
            console.print("[red]❌ Invalid input![/red]")
            time.sleep(1)
            return False

# ================== START GAME ==================

def start_threads():
    threading.Thread(target=start_ws, daemon=True).start()
    threading.Thread(target=monitor_loop, daemon=True).start()

def start_game_flow():
    global stop_flag, _in_menu
    _in_menu = False
    if USER_ID is None or SECRET_KEY is None:
        safe_console_print("[red]❌ No account selected.[/red]")
        time.sleep(2)
        return
    
    safe_console_print(f"[bold gold]👑 FULL 42 LOGIC AI - Enhanced Version[/bold gold]")
    safe_console_print(Rule("[bold green]🚀 SYSTEM STARTING...[/]", style="green"))
    start_threads()
    
    with console.status("[bold green]Connecting to game server...[/]", spinner="dots") as status:
        initial_wait_start = time.time()
        while issue_id is None and (time.time() - initial_wait_start) < 30:
            time.sleep(0.5)
            status.update(f"[bold green]Connecting... ({int(time.time() - initial_wait_start)}s)[/]")
        if issue_id is None:
            safe_console_print("\n[bold red]❌ No game data received after 30 seconds.[/]")
            safe_console_print("[yellow]Please check network connection.[/yellow]")
            time.sleep(3)
            return
    
    poller = BalancePoller(USER_ID, SECRET_KEY, poll_seconds=max(1, int(BALANCE_POLL_INTERVAL)), on_balance=None, on_error=None, on_status=None)
    poller.start()
    safe_console_print("\n[bold green]✅ Connected successfully! Starting interface...[/bold green]")
    time.sleep(2)
    def generate_layout() -> Table:
        is_mobile = console.width < 100
        if is_mobile:
            main_layout = Table.grid(expand=True, pad_edge=False)
            main_layout.add_row(build_premium_rooms())
            main_layout.add_row(build_premium_mid())
            main_layout.add_row(build_premium_history())
        else:
            main_grid = Table.grid(expand=True, pad_edge=False)
            main_grid.add_column("main", ratio=60)
            main_grid.add_column("side", ratio=40)
            right_column_grid = Table.grid(expand=True, pad_edge=False)
            right_column_grid.add_row(build_premium_mid())
            right_column_grid.add_row(build_premium_history())
            main_grid.add_row(build_premium_rooms(), right_column_grid)
            main_layout = main_grid
        root_layout = Table.grid(expand=True, pad_edge=False)
        root_layout.add_row(build_premium_header())
        root_layout.add_row(build_premium_marquee())
        root_layout.add_row(main_layout)
        return root_layout
    with Live(generate_layout(), refresh_per_second=4, console=console, screen=True) as live:
        try:
            while not stop_flag:
                live.update(generate_layout())
                time.sleep(0.25)
            safe_console_print("[bold yellow]Tool stopped.[/]")
        except KeyboardInterrupt:
            safe_console_print("[yellow]User exit.[/]")
            poller.stop()

# ================== CDTD FUNCTIONS ==================

cdtd_session = requests.Session()
cdtd_headers = {}

NV = {1: 'Bậc thầy tấn công', 2: 'Quyền sắt', 3: 'Thợ lặn sâu', 4: 'Cơn lốc sân cỏ', 5: 'Hiệp sĩ phi nhanh', 6: 'Vua home run'}
NV_ICONS = {1: '🥋', 2: '👊', 3: '🤿', 4: '🌪️', 5: '🏇', 6: '⚾'}

CDTD_FREE_AI_LIST = [
    "RANDOM", "AVOID_LAST", "HOT_STREAK", "COLD_STREAK",
    "BALANCE", "PATTERN", "PROBABILITY", "FOLLOW_WINNER",
    "ANTI_WINNER", "SMART_ANALYSIS", "CYCLE_ANALYSIS", "TREND_ANALYSIS"
]

CDTD_VIP_AI_LIST = [
    "MARKOV_CHAIN", "BAYESIAN", "NEURAL_NETWORK", "GENETIC_ALGO",
    "REINFORCEMENT", "KNN", "DECISION_TREE", "RANDOM_FOREST",
    "GRADIENT_BOOST", "ENSEMBLE", "TREND_FOLLOWING", "MEAN_REVERSION",
    "MOMENTUM", "VOLATILITY", "SEASONAL", "CORRELATION",
    "CLUSTER", "ANOMALY", "ENTROPY", "FUZZY_LOGIC",
    "LSTM_PREDICT", "TRANSFORMER", "ATTENTION", "DEEP_Q",
    "A3C", "PPO", "GAN", "AUTOENCODER", "SWARM_INTEL",
    "META_LEARNING"
]

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
    "CYCLE_ANALYSIS": "11. PHÂN TÍCH CHU KỲ",
    "TREND_ANALYSIS": "12. PHÂN TÍCH XU HƯỚNG",
    "MARKOV_CHAIN": "13. CHUỖI MARKOV",
    "BAYESIAN": "14. XÁC SUẤT BAYES",
    "NEURAL_NETWORK": "15. MẠNG NƠ-RON",
    "GENETIC_ALGO": "16. THUẬT TOÁN DI TRUYỀN",
    "REINFORCEMENT": "17. HỌC TĂNG CƯỜNG",
    "KNN": "18. K-NEAREST NEIGHBORS",
    "DECISION_TREE": "19. CÂY QUYẾT ĐỊNH",
    "RANDOM_FOREST": "20. RỪNG NGẪU NHIÊN",
    "GRADIENT_BOOST": "21. TĂNG CƯỜNG GRADIENT",
    "ENSEMBLE": "22. TỔNG HỢP",
    "TREND_FOLLOWING": "23. THEO XU HƯỚNG",
    "MEAN_REVERSION": "24. ĐẢO CHIỀU TRUNG BÌNH",
    "MOMENTUM": "25. ĐỘNG LƯỢNG",
    "VOLATILITY": "26. BIẾN ĐỘNG",
    "SEASONAL": "27. CHU KỲ",
    "CORRELATION": "28. TƯƠNG QUAN",
    "CLUSTER": "29. PHÂN CỤM",
    "ANOMALY": "30. PHÁT HIỆN BẤT THƯỜNG",
    "ENTROPY": "31. ENTROPY",
    "FUZZY_LOGIC": "32. LOGIC MỜ",
    "LSTM_PREDICT": "33. LSTM",
    "TRANSFORMER": "34. TRANSFORMER",
    "ATTENTION": "35. ATTENTION",
    "DEEP_Q": "36. DEEP Q-LEARNING",
    "A3C": "37. A3C",
    "PPO": "38. PPO",
    "GAN": "39. GAN",
    "AUTOENCODER": "40. AUTOENCODER",
    "SWARM_INTEL": "41. TRÍ TUỆ BẦY ĐÀN",
    "META_LEARNING": "42. META LEARNING",
}

CDTD_AI_DESCRIPTIONS = {
    "RANDOM": "Ngẫu nhiên, không phân tích",
    "AVOID_LAST": "Tránh người thắng ván trước",
    "HOT_STREAK": "Theo chuỗi thắng liên tiếp",
    "COLD_STREAK": "Bắt đảo chiều khi thua nhiều",
    "BALANCE": "Cân bằng lịch sử thắng thua",
    "PATTERN": "Nhận diện mẫu lặp lại",
    "PROBABILITY": "Xác suất thống kê cơ bản",
    "FOLLOW_WINNER": "Theo người thắng gần nhất",
    "ANTI_WINNER": "Chống lại người thắng",
    "SMART_ANALYSIS": "Phân tích thông minh tổng hợp",
    "CYCLE_ANALYSIS": "Phân tích chu kỳ xuất hiện",
    "TREND_ANALYSIS": "Phân tích xu hướng",
    "MARKOV_CHAIN": "Chuỗi Markov xác suất chuyển tiếp",
    "BAYESIAN": "Xác suất Bayes có điều kiện",
    "NEURAL_NETWORK": "Mạng nơ-ron nhân tạo",
    "GENETIC_ALGO": "Thuật toán di truyền tiến hóa",
    "REINFORCEMENT": "Học tăng cường từ kinh nghiệm",
    "KNN": "K-Nearest Neighbors phân loại",
    "DECISION_TREE": "Cây quyết định phân nhánh",
    "RANDOM_FOREST": "Rừng ngẫu nhiên ensemble",
    "GRADIENT_BOOST": "Gradient Boosting tối ưu",
    "ENSEMBLE": "Tổng hợp tất cả AI lại",
    "TREND_FOLLOWING": "Theo xu hướng thị trường",
    "MEAN_REVERSION": "Đảo chiều về trung bình",
    "MOMENTUM": "Động lượng tăng tốc",
    "VOLATILITY": "Phân tích biến động",
    "SEASONAL": "Chu kỳ theo mùa",
    "CORRELATION": "Tương quan giữa các NV",
    "CLUSTER": "Phân cụm dữ liệu",
    "ANOMALY": "Phát hiện bất thường",
    "ENTROPY": "Phân tích entropy thông tin",
    "FUZZY_LOGIC": "Logic mờ xử lý bất định",
    "LSTM_PREDICT": "Long Short-Term Memory",
    "TRANSFORMER": "Transformer Attention",
    "ATTENTION": "Cơ chế Attention tập trung",
    "DEEP_Q": "Deep Q-Learning",
    "A3C": "Asynchronous Advantage Actor-Critic",
    "PPO": "Proximal Policy Optimization",
    "GAN": "Generative Adversarial Network",
    "AUTOENCODER": "Autoencoder nén dữ liệu",
    "SWARM_INTEL": "Trí tuệ bầy đàn tối ưu",
    "META_LEARNING": "Học cách học (Meta Learning)",
}

cdtd_settings = {"algo": "ENSEMBLE"}
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

def get_cdtd_available_ai_list(key_type: str = "free") -> List[str]:
    if key_type == "vip":
        return CDTD_FREE_AI_LIST + CDTD_VIP_AI_LIST
    else:
        return CDTD_FREE_AI_LIST

def is_cdtd_ai_available(ai_key: str, key_type: str = "free") -> bool:
    available = get_cdtd_available_ai_list(key_type)
    return ai_key in available

def get_filtered_candidates(data_top10, avoid_count=3):
    last_winner = None
    if data_top10 and len(data_top10) > 1 and data_top10[1]:
        try:
            last_winner = int(data_top10[1][0])
        except:
            pass
    
    recent = list(cdtd_recent_choices)[-avoid_count:] if len(cdtd_recent_choices) >= avoid_count else list(cdtd_recent_choices)
    candidates = [nv for nv in range(1, 7) if nv not in recent and nv != last_winner]
    if not candidates: 
        candidates = [nv for nv in range(1, 7) if nv != last_winner]
    if not candidates: 
        candidates = list(range(1, 7))
    return candidates

def cdtd_execute_ai_logic(mode: str, candidates: List[int], data_top10) -> int:
    mode = mode.upper()
    
    if not is_cdtd_ai_available(mode, _key_type):
        mode = "RANDOM"
    
    data_top100 = top_100_cdtd()
    
    if mode == "RANDOM":
        return random.choice(candidates)
    
    elif mode == "AVOID_LAST":
        if data_top10 and len(data_top10) > 1 and data_top10[1]:
            try:
                last_winner = int(data_top10[1][0])
                filtered = [c for c in candidates if c != last_winner]
                if filtered:
                    return random.choice(filtered)
            except:
                pass
        return random.choice(candidates)
    
    elif mode == "HOT_STREAK":
        if data_top100 and len(data_top100) > 1 and data_top100[1]:
            win_counts = data_top100[1]
            hot_candidates = [c for c in candidates if win_counts[c-1] == max(win_counts[i-1] for i in candidates)]
            if hot_candidates:
                return random.choice(hot_candidates)
        return random.choice(candidates)
    
    elif mode == "COLD_STREAK":
        if data_top100 and len(data_top100) > 1 and data_top100[1]:
            win_counts = data_top100[1]
            cold_candidates = [c for c in candidates if win_counts[c-1] == min(win_counts[i-1] for i in candidates)]
            if cold_candidates:
                return random.choice(cold_candidates)
        return random.choice(candidates)
    
    elif mode == "BALANCE":
        if data_top100 and len(data_top100) > 1 and data_top100[1]:
            win_counts = data_top100[1]
            avg = sum(win_counts) / len(win_counts)
            balanced = [c for c in candidates if abs(win_counts[c-1] - avg) <= 1]
            if balanced:
                return random.choice(balanced)
        return random.choice(candidates)
    
    elif mode == "PATTERN":
        if len(cdtd_bet_history) >= 3:
            recent_winners = [b.get('winner') for b in list(cdtd_bet_history)[-5:] if b.get('winner')]
            if len(recent_winners) >= 3 and recent_winners[-1] == recent_winners[-3]:
                predicted = recent_winners[-2]
                if predicted in candidates:
                    return predicted
        return random.choice(candidates)
    
    elif mode == "PROBABILITY":
        if data_top100 and len(data_top100) > 1 and data_top100[1]:
            win_counts = data_top100[1]
            total = sum(win_counts)
            if total > 0:
                weights = [win_counts[c-1] / total for c in candidates]
                return random.choices(candidates, weights=weights, k=1)[0]
        return random.choice(candidates)
    
    elif mode == "FOLLOW_WINNER":
        if data_top10 and len(data_top10) > 1 and data_top10[1]:
            try:
                last_winner = int(data_top10[1][0])
                if last_winner in candidates:
                    return last_winner
            except:
                pass
        return random.choice(candidates)
    
    elif mode == "ANTI_WINNER":
        if data_top10 and len(data_top10) > 1 and data_top10[1]:
            try:
                last_winner = int(data_top10[1][0])
                filtered = [c for c in candidates if c != last_winner]
                if filtered:
                    return random.choice(filtered)
            except:
                pass
        return random.choice(candidates)
    
    elif mode == "SMART_ANALYSIS":
        scores = {}
        for c in candidates:
            score = 0
            if data_top100 and len(data_top100) > 1 and data_top100[1]:
                score += data_top100[1][c-1] * 0.4
            if data_top10 and len(data_top10) > 1 and data_top10[1]:
                try:
                    if int(data_top10[1][0]) != c:
                        score += 0.6
                except:
                    pass
            scores[c] = score
        if scores:
            return max(scores, key=scores.get)
        return random.choice(candidates)
    
    elif mode == "ENSEMBLE":
        votes = {}
        ai_funcs = [
            lambda: cdtd_execute_ai_logic("RANDOM", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("AVOID_LAST", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("HOT_STREAK", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("COLD_STREAK", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("BALANCE", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("PROBABILITY", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("SMART_ANALYSIS", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("CYCLE_ANALYSIS", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("TREND_ANALYSIS", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("BAYESIAN", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("NEURAL_NETWORK", candidates, data_top10),
            lambda: cdtd_execute_ai_logic("MARKOV_CHAIN", candidates, data_top10),
        ]
        for func in ai_funcs:
            try:
                vote = func()
                votes[vote] = votes.get(vote, 0) + 1
            except:
                continue
        if votes:
            return max(votes, key=votes.get)
        return random.choice(candidates)
    
    return random.choice(candidates)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        try:
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('user-id') and data.get('user-secret-key'):
                    return data
        except:
            pass
    
    console.print(Rule(f"[bold {HTOOL_COLORS['gold']}]📋 NHẬP THÔNG TIN CDTD[/]", style=HTOOL_COLORS["gold"]))
    console.print("1. Truy cập xworld.io\n2. Đăng nhập\n3. Vào Chạy đua tốc độ\n4. Copy link\n")
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN'
    }

def top_100_cdtd():
    try:
        response = cdtd_session.get(
            'https://api.sprintrun.win/sprint/recent_100_issues',
            headers={'accept': '*/*', 'origin': 'https://sprintrun.win', 'referer': 'https://sprintrun.win/', 'user-agent': 'Mozilla/5.0'},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0 and 'data' in data:
                win_times = data['data'].get('athlete_2_win_times', {})
                return [1, 2, 3, 4, 5, 6], [win_times.get(str(i), 0) for i in range(1, 7)]
    except Exception as e:
        safe_console_print(f"[yellow]⚠️ Lỗi top_100: {e}[/yellow]")
    return [1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 0, 0]

def top_10_cdtd():
    try:
        response = cdtd_session.get(
            'https://api.sprintrun.win/sprint/recent_10_issues',
            headers=cdtd_headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0 and 'data' in data:
                recent = data['data'].get('recent_10', [])
                issues = [i['issue_id'] for i in recent]
                results = [i['result'][0] if i.get('result') else 1 for i in recent]
                return issues, results
    except Exception as e:
        safe_console_print(f"[yellow]⚠️ Lỗi top_10: {e}[/yellow]")
    return [0], [1]

def user_asset_cdtd():
    try:
        response = cdtd_session.post(
            'https://wallet.3games.io/api/wallet/user_asset',
            headers=cdtd_headers,
            json={'user_id': int(cdtd_headers.get('user-id', 0)), 'source': 'home'},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0 and 'data' in data:
                user_asset = data['data'].get('user_asset', {})
                return {
                    'USDT': float(user_asset.get('USDT', 0)),
                    'WORLD': float(user_asset.get('WORLD', 0)),
                    'BUILD': float(user_asset.get('BUILD', 0))
                }
    except Exception as e:
        safe_console_print(f"[yellow]⚠️ Lỗi user_asset: {e}[/yellow]")
    return {'USDT': 0, 'WORLD': 0, 'BUILD': 0}

def bet_cdtd(issue_id, nv_id, amount):
    try:
        response = cdtd_session.post(
            'https://api.sprintrun.win/sprint/bet',
            headers=cdtd_headers,
            json={
                'issue_id': int(issue_id),
                'bet_group': 'not_winner',
                'asset_type': cdtd_coin,
                'athlete_id': nv_id,
                'bet_amount': float(amount)
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                return True, "ok"
            else:
                return False, data.get('msg', 'Unknown error')
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

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
┣ 💵 Lãi: <b>{pnl_van:+,.4f}</b> | Tổng: <b>{total_pnl:+,.2f}</b>
┣ 📊 {win_count}W/{lose_count}L ({win_rate:.0f}%) | {bal_start} → {bal_end}
┗ 🔥 Max: 🟢{max_win_streak} 🔴{max_lose_streak} | 🕐 {datetime.now(tz).strftime('%H:%M %d/%m')}"""
    return message

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
    info_table.add_row(f"{ICONS['key']} KEY:", f"[bold {HTOOL_COLORS['gold'] if _key_type == 'vip' else 'white'}]{_key_type.upper()}[/]")
    info_table.add_row(f"{ICONS['brain']} AI:", f"[bold {HTOOL_COLORS['neon_pink']}]{CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')}[/]")
    info_table.add_row(f"{ICONS['clock']} TIME:", f"[{HTOOL_COLORS['sapphire']}]{datetime.now(tz).strftime('%H:%M:%S')}[/]")
    info_table.add_row(f"{ICONS['target']} ISSUE:", f"[bold {HTOOL_COLORS['gold']}]{cdtd_issue_id or 'Waiting...'}[/]")
    info_table.add_row(f"{ICONS['bell']} TG:", f"[{'green' if TELEGRAM_ENABLED else 'dim'}] {'BẬT' if TELEGRAM_ENABLED else 'TẮT'}[/]")
    info_table.add_row(f"🌐 IP:", f"[dim]{_ip_info.get('public_ip', 'N/A')}[/dim]")
    info_table.add_row(f"🛡️ Anti-Detection:", f"[{'green' if _secure_mode else 'dim'}] {'ON' if _secure_mode else 'OFF'}[/]")
    return Panel(Group(Align.center(logo_text), info_table), border_style=HTOOL_COLORS["gold"], box=box.HEAVY, padding=(1, 2))

def build_cdtd_racers():
    data_top100, data_top10 = top_100_cdtd(), top_10_cdtd()
    racer_panels = []
    for i in range(1, 7):
        wins = data_top100[1][i-1] if data_top100 and len(data_top100) > 1 and data_top100[1] else 0
        is_predicted = cdtd_predicted_nv == i
        is_last_winner = False
        if data_top10 and len(data_top10) > 1 and data_top10[1]:
            try:
                is_last_winner = int(data_top10[1][0]) == i
            except:
                pass
        
        if is_predicted:
            border, title_style, bg, glow = f"bold {HTOOL_COLORS['emerald']}", f"bold {HTOOL_COLORS['emerald']}", "on #003300", "✨⭐"
        elif is_last_winner:
            border, title_style, bg, glow = HTOOL_COLORS["gold"], HTOOL_COLORS["gold"], "on #332200", "🏆"
        else:
            border, title_style, bg, glow = HTOOL_COLORS["onyx"], "white", "", ""
        
        content = Text.assemble(
            ("\n", ""),
            (f"{glow} {NV_ICONS[i]}\n", "default"),
            (f"{NV[i]}\n", title_style),
            (f"🏆 {wins} wins", "dim"),
            ("\n", ""),
            justify="center"
        )
        racer_panels.append(Panel(
            Align.center(content, vertical="middle"),
            title=f"[{title_style}]#{i}[/{title_style}]",
            border_style=border,
            box=box.HEAVY,
            expand=True,
            height=6,
            style=bg
        ))
    return Panel(
        Columns(racer_panels, equal=True, expand=True),
        title=f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ CHẠY ĐUA TỐC ĐỘ 🏎️[/]",
        box=box.HEAVY,
        border_style=HTOOL_COLORS["neon_orange"],
        expand=True
    )

def build_cdtd_mid():
    if cdtd_ui_state == "ANALYZING":
        elapsed = time.time() - (cdtd_analysis_start_ts or time.time())
        progress = min(1.0, elapsed / cdtd_analysis_duration)
        bar = "█" * int(30 * progress) + "░" * (30 - int(30 * progress))
        content = Text.assemble(
            ("\n🧠 ĐANG PHÂN TÍCH...\n\n", f"bold {HTOOL_COLORS['neon_blue']}"),
            (f"[{HTOOL_COLORS['gold']}]{bar}[/]\n\n", ""),
            (f"Tiến độ: {progress*100:.0f}%\n", HTOOL_COLORS['neon_pink']),
            (f"⏱️ Còn {max(0, int(cdtd_analysis_duration - elapsed))}s\n", "dim"),
            justify="center"
        )
        return Panel(content, border_style=HTOOL_COLORS["neon_blue"], box=box.HEAVY, expand=True)
    
    elif cdtd_ui_state == "PREDICTED":
        bet_amt = cdtd_current_bet or cdtd_base_bet
        content = Text.assemble(
            ("\n╔══════════════════════════════╗\n", HTOOL_COLORS["gold"]),
            ("║  🎯 DỰ ĐOÁN CỦA BOT  🎯    ║\n", HTOOL_COLORS["gold"]),
            ("║  ", HTOOL_COLORS["gold"]),
            (f"{NV_ICONS.get(cdtd_predicted_nv, '🤖')} {NV.get(cdtd_predicted_nv, 'N/A'):^20}", f"bold {HTOOL_COLORS['emerald']}"),
            ("  ║\n", HTOOL_COLORS["gold"]),
            ("║  💰 Cược: ", HTOOL_COLORS["gold"]),
            (f"{bet_amt:.2f} {cdtd_coin:<10}", f"bold {HTOOL_COLORS['gold']}"),
            ("  ║\n", HTOOL_COLORS["gold"]),
            ("╚══════════════════════════════╝\n", HTOOL_COLORS["gold"]),
            (f"\n📈 Chuỗi thắng: {cdtd_win_streak}  📉 Chuỗi thua: {cdtd_lose_streak}\n", "white"),
            justify="center"
        )
        return Panel(content, border_style=HTOOL_COLORS["emerald"], box=box.HEAVY, expand=True)
    
    elif cdtd_ui_state == "RESULT":
        last_bet = cdtd_bet_history[-1] if cdtd_bet_history else None
        if last_bet and last_bet.get('result') == 'win':
            result_text, result_color, border_color = "🎉 CHIẾN THẮNG! 🎉", HTOOL_COLORS["emerald"], HTOOL_COLORS["emerald"]
        elif last_bet and last_bet.get('result') == 'lose':
            result_text, result_color, border_color = "💀 THUA CUỘC! 💀", HTOOL_COLORS["ruby"], HTOOL_COLORS["ruby"]
        else:
            result_text, result_color, border_color = "⏳ ĐANG CHỜ...", HTOOL_COLORS["gold"], HTOOL_COLORS["gold"]
        
        content = Text.assemble(
            ("\n", ""),
            (f"{result_text}\n\n", f"bold {result_color}"),
            ("Người thắng: ", "white"),
            (f"{NV_ICONS.get(cdtd_last_winner, '🏆')} {NV.get(cdtd_last_winner, 'N/A')}\n", f"bold {HTOOL_COLORS['gold']}"),
            ("\n⏳ Đang chờ kỳ mới...", "dim"),
            justify="center"
        )
        return Panel(content, border_style=border_color, box=box.HEAVY, expand=True)
    
    return Panel(
        Align.center(Text("\n⏳ ĐANG CHỜ DỮ LIỆU...\n\n🔄 Đang kết nối...\n", justify="center")),
        border_style=HTOOL_COLORS["gold"],
        box=box.HEAVY,
        expand=True
    )

def build_cdtd_history():
    t = Table(title=f"[bold {HTOOL_COLORS['gold']}]📜 LỊCH SỬ CƯỢC[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["onyx"])
    t.add_column("Kỳ", style=HTOOL_COLORS["sapphire"], width=6)
    t.add_column("Chọn", style=HTOOL_COLORS["neon_blue"])
    t.add_column("Cược", justify="right", style=HTOOL_COLORS["gold"], width=10)
    t.add_column("KQ")
    
    for b in list(cdtd_bet_history)[-10:]:
        chosen = NV.get(b.get('chosen'), str(b.get('chosen', '-')))
        amount = f"{b.get('amount', 0):.2f}"
        if b.get('result') == 'win':
            result_text = Text("✅ THẮNG", style=f"bold {HTOOL_COLORS['emerald']}")
        elif b.get('result') == 'lose':
            result_text = Text("❌ THUA", style=f"bold {HTOOL_COLORS['ruby']}")
        else:
            result_text = Text("⏳", style=HTOOL_COLORS["gold"])
        t.add_row(str(b.get('issue', '-')), chosen, amount, result_text)
    
    return Panel(t, border_style=HTOOL_COLORS["sapphire"], box=box.HEAVY, expand=True)

def build_cdtd_stats():
    data_top100 = top_100_cdtd()
    t = Table(title=f"[bold {HTOOL_COLORS['neon_blue']}]📊 THỐNG KÊ 100 VÁN[/]", box=box.ROUNDED, expand=True, border_style=HTOOL_COLORS["neon_blue"])
    t.add_column("NV", style=HTOOL_COLORS["gold"], width=4)
    t.add_column("Tên", style="white")
    t.add_column("Thắng", justify="right", style=HTOOL_COLORS["emerald"], width=8)
    t.add_column("Tỷ lệ", justify="right", style=HTOOL_COLORS["neon_pink"], width=8)
    
    total_wins = sum(data_top100[1]) if data_top100 and len(data_top100) > 1 and data_top100[1] else 1
    for i in range(6):
        wins = data_top100[1][i] if data_top100 and len(data_top100) > 1 and data_top100[1] else 0
        t.add_row(
            f"{NV_ICONS.get(i+1, '🏆')}",
            NV.get(i+1, f'NV{i+1}'),
            str(wins),
            f"{wins/total_wins*100:.1f}%"
        )
    
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
    
    return Panel(
        Columns([t, summary], equal=True, expand=True),
        border_style=HTOOL_COLORS["gold"],
        box=box.HEAVY,
        expand=True
    )

def build_cdtd_marquee():
    messages = [
        f"⚡ CDTD - 42 AI {ICONS['rocket']}",
        f"🧠 {CDTD_ALGORITHMS.get(cdtd_settings.get('algo', 'RANDOM'), 'N/A')} {ICONS['robot']}",
        f"💰 {cdtd_coin} | Cược: {cdtd_base_bet} | x{cdtd_multiplier}",
        f"🎯 W:{cdtd_stats['win']} L:{cdtd_stats['lose']} {ICONS['chart']}",
        f"🔑 Key: {_key_type.upper()} | AI: {len(get_cdtd_available_ai_list(_key_type))}/42",
    ]
    message = messages[int(time.time() / 5) % len(messages)]
    full_text = " " * 20 + message + " " * 20
    width = console.width or 80
    display_text = (full_text * 3)[int(time.time() * 3) % len(full_text) : int(time.time() * 3) % len(full_text) + width]
    return Panel(
        Text(display_text, style=f"bold {HTOOL_COLORS['neon_blue']}", no_wrap=True),
        box=box.ROUNDED,
        border_style=HTOOL_COLORS["onyx"],
        padding=0,
        expand=True
    )

def cdtd_generate_layout():
    main_grid = Table.grid(expand=True, pad_edge=False)
    main_grid.add_column("main", ratio=55)
    main_grid.add_column("side", ratio=45)
    
    right_grid = Table.grid(expand=True, pad_edge=False)
    right_grid.add_row(build_cdtd_mid())
    right_grid.add_row(build_cdtd_history())
    
    main_grid.add_row(build_cdtd_racers(), right_grid)
    
    root = Table.grid(expand=True, pad_edge=False)
    root.add_row(build_cdtd_header())
    root.add_row(build_cdtd_marquee())
    root.add_row(main_grid)
    root.add_row(build_cdtd_stats())
    
    return root

def cdtd_prompt_settings():
    global cdtd_base_bet, cdtd_multiplier, cdtd_coin, cdtd_current_bet, cdtd_pause_rounds, cdtd_bet_rounds_before_skip, cdtd_settings, _key_type
    
    console.clear()
    header = Panel(
        Align.center(Text.assemble(
            (f"{ICONS['settings']} ", f"bold {HTOOL_COLORS['gold']}"),
            ("CẤU HÌNH CHẠY ĐUA TỐC ĐỘ", f"bold {HTOOL_COLORS['neon_blue']}")
        )),
        border_style=HTOOL_COLORS["gold"],
        box=box.DOUBLE
    )
    console.print(header)
    console.print()
    
    key_info = Panel(
        Text.assemble(
            (f"🔑 Loại Key: ", "white"),
            (f"{_key_type.upper()}\n", "bold gold" if _key_type == "vip" else "bold white"),
            (f"📊 Số AI có thể dùng: ", "white"),
            (f"{len(get_cdtd_available_ai_list(_key_type))}/42\n", "bold cyan"),
            (f"{'⭐ Bạn đang sử dụng KEY VIP - Full 42 AI' if _key_type == 'vip' else '🔓 Bạn đang sử dụng KEY FREE - Chỉ 12 AI cơ bản'}",
             "bold gold" if _key_type == "vip" else "dim")
        ),
        title="[bold]THÔNG TIN KEY - CDTD[/bold]",
        border_style=HTOOL_COLORS["gold"],
        box=box.ROUNDED
    )
    console.print(key_info)
    console.print()
    
    coin_choice = Prompt.ask(
        f"[bold {HTOOL_COLORS['gold']}]💰 Chọn tiền: [1] USDT [2] BUILD [3] WORLD[/]\n   >>",
        choices=['1', '2', '3'],
        default='2'
    )
    cdtd_coin = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}[coin_choice]
    
    cdtd_base_bet = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]💵 Cược gốc ({cdtd_coin})[/]\n   >>", default=1.0)
    cdtd_multiplier = FloatPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]📈 Hệ số nhân[/]\n   >>", default=2.0)
    cdtd_current_bet = cdtd_base_bet
    cdtd_bet_rounds_before_skip = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]🛡️ Nghỉ 1 ván sau N ván (0=không)[/]\n   >>", default=0)
    cdtd_pause_rounds = IntPrompt.ask(f"\n[bold {HTOOL_COLORS['gold']}]⏸️ Nghỉ N ván sau khi thua (0=không)[/]\n   >>", default=0)
    
    console.clear()
    console.print(header)
    
    available_ai = get_cdtd_available_ai_list(_key_type)
    console.print(f"\n[bold {HTOOL_COLORS['neon_pink']}]🧠 Chọn AI ({len(available_ai)} AI khả dụng):[/]\n")
    
    algo_table = Table(box=box.ROUNDED, border_style=HTOOL_COLORS["neon_pink"])
    algo_table.add_column("#", style=HTOOL_COLORS["gold"], width=4)
    algo_table.add_column("Thuật toán", style=HTOOL_COLORS["neon_blue"])
    algo_table.add_column("Loại", style="dim", width=8)
    algo_table.add_column("Mô tả", style="dim")
    
    for i, ai_key in enumerate(available_ai, 1):
        label = CDTD_ALGORITHMS.get(ai_key, ai_key)
        desc = CDTD_AI_DESCRIPTIONS.get(ai_key, "")
        ai_type = "🆓 FREE" if ai_key in CDTD_FREE_AI_LIST else "👑 VIP"
        algo_table.add_row(str(i), label, ai_type, desc)
    
    console.print(algo_table)
    console.print()
    
    if _key_type == "free":
        console.print("[dim]🔓 Key Free: Chỉ được sử dụng 12 AI cơ bản (đánh dấu 🆓)[/dim]")
        console.print("[dim]💡 Nâng cấp lên VIP để mở khóa 30 AI cao cấp còn lại[/dim]")
    else:
        console.print("[bold gold]👑 Key VIP: Sử dụng toàn bộ 42 AI[/bold gold]")
    
    console.print()
    algo_choice = IntPrompt.ask(
        f"[bold {HTOOL_COLORS['gold']}]>> Chọn số thứ tự (1-{len(available_ai)})[/bold {HTOOL_COLORS['gold']}]",
        choices=[str(i) for i in range(1, len(available_ai) + 1)],
        default=1
    )
    
    cdtd_settings["algo"] = available_ai[algo_choice - 1]
    console.print(f'\n[green]✅ Đã chọn: {CDTD_ALGORITHMS[cdtd_settings["algo"]]}[/]')
    console.print(f'[dim]   Mô tả: {CDTD_AI_DESCRIPTIONS.get(cdtd_settings["algo"], "")}[/]')
    
    console.print(f"\n[bold {HTOOL_COLORS['gold']}]📱 Cấu hình Telegram? (y/n)[/]")
    if Prompt.ask("   >>", choices=['y', 'n'], default='n') == 'y':
        setup_telegram()
    
    console.print(f'\n[green]✅ Cấu hình hoàn tất![/]')
    time.sleep(1.5)
    return True

def cdtd_game_loop():
    global cdtd_issue_id, cdtd_previous_issue, cdtd_last_winner, cdtd_predicted_nv, cdtd_ui_state, cdtd_analysis_start_ts
    global cdtd_current_bet, cdtd_win_streak, cdtd_lose_streak, cdtd_max_win_streak, cdtd_max_lose_streak, cdtd_stop_flag
    global cdtd_stats, cdtd_pause_remaining, cdtd_skip_next, cdtd_rounds_placed, cdtd_bet_placed_this_round, cdtd_checked_result
    global cdtd_recent_choices, cdtd_avoid_repeat
    
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
    cdtd_recent_choices.clear()
    cdtd_avoid_repeat = 3
    cdtd_stats = {'win': 0, 'lose': 0, 'asset_0': user_asset_cdtd().get(cdtd_coin, 0)}
    
    with Live(cdtd_generate_layout(), refresh_per_second=3, console=console, screen=True) as live:
        while not cdtd_stop_flag:
            try:
                data_top10 = top_10_cdtd()
                if not data_top10 or len(data_top10) < 1:
                    time.sleep(1)
                    continue
                    
                current_issue = data_top10[0][0] if data_top10[0] else None
                
                if current_issue and current_issue != cdtd_previous_issue:
                    if cdtd_previous_issue is not None and cdtd_predicted_nv is not None and not cdtd_checked_result:
                        try:
                            winner = int(data_top10[1][0]) if data_top10 and len(data_top10) > 1 and data_top10[1] else None
                            if winner is not None:
                                cdtd_last_winner = winner
                                balance_before = user_asset_cdtd().get(cdtd_coin, 0)
                                result_type = 'win'
                                
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
                                            result_type = 'win'
                                        else:
                                            b['result'] = 'lose'
                                            cdtd_lose_streak += 1
                                            cdtd_win_streak = 0
                                            cdtd_max_lose_streak = max(cdtd_max_lose_streak, cdtd_lose_streak)
                                            cdtd_current_bet *= cdtd_multiplier
                                            cdtd_stats['lose'] += 1
                                            result_type = 'lose'
                                            if cdtd_pause_rounds > 0:
                                                cdtd_pause_remaining = cdtd_pause_rounds
                                
                                time.sleep(1)
                                balance_after = user_asset_cdtd().get(cdtd_coin, 0)
                                pnl_van = balance_after - balance_before
                                total_pnl = balance_after - cdtd_stats['asset_0']
                                
                                if TELEGRAM_ENABLED and TELEGRAM_CHAT_ID and cdtd_bet_history:
                                    bet_nv = cdtd_predicted_nv
                                    bet_amount = cdtd_bet_history[-1].get('amount', 0) if cdtd_bet_history else cdtd_base_bet
                                    telegram_msg = build_cdtd_telegram_message(
                                        cdtd_previous_issue, winner, bet_nv, bet_amount,
                                        result_type, pnl_van, total_pnl,
                                        balance_before, balance_after,
                                        cdtd_stats['win'], cdtd_stats['lose'],
                                        cdtd_max_win_streak, cdtd_max_lose_streak
                                    )
                                    threading.Thread(target=send_telegram_message, args=(telegram_msg,), daemon=True).start()
                                
                                cdtd_checked_result = True
                                cdtd_ui_state = "RESULT"
                                live.update(cdtd_generate_layout())
                                time.sleep(2)
                        except Exception as e:
                            safe_console_print(f"[yellow]⚠️ Lỗi xử lý kết quả: {e}[/yellow]")
                    
                    cdtd_previous_issue = current_issue
                    cdtd_issue_id = current_issue
                    cdtd_predicted_nv = None
                    cdtd_bet_placed_this_round = False
                    cdtd_checked_result = False
                    cdtd_analysis_start_ts = time.time()
                    cdtd_ui_state = "ANALYZING"
                    live.update(cdtd_generate_layout())
                
                if cdtd_ui_state == "ANALYZING":
                    elapsed = time.time() - (cdtd_analysis_start_ts or time.time())
                    if elapsed >= cdtd_analysis_duration - 8 and not cdtd_bet_placed_this_round:
                        mode = cdtd_settings.get("algo", "ENSEMBLE")
                        
                        if not is_cdtd_ai_available(mode, _key_type):
                            mode = "RANDOM"
                        
                        candidates = get_filtered_candidates(data_top10, cdtd_avoid_repeat)
                        chosen = cdtd_execute_ai_logic(mode, candidates, data_top10)
                        
                        cdtd_recent_choices.append(chosen)
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
                        
                        if should_bet and cdtd_issue_id is not None:
                            next_issue = cdtd_issue_id + 1
                            bet_amount = cdtd_current_bet if cdtd_current_bet else cdtd_base_bet
                            asset = user_asset_cdtd()
                            if bet_amount > asset.get(cdtd_coin, 0):
                                cdtd_current_bet = cdtd_base_bet
                                bet_amount = cdtd_base_bet
                            
                            success, msg = bet_cdtd(next_issue, chosen, bet_amount)
                            if success:
                                cdtd_bet_history.append({
                                    'issue': next_issue,
                                    'chosen': chosen,
                                    'amount': bet_amount,
                                    'result': 'pending',
                                    'algo': mode
                                })
                                cdtd_rounds_placed += 1
                                cdtd_bet_placed_this_round = True
                                if cdtd_bet_rounds_before_skip > 0 and cdtd_rounds_placed >= cdtd_bet_rounds_before_skip:
                                    cdtd_skip_next = True
                                    cdtd_rounds_placed = 0
                            else:
                                safe_console_print(f"[red]❌ Đặt cược thất bại: {msg}[/red]")
                        
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
            except Exception as e:
                safe_console_print(f"[yellow]⚠️ Lỗi CDTD: {e}[/yellow]")
                time.sleep(3)

def main_cdtd_v3():
    console.clear()
    header = Panel(
        Align.center(Text.assemble(
            (f"{ICONS['rocket']} ", f"bold {HTOOL_COLORS['gold']}"),
            ("CHẠY ĐUA TỐC ĐỘ - 42 AI", f"bold {HTOOL_COLORS['neon_blue']}")
        )),
        border_style=HTOOL_COLORS["gold"],
        box=box.DOUBLE
    )
    console.print(header)
    console.print(f"[dim]💬 Support: @htool88 | 42 AI | Auto Né Lặp | Telegram[/dim]\n")
    
    data = load_data_cdtd()
    setup_cdtd_headers(data)
    
    if not cdtd_prompt_settings():
        return
    
    console.clear()
    console.print(f"[bold {HTOOL_COLORS['neon_orange']}]🏎️ KHỞI ĐỘNG VỚI {len(get_cdtd_available_ai_list(_key_type))} AI...[/]")
    
    with console.status(f"[bold {HTOOL_COLORS['gold']}]🔍 Đang kiểm tra...[/]", spinner="dots"):
        asset = user_asset_cdtd()
        time.sleep(1)
    
    if asset.get(cdtd_coin, 0) <= 0:
        console.print(f'[red]❌ Số dư {cdtd_coin} = 0![/]')
        time.sleep(2)
        return
    
    console.print(f'[green]✅ Số dư: {asset[cdtd_coin]:.4f} {cdtd_coin}[/]')
    console.print(f'[green]✅ {len(get_cdtd_available_ai_list(_key_type))} AI sẵn sàng (Key {_key_type.upper()})[/]')
    console.print(f'[green]✅ Tự động né lặp {cdtd_avoid_repeat} ván[/]')
    if TELEGRAM_ENABLED:
        console.print(f'[green]✅ Telegram: BẬT[/]')
    
    time.sleep(2)
    cdtd_game_loop()
    
    console.clear()
    final_asset = user_asset_cdtd()
    pnl = final_asset.get(cdtd_coin, 0) - cdtd_stats['asset_0']
    summary = Panel(
        Align.center(Text.assemble(
            ("\n📊 TỔNG KẾT\n\n", f"bold {HTOOL_COLORS['gold']}"),
            (f"Thắng: {cdtd_stats['win']} | Thua: {cdtd_stats['lose']}\n", "white"),
            (f"P&L: {pnl:+.4f} {cdtd_coin}\n", HTOOL_COLORS["gold"] if pnl >= 0 else HTOOL_COLORS["ruby"])
        )),
        border_style=HTOOL_COLORS["gold"],
        box=box.DOUBLE
    )
    console.print(summary)
    console.print("\n[dim]Nhấn Enter để quay lại menu...[/]")
    input()

# ================== MAIN MENU ==================

def build_main_menu():
    global _in_menu, _ws_status, _secure_mode
    _in_menu = True
    console.clear()
    logo_text = build_logo_with_gradient(LOGO)
    console.print(Align.center(logo_text))
    
    console.print()
    menu_panel = Panel(Align.center(Text.assemble(
        ("\n", ""),
        (f"  {ICONS['crown']}  ", f"bold {HTOOL_COLORS['gold']}"),
        ("HTOOL VIP PREMIUM v3.0", f"bold {HTOOL_COLORS['neon_blue']}"),
        (f"  {ICONS['crown']}  ", f"bold {HTOOL_COLORS['gold']}"),
        ("\n", ""),
        ("╔════════════════════════════════════════════════════════════╗\n", f"dim {HTOOL_COLORS['gold']}"),
        ("║  [1]  🎯  VUA THOÁT HIỂM - PLAY & CONFIG                ║\n", f"bold {HTOOL_COLORS['neon_green']}"),
        ("║       ➜ Chọn tài khoản và thiết lập chiến lược chơi      ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [2]  🏎️  CHẠY ĐUA TỐC ĐỘ (42 AI)                       ║\n", f"bold {HTOOL_COLORS['neon_orange']}"),
        ("║       ➜ Tool tự động chơi Chạy đua tốc độ                ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [3]  ➕  ADD ACCOUNT                                    ║\n", f"bold {HTOOL_COLORS['sapphire']}"),
        ("║       ➜ Thêm tài khoản mới vào danh sách                 ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [4]  🗑️  DELETE ACCOUNT                                 ║\n", f"bold {HTOOL_COLORS['ruby']}"),
        ("║       ➜ Xóa tài khoản khỏi danh sách                     ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [5]  ⚙️  SAVE CONFIG                                    ║\n", f"bold {HTOOL_COLORS['gold']}"),
        ("║       ➜ Lưu cấu hình hiện tại để dùng sau                ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [6]  🚀  PLAY WITH CONFIG                               ║\n", f"bold {HTOOL_COLORS['neon_pink']}"),
        ("║       ➜ Chơi ngay với cấu hình đã lưu                    ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [7]  🛡️  ANTI-DETECTION STATUS                          ║\n", f"bold {HTOOL_COLORS['emerald']}"),
        ("║       ➜ Xem trạng thái chống soi                        ║\n", "dim"),
        ("║                                                          ║\n", "dim"),
        ("║  [q]  👋  EXIT                                           ║\n", f"bold {HTOOL_COLORS['rose']}"),
        ("║       ➜ Thoát chương trình                               ║\n", "dim"),
        ("╚════════════════════════════════════════════════════════════╝\n", f"dim {HTOOL_COLORS['gold']}"),
        ("\n", ""),
        (f"  💬  Support: @htool88  |  Version: 3.0 Enhanced + Anti-Detection\n", f"bold {HTOOL_COLORS['neon_blue']}"),
        (f"  🔗  WebSocket: {_ws_status}\n", "dim"),
        (f"  🌐  IP: {_ip_info.get('public_ip', 'N/A')}\n", "dim"),
        (f"  🛡️  Anti-Detection: {'✅ ON' if _secure_mode else '❌ OFF'}\n", "dim"),
        ("\n", ""),
    )), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE, padding=(1, 2))
    console.print(menu_panel)
    console.print()
    choice = Prompt.ask(f"[bold {HTOOL_COLORS['gold']}]>> Enter your choice[/bold {HTOOL_COLORS['gold']}]", 
                        choices=['1','2','3','4','5','6','7','q'], default='q').lower()
    return choice

# ================== MAIN ==================

def main_vth():
    global _in_menu, _is_authenticated, _user_key, _key_type, _ws_status, _ip_info, _secure_mode
    
    if not anti_crack_check():
        console.print("[red]❌ Tool bị chặn do phát hiện can thiệp![/red]")
        sys.exit(1)
    
    while not _is_authenticated:
        success, key, key_type = show_auth_screen()
        if success:
            _is_authenticated = True
            _user_key = key
            _key_type = key_type
            start_heartbeat()
            break
        else:
            console.print()
            retry = Prompt.ask(
                "[bold yellow]Bạn có muốn thử lại không? (y/n)[/bold yellow]",
                choices=['y', 'n'],
                default='y'
            )
            if retry.lower() == 'n':
                console.print("[red]👋 Tạm biệt![/red]")
                sys.exit(0)
    
    console.clear()
    welcome = Panel(Align.center(Text.assemble(
        (f"{ICONS['crown']} ", f"bold {HTOOL_COLORS['gold']}"),
        ("WELCOME TO ", "bold white"),
        ("HTOOL VIP PREMIUM v3.0", f"bold {HTOOL_COLORS['neon_blue']}"),
        (f" {ICONS['crown']}", f"bold {HTOOL_COLORS['gold']}")
    )), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE)
    console.print(welcome)
    console.print(f"[dim]💬 Support: @htool88 | Version 3.0 Enhanced + Anti-Detection[/dim]")
    console.print(f"[dim]🔑 Đã xác thực với key: {_user_key} ({_key_type.upper()})[/dim]")
    console.print(f"[dim]🔒 Anti-Crack: Đã kích hoạt[/dim]")
    console.print(f"[dim]🌐 IP Security: Đã kích hoạt - {_ip_info.get('public_ip', 'N/A')}[/dim]")
    console.print(f"[dim]🛡️ Anti-Detection: {'✅ BẬT' if _secure_mode else '❌ TẮT'}[/dim]")
    console.print(f"[dim]🧠 Số AI khả dụng: {len(get_available_ai_list(_key_type))}/42[/dim]")
    console.print()
    time.sleep(1)
    
    while True:
        global stop_flag
        stop_flag = False

        if not require_valid_auth():
            console.print("[bold red]🔒 Key đã mất hiệu lực hoặc bị vô hiệu hóa![/bold red]")
            stop_heartbeat()
            time.sleep(1.5)
            break

        choice = build_main_menu()
        if choice == '1':
            console.clear()
            if select_account_premium():
                if prompt_settings():
                    start_game_flow()
        elif choice == '2':
            try:
                main_cdtd_v3()
            except Exception as e:
                console.print(f"[red]❌ Lỗi khi chạy Chạy đua tốc độ: {e}[/red]")
                time.sleep(2)
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
        elif choice == '7':
            console.clear()
            if _secure_tool:
                _secure_tool.display_status()
            else:
                console.print("[yellow]⚠️ Chế độ chống soi chưa được bật![/yellow]")
            time.sleep(3)
        elif choice == 'q':
            stop_heartbeat()
            console.print(Panel(Align.center(Text.assemble((f"{ICONS['crown']} ", "bold gold"), ("THANK YOU FOR USING HTOOL VIP PREMIUM!", "bold white"), (f" {ICONS['crown']}", "bold gold"))), border_style=HTOOL_COLORS["gold"], box=box.DOUBLE))
            break

if __name__ == "__main__":
    # Tạo file cấu hình proxy nếu chưa có
    if not os.path.exists('proxy_list.txt'):
        sample_proxies = [
            "# Danh sách proxy - Thay bằng proxy thật của bạn",
            "# Định dạng: ip:port hoặc http://user:pass@ip:port",
            "# Ví dụ:",
            "# 123.456.789.0:8080",
            "# http://user:pass@123.456.789.0:8080",
            "# socks5://user:pass@123.456.789.0:1080",
            "",
            "# ===== HTTP PROXIES =====",
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080",
            "",
            "# ===== SOCKS5 PROXIES =====",
            "socks5://proxy4.example.com:1080",
            "socks5://proxy5.example.com:1080",
        ]
        with open('proxy_list.txt', 'w', encoding='utf-8') as f:
            for line in sample_proxies:
                f.write(f"{line}\n")
        print("[green]✅ Đã tạo file proxy_list.txt[/green]")
        print("[yellow]💡 Thay thế proxy mẫu bằng proxy thật để hiệu quả hơn![/yellow]")
        print()
    
    try:
        main_vth()
    except KeyboardInterrupt:
        stop_heartbeat()
        console.print(f"\n[bold {HTOOL_COLORS['gold']}]Đã dừng. {ICONS['crown']}[/bold {HTOOL_COLORS['gold']}]")
        sys.exit(0)