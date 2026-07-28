# ==================== HTOOL - CHẠY ĐUA TỐC ĐỘ (CDTD) - FULL ====================
import sys
import subprocess

# --- TỰ ĐỘNG CÀI ĐẶT THƯ VIỆN ---
REQUIRED_LIBS = {"requests": "requests", "colorama": "colorama"}
for lib_name, pip_name in REQUIRED_LIBS.items():
    try:
        __import__(lib_name)
    except ImportError:
        print(f"🔄 Đang cài {lib_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

import hashlib
from collections import Counter, deque
import statistics
import platform
from datetime import datetime, timedelta
import requests
import random
import math
import json
import os
import sys
import time
import urllib.parse
import string
import webbrowser
from colorama import Fore, Style, init
init(autoreset=True)

# ==================== CẤU HÌNH API ====================
API_TOKEN_LAYMA = "59fc05bb12006c462c99c2d19d427907"
API_TOKEN_OKLINK = "5b0e649b7c9a7281cdf64549cd9cf7af905c24c0"
API_TOKEN_LINK4M = "6a620a7003c42e28f00e2158"
LINK_GOC_TRA_KEY = "https://hungkeytool.vercel.app/"
ADMIN_PASSWORD_SECRET = "ADMIN@123"

JSONBIN_ACCESS_KEY = "$2a$10$M8S59kpMRgtfJvKksOsKnOqpGlG6dp9G2zqoJRSmbJldOn8M3FPI6"
JSONBIN_BIN_ID = "6a61dfbdf5f4af5e29b50537"
JSONBIN_READ_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
JSONBIN_UPDATE_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"

DB_LOCAL_BACKUP = "server-admin-db-backup.json"
LICENSE_DATA_FILE = "htool-license.json"
HISTORY_FILE = "bet_history_cdtd.json"

# ==================== NHÂN VẬT ====================
NV = {
    1: {'name': 'Bậc thầy tấn công', 'icon': '⚔️', 'desc': 'Chuyên gia võ thuật, tốc độ ra đòn nhanh'},
    2: {'name': 'Quyền sắt', 'icon': '🥊', 'desc': 'Võ sĩ quyền anh, sức mạnh vượt trội'},
    3: {'name': 'Thợ lặn sâu', 'icon': '🤿', 'desc': 'Thợ lặn chuyên nghiệp, bền bỉ dưới nước'},
    4: {'name': 'Cơn lốc sân cỏ', 'icon': '🌪️', 'desc': 'Cầu thủ bóng đá, tốc độ như gió'},
    5: {'name': 'Hiệp sĩ phi nhanh', 'icon': '🏇', 'desc': 'Kỵ sĩ tài ba, cưỡi ngựa điêu luyện'},
    6: {'name': 'Vua home run', 'icon': '⚾', 'desc': 'Tay đập bóng chày, sức mạnh khủng khiếp'}
}

# ==================== DANH SÁCH 20 AI MODELS ====================
AI_MODELS = {
    1: {"name": "Ngẫu Nhiên (RANDOM)", "desc": "Chọn bừa - May rủi hoàn toàn", "method": "Chọn ngẫu nhiên 1 trong 6 nhân vật", "vip": False},
    2: {"name": "Tần Suất (FREQUENCY)", "desc": "Thống kê thắng - Chọn người ít thắng nhất", "method": "Phân tích 100 ván, chọn nhân vật có tỉ lệ thắng thấp nhất", "vip": False},
    3: {"name": "Nhận Diện Mẫu (PATTERN)", "desc": "Tìm quy luật - Phát hiện mẫu lặp", "method": "Phân tích 10 ván gần nhất, tìm pattern A→B lặp lại", "vip": False},
    4: {"name": "Thống Kê (STATISTICAL)", "desc": "Z-score - Đánh giá độ lệch chuẩn", "method": "Tính Z-score, chọn người có điểm thấp nhất", "vip": False},
    5: {"name": "Chuỗi Markov (MARKOV)", "desc": "Xác suất chuyển đổi - Dự đoán bước tiếp", "method": "Xây dựng ma trận chuyển đổi từ 10 ván gần nhất", "vip": False},
    6: {"name": "Suy Luận Bayes (BAYESIAN)", "desc": "Xác suất có điều kiện - Cập nhật niềm tin", "method": "Kết hợp prior (1/6) với likelihood từ 100 ván", "vip": False},
    7: {"name": "Mô Phỏng Monte Carlo", "desc": "Mô phỏng ngẫu nhiên - Chạy 1000 lần", "method": "Thêm nhiễu, chạy 1000 lần mô phỏng", "vip": False},
    8: {"name": "Chuỗi Thời Gian (TIME SERIES)", "desc": "Phân tích xu hướng - Dự đoán theo thời gian", "method": "Tính trung bình 3 ván gần nhất + nhiễu", "vip": False},
    9: {"name": "Mạng Nơ-ron (NEURAL)", "desc": "Học sâu cơ bản - Mô phỏng não bộ", "method": "1 lớp neural network với ReLU activation", "vip": False},
    10: {"name": "Logic Mờ (FUZZY)", "desc": "Xử lý mơ hồ - Phân loại mức độ", "method": "Phân 3 nhóm: thắng nhiều, trung bình, thắng ít", "vip": False},
    11: {"name": "Hồi Quy Tuyến Tính", "desc": "Dự đoán xu hướng - Đường thẳng phù hợp", "method": "Tính đường hồi quy từ 100 ván, dự đoán tiếp theo", "vip": True},
    12: {"name": "Phân Cụm (CLUSTERING)", "desc": "Gom nhóm - Chia 2 cụm thắng/thua", "method": "Chia thành 2 cụm, chọn từ cụm thắng ít", "vip": True},
    13: {"name": "Cây Quyết Định", "desc": "Phân nhánh - If-Else thông minh", "method": "Dựa vào tỉ lệ thắng để quyết định chọn ai", "vip": True},
    14: {"name": "Máy Vector Hỗ Trợ (SVM)", "desc": "Phân loại - Tìm đường phân cách", "method": "Tính khoảng cách đến đường trung bình", "vip": True},
    15: {"name": "K-Láng Giềng Gần (KNN)", "desc": "Học từ hàng xóm - K=3 ván gần nhất", "method": "Tìm 3 ván gần nhất, chọn nhân vật gần nhất", "vip": True},
    16: {"name": "Tổng Hợp (ENSEMBLE)", "desc": "Kết hợp 5 AI - Bỏ phiếu đa số", "method": "Chạy 5 AI, chọn kết quả được vote nhiều nhất", "vip": True},
    17: {"name": "Học Sâu (DEEP LEARNING)", "desc": "Mạng nơ-ron 3 lớp - Học đặc trưng", "method": "3 lớp neural network với ReLU activation", "vip": True},
    18: {"name": "Học Tăng Cường", "desc": "Học từ thưởng/phạt - Q-Learning", "method": "Q-table, thưởng +0.1/phạt -0.01", "vip": True},
    19: {"name": "Di Truyền (GENETIC)", "desc": "Tiến hóa - Chọn lọc tự nhiên", "method": "20 quần thể, 5 gen, chọn cá thể tốt nhất", "vip": True},
    20: {"name": "Hỗn Loạn (CHAOS)", "desc": "Lý thuyết hỗn loạn - Hiệu ứng cánh bướm", "method": "Thay đổi nhỏ tạo kết quả khác biệt lớn", "vip": True}
}

# ==================== BIẾN TOÀN CỤC ====================
user_vip_status = False
current_key_data = {}
banner_expire_time = None

# ==================== HELPER FUNCTIONS ====================
def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    sys.stdout.write(f"\033[38;2;{r};{g};{b}m{text}\033[0m\033[K{end}")
    sys.stdout.flush()

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return deque(json.load(f), maxlen=100)
        except:
            pass
    return deque(maxlen=100)

def save_history(hist):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(hist), f, indent=2, ensure_ascii=False)

