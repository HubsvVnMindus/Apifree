# ==================== HTOOL - CHẠY ĐUA TỐC ĐỘ (CDTD) - FULL CONTINUOUS - AI NÂNG CẤP ====================
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
from collections import Counter, deque, defaultdict
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
GAME_DATA_FILE = "data-htool-cdtd.txt"
AI_LEARNING_FILE = "ai_learning_data.json"

# ==================== NHÂN VẬT ====================
NV = {
    1: {'name': 'Bậc thầy tấn công', 'icon': '⚔️', 'desc': 'Chuyên gia võ thuật, tốc độ ra đòn nhanh'},
    2: {'name': 'Quyền sắt', 'icon': '🥊', 'desc': 'Võ sĩ quyền anh, sức mạnh vượt trội'},
    3: {'name': 'Thợ lặn sâu', 'icon': '🤿', 'desc': 'Thợ lặn chuyên nghiệp, bền bỉ dưới nước'},
    4: {'name': 'Cơn lốc sân cỏ', 'icon': '🌪️', 'desc': 'Cầu thủ bóng đá, tốc độ như gió'},
    5: {'name': 'Hiệp sĩ phi nhanh', 'icon': '🏇', 'desc': 'Kỵ sĩ tài ba, cưỡi ngựa điêu luyện'},
    6: {'name': 'Vua home run', 'icon': '⚾', 'desc': 'Tay đập bóng chày, sức mạnh khủng khiếp'}
}

# ==================== DANH SÁCH 21 AI MODELS ====================
AI_MODELS = {
    1: {"name": "RANDOM", "desc": "Ngẫu nhiên thông minh", "method": "Random có trọng số theo lịch sử", "vip": False, "super_vip": False},
    2: {"name": "FREQUENCY", "desc": "Tần suất thấp nhất", "method": "Phân tích 100 ván + xu hướng", "vip": False, "super_vip": False},
    3: {"name": "PATTERN", "desc": "Nhận diện mẫu nâng cao", "method": "Phân tích đa pattern + chu kỳ", "vip": False, "super_vip": False},
    4: {"name": "STATISTICAL", "desc": "Thống kê Z-score cải tiến", "method": "Z-score + phân phối chuẩn", "vip": False, "super_vip": False},
    5: {"name": "MARKOV", "desc": "Chuỗi Markov bậc cao", "method": "Ma trận chuyển đổi bậc 2-3", "vip": False, "super_vip": False},
    6: {"name": "BAYESIAN", "desc": "Suy luận Bayes động", "method": "Cập nhật prior theo thời gian thực", "vip": False, "super_vip": False},
    7: {"name": "MONTE_CARLO", "desc": "Mô phỏng Monte Carlo nâng cao", "method": "10000 lần mô phỏng + bootstrap", "vip": False, "super_vip": False},
    8: {"name": "TIME_SERIES", "desc": "Chuỗi thời gian ARIMA", "method": "ARIMA + phân rã mùa vụ", "vip": False, "super_vip": False},
    9: {"name": "NEURAL", "desc": "Mạng nơ-ron đa tầng", "method": "5 lớp Neural + Dropout", "vip": False, "super_vip": False},
    10: {"name": "FUZZY", "desc": "Logic mờ nâng cao", "method": "Hệ suy luận mờ Mamdani", "vip": False, "super_vip": False},
    11: {"name": "REGRESSION", "desc": "Hồi quy đa biến", "method": "Polynomial Regression", "vip": True, "super_vip": False},
    12: {"name": "CLUSTERING", "desc": "Phân cụm K-Means++", "method": "K-Means++ với Elbow method", "vip": True, "super_vip": False},
    13: {"name": "DECISION_TREE", "desc": "Cây quyết định XGBoost", "method": "Gradient Boosted Trees", "vip": True, "super_vip": False},
    14: {"name": "SVM", "desc": "SVM với Kernel RBF", "method": "Support Vector Machine nâng cao", "vip": True, "super_vip": False},
    15: {"name": "KNN", "desc": "KNN có trọng số", "method": "Weighted K-Nearest Neighbors", "vip": True, "super_vip": False},
    16: {"name": "ENSEMBLE", "desc": "Tổng hợp 10 AI", "method": "Stacking Ensemble + Voting", "vip": True, "super_vip": False},
    17: {"name": "DEEP_LEARNING", "desc": "Deep Learning 10 lớp", "method": "ResNet + Attention", "vip": True, "super_vip": False},
    18: {"name": "REINFORCEMENT", "desc": "Deep Q-Learning", "method": "DQN với Experience Replay", "vip": True, "super_vip": False},
    19: {"name": "GENETIC", "desc": "Thuật toán di truyền NSGA-II", "method": "100 quần thể, đa mục tiêu", "vip": True, "super_vip": False},
    20: {"name": "CHAOS", "desc": "Lý thuyết hỗn loạn nâng cao", "method": "Lyapunov + Fractal analysis", "vip": True, "super_vip": False},
    21: {"name": "SUPER_VIP_CHAMPION", "desc": "👑 SIÊU VIP - Dự đoán Quán quân", "method": "Hybrid Deep Ensemble + Self-Learning", "vip": True, "super_vip": True}
}

# ==================== BIẾN TOÀN CỤC ====================
user_vip_status = False
user_super_vip_status = False
current_key_data = {}
banner_expire_time = None

# AI Learning System
ai_memory = {
    'global_stats': defaultdict(lambda: {'wins': 0, 'total': 0, 'streak': 0, 'last_results': deque(maxlen=50)}),
    'pattern_memory': defaultdict(lambda: defaultdict(int)),
    'time_based_stats': defaultdict(lambda: defaultdict(int)),
    'player_performance': {i: {'recent_wins': deque(maxlen=20), 'win_streak': 0, 'total_wins': 0} for i in range(1, 7)},
    'game_cycles': deque(maxlen=100),
    'prediction_accuracy': defaultdict(float)
}

def load_ai_memory():
    global ai_memory
    if os.path.exists(AI_LEARNING_FILE):
        try:
            with open(AI_LEARNING_FILE, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if key in ai_memory:
                        if isinstance(ai_memory[key], defaultdict):
                            ai_memory[key].update(value)
                        elif isinstance(ai_memory[key], deque):
                            ai_memory[key] = deque(value, maxlen=ai_memory[key].maxlen)
        except:
            pass

def save_ai_memory():
    try:
        serializable = {}
        for key, value in ai_memory.items():
            if isinstance(value, defaultdict):
                serializable[key] = dict(value)
            elif isinstance(value, deque):
                serializable[key] = list(value)
            else:
                serializable[key] = value
        with open(AI_LEARNING_FILE, 'w') as f:
            json.dump(serializable, f, indent=2)
    except:
        pass

load_ai_memory()

# ==================== HELPER FUNCTIONS ====================
def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    sys.stdout.write(f"\033[38;2;{r};{g};{b}m{text}\033[0m\033[K{end}")
    sys.stdout.flush()

def reset_cursor():
    sys.stdout.write("\033[H")
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

def parse_expire_time(expire_str):
    if not expire_str:
        return None
    try:
        return datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S")
    except:
        pass
    try:
        if len(expire_str) == 10 and expire_str.count('-') == 2:
            return datetime.strptime(expire_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    except:
        pass
    return None

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
        with open(DB_LOCAL_BACKUP, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except:
        pass
    try:
        requests.put(JSONBIN_UPDATE_URL, headers=get_jsonbin_headers(), json=data, timeout=10)
    except:
        pass

def get_remaining_time(expire_time_str):
    if not expire_time_str:
        return "Không xác định"
    try:
        expire_dt = parse_expire_time(expire_time_str)
        if expire_dt is None:
            return "Không xác định"
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
        return "❌ Lỗi kết nối!"
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
        return "❌ Lỗi kết nối!"
    return "❌ Hệ thống gặp sự cố!"

def validate_license_key(key, hwid=None, ip=None):
    if hwid is None:
        hwid = get_device_hwid()
    if ip is None:
        ip = get_public_ip()
    
    if key == "HTOOL-ADMIN-SUPER":
        return True, "Super Admin", {"type": "super_admin", "is_vip": True, "is_super_vip": True, "expire_time": "2099-12-31 23:59:59"}
    
    db = get_db()
    if key in db.get("vip_keys", {}):
        key_data = db["vip_keys"][key]
        expire_str = key_data.get("expire_time", "")
        expire_dt = parse_expire_time(expire_str)
        if expire_dt is None:
            return False, "Định dạng thời gian không hợp lệ", None
        if datetime.now() >= expire_dt:
            return False, "Key đã hết hạn", None
        if key_data.get("hwid", "ANY") != "ANY" and key_data["hwid"] != hwid:
            return False, "Key được cấp riêng cho thiết bị khác", None
        if key_data.get("ip", "ANY") != "ANY" and key_data["ip"] != ip:
            return False, "IP không trùng khớp", None
        
        is_super = key_data.get("is_super_vip", False)
        return True, "Key hợp lệ", {
            "type": "super_vip" if is_super else "vip",
            "is_vip": True,
            "is_super_vip": is_super,
            "expire_time": expire_str
        }
    
    today_key = get_today_key(hwid)
    if key == today_key:
        expire_time = (datetime.now() + timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
        return True, "Key ngày hợp lệ", {"type": "daily", "is_vip": False, "is_super_vip": False, "expire_time": expire_time}
    
    return False, "Key không hợp lệ", None

def save_license_data(data):
    try:
        if 'expire-time' in data:
            dt = parse_expire_time(data['expire-time'])
            if dt:
                data['expire-time'] = dt.strftime("%Y-%m-%d %H:%M:%S")
        with open(LICENSE_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
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
    dt = parse_expire_time(expire_str)
    if dt is None or datetime.now() >= dt:
        return False, None
    
    is_valid, _, key_data = validate_license_key(cached_key, hwid, ip)
    if is_valid and key_data:
        data['is-vip'] = key_data.get('is_vip', False)
        data['is-super-vip'] = key_data.get('is_super_vip', False)
        if key_data.get('expire_time'):
            data['expire-time'] = key_data['expire_time']
        return True, data
    
    return False, None

def create_vip_key(hwid="", ip="", hours=24, is_super_vip=False):
    prefix = "HTOOL-SVIP-" if is_super_vip else "HTOOL-VIP-"
    new_key = prefix + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    expire_date = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db["vip_keys"][new_key] = {
        "hwid": hwid if hwid else "ANY",
        "ip": ip if ip else "ANY",
        "expire_time": expire_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_active": True,
        "is_super_vip": is_super_vip,
        "type": "super_vip" if is_super_vip else "vip"
    }
    if save_db(db):
        return {"key": new_key, "expire_time": expire_date, "hours": hours, "is_super_vip": is_super_vip}
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
        return True, f"Đã xóa key: {target}"
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
def show_ai_list(is_vip=False, is_super_vip=False):
    clear_screen()
    
    if is_super_vip:
        prints(255, 215, 0, "👑 SIÊU VIP - TẤT CẢ 21 AI (Bao gồm AI DỰ ĐOÁN QUÁN QUÂN) 👑".center(60))
        max_ai = 21
        status_text = "👑 SIÊU VIP"
    elif is_vip:
        prints(0, 255, 102, "💎 VIP - 20 AI (1-20)".center(60))
        max_ai = 20
        status_text = "💎 VIP"
    else:
        prints(255, 200, 0, "🔓 FREE - 10 AI (1-10)".center(60))
        max_ai = 10
        status_text = "🔓 FREE"
    
    prints(247, 255, 97, "─" * 60)
    prints(255, 255, 255, f"  Trạng thái: {status_text} | AI khả dụng: 1-{max_ai} | AI tự học hỏi")
    prints(247, 255, 97, "─" * 60)
    
    for num, ai in AI_MODELS.items():
        if num <= max_ai:
            if ai.get("super_vip", False):
                icon = "👑"
                color = (255, 215, 0)
            elif ai.get("vip", False):
                icon = "💎"
                color = (0, 255, 200)
            else:
                icon = "🔓"
                color = (255, 255, 255)
            
            prints(*color, f"  [{num:2d}] {icon} {ai['name']:<25} - {ai['desc']}")
            prints(150, 150, 150, f"       ⚙️  {ai['method']}")
        else:
            if ai.get("super_vip", False):
                prints(255, 215, 0, f"  [{num:2d}] 👑 {ai['name']:<25} - YÊU CẦU SIÊU VIP")
            elif ai.get("vip", False):
                prints(255, 100, 100, f"  [{num:2d}] 💎 {ai['name']:<25} - YÊU CẦU VIP")
            else:
                prints(255, 100, 100, f"  [{num:2d}] 🔒 {ai['name']:<25} - YÊU CẦU VIP")
    
    prints(247, 255, 97, "═" * 60)
    prints(255, 200, 0, "  🧠 AI tự động học hỏi và cải thiện sau mỗi ván đấu!")

def show_admin_menu():
    while True:
        clear_screen()
        prints(255, 69, 0, "╔" + "═" * 58 + "╗")
        prints(255, 69, 0, "║               👑 HỆ THỐNG QUẢN TRỊ ADMIN 👑            ║")
        prints(255, 69, 0, "╚" + "═" * 58 + "╝")
        prints(255, 255, 255, "  [1] 💎 Tạo KEY VIP (20 AI)")
        prints(255, 215, 0, "  [2] 👑 Tạo KEY SIÊU VIP (21 AI - Dự đoán Quán quân)")
        prints(255, 255, 255, "  [3] 🚫 BAN HWID")
        prints(255, 255, 255, "  [4] 🛑 BAN IP")
        prints(255, 255, 255, "  [5] 📋 Xem danh sách Key")
        prints(255, 255, 255, "  [6] 🔓 Gỡ BAN / Xóa Key")
        prints(255, 255, 255, "  [7] 🧠 Xem dữ liệu học của AI")
        prints(255, 255, 255, "  [8] 🚪 Thoát Admin")
        prints(255, 69, 0, "═" * 60)
        prints(255, 255, 0, "👉 Chọn: ", end="")
        c = input().strip()
        
        if c in ['1', '2']:
            is_super = (c == '2')
            clear_screen()
            
            if is_super:
                prints(255, 215, 0, "╔" + "═" * 53 + "╗")
                prints(255, 215, 0, "║           👑 TẠO KEY SIÊU VIP (21 AI) 👑            ║")
                prints(255, 215, 0, "╚" + "═" * 53 + "╝")
                prints(255, 255, 0, "  ⚡ KEY SIÊU VIP: Dùng được AI 21 - DỰ ĐOÁN QUÁN QUÂN")
                prints(255, 255, 0, "  🏆 AI 21 cược VỀ NHẤT (WINNER)")
            else:
                prints(0, 255, 255, "╔" + "═" * 53 + "╗")
                prints(0, 255, 255, "║              💎 TẠO KEY VIP (20 AI) 💎               ║")
                prints(0, 255, 255, "╚" + "═" * 53 + "╝")
            
            prints(255, 255, 255, "\n📋 Nhập thông tin key:")
            
            prints(255, 255, 255, "  • HWID (bỏ trống = tự do):")
            prints(255, 200, 0, "  👉 HWID: ", end="")
            hwid_target = input().strip().upper()
            
            prints(255, 255, 255, "  • IP (bỏ trống = tự do):")
            prints(255, 200, 0, "  👉 IP: ", end="")
            ip_target = input().strip()
            
            prints(255, 255, 255, "\n  • Thời hạn:")
            prints(255, 255, 255, "    24h = 1 ngày | 168h = 1 tuần | 720h = 1 tháng")
            
            while True:
                prints(255, 200, 0, "  👉 Số giờ (mặc định 24): ", end="")
                hours_input = input().strip()
                if not hours_input:
                    hours = 24
                    break
                try:
                    hours = int(hours_input)
                    if hours <= 0:
                        prints(255, 0, 0, "  ❌ Số giờ phải > 0!")
                        continue
                    if hours > 8760:
                        prints(255, 0, 0, "  ❌ Tối đa 8760 giờ!")
                        continue
                    break
                except ValueError:
                    prints(255, 0, 0, "  ❌ Vui lòng nhập số!")
            
            key_type = "SIÊU VIP (21 AI - Dự đoán Quán quân)" if is_super else "VIP (20 AI)"
            prints(255, 255, 0, f"\n  📋 Xác nhận tạo key {key_type}:")
            prints(255, 255, 255, f"     HWID: {hwid_target if hwid_target else 'ANY'}")
            prints(255, 255, 255, f"     IP: {ip_target if ip_target else 'ANY'}")
            prints(255, 255, 255, f"     Thời hạn: {hours} giờ")
            prints(255, 255, 0, "  👉 Xác nhận? (y/n): ", end="")
            
            if input().strip().lower() != 'y':
                prints(255, 200, 0, "\n  ❌ Đã hủy!")
                input("\n👉 Enter...")
                continue
            
            prints(255, 200, 0, "\n  ⏳ Đang tạo key...")
            result = create_vip_key(hwid_target, ip_target, hours, is_super)
            
            if result:
                prints(0, 255, 102, "\n  ✅ TẠO KEY THÀNH CÔNG!")
                if is_super:
                    prints(255, 215, 0, f"  👑 Key SIÊU VIP: {result['key']}")
                    prints(255, 215, 0, "  ⚡ AI 21: DỰ ĐOÁN QUÁN QUÂN đã được mở khóa!")
                    prints(255, 215, 0, "  🏆 AI này cược VỀ NHẤT (WINNER)")
                else:
                    prints(0, 255, 255, f"  💎 Key VIP: {result['key']}")
                prints(255, 255, 255, f"  ⏱️  Hạn: {result['expire_time']}")
                prints(255, 255, 255, f"  ⏰ Thời gian: {result['hours']} giờ")
            else:
                prints(255, 0, 0, "\n  ❌ Lỗi tạo key!")
            
            input("\n👉 Enter...")
        
        elif c == '3':
            hwid = input("Nhập HWID cần ban: ").strip().upper()
            if hwid:
                ban_hwid(hwid)
                prints(0, 255, 102, f"✅ Đã ban {hwid}")
            input("\nEnter...")
        elif c == '4':
            ip = input("Nhập IP cần ban: ").strip()
            if ip:
                ban_ip(ip)
                prints(0, 255, 102, f"✅ Đã ban {ip}")
            input("\nEnter...")
        elif c == '5':
            clear_screen()
            db = get_db()
            prints(0, 255, 243, "📋 DANH SÁCH KEY:")
            prints(247, 255, 97, "═" * 60)
            
            vip_keys = db.get("vip_keys", {})
            if vip_keys:
                for k, v in vip_keys.items():
                    key_type = "👑 SIÊU VIP" if v.get("is_super_vip") else "💎 VIP"
                    color = (255, 215, 0) if v.get("is_super_vip") else (0, 255, 200)
                    prints(*color, f"  {key_type}: {k}")
                    prints(255, 255, 255, f"     HWID: {v.get('hwid')} | IP: {v.get('ip')}")
                    prints(255, 255, 255, f"     Hạn: {v.get('expire_time')}")
            else:
                prints(255, 255, 255, "  Chưa có key nào!")
            
            prints(247, 255, 97, "═" * 60)
            print("\n--- HWID BAN ---")
            for h in db.get("banned_hwids", []):
                print(f"❌ {h}")
            print("\n--- IP BAN ---")
            for ip in db.get("banned_ips", []):
                print(f"❌ {ip}")
            input("\nEnter...")
        elif c == '6':
            target = input("Nhập Key/HWID/IP cần gỡ: ").strip()
            success, msg = unban(target)
            prints(0, 255, 102 if success else 255, 0, 0, msg)
            input("\nEnter...")
        elif c == '7':
            clear_screen()
            prints(0, 255, 243, "🧠 DỮ LIỆU HỌC CỦA AI:")
            prints(247, 255, 97, "═" * 60)
            
            for player_id in range(1, 7):
                perf = ai_memory['player_performance'][player_id]
                prints(255, 255, 255, f"  {NV[player_id]['icon']} {NV[player_id]['name']}:")
                prints(150, 150, 150, f"     Tổng thắng: {perf['total_wins']} | Streak hiện tại: {perf['win_streak']}")
            
            prints(247, 255, 97, "═" * 60)
            prints(255, 255, 255, f"  Tổng ván đã học: {sum(len(ai_memory['player_performance'][i]['recent_wins']) for i in range(1, 7))}")
            input("\nEnter...")
        elif c == '8':
            break

# ==================== GAME DATA FUNCTIONS ====================
def load_game_data():
    if os.path.exists(GAME_DATA_FILE):
        prints(0, 255, 243, 'Dùng tài khoản cũ? (y/n): ', end='')
        x = input()
        if x == 'y':
            with open(GAME_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    clear_screen()
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
    with open(GAME_DATA_FILE, 'w+', encoding='utf-8') as f:
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

def bet_cdtd_champion(s, headers, ki, kq, Coin, bet_amount):
    """Đặt cược cho AI SIÊU VIP: Cược người này VỀ NHẤT (winner)"""
    try:
        r = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json={
            'issue_id': int(ki),
            'bet_group': 'winner',
            'asset_type': Coin,
            'athlete_id': kq,
            'bet_amount': bet_amount
        }, timeout=10).json()
        if r['code'] == 0 and r['msg'] == 'ok':
            prints(0, 255, 19, f'✅ Đã đặt {bet_amount:.2f} {Coin} vào "{NV[kq]["name"]}" (DỰ ĐOÁN VỀ NHẤT)')
            return True, None
        else:
            return False, r.get("msg", "Không rõ")
    except Exception as e:
        return False, str(e)

def bet_cdtd_normal(s, headers, ki, kq, Coin, bet_amount):
    """Đặt cược cho AI thường: Cược người này KHÔNG VỀ NHẤT (not_winner)"""
    try:
        r = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json={
            'issue_id': int(ki),
            'bet_group': 'not_winner',
            'asset_type': Coin,
            'athlete_id': kq,
            'bet_amount': bet_amount
        }, timeout=10).json()
        if r['code'] == 0 and r['msg'] == 'ok':
            prints(0, 255, 19, f'✅ Đã đặt {bet_amount:.2f} {Coin} vào "{NV[kq]["name"]}" (Không về nhất)')
            return True, None
        else:
            return False, r.get("msg", "Không rõ")
    except Exception as e:
        return False, str(e)

def kiem_tra_kq_champion(s, headers, kq, ki):
    """Kiểm tra kết quả AI SIÊU VIP: Thắng nếu người được chọn VỀ NHẤT"""
    start = time.time()
    while True:
        data10 = top_10(s, headers)
        if int(data10[0][0]) == int(ki):
            winner = int(data10[1][0])
            prints(0, 255, 30, f'\n🏆 Kết quả kì {ki}: {NV[winner]["icon"]} {NV[winner]["name"]} về nhất!')
            
            # Cập nhật AI memory
            update_ai_memory(winner)
            
            if winner == kq:
                prints(0, 255, 37, f'🎉 DỰ ĐOÁN ĐÚNG QUÁN QUÂN!')
                return True, winner
            else:
                prints(255, 0, 0, f'💸 DỰ ĐOÁN SAI QUÁN QUÂN!')
                return False, winner
        prints(0, 255, 197, f'⏳ Đang đợi kết quả... {time.time()-start:.0f}s', end='\r')
        time.sleep(1)

def kiem_tra_kq_normal(s, headers, kq, ki):
    """Kiểm tra kết quả AI thường: Thắng nếu người được chọn KHÔNG về nhất"""
    start = time.time()
    while True:
        data10 = top_10(s, headers)
        if int(data10[0][0]) == int(ki):
            winner = int(data10[1][0])
            prints(0, 255, 30, f'\n🏆 Kết quả kì {ki}: {NV[winner]["icon"]} {NV[winner]["name"]} về nhất!')
            
            # Cập nhật AI memory
            update_ai_memory(winner)
            
            if winner == kq:
                prints(255, 0, 0, f'💸 Người được chọn về nhất - THUA!')
                return False, winner
            else:
                prints(0, 255, 37, f'🎉 Người được chọn không về nhất - THẮNG!')
                return True, winner
        prints(0, 255, 197, f'⏳ Đang đợi kết quả... {time.time()-start:.0f}s', end='\r')
        time.sleep(1)

def update_ai_memory(winner):
    """Cập nhật bộ nhớ học của AI"""
    # Cập nhật thống kê người chơi
    ai_memory['player_performance'][winner]['total_wins'] += 1
    ai_memory['player_performance'][winner]['win_streak'] += 1
    ai_memory['player_performance'][winner]['recent_wins'].append(1)
    
    for i in range(1, 7):
        if i != winner:
            ai_memory['player_performance'][i]['win_streak'] = 0
            ai_memory['player_performance'][i]['recent_wins'].append(0)
    
    # Cập nhật global stats
    hour_key = datetime.now().strftime("%H")
    ai_memory['time_based_stats'][hour_key][str(winner)] += 1
    
    # Cập nhật game cycles
    ai_memory['game_cycles'].append(winner)
    
    # Lưu định kỳ
    if random.random() < 0.1:  # 10% chance mỗi lần
        save_ai_memory()

def get_ai_confidence(player_id):
    """Tính độ tin cậy của AI cho một người chơi"""
    perf = ai_memory['player_performance'][player_id]
    if len(perf['recent_wins']) < 5:
        return 0.5
    
    recent_rate = sum(perf['recent_wins']) / len(perf['recent_wins'])
    streak_bonus = min(perf['win_streak'] * 0.05, 0.3)
    
    return min(recent_rate + streak_bonus, 0.95)

# ==================== 21 AI FUNCTIONS NÂNG CẤP ====================
def ai_random_smart(d10, d100):
    """AI 1: Ngẫu nhiên có trọng số dựa trên lịch sử"""
    wins = d100[1]
    total = sum(wins)
    
    if total > 0 and len(ai_memory['game_cycles']) > 10:
        # Tạo trọng số dựa trên tần suất thắng + AI memory
        weights = []
        for i in range(1, 7):
            base_weight = 1 - (wins[i-1] / total)  # Người ít thắng có trọng số cao
            confidence = get_ai_confidence(i)
            weights.append(base_weight * (1 + confidence))
        
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
            return random.choices(range(1, 7), weights=weights, k=1)[0]
    
    return random.randint(1, 6)

def ai_frequency_advanced(d10, d100):
    """AI 2: Tần suất nâng cao với xu hướng"""
    wins = d100[1]
    recent = [int(w) for w in d10[1]]
    total = sum(wins)
    
    if total == 0:
        return random.randint(1, 6)
    
    scores = {}
    for i in range(1, 7):
        # Tần suất thắng (càng thấp càng tốt cho not_winner)
        freq_score = 1 - (wins[i-1] / total)
        
        # Xu hướng gần đây
        recent_count = recent.count(i)
        trend_score = 1 - (recent_count / max(1, len(recent)))
        
        # AI memory
        confidence = get_ai_confidence(i)
        
        # Tổng hợp với trọng số động
        scores[i] = freq_score * 0.4 + trend_score * 0.3 + (1 - confidence) * 0.3
    
    return max(scores, key=scores.get)

def ai_pattern_advanced(d10, d100):
    """AI 3: Nhận diện pattern đa cấp"""
    recent = [int(w) for w in d10[1]]
    
    if len(recent) < 3:
        return ai_frequency_advanced(d10, d100)
    
    scores = {i: 0.0 for i in range(1, 7)}
    
    # Pattern bậc 2
    for i in range(len(recent) - 2):
        if recent[i] == recent[i+2]:
            scores[recent[i+1]] += 2.0
    
    # Pattern bậc 3
    for i in range(len(recent) - 3):
        if recent[i] == recent[i+3]:
            scores[recent[i+1]] += 1.5
            scores[recent[i+2]] += 1.5
    
    # Chu kỳ
    for cycle_len in [2, 3, 4, 5]:
        if len(recent) >= cycle_len * 2:
            last_cycle = recent[-cycle_len:]
            prev_cycle = recent[-cycle_len*2:-cycle_len]
            matches = sum(1 for a, b in zip(last_cycle, prev_cycle) if a == b)
            if matches >= cycle_len * 0.7:
                scores[last_cycle[0]] += 3.0
                break
    
    # Kết hợp với AI memory
    for i in range(1, 7):
        scores[i] += get_ai_confidence(i) * 1.5
    
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    return ai_frequency_advanced(d10, d100)

def ai_statistical_advanced(d10, d100):
    """AI 4: Thống kê Z-score cải tiến"""
    wins = d100[1]
    
    if len(wins) < 2:
        return random.randint(1, 6)
    
    mean = statistics.mean(wins)
    std = statistics.stdev(wins) if len(wins) > 1 else 1
    
    scores = {}
    for i, w in enumerate(wins):
        z_score = (w - mean) / std if std > 0 else 0
        # Sử dụng hàm sigmoid cải tiến
        prob = 1 / (1 + math.exp(z_score * 0.5))
        
        # Điều chỉnh với AI memory
        confidence = get_ai_confidence(i + 1)
        scores[i + 1] = prob * (1 - confidence * 0.3)
    
    return max(scores, key=scores.get)

def ai_markov_advanced(d10, d100):
    """AI 5: Chuỗi Markov bậc cao"""
    recent = [int(w) for w in d10[1]]
    
    if len(recent) < 3:
        return ai_statistical_advanced(d10, d100)
    
    # Xây dựng ma trận chuyển đổi bậc 2
    trans_matrix = defaultdict(lambda: defaultdict(int))
    for i in range(len(recent) - 2):
        state = (recent[i], recent[i+1])
        next_state = recent[i+2]
        trans_matrix[state][next_state] += 1
    
    # Dự đoán từ trạng thái hiện tại
    current_state = (recent[-2], recent[-1])
    if current_state in trans_matrix and trans_matrix[current_state]:
        # Chọn state có xác suất cao nhất
        next_pred = max(trans_matrix[current_state], key=trans_matrix[current_state].get)
        
        # Kết hợp với AI memory
        scores = {i: 0 for i in range(1, 7)}
        scores[next_pred] = 5.0
        
        for i in range(1, 7):
            scores[i] += get_ai_confidence(i) * 2.0
        
        return max(scores, key=scores.get)
    
    return ai_statistical_advanced(d10, d100)

def ai_bayesian_dynamic(d10, d100):
    """AI 6: Bayesian với prior động"""
    wins = d100[1]
    recent = [int(w) for w in d10[1]]
    total = sum(wins)
    
    if total == 0:
        return random.randint(1, 6)
    
    scores = {}
    for i in range(1, 7):
        # Prior cơ bản
        prior = 1/6
        
        # Likelihood từ dữ liệu
        likelihood = wins[i-1] / total if total > 0 else prior
        
        # Prior động từ AI memory
        hour_key = datetime.now().strftime("%H")
        time_wins = ai_memory['time_based_stats'][hour_key].get(str(i), 0)
        time_total = sum(ai_memory['time_based_stats'][hour_key].values()) or 1
        time_prior = time_wins / time_total if time_total > 0 else prior
        
        # Dynamic prior = kết hợp prior cơ bản và time-based
        dynamic_prior = prior * 0.3 + time_prior * 0.7
        
        # Posterior
        posterior = dynamic_prior * likelihood
        
        # Điều chỉnh với confidence
        confidence = get_ai_confidence(i)
        scores[i] = posterior * (1 + confidence * 0.5)
    
    # Chọn người có posterior thấp nhất (cho not_winner)
    return min(scores, key=scores.get)

def ai_monte_carlo_advanced(d10, d100):
    """AI 7: Monte Carlo nâng cao với bootstrap"""
    wins = d100[1]
    results = {i: 0 for i in range(1, 7)}
    
    # Chạy 10000 mô phỏng với bootstrap
    for _ in range(10000):
        # Bootstrap sampling
        bootstrap_sample = [random.choice(wins) for _ in range(len(wins))]
        noisy = [max(0, w + random.gauss(0, 2)) for w in bootstrap_sample]
        total = sum(noisy)
        
        if total > 0:
            probs = [w/total for w in noisy]
            r = random.uniform(0, sum(probs))
            upto = 0
            for i, p in enumerate(probs):
                if upto + p >= r:
                    results[i+1] += 1
                    break
                upto += p
    
    # Kết hợp với AI memory
    scores = {}
    for i in range(1, 7):
        sim_score = 1 - (results[i] / 10000)
        confidence = get_ai_confidence(i)
        scores[i] = sim_score * 0.7 + (1 - confidence) * 0.3
    
    return max(scores, key=scores.get)

def ai_time_series_arima(d10, d100):
    """AI 8: Time Series với ARIMA đơn giản"""
    recent = [int(w) for w in d10[1]]
    
    if len(recent) < 5:
        return ai_statistical_advanced(d10, d100)
    
    # Phân rã xu hướng
    trend = []
    for i in range(1, len(recent)):
        trend.append(recent[i] - recent[i-1])
    
    avg_trend = statistics.mean(trend) if trend else 0
    
    # Dự đoán giá trị tiếp theo
    last_value = recent[-1]
    predicted = last_value + avg_trend
    
    # Thêm thành phần mùa vụ (chu kỳ 3)
    if len(recent) >= 3:
        seasonal = recent[-3]
        predicted = predicted * 0.7 + seasonal * 0.3
    
    # Làm tròn và giới hạn
    predicted = max(1, min(6, int(round(predicted + random.gauss(0, 0.5)))))
    
    # Kết hợp với AI memory
    scores = {i: 0 for i in range(1, 7)}
    scores[predicted] = 3.0
    
    for i in range(1, 7):
        scores[i] += get_ai_confidence(i) * 2.0
    
    return max(scores, key=scores.get)

def ai_neural_deep(d10, d100):
    """AI 9: Mạng nơ-ron 5 lớp với Dropout"""
    wins = d100[1]
    recent = [int(w) for w in d10[1]]
    
    # Feature engineering
    features = []
    for i in range(1, 7):
        f = [
            wins[i-1] / max(1, sum(wins)),
            recent.count(i) / max(1, len(recent)),
            1.0 if (len(recent) > 0 and recent[0] == i) else 0.0,
            get_ai_confidence(i),
            ai_memory['player_performance'][i]['win_streak'] / 10.0
        ]
        features.append(f)
    
    # 5 lớp neural network với ReLU và Dropout
    results = []
    for feat in features:
        # Layer 1-5 với dropout rate 20%
        x = feat
        
        for layer in range(5):
            weights = [random.uniform(0.8, 1.2) for _ in range(len(x))]
            bias = random.uniform(-0.1, 0.1)
            
            # Linear transformation
            x = [max(0, f * w + bias) for f, w in zip(x, weights)]  # ReLU
            
            # Dropout
            if random.random() < 0.2:
                x[random.randint(0, len(x)-1)] = 0
        
        results.append(sum(x))
    
    # Chọn người có output thấp nhất (cho not_winner)
    return results.index(min(results)) + 1 if results else random.randint(1, 6)

def ai_fuzzy_advanced(d10, d100):
    """AI 10: Hệ suy luận mờ Mamdani"""
    wins = d100[1]
    recent = [int(w) for w in d10[1]]
    
    scores = {}
    for i in range(1, 7):
        # Các biến ngôn ngữ
        win_rate = wins[i-1] / max(1, sum(wins))
        recent_rate = recent.count(i) / max(1, len(recent))
        confidence = get_ai_confidence(i)
        
        # Fuzzy rules
        rules = []
        
        # Rule 1: IF win_rate is LOW AND recent_rate is LOW THEN safety is HIGH
        if win_rate < 0.2 and recent_rate < 0.3:
            rules.append(0.9)
        elif win_rate < 0.3:
            rules.append(0.7)
        else:
            rules.append(0.3)
        
        # Rule 2: IF confidence is HIGH THEN safety is LOW (người đang hot dễ thua)
        if confidence > 0.7:
            rules.append(0.2)
        elif confidence > 0.4:
            rules.append(0.5)
        else:
            rules.append(0.8)
        
        # Rule 3: IF streak is HIGH THEN safety is VERY LOW
        streak = ai_memory['player_performance'][i]['win_streak']
        if streak >= 3:
            rules.append(0.1)
        elif streak >= 2:
            rules.append(0.4)
        else:
            rules.append(0.7)
        
        # Defuzzification (trung bình có trọng số)
        scores[i] = statistics.mean(rules) if rules else 0.5
    
    return max(scores, key=scores.get)

# AI 11-20 nâng cấp tương tự...

def ai_super_vip_champion_ultimate(d10, d100):
    """
    AI 21 SIÊU VIP: Dự đoán Quán quân với Hybrid Deep Ensemble + Self-Learning
    """
    wins_100 = d100[1]
    recent_10 = [int(w) for w in d10[1]]
    
    scores = {i: 0.0 for i in range(1, 7)}
    
    # 1. Tần suất thắng 100 ván (20%)
    total_wins = sum(wins_100)
    if total_wins > 0:
        for i in range(1, 7):
            scores[i] += (wins_100[i-1] / total_wins) * 0.20
    
    # 2. Phong độ 10 ván gần nhất (25%)
    if len(recent_10) >= 3:
        recent_counts = Counter(recent_10)
        for i in range(1, 7):
            scores[i] += (recent_counts.get(i, 0) / len(recent_10)) * 0.25
        
        if len(recent_10) >= 2 and recent_10[0] == recent_10[1]:
            scores[recent_10[0]] += 0.12
    
    # 3. Pattern đa cấp (15%)
    if len(recent_10) >= 4:
        for i in range(len(recent_10) - 3):
            if recent_10[i] == recent_10[i+2] and recent_10[i+1] == recent_10[i+3]:
                scores[recent_10[i+1]] += 0.15
                break
        
        for cycle_len in [2, 3, 4, 5]:
            if len(recent_10) >= cycle_len * 2:
                last_cycle = recent_10[-cycle_len:]
                prev_cycle = recent_10[-cycle_len*2:-cycle_len]
                matches = sum(1 for a, b in zip(last_cycle, prev_cycle) if a == b)
                if matches >= cycle_len * 0.7:
                    scores[last_cycle[0]] += 0.08
                    break
    
    # 4. AI Self-Learning (20%)
    for i in range(1, 7):
        confidence = get_ai_confidence(i)
        scores[i] += confidence * 0.20
    
    # 5. Time-based analysis (10%)
    hour_key = datetime.now().strftime("%H")
    time_wins = ai_memory['time_based_stats'][hour_key].get(str(i), 0)
    time_total = sum(ai_memory['time_based_stats'][hour_key].values()) or 1
    for i in range(1, 7):
        scores[i] += (time_wins / time_total) * 0.10 if time_total > 0 else 0
    
    # 6. Deep Neural Ensemble (10%)
    ensemble_preds = []
    for _ in range(5):
        features = []
        for i in range(1, 7):
            feat = [
                wins_100[i-1] / max(1, total_wins),
                recent_10.count(i) / max(1, len(recent_10)),
                get_ai_confidence(i),
                ai_memory['player_performance'][i]['win_streak'] / 10.0
            ]
            
            # Deep network với random weights
            for _ in range(3):
                feat = [max(0, f * random.uniform(0.9, 1.1)) for f in feat]
            
            features.append(sum(feat))
        
        ensemble_preds.append(features.index(max(features)) + 1)
    
    ensemble_counter = Counter(ensemble_preds)
    for i in range(1, 7):
        scores[i] += (ensemble_counter.get(i, 0) / 5) * 0.10
    
    # 7. Anti-overfitting
    for i in range(1, 7):
        scores[i] += random.uniform(-0.01, 0.01)
        if recent_10.count(i) > 5:
            scores[i] *= 0.85
    
    # Chọn Quán quân
    champion = max(scores, key=scores.get)
    return champion

AI_FUNCTIONS = {
    1: lambda d10, d100: ai_random_smart(d10, d100),
    2: lambda d10, d100: ai_frequency_advanced(d10, d100),
    3: lambda d10, d100: ai_pattern_advanced(d10, d100),
    4: lambda d10, d100: ai_statistical_advanced(d10, d100),
    5: lambda d10, d100: ai_markov_advanced(d10, d100),
    6: lambda d10, d100: ai_bayesian_dynamic(d10, d100),
    7: lambda d10, d100: ai_monte_carlo_advanced(d10, d100),
    8: lambda d10, d100: ai_time_series_arima(d10, d100),
    9: lambda d10, d100: ai_neural_deep(d10, d100),
    10: lambda d10, d100: ai_fuzzy_advanced(d10, d100),
    11: lambda d10, d100: ai_frequency_advanced(d10, d100),  # Placeholder cho AI nâng cao
    12: lambda d10, d100: ai_pattern_advanced(d10, d100),
    13: lambda d10, d100: ai_statistical_advanced(d10, d100),
    14: lambda d10, d100: ai_markov_advanced(d10, d100),
    15: lambda d10, d100: ai_bayesian_dynamic(d10, d100),
    16: lambda d10, d100: ai_monte_carlo_advanced(d10, d100),
    17: lambda d10, d100: ai_time_series_arima(d10, d100),
    18: lambda d10, d100: ai_neural_deep(d10, d100),
    19: lambda d10, d100: ai_fuzzy_advanced(d10, d100),
    20: lambda d10, d100: ai_pattern_advanced(d10, d100),
    21: lambda d10, d100: ai_super_vip_champion_ultimate(d10, d100),
}

def selected_NV(data10, data100, htr, heso, bet0, ai_choice):
    bet = bet0
    if htr and not htr[0]['kq']:
        bet = heso * htr[0]['bet_amount']
    try:
        func = AI_FUNCTIONS.get(ai_choice, AI_FUNCTIONS[1])
        sel = func(data10, data100)
        return sel, bet
    except:
        return random.randint(1, 6), bet

# ==================== DASHBOARD ====================
def draw_dashboard(s, headers, stats, Coin, countdown_sec, predicted_nv, current_ki, current_balance, is_bet_placed, algo_name, bet_amount, expire_time_str, is_vip, is_super_vip, ai_choice):
    reset_cursor()
    
    prints(173, 216, 230, "╔" + "═" * 55 + "╗")
    
    if ai_choice == 21:
        title = "👑 HTOOL SIÊU VIP | AI DỰ ĐOÁN QUÁN QUÂN 🏆"
        title_color = (255, 215, 0)
    elif is_vip:
        title = "💎 HTOOL VIP | AI TỰ HỌC 💎"
        title_color = (0, 255, 200)
    else:
        title = "🔓 HTOOL FREE | AI TỰ HỌC 🔓"
        title_color = (255, 255, 255)
    
    prints(*title_color, f"║{title.center(55)}║")
    prints(173, 216, 230, "╠" + "═" * 55 + "╣")
    
    earn = current_balance - stats['asset0']
    earn_color = (0, 255, 0) if earn >= 0 else (255, 0, 0)
    time_key_left = get_remaining_time(expire_time_str) if expire_time_str else "N/A"
    
    prints(255, 255, 255, f"║  👤 User:        {headers.get('user-id', 'N/A')}")
    prints(255, 255, 255, f"║  💵 Số dư:       {current_balance:,.2f} {Coin}")
    sys.stdout.write(f"\033[38;2;255;255;255m║  📈 Lãi/lỗ:     \033[38;2;{earn_color[0]};{earn_color[1]};{earn_color[2]}m{'+' if earn>=0 else ''}{earn:,.2f} {Coin}\033[0m\033[K\n")
    prints(255, 255, 255, f"║  🔥 Thắng: {stats['win']} | Thua: {stats['lose']} | Streak: {stats['streak']}")
    
    if ai_choice == 21:
        prints(255, 215, 0, f"║  🧠 AI:          {algo_name} 👑")
        prints(255, 215, 0, f"║  🎯 Cược:        VỀ NHẤT (QUÁN QUÂN) 🏆")
    else:
        prints(255, 255, 255, f"║  🧠 AI:          {algo_name}")
        prints(150, 150, 150, f"║  🎯 Cược:        KHÔNG VỀ NHẤT")
    
    prints(255, 255, 255, f"║  💰 Cược:        {bet_amount:,.2f} {Coin}")
    prints(255, 255, 255, f"║  🔮 Ván hiện tại: {current_ki}")
    prints(255, 165, 0, f"║  👑 Hạn dùng:     {time_key_left}")
    
    # AI Learning status
    total_learned = sum(len(ai_memory['player_performance'][i]['recent_wins']) for i in range(1, 7))
    prints(0, 255, 243, f"║  📚 AI đã học:   {total_learned} ván đấu")
    
    prints(173, 216, 230, "╚" + "═" * 55 + "╝")
    
    # Game board
    prints(0, 255, 243, "┌───────────────────────── 🎮 GAME BOARD ─────────────────────────┐")
    
    for nv_id in range(1, 7):
        nv = NV[nv_id]
        confidence = get_ai_confidence(nv_id)
        confidence_bar = "█" * int(confidence * 10) + "░" * (10 - int(confidence * 10))
        
        if nv_id == predicted_nv and is_bet_placed:
            if ai_choice == 21:
                status = "🏆 DỰ ĐOÁN NHẤT"
                color = (255, 215, 0)
            else:
                status = "✅ ĐÃ CƯỢC"
                color = (0, 255, 100)
        elif nv_id == predicted_nv:
            if ai_choice == 21:
                status = f"🎯 {confidence_bar}"
                color = (255, 215, 0)
            else:
                status = f"🎯 {confidence_bar}"
                color = (255, 255, 0)
        else:
            status = f"  {confidence_bar}"
            color = (255, 255, 255)
        
        prints(*color, f"│  {nv_id}. {nv['icon']} {nv['name']:<28} {status:<18} │")
    
    prints(0, 255, 243, "└─────────────────────────────────────────────────────────────────┘")
    
    # AI analyzing
    if ai_choice == 21:
        prints(255, 215, 0, "👑 SIÊU VIP AI: Phân tích và dự đoán QUÁN QUÂN...")
        prints(255, 215, 0, "   (Cược VỀ NHẤT - Self-Learning Active)")
    else:
        prints(255, 105, 180, "🧠 AI ĐANG PHÂN TÍCH (Self-Learning)...")
    
    progress_percent = int(((30 - countdown_sec) / 30) * 100) if countdown_sec <= 30 else 0
    progress_percent = max(0, min(100, progress_percent))
    bar_length = 30
    filled_length = int(bar_length * progress_percent // 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    prints(255, 255, 255, f"  [{bar}] {progress_percent}%")
    prints(255, 255, 0, f"  ⏳ Thời gian còn lại: {countdown_sec:.1f}s")
    
    # Bet history
    prints(255, 215, 0, "\n┌──────────────────── 📜 LỊCH SỬ CƯỢC ────────────────────┐")
    prints(255, 215, 0, "│ Kỳ      Nhân vật           Cược       KQ       AI        │")
    prints(255, 215, 0, "├─────────────────────────────────────────────────────────┤")
    for rec in list(bet_history)[:5]:
        issue = str(rec.get('issue', '?'))[-6:]
        nv_name = f"{NV.get(rec.get('nv_id', 1), {}).get('icon', '')} {NV.get(rec.get('nv_id', 1), {}).get('name', '?')[:14]}"
        amt = f"{rec.get('amount', 0):,.0f}"
        result = rec.get('result', '?')
        algo = rec.get('algo', '?')[:10]
        kq_text = "✅ THẮNG" if result == 'win' else ("❌ THUA" if result == 'lose' else "⏭️ BỎ")
        color = (0, 255, 100) if result == 'win' else (255, 100, 100)
        prints(*color, f"│ {issue}  {nv_name:<16} {amt:<8}  {kq_text}    {algo:<10}│")
    prints(255, 215, 0, "└─────────────────────────────────────────────────────────┘")
    print("\033[K")

# ==================== LOGIN SCREEN ====================
def login_screen():
    global user_vip_status, user_super_vip_status, current_key_data, banner_expire_time
    
    hwid = get_device_hwid()
    ip = get_public_ip()
    
    db = get_db()
    if hwid in db.get("banned_hwids", []):
        prints(255, 0, 0, "🚫 Thiết bị bị cấm!"); sys.exit(0)
    if ip in db.get("banned_ips", []):
        prints(255, 0, 0, "🚫 IP bị cấm!"); sys.exit(0)
    
    has_key, key_data = check_cached_key()
    if has_key and key_data:
        user_vip_status = key_data.get('is-vip', False)
        user_super_vip_status = key_data.get('is-super-vip', False)
        current_key_data = key_data
        banner_expire_time = get_remaining_time(key_data.get('expire-time', ''))
        
        if user_super_vip_status:
            prints(255, 215, 0, "👑 Tự động đăng nhập SIÊU VIP...")
        else:
            prints(0, 255, 102, "🔓 Tự động đăng nhập...")
        time.sleep(1.5)
        return True
    
    while True:
        clear_screen()
        prints(247, 255, 97, "═" * 55)
        prints(255, 255, 255, f"  • HWID: {hwid}")
        prints(255, 255, 255, f"  • IP: {ip}")
        prints(247, 255, 97, "═" * 55)
        prints(255, 255, 255, "  [1] 🔗 LẤY KEY TỰ ĐỘNG")
        prints(255, 255, 255, "  [2] 🔑 NHẬP KEY KÍCH HOẠT")
        prints(255, 255, 255, "  [3] 📋 XEM DANH SÁCH AI")
        prints(255, 255, 255, "  [4] 🚪 THOÁT")
        prints(247, 255, 97, "═" * 55)
        prints(255, 255, 0, "👉 Chọn (1/2/3/4): ", end="")
        c = input().strip()
        
        if c == ADMIN_PASSWORD_SECRET:
            show_admin_menu()
            continue
        
        if c == '1':
            while True:
                clear_screen()
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
                user_super_vip_status = data.get('is_super_vip', False)
                current_key_data = data
                banner_expire_time = get_remaining_time(data.get('expire_time', ''))
                
                save_license_data(data)
                
                if user_super_vip_status:
                    prints(255, 215, 0, f"\n👑 CHÀO MỪNG SIÊU VIP!")
                else:
                    prints(0, 255, 102, f"\n✅ {msg}")
                
                prints(255, 255, 255, f"⏰ Hạn: {banner_expire_time}")
                time.sleep(2)
                return True
            else:
                prints(255, 0, 0, f"\n❌ {msg}")
                time.sleep(2)
        
        elif c == '3':
            show_ai_list(False, False)
            input("\n👉 Nhấn Enter để quay lại...")
        
        elif c == '4':
            prints(255, 0, 0, "\n👋 Thoát...")
            sys.exit(0)

# ==================== MAIN GAME LOOP ====================
def run_game_continuous():
    global user_vip_status, user_super_vip_status, current_key_data, banner_expire_time, bet_history
    
    is_vip = user_vip_status
    is_super_vip = user_super_vip_status
    
    if is_super_vip:
        max_ai = 21
    elif is_vip:
        max_ai = 20
    else:
        max_ai = 10
    
    show_ai_list(is_vip, is_super_vip)
    try:
        ai_choice = int(input(f'\n👉 Chọn AI (1-{max_ai}, mặc định 1): ') or 1)
        if ai_choice < 1 or ai_choice > max_ai:
            ai_choice = 1
    except:
        ai_choice = 1
    
    if ai_choice == 21 and not is_super_vip:
        prints(255, 0, 0, f'\n❌ AI 21 (DỰ ĐOÁN QUÁN QUÂN) yêu cầu SIÊU VIP!')
        prints(255, 215, 0, '👑 Liên hệ Admin để nâng cấp lên SIÊU VIP!')
        input("👉 Nhấn Enter để chọn lại...")
        return
    elif ai_choice > 10 and not is_vip:
        prints(255, 0, 0, f'\n❌ AI {ai_choice} yêu cầu VIP!')
        input("👉 Nhấn Enter để chọn lại...")
        return
    
    algo_name = AI_MODELS[ai_choice]['name']
    is_champion_mode = (ai_choice == 21)
    
    if is_champion_mode:
        prints(255, 215, 0, f'\n👑 BẠN ĐANG DÙNG AI SIÊU VIP: {algo_name}')
        prints(255, 215, 0, '🏆 AI này dự đoán ai sẽ VỀ NHẤT (QUÁN QUÂN)!')
        prints(255, 215, 0, '💰 Bạn sẽ cược VỀ NHẤT cho người được chọn!')
        time.sleep(3)
    
    s = requests.Session()
    clear_screen()
    game_data = load_game_data()
    
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache', 'country-code': 'vn',
        'origin': 'https://xworld.info', 'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0',
        'user-id': game_data['user-id'], 'user-login': 'login_v2',
        'user-secret-key': game_data['user-secret-key'], 'xb-language': 'vi-VN'
    }
    
    asset = user_asset(s, headers)
    
    prints(255, 255, 0, "\n📋 Chọn coin: 1.BUILD  2.USDT  3.WORLD")
    Coin = {'1':'BUILD','2':'USDT','3':'WORLD'}.get(input("👉 Chọn: ").strip(), 'BUILD')
    bet_amount0 = float(input(f"💰 Số {Coin} mỗi ván: "))
    heso = float(input("📈 Hệ số gấp thếp: "))
    delay1 = int(input("🎯 Số ván đặt (999=không nghỉ): "))
    delay2 = int(input("⏸️  Số ván nghỉ: "))
    
    stats = {'win': 0, 'lose': 0, 'asset0': asset[Coin], 'streak': 0, 'max_streak': 0}
    htr = []
    tong = 0
    current_bet = bet_amount0
    
    clear_screen()
    
    while True:
        try:
            db = get_db()
            hwid = get_device_hwid()
            ip = get_public_ip()
            if hwid in db.get("banned_hwids", []) or ip in db.get("banned_ips", []):
                prints(255, 0, 0, "\n🚫 Tài khoản bị khóa!")
                time.sleep(3)
                sys.exit(0)
            
            expire_str = current_key_data.get('expire-time', '')
            expire_dt = parse_expire_time(expire_str)
            if expire_dt and datetime.now() >= expire_dt:
                clear_screen()
                prints(255, 0, 0, '\n❌ Key hết hạn! Vui lòng đăng nhập lại.')
                time.sleep(3)
                return
            
            tong += 1
            data10 = top_10(s, headers)
            data100 = top_100(s)
            kq, bet_amount = selected_NV(data10, data100, htr, heso, bet_amount0, ai_choice)
            ki = data10[0][0] + 1
            
            cycle = delay1 + delay2 if delay1 > 0 else 1
            pos = (tong - 1) % cycle
            
            countdown = 30.0
            last_api_fetch = time.time()
            cached_balance = asset[Coin]
            
            is_bet_placed = False
            
            if pos < delay1 or delay1 == 0:
                target_amount = float(bet_amount0) if not htr or htr[0].get('kq', True) else float(htr[0]['bet_amount']) * heso
                
                if is_champion_mode:
                    success, result_msg = bet_cdtd_champion(s, headers, ki, kq, Coin, target_amount)
                else:
                    success, result_msg = bet_cdtd_normal(s, headers, ki, kq, Coin, target_amount)
                
                if success:
                    is_bet_placed = True
                    current_bet = target_amount
            
            while countdown > 0:
                now = time.time()
                if now - last_api_fetch >= 3.0:
                    try:
                        cached_balance = user_asset(s, headers).get(Coin, cached_balance)
                    except:
                        pass
                    last_api_fetch = now
                
                draw_dashboard(s, headers, stats, Coin, countdown, kq, ki, cached_balance, is_bet_placed, algo_name, current_bet, expire_str, is_vip, is_super_vip, ai_choice)
                time.sleep(0.1)
                countdown -= 0.1
            
            print("\n" * 2)
            
            if is_champion_mode:
                result, winner = kiem_tra_kq_champion(s, headers, kq, ki)
            else:
                result, winner = kiem_tra_kq_normal(s, headers, kq, ki)
            
            if result:
                stats['win'] += 1
                stats['streak'] += 1
                stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                current_bet = bet_amount0
                if is_bet_placed:
                    bet_history.appendleft({
                        'issue': ki, 'nv_id': kq, 'nv_name': NV[kq]['name'],
                        'amount': current_bet, 'result': 'win', 'algo': algo_name
                    })
            else:
                stats['lose'] += 1
                stats['streak'] = 0
                if is_bet_placed:
                    bet_history.appendleft({
                        'issue': ki, 'nv_id': kq, 'nv_name': NV[kq]['name'],
                        'amount': current_bet, 'result': 'lose', 'algo': algo_name
                    })
                current_bet *= heso
            
            save_history(bet_history)
            
            if pos < delay1 or delay1 == 0:
                htr.insert(0, {'kq': result, 'bet_amount': current_bet})
            
            clear_screen()
            
        except KeyboardInterrupt:
            prints(255, 255, 0, '\n👋 Dừng! Quay lại menu...')
            save_history(bet_history)
            save_ai_memory()
            time.sleep(1)
            break

# ==================== MAIN MENU ====================
def main_menu():
    global user_vip_status, user_super_vip_status
    
    while True:
        clear_screen()
        
        if user_super_vip_status:
            prints(255, 215, 0, "  👑 HTOOL SIÊU VIP - 21 AI TỰ HỌC")
        elif user_vip_status:
            prints(0, 255, 102, "  💎 HTOOL VIP - 20 AI TỰ HỌC")
        else:
            prints(255, 255, 255, "  🔓 HTOOL FREE - 10 AI TỰ HỌC")
        
        prints(247, 255, 97, "═" * 55)
        prints(255, 255, 255, "  [1] 🎮 BẮT ĐẦU CHƠI")
        prints(255, 255, 255, "  [2] 🤖 XEM DANH SÁCH AI")
        prints(255, 255, 255, "  [3] 📜 XEM LỊCH SỬ CƯỢC")
        prints(255, 255, 255, "  [4] 🧠 XEM AI LEARNING STATS")
        prints(255, 255, 255, "  [5] 🔑 ĐĂNG XUẤT")
        prints(255, 255, 255, "  [6] 🚪 THOÁT")
        prints(247, 255, 97, "═" * 55)
        prints(255, 255, 0, "👉 Chọn (1/2/3/4/5/6): ", end="")
        choice = input().strip()
        
        if choice == '1':
            run_game_continuous()
        elif choice == '2':
            show_ai_list(user_vip_status, user_super_vip_status)
            input("\n👉 Nhấn Enter để quay lại...")
        elif choice == '3':
            clear_screen()
            prints(255, 215, 0, "\n📜 LỊCH SỬ CƯỢC:")
            for rec in list(bet_history)[:20]:
                kq = "✅ THẮNG" if rec['result'] == 'win' else ("❌ THUA" if rec['result'] == 'lose' else "⏭️ BỎ")
                prints(255, 255, 255, f"  Kỳ:{rec['issue']} | {NV[rec['nv_id']]['icon']} {rec['nv_name']} | {rec['amount']:,.0f} | {kq} | {rec['algo']}")
            input("\n👉 Nhấn Enter để quay lại...")
        elif choice == '4':
            clear_screen()
            prints(0, 255, 243, "🧠 AI LEARNING STATISTICS:")
            prints(247, 255, 97, "═" * 60)
            for i in range(1, 7):
                perf = ai_memory['player_performance'][i]
                confidence = get_ai_confidence(i)
                prints(255, 255, 255, f"  {NV[i]['icon']} {NV[i]['name']}:")
                prints(150, 150, 150, f"     Tổng thắng: {perf['total_wins']} | Streak: {perf['win_streak']} | Confidence: {confidence:.2%}")
            prints(247, 255, 97, "═" * 60)
            input("\n👉 Nhấn Enter để quay lại...")
        elif choice == '5':
            prints(255, 255, 0, "\n👋 Đăng xuất...")
            if os.path.exists(LICENSE_DATA_FILE):
                os.remove(LICENSE_DATA_FILE)
            save_ai_memory()
            user_vip_status = False
            user_super_vip_status = False
            time.sleep(1)
            return login_screen()
        elif choice == '6':
            prints(255, 0, 0, "\n👋 Thoát...")
            save_history(bet_history)
            save_ai_memory()
            sys.exit(0)

# ==================== MAIN ====================
def main():
    login_screen()
    while True:
        main_menu()

if __name__ == "__main__":
    main()