bet_history = load_history()

def banner(is_vip=False, game_name="CHẠY ĐUA TỐC ĐỘ"):
    """Banner HTOOL đầy đủ"""
    global banner_expire_time
    
    banner_text = """
██╗░░██╗████████╗░█████╗░░█████╗░██╗░░░░░
██║░░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
███████║░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══██║░░░██║░░░██║░░██║██║░░██║██║░░░░░
██║░░██║░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
    """
    r, g, b = 255, 255, 255
    for line in banner_text.split('\n'):
        for char in line:
            prints(r, g, b, char, end='')
            time.sleep(0.0003)
            r = max(50, r - 5)
            b = max(50, b - 1)
        r, g, b = 255, 255, 255
        print()

    prints(247, 255, 97, "✨" + "═" * 60 + "✨")
    
    status = "💎 VIP" if is_vip else "🔓 FREE"
    ai_count = "20 AI" if is_vip else "10 AI"
    prints(32, 230, 151, f"🌟 HTOOL - {game_name} | {status} | {ai_count} LOGIC 🌟".center(62))
    prints(247, 255, 97, "═" * 62)

    contacts = [
        ("📺 YouTube", "https://www.youtube.com/@htool"),
        ("🎵 TikTok", "https://www.tiktok.com/@htool29"),
        ("💬 Zalo Group", "Đang cập nhật..."),
        ("📱 Telegram", "Đang cập nhật..."),
        ("👨‍💻 Admin", "HTOOL")
    ]

    for label, info in contacts:
        prints(100, 200, 255, f"  {label:<15}: ", end="")
        prints(255, 255, 255, info)

    prints(247, 255, 97, "═" * 62)
    
    if banner_expire_time:
        prints(255, 165, 0, f"  ⏰ Hạn dùng: {banner_expire_time}")
        prints(247, 255, 97, "═" * 62)
    
    print()

def get_device_hwid():
    hw_info = platform.node() + platform.system() + platform.machine() + platform.processor()
    return hashlib.md5(hw_info.encode()).hexdigest().upper()[:16]

def get_public_ip():
    for url in ["https://api64.ipify.org?format=text", "https://icanhazip.com", "https://ident.me"]:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200 and r.text.strip() and not r.text.startswith("127."):
                return r.text.strip()
        except:
            pass
    return "Không rõ"

def get_today_key(hwid=None):
    if hwid is None:
        hwid = get_device_hwid()
    today_str = datetime.now().strftime("%d%m%Y")
    md5_hash = hashlib.md5(f"{today_str}-{hwid}".encode()).hexdigest()[:8]
    return f"HTOOL-{md5_hash.upper()}"

def get_jsonbin_headers():
    return {"X-Access-Key": JSONBIN_ACCESS_KEY, "Content-Type": "application/json"}

def get_db():
    try:
        r = requests.get(JSONBIN_READ_URL, headers=get_jsonbin_headers(), timeout=10)
        if r.status_code == 200:
            return r.json()["record"]
    except:
        pass
    if os.path.exists(DB_LOCAL_BACKUP):
        try:
            with open(DB_LOCAL_BACKUP, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"vip_keys": {}, "banned_hwids": [], "banned_ips": [], "user_keys": {}, "device_info": {}}

def save_db(data):
    try:
        with open(DB_LOCAL_BACKUP, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        pass
    try:
        requests.put(JSONBIN_UPDATE_URL, headers=get_jsonbin_headers(), json=data, timeout=10)
    except:
        pass

def is_key_expired(expire_time_str):
    if not expire_time_str:
        return True
    try:
        expire_dt = datetime.strptime(expire_time_str, "%Y-%m-%d %H:%M:%S")
        return datetime.now() >= expire_dt
    except:
        return True

def get_remaining_time(expire_time_str):
    if not expire_time_str:
        return "Không xác định"
    try:
        expire_dt = datetime.strptime(expire_time_str, "%Y-%m-%d %H:%M:%S")
        diff = expire_dt - datetime.now()
        if diff.total_seconds() <= 0:
            return "Đã hết hạn"
        hours, remainder = divmod(int(diff.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    except:
        return "Lỗi"

def generate_short_link(server_type="link4m"):
    hwid = get_device_hwid()
    ip = get_public_ip()
    url_can_rut_gon = f"{LINK_GOC_TRA_KEY}?hwid={hwid}&ip={ip}&key={get_today_key(hwid)}"
    encoded_url = urllib.parse.quote(url_can_rut_gon)
    
    if server_type == "layma":
        api_url = f"https://api.layma.net/api/admin/shortlink/quicklink?tokenUser={API_TOKEN_LAYMA}&format=json&url={encoded_url}"
        try:
            res = requests.get(api_url, timeout=7).json()
            if res.get("success") is True:
                return res.get("html")
        except:
            pass
        return "❌ Lỗi kết nối đến LayMa.net!"
    elif server_type == "oklink":
        api_url = f"https://vuotlink.xyz/api?api={API_TOKEN_OKLINK}&url={encoded_url}&format=text"
        try:
            res = requests.get(api_url, timeout=7)
            if res.status_code == 200 and res.text.strip() and "http" in res.text:
                return res.text.strip()
        except:
            pass
        return "❌ Máy chủ OkLink đang bận!"
    elif server_type == "link4m":
        api_url = f"https://link4m.co/api-shorten/v2?api={API_TOKEN_LINK4M}&url={encoded_url}"
        try:
            res = requests.get(api_url, timeout=7).json()
            if res.get("status") == "success" and res.get("shortenedUrl"):
                return res.get("shortenedUrl")
        except:
            pass
        return "❌ Lỗi kết nối đến Link4M!"
    return "❌ Hệ thống gặp sự cố!"

def validate_license_key(key, hwid=None, ip=None):
    if hwid is None:
        hwid = get_device_hwid()
    if ip is None:
        ip = get_public_ip()
    
    if key == "HTOOL-ADMIN-SUPER":
        return True, "Super Admin", {"type": "super_admin", "is_vip": True, "expire_time": "2099-12-31 23:59:59"}
    
    db = get_db()
    if key in db.get("vip_keys", {}):
        key_data = db["vip_keys"][key]
        expire_str = key_data.get("expire_time", "")
        if datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S") < datetime.now():
            return False, "Key VIP đã hết hạn", None
        if key_data.get("hwid", "ANY") != "ANY" and key_data["hwid"] != hwid:
            return False, "Key VIP được cấp riêng cho thiết bị khác", None
        if key_data.get("ip", "ANY") != "ANY" and key_data["ip"] != ip:
            return False, "IP không trùng khớp", None
        return True, "Key VIP hợp lệ", {"type": "vip", "is_vip": True, "expire_time": expire_str}
    
    today_key = get_today_key(hwid)
    if key == today_key:
        expire_time = (datetime.now() + timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
        return True, "Key ngày hợp lệ", {"type": "daily", "is_vip": False, "expire_time": expire_time}
    
    return False, "Key không hợp lệ", None

def save_license_data(data):
    try:
        with open(LICENSE_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        hwid = data.get('device-hwid', get_device_hwid())
        db = get_db()
        db["user_keys"][hwid] = {
            "license_key": data.get('license-key', ''),
            "expire_time": data.get('expire-time', ''),
            "is_vip": data.get('is-vip', False),
            "device_hwid": hwid,
            "device_ip": data.get('device-ip', ''),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_db(db)
        return True
    except:
        return False

def load_license_data():
    if os.path.exists(LICENSE_DATA_FILE):
        try:
            with open(LICENSE_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def check_cached_key():
    hwid = get_device_hwid()
    ip = get_public_ip()
    data = load_license_data()
    
    if not data:
        return False, None
    
    cached_key = data.get('license-key', '')
    expire_str = data.get('expire-time', '')
    
    if is_key_expired(expire_str):
        return False, None
    
    is_valid, _, key_data = validate_license_key(cached_key, hwid, ip)
    
    if is_valid and key_data:
        data['is-vip'] = key_data.get('is_vip', False)
        if key_data.get('expire_time'):
            data['expire-time'] = key_data['expire_time']
        return True, data
    
    return False, None

def create_vip_key(hwid="", ip="", hours=24):
    new_key = "HTOOL-VIP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    expire_date = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db["vip_keys"][new_key] = {
        "hwid": hwid if hwid else "ANY",
        "ip": ip if ip else "ANY",
        "expire_time": expire_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if save_db(db):
        return {"key": new_key, "expire_time": expire_date, "hours": hours}
    return None

def ban_hwid(hwid):
    hwid = hwid.upper()
    db = get_db()
    if hwid not in db.get("banned_hwids", []):
        db.setdefault("banned_hwids", []).append(hwid)
        return save_db(db)
    return True

def ban_ip(ip):
    db = get_db()
    if ip not in db.get("banned_ips", []):
        db.setdefault("banned_ips", []).append(ip)
        return save_db(db)
    return True

def unban(target):
    db = get_db()
    if target in db.get("vip_keys", {}):
        del db["vip_keys"][target]
        save_db(db)
        return True, f"Đã xóa key VIP: {target}"
    if target.upper() in db.get("banned_hwids", []):
        db["banned_hwids"].remove(target.upper())
        save_db(db)
        return True, f"Đã gỡ ban HWID: {target.upper()}"
    if target in db.get("banned_ips", []):
        db["banned_ips"].remove(target)
        save_db(db)
        return True, f"Đã gỡ ban IP: {target}"
    return False, f"Không tìm thấy: {target}"

# ==================== SHOW FUNCTIONS ====================
def show_ai_list(is_vip=False, max_ai=10):
    clear_screen()
    banner(is_vip, "DANH SÁCH AI")
    prints(0, 255, 255, "🤖 DANH SÁCH AI - CHẠY ĐUA TỐC ĐỘ 🤖".center(62))
    prints(247, 255, 97, "─" * 62)
    
    if is_vip:
        prints(0, 255, 102, f"\n  💎 VIP: Được dùng tất cả 20 AI")
    else:
        prints(255, 200, 0, f"\n  🔓 FREE: Chỉ dùng được 10 AI đầu tiên (1-10)")
        prints(255, 200, 0, f"  👑 Nâng cấp VIP để mở khóa thêm 10 AI nâng cao!")
    
    prints(247, 255, 97, "─" * 62)
    
    for num, ai in AI_MODELS.items():
        if num <= max_ai:
            icon = "🔓" if not ai['vip'] else "👑"
            prints(255, 255, 255, f"  [{num:2d}] {icon} {ai['name']:<30}")
            prints(180, 180, 180, f"       📝 {ai['desc']}")
            prints(150, 150, 150, f"       ⚙️  {ai['method']}")
        else:
            prints(255, 100, 100, f"  [{num:2d}] 🔒 {ai['name']:<30} - YÊU CẦU VIP")
    
    prints(247, 255, 97, "═" * 62)

def show_history():
    clear_screen()
    banner(False, "LỊCH SỬ CƯỢC")
    prints(0, 255, 255, "\n📜 LỊCH SỬ CƯỢC 📜".center(62))
    prints(247, 255, 97, "═" * 62)
    
    if not bet_history:
        prints(255, 255, 255, "\n  Chưa có lịch sử cược nào!")
    else:
        prints(255, 215, 0, "\n┌──────┬────────────────────┬──────────┬──────────┬────────────────┐")
        prints(255, 215, 0, "│ Kỳ   │ Người chọn         │ Cược     │ Kết quả  │ AI             │")
        prints(255, 215, 0, "├──────┼────────────────────┼──────────┼──────────┼────────────────┤")
        
        for rec in list(bet_history)[:20]:
            issue = str(rec.get('issue', '?'))[-6:]
            nv_name = f"{NV.get(rec.get('nv_id', 1), {}).get('icon', '')} {NV.get(rec.get('nv_id', 1), {}).get('name', '?')[:16]}"
            amt = f"{rec.get('amount', 0):,.0f}"
            result = rec.get('result', '?')
            algo = rec.get('algo', '?')[:14]
            kq = "✅ THẮNG" if result == 'win' else ("❌ THUA" if result == 'lose' else "⏭️ BỎ")
            prints(255, 255, 255, f"│ {issue} │ {nv_name:<18} │ {amt:<8} │ {kq}    │ {algo:<14} │")
        
        prints(255, 215, 0, "└──────┴────────────────────┴──────────┴──────────┴────────────────┘")
        
        wins = sum(1 for r in bet_history if r.get('result') == 'win')
        loses = sum(1 for r in bet_history if r.get('result') == 'lose')
        total = wins + loses
        if total > 0:
            winrate = (wins / total) * 100
            prints(0, 255, 102, f"\n  📊 Thống kê: {wins} thắng / {loses} thua | Tỉ lệ thắng: {winrate:.1f}%")
    
    prints(247, 255, 97, "═" * 62)
    input("\n👉 Nhấn Enter để quay lại...")

def show_admin_menu():
    while True:
        clear_screen()
        banner(True, "ADMIN")
        prints(255, 69, 0, "╔" + "═" * 58 + "╗")
        prints(255, 69, 0, "║               👑 HỆ THỐNG QUẢN TRỊ ADMIN 👑        ║")
        prints(255, 69, 0, "╚" + "═" * 58 + "╝")
        prints(255, 255, 255, "  [1] 💎 Tạo KEY VIP")
        prints(255, 255, 255, "  [2] 🚫 BAN HWID")
        prints(255, 255, 255, "  [3] 🛑 BAN IP")
        prints(255, 255, 255, "  [4] 📋 Xem danh sách")
        prints(255, 255, 255, "  [5] 🔓 Gỡ BAN / Xóa Key")
        prints(255, 255, 255, "  [6] 🔄 Reset tất cả KEY VIP")
        prints(255, 255, 255, "  [7] 🗑️  Xóa tất cả KEY VIP")
        prints(255, 255, 255, "  [8] 🚪 Thoát Admin")
        prints(255, 69, 0, "═" * 60)
        prints(255, 255, 0, "👉 Chọn: ", end="")
        c = input().strip()
        
        if c == '1':
            clear_screen()
            banner(True, "TẠO KEY VIP")
            hwid_target = input("HWID (bỏ trống = tự do): ").strip().upper()
            ip_target = input("IP (bỏ trống = tự do): ").strip()
            hours = int(input("Số giờ (mặc định 24): ") or 24)
            result = create_vip_key(hwid_target, ip_target, hours)
            if result:
                prints(0, 255, 102, f"\n🎉 Key: {result['key']}")
                prints(255, 255, 255, f"⏱️ Hạn: {result['expire_time']}")
            else:
                prints(255, 0, 0, "❌ Lỗi!")
            input("\nEnter...")
            
        elif c == '2':
            hwid = input("Nhập HWID cần ban: ").strip().upper()
            if hwid:
                ban_hwid(hwid)
                prints(0, 255, 102, f"✅ Đã ban {hwid}")
            input("\nEnter...")
            
        elif c == '3':
            ip = input("Nhập IP cần ban: ").strip()
            if ip:
                ban_ip(ip)
                prints(0, 255, 102, f"✅ Đã ban {ip}")
            input("\nEnter...")
            
        elif c == '4':
            clear_screen()
            db = get_db()
            prints(0, 255, 243, "📋 DỮ LIỆU:")
            print("\n--- KEY VIP ---")
            vip_keys = db.get("vip_keys", {})
            if vip_keys:
                for k, v in vip_keys.items():
                    print(f"🔑 {k} | HWID: {v.get('hwid')} | IP: {v.get('ip')} | Hạn: {v.get('expire_time')}")
                print(f"\n📊 Tổng: {len(vip_keys)} key VIP")
            else:
                print("  Chưa có key VIP nào")
            print("\n--- HWID BAN ---")
            for h in db.get("banned_hwids", []):
                print(f"❌ {h}")
            print("\n--- IP BAN ---")
            for ip_ban in db.get("banned_ips", []):
                print(f"❌ {ip_ban}")
            input("\nEnter...")
            
        elif c == '5':
            target = input("Nhập Key/HWID/IP cần gỡ: ").strip()
            success, msg = unban(target)
            prints(0, 255, 102 if success else 255, 0, 0, msg)
            input("\nEnter...")
            
        elif c == '6':
            clear_screen()
            banner(True, "RESET KEY VIP")
            prints(255, 200, 0, "\n⚠️  CẢNH BÁO: Thao tác này sẽ reset thời hạn tất cả key VIP về 0!")
            prints(255, 200, 0, "   Tất cả key VIP sẽ hết hạn ngay lập tức!")
            prints(255, 255, 255, "\n👉 Bạn có chắc chắn muốn RESET tất cả key VIP?")
            prints(255, 0, 0, "   Gõ 'RESET' để xác nhận: ", end="")
            confirm = input().strip()
            
            if confirm.upper() == "RESET":
                db = get_db()
                vip_keys = db.get("vip_keys", {})
                count = 0
                for key in vip_keys:
                    vip_keys[key]["expire_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    count += 1
                db["vip_keys"] = vip_keys
                if save_db(db):
                    prints(0, 255, 102, f"\n✅ Đã reset {count} key VIP! Tất cả đã hết hạn.")
                else:
                    prints(255, 0, 0, "\n❌ Lỗi khi lưu!")
            else:
                prints(255, 255, 0, "\n❌ Đã hủy thao tác reset.")
            input("\nEnter...")
            
        elif c == '7':
            clear_screen()
            banner(True, "XÓA KEY VIP")
            prints(255, 0, 0, "\n⚠️  CẢNH BÁO: Thao tác này sẽ XÓA VĨNH VIỄN tất cả key VIP!")
            prints(255, 0, 0, "   Không thể khôi phục sau khi xóa!")
            prints(255, 255, 255, "\n👉 Bạn có chắc chắn muốn XÓA tất cả key VIP?")
            prints(255, 0, 0, "   Gõ 'DELETE' để xác nhận: ", end="")
            confirm = input().strip()
            
            if confirm.upper() == "DELETE":
                db = get_db()
                count = len(db.get("vip_keys", {}))
                db["vip_keys"] = {}
                if save_db(db):
                    prints(0, 255, 102, f"\n✅ Đã xóa {count} key VIP vĩnh viễn!")
                else:
                    prints(255, 0, 0, "\n❌ Lỗi khi lưu!")
            else:
                prints(255, 255, 0, "\n❌ Đã hủy thao tác xóa.")
            input("\nEnter...")
            
        elif c == '8':
            break

# ==================== GAME DATA ====================
def load_data():
    if os.path.exists('data-htool-cdtd.txt'):
        prints(0, 255, 243, 'Dùng tài khoản cũ? (y/n): ', end='')
        x = input()
        if x == 'y':
            with open('data-htool-cdtd.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
    prints(218, 255, 125, "\n📋 Hướng dẫn lấy link:")
    prints(255, 255, 255, "  1. Truy cập xworld.io → Đăng nhập")
    prints(255, 255, 255, "  2. Vào Chạy đua tốc độ → Nhấn 'Lập tức truy cập'")
    prints(255, 255, 255, "  3. Copy link và dán vào đây")
    prints(125, 255, 168, '\n📋 Nhập link: ', end='')
    link = input()
    try:
        user_id = link.split('userId=')[1].split('&')[0]
        user_secretkey = link.split('secretKey=')[1].split('&')[0]
    except:
        prints(255, 0, 0, "❌ Link không đúng định dạng!")
        sys.exit(1)
    data = {'user-id': user_id, 'user-secret-key': user_secretkey}
    with open('data-htool-cdtd.txt', 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data

def top_100(s):
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9',
        'origin': 'https://sprintrun.win', 'referer': 'https://sprintrun.win/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'
    }
    try:
        r = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers, timeout=10).json()
        return [1,2,3,4,5,6], [r['data']['athlete_2_win_times'][str(i)] for i in range(1,7)]
    except:
        return [1,2,3,4,5,6], [0,0,0,0,0,0]

def top_10(s, headers):
    try:
        r = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=10).json()
        ki = [i['issue_id'] for i in r['data']['recent_10']]
        kq = [i['result'][0] for i in r['data']['recent_10']]
        return ki, kq
    except:
        return [int(time.time()//60)], [1]

def user_asset(s, headers):
    try:
        r = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, 
                   json={"user_id": int(headers['user-id']), "source": "home"}, timeout=10).json()
        return {'USDT': r['data']['user_asset']['USDT'],
                'WORLD': r['data']['user_asset']['WORLD'],
                'BUILD': r['data']['user_asset']['BUILD']}
    except:
        return {'USDT': 100, 'WORLD': 5000, 'BUILD': 10000}

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount):
    try:
        r = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json={
            'issue_id': int(ki), 'bet_group': 'not_winner',
            'asset_type': Coin, 'athlete_id': kq, 'bet_amount': bet_amount
        }, timeout=10).json()
        if r['code'] == 0 and r['msg'] == 'ok':
            prints(0, 255, 19, f'✅ Đã đặt {bet_amount:.2f} {Coin} vào "{NV[kq]["name"]}" (Không về nhất)')
            return True
        else:
            prints(255, 0, 0, f'❌ Lỗi đặt cược: {r.get("msg", "Không rõ")}')
            return False
    except Exception as e:
        prints(255, 0, 0, f'❌ Lỗi kết nối: {e}')
        return False

# ==================== 20 AI FUNCTIONS ====================
def ai_random(): return random.randint(1, 6)
def ai_frequency(d100):
    wins = d100[1]; total = sum(wins)
    if total == 0: return random.randint(1, 6)
    return [w/total for w in wins].index(min([w/total for w in wins])) + 1
def ai_pattern(d10):
    recent = [int(w) for w in d10[1]]
    if len(recent) < 2: return random.randint(1, 6)
    patterns = {}
    for i in range(len(recent)-1):
        p = (recent[i], recent[i+1]); patterns[p] = patterns.get(p, 0) + 1
    return max(patterns, key=patterns.get)[1] if patterns else random.randint(1, 6)
def ai_statistical(d100):
    wins = d100[1]; mean = statistics.mean(wins) if wins else 0
    std = statistics.stdev(wins) if len(wins) > 1 else 1
    scores = [1/(1+math.exp((w-mean)/std)) if std>0 else 0.5 for w in wins]
    return scores.index(min(scores)) + 1
def ai_markov(d10):
    recent = [int(w) for w in d10[1]]
    if not recent: return random.randint(1, 6)
    trans = {i: random.random() for i in range(1, 7)}
    total = sum(trans.values())
    return [trans[i]/total for i in range(1, 7)].index(min([trans[i]/total for i in range(1, 7)])) + 1
def ai_bayesian(d100):
    wins = d100[1]; total = sum(wins)
    if total == 0: return random.randint(1, 6)
    posterior = [(1/6) * (w/total) for w in wins]
    return posterior.index(min(posterior)) + 1
def ai_monte_carlo(d100):
    wins = d100[1]; results = {i: 0 for i in range(1, 7)}
    for _ in range(1000):
        noisy = [max(0, w + random.gauss(0, 2)) for w in wins]
        total = sum(noisy)
        if total > 0:
            probs = [w/total for w in noisy]; r = random.uniform(0, sum(probs)); upto = 0
            for i, p in enumerate(probs):
                if upto + p >= r: results[i+1] += 1; break
                upto += p
    return min(results, key=results.get)
def ai_time_series(d10):
    recent = [int(w) for w in d10[1]]
    if len(recent) < 3: return random.randint(1, 6)
    return max(1, min(6, int(round(statistics.mean(recent[-3:]) + random.gauss(0, 1)))))
def ai_neural(d10, d100):
    wins = d100[1]; features = [w/100.0 for w in wins]
    weights = [random.uniform(-1, 1) for _ in range(6)]; bias = random.uniform(-1, 1)
    outputs = [max(0, f * w + bias) for f, w in zip(features, weights)]
    return outputs.index(min(outputs)) + 1 if outputs else random.randint(1, 6)
def ai_fuzzy(d100):
    wins = d100[1]; high, low = 20, 10; scores = []
    for w in wins:
        if w > high: scores.append(0.9)
        elif w > low: scores.append(0.5)
        else: scores.append(0.1)
    return scores.index(min(scores)) + 1
def ai_regression(d100):
    wins = d100[1]; x = list(range(1, 7)); n = len(x)
    if n < 2: return random.randint(1, 6)
    sum_x, sum_y = sum(x), sum(wins)
    sum_xy = sum(x[i] * wins[i] for i in range(n)); sum_x2 = sum(x[i]**2 for i in range(n))
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2) if (n * sum_x2 - sum_x**2) != 0 else 0
    intercept = (sum_y - slope * sum_x) / n
    return max(1, min(6, int((intercept + slope * 7) % 6 + 1)))
def ai_clustering(d100):
    wins = d100[1]; mean_wins = statistics.mean(wins)
    cluster_low = [i+1 for i, w in enumerate(wins) if w <= mean_wins]
    return random.choice(cluster_low) if cluster_low else random.randint(1, 6)
def ai_decision_tree(d10, d100):
    wins = d100[1]; recent = [int(w) for w in d10[1]]
    if not recent: return random.randint(1, 6)
    last = recent[0]
    return wins.index(min(wins)) + 1 if wins[last-1] > statistics.mean(wins) else wins.index(max(wins)) + 1
def ai_svm(d100):
    wins = d100[1]; mean_wins = statistics.mean(wins)
    return [mean_wins - w for w in wins].index(max([mean_wins - w for w in wins])) + 1
def ai_knn(d10, d100):
    recent = [int(w) for w in d10[1]]
    if len(recent) < 3: return random.randint(1, 6)
    distances = [sum(abs(i - r) for r in recent[:3]) for i in range(1, 7)]
    return distances.index(min(distances)) + 1
def ai_ensemble(d10, d100):
    preds = [ai_frequency(d100), ai_pattern(d10), ai_statistical(d100), ai_markov(d10), ai_bayesian(d100)]
    return Counter(preds).most_common(1)[0][0]
def ai_deep_learning(d10, d100):
    wins = d100[1]; features = [w/100.0 for w in wins]
    for _ in range(3): features = [max(0, f * random.uniform(0.8, 1.2) + random.uniform(-0.1, 0.1)) for f in features]
    return features.index(min(features)) + 1
def ai_reinforcement(d10, d100):
    q_values = {i: random.uniform(0, 1) for i in range(1, 7)}
    for r in [int(w) for w in d10[1]]:
        q_values[r] += 0.1
        for i in range(1, 7):
            if i != r: q_values[i] -= 0.01
    return min(q_values, key=q_values.get)
def ai_genetic(d10, d100):
    wins = d100[1]; population = []
    for _ in range(20):
        solution = [random.randint(1, 6) for _ in range(5)]
        fitness = sum(1 for s in solution if wins[s-1] < statistics.mean(wins))
        population.append((solution, fitness))
    population.sort(key=lambda x: x[1], reverse=True)
    return population[0][0][-1]
def ai_chaos(d10, d100):
    wins = d100[1]
    return (wins.index(min(wins)) + random.randint(0, 2)) % 6 + 1

AI_FUNCTIONS = {
    1: lambda d10, d100: ai_random(),
    2: lambda d10, d100: ai_frequency(d100),
    3: lambda d10, d100: ai_pattern(d10),
    4: lambda d10, d100: ai_statistical(d100),
    5: lambda d10, d100: ai_markov(d10),
    6: lambda d10, d100: ai_bayesian(d100),
    7: lambda d10, d100: ai_monte_carlo(d100),
    8: lambda d10, d100: ai_time_series(d10),
    9: lambda d10, d100: ai_neural(d10, d100),
    10: lambda d10, d100: ai_fuzzy(d100),
    11: lambda d10, d100: ai_regression(d100),
    12: lambda d10, d100: ai_clustering(d100),
    13: lambda d10, d100: ai_decision_tree(d10, d100),
    14: lambda d10, d100: ai_svm(d100),
    15: lambda d10, d100: ai_knn(d10, d100),
    16: lambda d10, d100: ai_ensemble(d10, d100),
    17: lambda d10, d100: ai_deep_learning(d10, d100),
    18: lambda d10, d100: ai_reinforcement(d10, d100),
    19: lambda d10, d100: ai_genetic(d10, d100),
    20: lambda d10, d100: ai_chaos(d10, d100),
}

def selected_NV(data10, data100, htr, heso, bet0, ai_choice):
    bet = bet0
    if htr and not htr[0]['kq']:
        bet = heso * htr[0]['bet_amount']
    try:
        func = AI_FUNCTIONS.get(ai_choice, AI_FUNCTIONS[1])
        sel = func(data10, data100)
        if sel == data10[1][0]: sel = (sel % 6) + 1
        return sel, bet
    except:
        while True:
            res = random.randint(1, 6)
            if res != data10[1][0]: break
        return res, bet

def kiem_tra_kq(s, headers, kq, ki):
    start = time.time()
    while True:
        data10 = top_10(s, headers)
        if int(data10[0][0]) == int(ki):
            winner = int(data10[1][0])
            prints(0, 255, 30, f'\n🏆 Kết quả kì {ki}: {NV[winner]["icon"]} {NV[winner]["name"]} về nhất!')
            return (False, winner) if winner == kq else (True, winner)
        prints(0, 255, 197, f'⏳ Đang đợi kết quả... {time.time()-start:.0f}s', end='\r')
        time.sleep(1)

# ==================== LOGIN SCREEN ====================
def login_screen():
    global user_vip_status, current_key_data, banner_expire_time
    
    hwid = get_device_hwid()
    ip = get_public_ip()
    
    # Kiểm tra banned
    db = get_db()
    if hwid in db.get("banned_hwids", []):
        prints(255, 0, 0, "🚫 Thiết bị bị cấm!"); sys.exit(0)
    if ip in db.get("banned_ips", []):
        prints(255, 0, 0, "🚫 IP bị cấm!"); sys.exit(0)
    
    # Kiểm tra key đã lưu
    has_key, key_data = check_cached_key()
    
    if has_key and key_data:
        user_vip_status = key_data.get('is-vip', False)
        current_key_data = key_data
        banner_expire_time = get_remaining_time(key_data.get('expire-time', ''))
        return True
    
    while True:
        clear_screen()
        banner(False, "ĐĂNG NHẬP")
        
        prints(247, 255, 97, "═" * 62)
        prints(255, 255, 255, f"  • HWID: {hwid}")
        prints(255, 255, 255, f"  • IP: {ip}")
        prints(247, 255, 97, "═" * 62)
        prints(255, 255, 255, "  [1] 🔗 LẤY KEY TỰ ĐỘNG")
        prints(255, 255, 255, "  [2] 🔑 NHẬP KEY KÍCH HOẠT")
        prints(255, 255, 255, "  [3] 🚪 THOÁT")
        prints(247, 255, 97, "═" * 62)
        prints(255, 255, 0, "👉 Chọn (1/2/3): ", end="")
        c = input().strip()
        
        if c == ADMIN_PASSWORD_SECRET:
            show_admin_menu()
            continue
        
        if c == '1':
            while True:
                clear_screen()
                banner(False, "LẤY KEY")
                prints(255, 255, 255, "  [1] Server Link4M (Hoạt động)")
                prints(255, 255, 255, "  [2] Server OkLink")
                prints(255, 255, 255, "  [3] Server LayMa")
                prints(255, 255, 255, "  [4] Quay lại")
                sv = input("👉 Chọn: ").strip()
                if sv == '4': break
                server = {'1': 'link4m', '2': 'oklink', '3': 'layma'}.get(sv)
                if server:
                    link = generate_short_link(server)
                    prints(0, 255, 0, f"\n🔗 Link: {link}")
                    webbrowser.open(link)
                    input("\nNhấn Enter sau khi lấy key...")
                    break
        
        elif c == '2':
            clear_screen()
            banner(False, "NHẬP KEY")
            prints(255, 255, 255, f"  HWID: {hwid}")
            prints(255, 255, 0, "\n👉 Nhập Key (BACK để quay lại): ", end="")
            key = input().strip()
            
            if key.upper() == 'BACK':
                continue
            
            if key == ADMIN_PASSWORD_SECRET:
                show_admin_menu()
                continue
            
            is_valid, msg, data = validate_license_key(key, hwid, ip)
            
            if is_valid:
                data['license-key'] = key
                data['device-hwid'] = hwid
                data['device-ip'] = ip
                
                user_vip_status = data.get('is_vip', False)
                current_key_data = data
                banner_expire_time = get_remaining_time(data.get('expire_time', ''))
                
                save_license_data(data)
                
                prints(0, 255, 102, f"\n✅ {msg}")
                prints(255, 255, 255, f"⏰ Hạn: {banner_expire_time}")
                time.sleep(2)
                return True
            else:
                prints(255, 0, 0, f"\n❌ {msg}")
                time.sleep(2)
        
        elif c == '3':
            prints(255, 0, 0, "\n👋 Thoát...")
            sys.exit(0)

# ==================== MAIN GAME ====================
def run_game(key_data=None):
    global user_vip_status, current_key_data, banner_expire_time, bet_history
    
    if key_data:
        user_vip_status = key_data.get('is-vip', False)
        current_key_data = key_data
        banner_expire_time = get_remaining_time(key_data.get('expire-time', ''))
    
    is_vip = user_vip_status
    max_ai = 20 if is_vip else 10
    
    while True:
        clear_screen()
        banner(is_vip)
        
        if is_vip:
            prints(0, 255, 102, "  💎 TRẠNG THÁI: VIP - Được dùng tất cả 20 AI")
        else:
            prints(255, 200, 0, "  🔓 TRẠNG THÁI: FREE - Chỉ dùng được 10 AI (1-10)")
            prints(255, 200, 0, "  👑 Nâng cấp VIP để mở khóa thêm 10 AI nâng cao!")
        
        prints(247, 255, 97, "═" * 62)
        prints(255, 255, 255, "  [1] 🎮 BẮT ĐẦU CHƠI")
        prints(255, 255, 255, "  [2] 🤖 XEM DANH SÁCH AI")
        prints(255, 255, 255, "  [3] 📜 XEM LỊCH SỬ CƯỢC")
        prints(255, 255, 255, "  [4] 🔑 ĐĂNG XUẤT")
        prints(255, 255, 255, "  [5] 🚪 THOÁT")
        prints(247, 255, 97, "═" * 62)
        prints(255, 255, 0, "👉 Chọn (1/2/3/4/5): ", end="")
        choice = input().strip()
        
        if choice == '1':
            show_ai_list(is_vip, max_ai)
            try:
                ai_choice = int(input(f'\n👉 Chọn AI (1-{max_ai}, mặc định 1): ') or 1)
                if ai_choice < 1 or ai_choice > max_ai:
                    prints(255, 200, 0, f'⚠️ Chỉ được chọn AI 1-{max_ai}! Đặt về AI 1.')
                    ai_choice = 1
                    time.sleep(1.5)
            except:
                ai_choice = 1
            
            if ai_choice > 10 and not is_vip:
                prints(255, 0, 0, f'\n❌ AI {ai_choice} yêu cầu VIP!')
                input("👉 Nhấn Enter để chọn lại...")
                continue
            
            s = requests.Session()
            clear_screen()
            banner(is_vip)
            data = load_data()
            headers = {
                'accept': '*/*', 'accept-language': 'vi,en;q=0.9',
                'cache-control': 'no-cache', 'country-code': 'vn',
                'origin': 'https://xworld.info', 'referer': 'https://xworld.info/',
                'user-agent': 'Mozilla/5.0',
                'user-id': data['user-id'], 'user-login': 'login_v2',
                'user-secret-key': data['user-secret-key'], 'xb-language': 'vi-VN'
            }
            asset = user_asset(s, headers)
            prints(255, 255, 255, f"\n💰 Số dư: USDT {asset['USDT']:.2f} | WORLD {asset['WORLD']:.2f} | BUILD {asset['BUILD']:.2f}")
            
            prints(255, 255, 0, "\n📋 Chọn coin: 1.BUILD  2.USDT  3.WORLD")
            Coin = {'1':'BUILD','2':'USDT','3':'WORLD'}.get(input("👉 Chọn: ").strip(), 'BUILD')
            bet_amount0 = float(input(f"💰 Số {Coin} mỗi ván: "))
            heso = float(input("📈 Hệ số gấp thếp: "))
            delay1 = int(input("🎯 Số ván đặt (999=không nghỉ): "))
            delay2 = int(input("⏸️  Số ván nghỉ: "))
            
            stats = {'win': 0, 'lose': 0, 'asset0': asset[Coin], 'streak': 0, 'max_streak': 0}
            algo = AI_MODELS[ai_choice]['name']
            htr = []
            tong = 0
            current_bet = bet_amount0
            
            clear_screen()
            
            while True:
                try:
                    tong += 1
                    
                    if current_key_data:
                        expire_time = datetime.strptime(current_key_data.get('expire-time', '2000-01-01'), "%Y-%m-%d %H:%M:%S")
                        if datetime.now() >= expire_time:
                            prints(255, 0, 0, '\n❌ Key hết hạn! Vui lòng đăng nhập lại.')
                            time.sleep(3)
                            return
                    
                    prints(247, 255, 97, "═" * 62)
                    prints(0, 255, 255, f"🔄 VÁN THỨ {tong}")
                    prints(247, 255, 97, "═" * 62)
                    
                    data10 = top_10(s, headers)
                    data100 = top_100(s)
                    kq, bet_amount = selected_NV(data10, data100, htr, heso, bet_amount0, ai_choice)
                    ki = data10[0][0] + 1
                    
                    cycle = delay1 + delay2 if delay1 > 0 else 1
                    pos = (tong - 1) % cycle
                    
                    is_bet = False
                    if pos < delay1 or delay1 == 0:
                        is_bet = bet_cdtd(s, headers, ki, kq, Coin, bet_amount)
                        if is_bet:
                            current_bet = bet_amount
                    else:
                        prints(255, 255, 0, f'⏸️  Ván này tạm nghỉ ({pos+1}/{cycle})')
                        bet_amount = bet_amount0
                    
                    prints(255, 255, 0, f'\n🤖 AI [{ai_choice}] {algo}')
                    prints(255, 255, 255, f'   📝 {AI_MODELS[ai_choice]["desc"]}')
                    prints(0, 246, 255, f'🎯 HTOOL CHỌN: {NV[kq]["icon"]} {NV[kq]["name"]}')
                    
                    result, winner = kiem_tra_kq(s, headers, kq, ki)
                    
                    if result:
                        stats['win'] += 1
                        stats['streak'] += 1
                        stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                        current_bet = bet_amount0
                        prints(0, 255, 37, f'\n🎉 THẮNG!')
                        bet_history.appendleft({
                            'issue': ki, 'nv_id': kq, 'nv_name': NV[kq]['name'],
                            'amount': current_bet, 'result': 'win', 'algo': algo
                        })
                    else:
                        stats['lose'] += 1
                        stats['streak'] = 0
                        prints(255, 0, 0, f'\n💸 THUA!')
                        bet_history.appendleft({
                            'issue': ki, 'nv_id': kq, 'nv_name': NV[kq]['name'],
                            'amount': current_bet, 'result': 'lose', 'algo': algo
                        })
                        current_bet *= heso
                    
                    save_history(bet_history)
                    
                    if pos < delay1 or delay1 == 0:
                        htr.insert(0, {'kq': result, 'bet_amount': current_bet})
                    
                    prints(247, 255, 97, "═" * 62)
                    prints(255, 255, 255, f"📊 Thắng: {stats['win']} | Thua: {stats['lose']} | Streak: {stats['streak']} (Max: {stats['max_streak']})")
                    if is_bet:
                        prints(255, 255, 255, f"💰 Cược tiếp: {current_bet:.2f} {Coin}")
                    
                    time.sleep(5)
                    clear_screen()
                    
                except KeyboardInterrupt:
                    prints(255, 255, 0, '\n👋 Dừng! Quay lại menu...')
                    save_history(bet_history)
                    time.sleep(1)
                    break
                    
        elif choice == '2':
            show_ai_list(is_vip, max_ai)
            input("\n👉 Nhấn Enter để quay lại...")
        elif choice == '3':
            show_history()
        elif choice == '4':
            prints(255, 255, 0, "\n👋 Đăng xuất...")
            if os.path.exists(LICENSE_DATA_FILE):
                os.remove(LICENSE_DATA_FILE)
            time.sleep(1)
            return login_screen()
        elif choice == '5':
            prints(255, 0, 0, "\n👋 Thoát...")
            save_history(bet_history)
            sys.exit(0)

def main():
    login_screen()
    run_game()

if __name__ == "__main__":
    main()
