import sys
import subprocess

# --- BỘ TỰ ĐỘNG KIỂM TRA VÀ CÀI ĐẶT THƯ VIỆN CÒN THIẾU ---
REQUIRED_LIBS = {
    "requests": "requests",
    "colorama": "colorama"
}

for lib_name, pip_name in REQUIRED_LIBS.items():
    try:
        __import__(lib_name)
    except ImportError:
        print(f"🔄 Không tìm thấy thư viện '{lib_name}'. Đang tự động cài đặt qua pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"✅ Đã cài đặt thành công: {pip_name}")
        except Exception as e:
            print(f"❌ Lỗi tự động cài đặt {pip_name}: {e}")
            sys.exit(1)
# --------------------------------------------------------

from datetime import datetime, timedelta
import random
import hashlib
from collections import Counter, defaultdict, deque
import statistics
import platform
import base64
import urllib.parse
import requests
import string
import math
import json
import os
import time
import webbrowser
from colorama import Fore, Style, init

# ==================== CẤU HÌNH JSONBIN ====================
JSONBIN_API_KEY = "$2a$10$YOUR_JSONBIN_API_KEY_HERE"  # Thay bằng API Key của bạn
JSONBIN_BIN_ID = "6a61dfbdf5f4af5e29b50537"  # Thay bằng Bin ID của bạn
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
# ==========================================================

HISTORY_FILE = "bet_history.json"
LOCAL_DB_FILE = "local_keys.json"
DEVICE_FILE = "device_info.json"
GAME_DATA_FILE = "game_data.json"

def init_local_db():
    """Khởi tạo database local cho keys"""
    if not os.path.exists(LOCAL_DB_FILE):
        default_data = {
            "vip_keys": {},
            "banned_hwids": [],
            "banned_ips": []
        }
        with open(LOCAL_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=4)

def get_local_db():
    """Đọc database local"""
    init_local_db()
    with open(LOCAL_DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_local_db(data):
    """Lưu database local"""
    with open(LOCAL_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_device_info(hwid, ip):
    """Lưu thông tin thiết bị"""
    data = {
        "hwid": hwid,
        "ip": ip,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(DEVICE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_saved_device_info():
    """Lấy thông tin thiết bị đã lưu"""
    if os.path.exists(DEVICE_FILE):
        try:
            with open(DEVICE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('hwid'), data.get('ip')
        except:
            pass
    return None, None

def save_game_data(data):
    """Lưu dữ liệu game"""
    with open(GAME_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_game_data():
    """Tải dữ liệu game"""
    if os.path.exists(GAME_DATA_FILE):
        try:
            with open(GAME_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def fetch_keys_from_jsonbin():
    """Lấy danh sách keys từ JSONbin"""
    try:
        headers = {
            "X-Master-Key": JSONBIN_API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.get(f"{JSONBIN_URL}/latest", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("record", {})
        else:
            print(f"⚠️ Lỗi kết nối JSONbin: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Không thể kết nối đến JSONbin: {e}")
        return None

def sync_keys_from_jsonbin():
    """Đồng bộ keys từ JSONbin về local"""
    remote_data = fetch_keys_from_jsonbin()
    if remote_data:
        local_db = get_local_db()
        if "vip_keys" in remote_data:
            local_db["vip_keys"].update(remote_data["vip_keys"])
        if "banned_hwids" in remote_data:
            local_db["banned_hwids"] = list(set(local_db["banned_hwids"] + remote_data["banned_hwids"]))
        if "banned_ips" in remote_data:
            local_db["banned_ips"] = list(set(local_db["banned_ips"] + remote_data["banned_ips"]))
        
        save_local_db(local_db)
        return True
    return False

def get_today_key(hwid):
    """Tạo key free theo ngày"""
    today_str = datetime.now().strftime("%d%m%Y")
    md5_hash = hashlib.md5(f"{today_str}-{hwid}".encode()).hexdigest()[:8]
    return f"HTOOL-{md5_hash.upper()}"

def check_key_status(hwid):
    """Tự động kiểm tra trạng thái key"""
    sync_keys_from_jsonbin()
    
    local_db = get_local_db()
    
    # Tạo key free hôm nay
    today_key = get_today_key(hwid)
    
    # Kiểm tra xem có key VIP nào cho HWID này không
    for key, key_data in local_db.get("vip_keys", {}).items():
        if key_data.get("hwid") == hwid or key_data.get("hwid") == "ANY":
            try:
                expire_time = datetime.strptime(key_data["expire_time"], "%Y-%m-%d %H:%M:%S")
                if expire_time > datetime.now():
                    return {
                        "key": key,
                        "type": "vip",
                        "expire_time": key_data["expire_time"],
                        "hwid": hwid
                    }
            except:
                pass
    
    # Nếu không có key VIP, trả về key free
    return {
        "key": today_key,
        "type": "free",
        "expire_time": (datetime.now() + timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S"),
        "hwid": hwid
    }

def check_security_status():
    """Kiểm tra trạng thái bảo mật"""
    sync_keys_from_jsonbin()
    
    hwid = get_device_hwid()
    ip = get_public_ip()
    local_db = get_local_db()
    
    if hwid in local_db.get("banned_hwids", []):
        clear_screen()
        prints(255, 0, 0, "╔" + "═" * 60 + "╗")
        prints(255, 0, 0, "║ [QUYẾT ĐỊNH KHÓA]: THIẾT BỊ CỦA BẠN ĐÃ BỊ CẤM KHỎI HỆ THỐNG!  ║")
        prints(255, 0, 0, f"║ Lý do: Vi phạm chính sách / HWID BAN: {hwid:<23} ║")
        prints(255, 0, 0, "╚" + "═" * 60 + "╝")
        input("\nNhấn Enter để thoát...")
        sys.exit(0)
        
    if ip in local_db.get("banned_ips", []):
        clear_screen()
        prints(255, 0, 0, "╔" + "═" * 60 + "╗")
        prints(255, 0, 0, "║ [QUYẾT ĐỊNH KHÓA]: ĐỊA CHỈ IP CỦA BẠN ĐÃ BỊ BAN KHỎI TOOL!   ║")
        prints(255, 0, 0, f"║ IP Hiện tại: {ip:<45} ║")
        prints(255, 0, 0, "╚" + "═" * 60 + "╝")
        input("\nNhấn Enter để thoát...")
        sys.exit(0)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return deque(json.load(f), maxlen=50)
        except:
            pass
    return deque(maxlen=50)

def save_history(hist):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(list(hist), f, indent=2, ensure_ascii=False)

bet_history = load_history()

room_info = {
    1: {'name': 'Nhà kho', 'icon': '📦'},
    2: {'name': 'Phòng họp', 'icon': '🪑'},
    3: {'name': 'Phòng Giám đốc', 'icon': '💼'},
    4: {'name': 'Phòng trò chuyện', 'icon': '💬'},
    5: {'name': 'Phòng Giám sát', 'icon': '📹'},
    6: {'name': 'Vavan phòng', 'icon': '🏢'},
    7: {'name': 'Phòng Tài Vụ', 'icon': '💰'},
    8: {'name': 'Phòng Nhân sự', 'icon': '👥'}
}

# ==================== 40 LOGIC AI ====================
AI_LIST = {
    1:  {"name": "RANDOM", "desc": "🎲 Phật Độ - Ngẫu nhiên", "vip": False},
    2:  {"name": "MIN_PLAYER_BET", "desc": "🛡️ An Toàn - Ít người & tiền", "vip": False},
    3:  {"name": "PROBABILITY", "desc": "📊 Xác Suất - Tỉ lệ sống sót", "vip": False},
    4:  {"name": "FOLLOW_KILLER", "desc": "🔪 Theo Sát Thủ - Phòng vừa kill", "vip": False},
    5:  {"name": "SEQUENTIAL", "desc": "🔢 Tuần Tự - 1→2→3→...→8", "vip": False},
    6:  {"name": "KILLER_PERSONALITY", "desc": "🧠 Tính Cách Sát Thủ", "vip": False},
    7:  {"name": "SMART_SAFE", "desc": "🤖 Thông Minh - AI an toàn", "vip": False},
    8:  {"name": "FOLLOW_KILLER_DELAYED", "desc": "👣 Theo Vết - Delay 1 ván", "vip": False},
    9:  {"name": "HIDE_SEEK_MASTER", "desc": "🙈 Thánh Trốn Tìm", "vip": False},
    10: {"name": "BALANCE", "desc": "⚖️ Cân Bằng", "vip": False},
    11: {"name": "MOST_PLAYERS", "desc": "👥 Đông Nhất", "vip": False},
    12: {"name": "LEAST_PLAYERS", "desc": "👤 Ít Nhất", "vip": False},
    13: {"name": "RICHEST", "desc": "💎 Giàu Nhất", "vip": False},
    14: {"name": "POOREST", "desc": "🪙 Nghèo Nhất", "vip": False},
    15: {"name": "ALTERNATE", "desc": "🔄 Xen Kẽ", "vip": False},
    16: {"name": "AVOID_RESULT", "desc": "🚫 Tránh Kết Quả", "vip": False},
    17: {"name": "COLD", "desc": "❄️ Phòng Lạnh", "vip": False},
    18: {"name": "HOT", "desc": "🔥 Phòng Nóng", "vip": False},
    19: {"name": "MEDIAN", "desc": "📐 Trung Vị", "vip": False},
    20: {"name": "PATTERN", "desc": "🔍 Mẫu Lặp", "vip": False},
    21: {"name": "VIP_RANDOM", "desc": "👑 VIP Random", "vip": True},
    22: {"name": "KILLER_WAVE", "desc": "🌊 Bắt Sóng Sát Thủ", "vip": True},
    23: {"name": "PSYCHO_ANALYSIS", "desc": "🔮 Phân Tích Tâm Lý", "vip": True},
    24: {"name": "MARKOV_CHAIN", "desc": "⛓️ Chuỗi Markov", "vip": True},
    25: {"name": "DEEP_LEARNING", "desc": "🧬 Học Sâu", "vip": True},
    26: {"name": "REINFORCEMENT", "desc": "🎓 Học Tăng Cường", "vip": True},
    27: {"name": "BAYESIAN", "desc": "📈 Xác Suất Bayes", "vip": True},
    28: {"name": "K_MEANS", "desc": "🔵 Phân Cụm K-Means", "vip": True},
    29: {"name": "NEURAL", "desc": "🧠 Mạng Nơ-ron", "vip": True},
    30: {"name": "FUZZY", "desc": "🌫️ Logic Mờ", "vip": True},
    31: {"name": "GENETIC", "desc": "🧬 Thuật Toán Di Truyền", "vip": True},
    32: {"name": "ANT_COLONY", "desc": "🐜 Kiến Bò", "vip": True},
    33: {"name": "PARTICLE_SWARM", "desc": "🕊️ Bầy Đàn", "vip": True},
    34: {"name": "KNN", "desc": "🎯 K-Nearest Neighbors", "vip": True},
    35: {"name": "DECISION_TREE", "desc": "🌳 Cây Quyết Định", "vip": True},
    36: {"name": "RANDOM_FOREST", "desc": "🌲 Rừng Ngẫu Nhiên", "vip": True},
    37: {"name": "GRADIENT_BOOST", "desc": "📈 Gradient Boost", "vip": True},
    38: {"name": "LSTM", "desc": "🔮 LSTM", "vip": True},
    39: {"name": "TRANSFORMER", "desc": "🤖 Transformer", "vip": True},
    40: {"name": "ENSEMBLE", "desc": "👥 Tổng Hợp", "vip": True},
}

# Game state cho AI
game_state = {
    'room_players': {r: 0 for r in range(1, 9)},
    'room_bets': {r: 0 for r in range(1, 9)},
    'room_stats': {r: {"kills": 0, "survives": 0} for r in range(1, 9)},
    'kill_log': deque(maxlen=100),
    'last_killed': None,
}
_sequential_index = 0

# ==================== 40 AI FUNCTIONS ====================
def ai_random():
    return random.randint(1, 8)

def ai_min_player_bet():
    scores = {}
    for r in range(1, 9):
        scores[r] = game_state['room_players'][r] * 0.6 + game_state['room_bets'][r] * 0.0004
    if game_state['last_killed']:
        scores[game_state['last_killed']] += 5
    return min(scores, key=scores.get)

def ai_probability():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        scores[r] = (s + 1) / (k + s + 2)
    return max(scores, key=scores.get)

def ai_follow_killer():
    return game_state['last_killed'] if game_state['last_killed'] else random.randint(1, 8)

def ai_sequential():
    global _sequential_index
    room = (_sequential_index % 8) + 1
    _sequential_index += 1
    return room

def ai_killer_personality():
    scores = {}
    for r in range(1, 9):
        if r == game_state['last_killed']:
            scores[r] = 999
        else:
            scores[r] = game_state['room_players'][r] + game_state['room_bets'][r] * 0.001
    return min(scores, key=scores.get)

def ai_smart_safe():
    scores = {}
    max_p = max(game_state['room_players'].values()) or 1
    max_b = max(game_state['room_bets'].values()) or 1
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        sr = (s + 1) / (k + s + 2)
        ps = 1 - game_state['room_players'][r] / max_p
        bs = 1 - game_state['room_bets'][r] / max_b
        penalty = 0.5 if r == game_state['last_killed'] else 0
        scores[r] = 0.4 * sr + 0.3 * ps + 0.3 * bs - penalty
    return max(scores, key=scores.get)

def ai_follow_killer_delayed():
    if len(game_state['kill_log']) >= 2:
        return list(game_state['kill_log'])[-2]
    return random.randint(1, 8)

def ai_hide_seek_master():
    scores = {}
    max_p = max(game_state['room_players'].values()) or 1
    max_b = max(game_state['room_bets'].values()) or 1
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        danger = (k + 1) / (k + s + 2)
        crowd = game_state['room_players'][r] / max_p
        money = game_state['room_bets'][r] / max_b
        penalty = 1 if r == game_state['last_killed'] else 0
        scores[r] = 0.4 * danger + 0.3 * crowd + 0.3 * money + penalty
    return min(scores, key=scores.get)

def ai_balance():
    total_p = sum(game_state['room_players'].values())
    total_b = sum(game_state['room_bets'].values())
    avg_p = total_p / 8 if total_p > 0 else 0
    avg_b = total_b / 8 if total_b > 0 else 0
    scores = {}
    for r in range(1, 9):
        scores[r] = abs(game_state['room_players'][r] - avg_p) / (avg_p + 1) + abs(game_state['room_bets'][r] - avg_b) / (avg_b + 1)
    return min(scores, key=scores.get)

def ai_most_players():
    return max(range(1, 9), key=lambda r: game_state['room_players'][r])

def ai_least_players():
    return min(range(1, 9), key=lambda r: game_state['room_players'][r])

def ai_richest():
    return max(range(1, 9), key=lambda r: game_state['room_bets'][r])

def ai_poorest():
    return min(range(1, 9), key=lambda r: game_state['room_bets'][r])

def ai_alternate():
    if len(game_state['kill_log']) >= 3:
        last3 = list(game_state['kill_log'])[-3:]
        candidates = [r for r in range(1, 9) if r not in last3]
        if candidates:
            return random.choice(candidates)
    return random.randint(1, 8)

def ai_avoid_result():
    if game_state['last_killed']:
        candidates = [r for r in range(1, 9) if r != game_state['last_killed']]
        if candidates:
            return random.choice(candidates)
    return random.randint(1, 8)

def ai_cold():
    scores = {}
    for r in range(1, 9):
        scores[r] = -game_state['room_players'][r] * 2 - game_state['room_bets'][r] * 0.001
    return min(scores, key=scores.get)

def ai_hot():
    scores = {}
    for r in range(1, 9):
        scores[r] = game_state['room_players'][r] * 2 + game_state['room_bets'][r] * 0.001
    return max(scores, key=scores.get)

def ai_median():
    sorted_rooms = sorted(range(1, 9), key=lambda r: game_state['room_players'][r])
    return sorted_rooms[len(sorted_rooms) // 2]

def ai_pattern():
    if len(game_state['kill_log']) >= 3:
        last3 = list(game_state['kill_log'])[-3:]
        if last3[0] == last3[2]:
            return last3[1]
    return random.randint(1, 8)

def ai_vip_random():
    funcs = [ai_random, ai_min_player_bet, ai_probability, ai_follow_killer,
             ai_sequential, ai_killer_personality, ai_smart_safe, ai_follow_killer_delayed,
             ai_hide_seek_master, ai_balance, ai_most_players, ai_least_players,
             ai_richest, ai_poorest, ai_alternate, ai_avoid_result,
             ai_cold, ai_hot, ai_median, ai_pattern]
    return random.SystemRandom().choice(funcs)()

def ai_killer_wave():
    if len(game_state['kill_log']) >= 4:
        last4 = list(game_state['kill_log'])[-4:]
        for i in range(1, 4):
            if len(last4) >= i*2 and last4[-i:] == last4[-i*2:-i]:
                return last4[-i-1] if len(last4) > i else last4[-1]
    return ai_smart_safe()

def ai_psycho_analysis():
    max_room = max(range(1, 9), key=lambda r: game_state['room_players'][r])
    candidates = [r for r in range(1, 9) if r != max_room]
    return random.choice(candidates) if candidates else random.randint(1, 8)

def ai_markov_chain():
    if len(game_state['kill_log']) >= 5:
        transitions = defaultdict(lambda: defaultdict(int))
        kill_list = list(game_state['kill_log'])
        for i in range(len(kill_list) - 1):
            transitions[kill_list[i]][kill_list[i+1]] += 1
        last = kill_list[-1]
        if transitions[last]:
            return max(transitions[last].items(), key=lambda x: x[1])[0]
    return ai_smart_safe()

def ai_deep_learning():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        sr = (s + 1) / (k + s + 2)
        boost = -0.5 if r == game_state['last_killed'] else 0
        scores[r] = 0.5 * sr + 0.5 * boost + random.uniform(-0.1, 0.1)
    return max(scores, key=scores.get)

def ai_reinforcement():
    if len(game_state['kill_log']) >= 3:
        scores = {r: 0 for r in range(1, 9)}
        for room in list(game_state['kill_log'])[-20:]:
            scores[room] -= 1
        return min(scores, key=scores.get)
    return random.randint(1, 8)

def ai_bayesian():
    if len(game_state['kill_log']) >= 3:
        counts = Counter(game_state['kill_log'])
        total = len(game_state['kill_log'])
        posterior = {}
        for r in range(1, 9):
            posterior[r] = (counts.get(r, 0) + 1) / (total + 8)
        return min(posterior, key=posterior.get)
    return random.randint(1, 8)

def ai_k_means():
    if len(game_state['kill_log']) >= 6:
        counts = Counter(list(game_state['kill_log'])[-10:])
        safe = [r for r in range(1, 9) if counts.get(r, 0) < 2]
        return random.choice(safe) if safe else random.randint(1, 8)
    return random.randint(1, 8)

def ai_neural():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        scores[r] = (s - k + 10) / 20
    return max(scores, key=scores.get)

def ai_fuzzy():
    scores = {}
    for r in range(1, 9):
        p = game_state['room_players'][r]
        b = game_state['room_bets'][r]
        safety = (10 - min(p, 10)) * 0.5 + (1000 - min(b, 1000)) * 0.0005
        if r == game_state['last_killed']:
            safety -= 5
        scores[r] = safety
    return max(scores, key=scores.get)

def ai_genetic():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        scores[r] = (s + 1) / (k + s + 2)
    return max(scores, key=scores.get)

def ai_ant_colony():
    if len(game_state['kill_log']) >= 3:
        pheromone = Counter(game_state['kill_log'])
        return min(range(1, 9), key=lambda r: pheromone.get(r, 0))
    return random.randint(1, 8)

def ai_particle_swarm():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        scores[r] = (s + 1) / (k + s + 2)
    return max(scores, key=scores.get)

def ai_knn():
    if len(game_state['kill_log']) >= 3:
        k = min(3, len(game_state['kill_log']))
        nearest = list(game_state['kill_log'])[-k:]
        counts = Counter(nearest)
        return min(counts, key=counts.get)
    return random.randint(1, 8)

def ai_decision_tree():
    if game_state['last_killed'] and game_state['room_players'][game_state['last_killed']] > 5:
        candidates = [r for r in range(1, 9) if r != game_state['last_killed']]
        return random.choice(candidates) if candidates else random.randint(1, 8)
    return ai_probability()

def ai_random_forest():
    preds = [ai_probability() if random.random() > 0.5 else ai_min_player_bet() for _ in range(5)]
    return Counter(preds).most_common(1)[0][0]

def ai_gradient_boost():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        scores[r] = (s + 1) / (k + s + 2)
    return max(scores, key=scores.get)

def ai_lstm():
    if len(game_state['kill_log']) >= 5:
        last5 = list(game_state['kill_log'])[-5:]
        if last5[0] == last5[3] and last5[1] == last5[4]:
            return last5[2]
    return ai_markov_chain()

def ai_transformer():
    scores = {}
    for r in range(1, 9):
        k = game_state['room_stats'][r]["kills"]
        s = game_state['room_stats'][r]["survives"]
        recency = 1 - (list(game_state['kill_log']).count(r) / max(1, len(game_state['kill_log'])))
        scores[r] = 0.4 * recency + 0.6 * (s / max(1, k + s))
    return max(scores, key=scores.get)

def ai_ensemble():
    funcs = [ai_killer_wave, ai_psycho_analysis, ai_markov_chain, ai_deep_learning,
             ai_reinforcement, ai_bayesian, ai_k_means, ai_neural, ai_fuzzy, ai_genetic,
             ai_ant_colony, ai_particle_swarm, ai_knn, ai_decision_tree, ai_random_forest,
             ai_gradient_boost, ai_lstm, ai_transformer]
    votes = defaultdict(int)
    for func in funcs:
        try:
            votes[func()] += 1
        except:
            continue
    return max(votes, key=votes.get) if votes else random.randint(1, 8)

AI_FUNCTIONS = {
    1: ai_random, 2: ai_min_player_bet, 3: ai_probability, 4: ai_follow_killer,
    5: ai_sequential, 6: ai_killer_personality, 7: ai_smart_safe, 8: ai_follow_killer_delayed,
    9: ai_hide_seek_master, 10: ai_balance, 11: ai_most_players, 12: ai_least_players,
    13: ai_richest, 14: ai_poorest, 15: ai_alternate, 16: ai_avoid_result,
    17: ai_cold, 18: ai_hot, 19: ai_median, 20: ai_pattern,
    21: ai_vip_random, 22: ai_killer_wave, 23: ai_psycho_analysis, 24: ai_markov_chain,
    25: ai_deep_learning, 26: ai_reinforcement, 27: ai_bayesian, 28: ai_k_means,
    29: ai_neural, 30: ai_fuzzy, 31: ai_genetic, 32: ai_ant_colony,
    33: ai_particle_swarm, 34: ai_knn, 35: ai_decision_tree, 36: ai_random_forest,
    37: ai_gradient_boost, 38: ai_lstm, 39: ai_transformer, 40: ai_ensemble,
}

# ==================== PHÂN BIỆT KEY FREE & VIP ====================
def is_vip_key(key):
    """Kiểm tra xem key có phải VIP không"""
    local_db = get_local_db()
    return key in local_db.get("vip_keys", {})

def get_available_ais(key):
    """Trả về danh sách AI có thể dùng dựa trên loại key"""
    if is_vip_key(key):
        return list(range(1, 41))  # VIP: Tất cả 40 AI
    else:
        return list(range(1, 11))  # Free: Chỉ 10 AI đầu

def choose_room_by_ai(ai_number, key):
    """Chọn phòng bằng AI, có kiểm tra quyền"""
    available_ais = get_available_ais(key)
    
    if ai_number not in available_ais:
        prints(255, 165, 0, f"\n⚠️ AI {ai_number} yêu cầu KEY VIP! Tự động chuyển sang AI 7 (Smart Safe)")
        time.sleep(2)
        ai_number = 7
    
    func = AI_FUNCTIONS.get(ai_number, ai_random)
    try:
        return func()
    except:
        return random.randint(1, 8)

def show_all_ai(key_type="free"):
    clear_screen()
    banner()
    prints(255, 215, 0, "\n📋 DANH SÁCH THUẬT TOÁN AI:")
    prints(255, 215, 0, "═" * 60)
    
    if key_type == "vip":
        prints(0, 255, 102, "\n👑 CHẾ ĐỘ VIP - TẤT CẢ 40 AI:")
        prints(0, 255, 102, "\n🔓 CƠ BẢN (1-20):")
        for num, ai in AI_LIST.items():
            if num <= 20:
                prints(255, 255, 255, f"  [{num:2d}] {ai['name']:<25} - {ai['desc']}")
        prints(255, 165, 0, "\n👑 NÂNG CAO VIP (21-40):")
        for num, ai in AI_LIST.items():
            if num > 20:
                prints(255, 255, 255, f"  [{num:2d}] {ai['name']:<25} - {ai['desc']}")
    else:
        prints(0, 255, 102, "\n🔓 FREE - 10 AI CƠ BẢN:")
        for num, ai in AI_LIST.items():
            if num <= 10:
                prints(255, 255, 255, f"  [{num:2d}] {ai['name']:<25} - {ai['desc']}")
        prints(255, 165, 0, "\n👑 VIP ONLY (11-40) - Yêu cầu Key VIP:")
        prints(255, 165, 0, "   (Các AI từ 11-40 chỉ dành cho tài khoản VIP)")
    
    prints(255, 215, 0, "═" * 60)

def update_game_state(killed_room):
    """Cập nhật game state khi có kết quả"""
    game_state['kill_log'].append(killed_room)
    game_state['last_killed'] = killed_room
    for r in range(1, 9):
        if r == killed_room:
            game_state['room_stats'][r]["kills"] += 1
        else:
            game_state['room_stats'][r]["survives"] += 1

init(autoreset=True)

def reset_cursor():
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    sys.stdout.write(f"\033[38;2;{r};{g};{b}m{text}\033[0m\033[K{end}")
    sys.stdout.flush()

def get_device_hwid():
    hw_info = (
        platform.node() + 
        platform.system() + 
        platform.machine() + 
        platform.processor()
    )
    return hashlib.md5(hw_info.encode()).hexdigest().upper()[:16]

def get_public_ip():
    urls = [
        "https://api64.ipify.org?format=text",
        "https://icanhazip.com",
        "https://ident.me",
        "https://v4.ident.me"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=4)
            if response.status_code == 200:
                ip = response.text.strip()
                if ip and not ip.startswith("127."):
                    return ip
        except Exception:
            continue
    return "Không rõ IP (Mất mạng)"

def banner():
    banner_text = """
░██╗░░██╗████████╗░██████╗░░██████╗░██╗░░░░░
░██║░░██║╚══██╔══╝██╔═══██╗██╔═══██╗██║░░░░░
░███████║░░░██║░░░██║░░░██║██║░░░██║██║░░░░░
░██╔══██║░░░██║░░░██║░░░██║██║░░░██║██║░░░░░
░██║░░██║░░░██║░░░╚██████╔╝╚██████╔╝███████╗
░╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░░╚══════╝░╚══════╝
    """
    r, g, b = 255, 255, 255
    for line in banner_text.split('\n'):
        for char in line:
            prints(r, g, b, char, end='')
            time.sleep(0.0005)
            r = max(50, r - 5)
            b = max(50, b - 1)
        r, g, b = 255, 255, 255
        print()

    prints(247, 255, 97, "✨" + "═" * 60 + "✨")
    prints(32, 230, 151, "🌟 HTOOL XWORLD AUTO | 40 AI LOGIC 🌟".center(62))
    prints(247, 255, 97, "═" * 62)

    contacts = [
        ("📺 YouTube", "https://www.youtube.com/@HTOOL-NC"),
        ("🎵 TikTok", "https://www.tiktok.com/@cng1237929"),
        ("💬 Zalo Group", "https://zalo.me/g/fmyvre167"),
        ("📱 Telegram", "https://t.me/+PByWNy8hDxYzYTRl"),
        ("👨‍💻 Admin", "Thành Công")
    ]

    for label, info in contacts:
        prints(100, 200, 255, f"  {label:<15}: ", end="")
        prints(255, 255, 255, info)

    prints(247, 255, 97, "═" * 62)
    print()

def draw_dashboard(s, headers, stats, Coin, countdown_sec, predicted_room, current_ki, current_balance, is_bet_placed=False, last_killed_room=None, expire_time_str="", algo_name="", bet_amount=0, key_type="free"):
    reset_cursor()
    
    if key_type == "vip":
        border_color = (255, 165, 0)
        title = "👑 HTOOL VIP | 40 AI LOGIC 👑"
    else:
        border_color = (173, 216, 230)
        title = "🏆 HTOOL FREE | 10 AI CƠ BẢN 🏆"
    
    prints(border_color[0], border_color[1], border_color[2], "╔" + "═" * 53 + "╗")
    prints(border_color[0], border_color[1], border_color[2], f"║           {title}            ║")
    prints(border_color[0], border_color[1], border_color[2], "╠" + "═" * 53 + "╣")
    
    earn = current_balance - stats['asset0']
    earn_color = (0, 255, 0) if earn >= 0 else (255, 0, 0)
    
    time_key_left = "Đang kiểm tra..."
    if expire_time_str:
        try:
            expire_dt = datetime.strptime(expire_time_str, "%Y-%m-%d %H:%M:%S")
            diff = expire_dt - datetime.now()
            if diff.total_seconds() > 0:
                hours, remainder = divmod(int(diff.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                time_key_left = f"{hours}h {minutes}m {seconds}s"
            else:
                time_key_left = "Đã hết hạn Key!"
        except Exception:
            pass

    prints(255, 255, 255, f"║  👤 User:        {headers.get('user-id', 'N/A')}")
    prints(255, 255, 255, f"║  💵 Số dư:       {current_balance:,.2f} {Coin}")
    sys.stdout.write(f"\033[38;2;255;255;255m║  📈 Lãi/lỗ:     \033[38;2;{earn_color[0]};{earn_color[1]};{earn_color[2]}m{'+' if earn>=0 else ''}{earn:,.2f} {Coin}\033[0m\033[K\n")
    prints(255, 255, 255, f"║  🔥 Thắng: {stats['win']} | Thua: {stats['lose']} | Streak: {stats['streak']}")
    
    if key_type == "vip":
        prints(255, 165, 0, f"║  🔑 Loại Key:    👑 VIP (40 AI)")
    else:
        prints(0, 255, 102, f"║  🔑 Loại Key:    🔓 FREE (10 AI)")
    
    prints(255, 255, 255, f"║  🧠 AI:          {algo_name}")
    prints(255, 255, 255, f"║  💰 Cược:        {bet_amount:,.2f} {Coin}")
    prints(255, 255, 255, f"║  🔮 Ván hiện tại: {current_ki}")
    prints(255, 165, 0,   f"║  ⏰ Hạn dùng Key: {time_key_left}")
    prints(border_color[0], border_color[1], border_color[2], "╚" + "═" * 53 + "╝")

    prints(0, 255, 243, "┌─────────────────────── 🎮 GAME BOARD ───────────────────────┐")
    for r_id in range(1, 9):
        r_name = room_info[r_id]['name']
        r_icon = room_info[r_id]['icon']
        
        status_text = "Bình thường"
        if r_id == predicted_room and is_bet_placed:
            status_text = "✅ ĐÃ CƯỢC"
        elif r_id == predicted_room:
            status_text = "🎯 GỢI Ý"
        elif last_killed_room and r_id == last_killed_room:
            status_text = "💀 SÁT THỦ"

        line = f"│  {r_id}. {r_icon} {r_name:<20} {status_text:>24}  │"
        
        if r_id == predicted_room:
            prints(46, 254, 46, line) 
        elif last_killed_room and r_id == last_killed_room:
            prints(254, 46, 46, line) 
        else:
            prints(255, 255, 255, line) 
        
    prints(0, 255, 243, "└─────────────────────────────────────────────────────────────┘")

    prints(255, 105, 180, "🧠 AI ĐANG PHÂN TÍCH...")
    progress_percent = int(((45 - countdown_sec) / 45) * 100)
    progress_percent = max(0, min(100, progress_percent))
    
    bar_length = 30
    filled_length = int(bar_length * progress_percent // 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    prints(255, 255, 255, f"  [{bar}] {progress_percent}%")
    prints(255, 255, 0, f"  ⏳ Thời gian còn lại: {countdown_sec:.1f}s")
    
    prints(255, 215, 0, "\n┌────────────────── 📜 LỊCH SỬ CƯỢC ──────────────────┐")
    prints(255, 215, 0, "│ Kỳ      Phòng           Cược       KQ       AI      │")
    prints(255, 215, 0, "├─────────────────────────────────────────────────────┤")
    for rec in list(bet_history)[:5]:
        issue = str(rec.get('issue', '?'))[-6:]
        room = f"{rec.get('room_icon', '')} {rec.get('room_name', '?'):<12}"
        amt = f"{rec.get('amount', 0):,.0f}"
        result = rec.get('result', '?')
        algo = rec.get('algo', '?')[:8]
        
        if result == 'win':
            kq = "✅ THẮNG"
        elif result == 'lose':
            kq = "❌ THUA "
        else:
            kq = "⏭️ BỎ  "
        
        prints(255, 255, 255, f"│ {issue}  {room}  {amt:<10} {kq}   {algo:<8}│")
    prints(255, 215, 0, "└─────────────────────────────────────────────────────┘")
    
    print("\033[K")

def top10_vth(s,headers,Coin):
    params = {'asset': Coin}
    try:
        response = s.get('https://api.escapemaster.net/escape_game/recent_10_issues', params=params, headers=headers, timeout=5).json()
        ki=[]
        phong=[]
        for i in response['data']:
            ki.append(i['issue_id'])
            phong.append(i['killed_room_id'])
        return ki,phong
    except Exception:
        fake_ki = [int(time.time() // 60)]
        fake_phong = [random.randint(1, 8)]
        return fake_ki, fake_phong

def chon_phong_ai(data10, data100, ai_number, key):
    """Chọn phòng bằng AI có kiểm tra quyền"""
    for r in range(1, 9):
        game_state['room_players'][r] = random.randint(0, 10)
        game_state['room_bets'][r] = random.randint(0, 5000)
    
    return choose_room_by_ai(ai_number, key)

def bet_vth(s,user_id,user_secretkey,room_id,Coin,bet_amount):
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9',
            'cache-control': 'no-cache',
            'country-code': 'vn',
            'origin': 'https://xworld.info',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://xworld.info/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, run with Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'user-id': user_id,
            'user-login': 'login_v2',
            'user-secret-key': user_secretkey,
            'xb-language': 'vi-VN',
        }
        json_data = {
            'asset_type': Coin,
            'user_id': user_id,
            'room_id': room_id,
            'bet_amount': float(bet_amount),
        }
        response = s.post('https://api.escapemaster.net/escape_game/bet', headers=headers, json=json_data, timeout=5).json()
        if response['code'] == 0 and response['msg'] == 'ok':
            return True, bet_amount
        else:
            return False, response['msg']
    except Exception as e:
        return False, str(e)

def user_asset(s,headers):
    try:
        json_data = {
            'user_id': int(headers['user-id']),
            'source': 'home',
        }
        response = requests.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data, timeout=5).json()
        asset={
            'USDT':response['data']['user_asset']['USDT'],
            'WORLD':response['data']['user_asset']['WORLD'],
            'BUILD':response['data']['user_asset']['BUILD']
        }
        return asset
    except Exception:
        return {'USDT': 100.0, 'WORLD': 5000.0, 'BUILD': 10000.0}

def top100_vth(s,headers,Coin):
    params = {'asset': Coin}
    try:
        response = s.get('https://api.escapemaster.net/escape_game/recent_100_issues', params=params, headers=headers, timeout=5).json()
        return response['data']['room_id_2_killed_times']
    except Exception:
        return {i: 12 for i in range(1, 9)}

def kiem_tra_kq_vth(s,headers,ki,bot_chon,Coin,tg):
    try:
        start_time=time.time()
        while True:
            if time.time()<=tg+60:
                prints(255,255,0,f'Đang chờ kết quả {time.time()-start_time:.0f}...',end='\r')
                time.sleep(1)
            data_top10=top10_vth(s,headers,Coin)
            if data_top10[0][0]==int(ki):
                p_name = room_info[data_top10[1][0]]['name']
                p_icon = room_info[data_top10[1][0]]['icon']
                prints(15, 87, 219,f'\n🔪 Sát thủ vào phòng {data_top10[1][0]} : {p_icon} {p_name}')
                
                killed_room = int(data_top10[1][0])
                update_game_state(killed_room)
                
                if int(bot_chon)==killed_room:
                    prints(255, 0, 38,'❌ Bạn thua rồi!')
                    time.sleep(3)
                    return False, time.time(), killed_room
                else:
                    prints(0, 255, 102,'✅ Xin chúc mừng, bạn đã thắng!')
                    time.sleep(3)
                    return True, time.time(), killed_room
            time.sleep(1)
    except Exception as e:
        return kiem_tra_kq_vth(s,headers,ki,bot_chon,Coin,tg)

def run_game(key_data):
    """Chạy game với key đã xác thực"""
    s = requests.Session()
    
    key_type = key_data["type"]
    current_key = key_data["key"]
    expire_time = key_data["expire_time"]
    
    clear_screen()
    banner()
    
    if key_type == "vip":
        prints(255, 165, 0, "👑 CHÀO MỪNG VIP! TRUY CẬP TOÀN BỘ 40 AI!")
        prints(255, 215, 0, f"🔑 Key: {current_key}")
    else:
        prints(0, 255, 102, "🔓 CHÀO MỪNG! BẠN ĐANG DÙNG KEY FREE (10 AI)")
        prints(255, 255, 255, f"🔑 Key: {current_key}")
        prints(255, 165, 0, "💡 Nâng cấp lên VIP để dùng 40 AI? Liên hệ Admin!")
    
    prints(125, 255, 168, f"⏰ Hạn dùng: {expire_time}")
    prints(255, 255, 255, f"🖥️ HWID: {key_data.get('hwid', 'N/A')}")
    time.sleep(3)
    
    # Kiểm tra xem có dữ liệu game đã lưu không
    saved_game = load_game_data()
    if saved_game:
        prints(0, 255, 243, '\nDùng tài khoản game cũ? (y/n): ', end='')
        x = input().lower().strip()
        if x == 'y':
            user_id = saved_game['user_id']
            user_secretkey = saved_game['user_secretkey']
        else:
            saved_game = None
    
    if not saved_game:
        clear_screen()
        banner()
        
        str_guide="""
    Hướng dẫn lấy link game:
        1. Truy cập website xworld.io
        2. Đăng nhập vào tài khoản
        3. Vào Vua thoát hiểm
        4. Copy link website và dán vào đây
    """
        prints(218, 255, 125, str_guide)
        prints(247, 255, 97, "═" * 47)
        prints(125, 255, 168, '📋 Nhập liên kết của bạn:', end=' ')
        link = input()
        try:
            user_id = link.split('userId=')[1].split('&')[0]
            user_secretkey = link.split('secretKey=')[1].split('&')[0]
        except Exception:
            prints(255, 0, 0, "❌ Cấu trúc Link sai!")
            sys.exit(1)
        
        # Lưu dữ liệu game
        save_game_data({
            'user_id': user_id,
            'user_secretkey': user_secretkey
        })
    
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, run with Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'user-id': user_id,
        'user-login': 'login_v2',
        'user-secret-key': user_secretkey,
        'xb-language': 'vi-VN',
    }
    
    clear_screen()
    banner()
    asset = user_asset(s, headers)
    
    prints(5, 255, 0, f'BALANCE: {asset["USDT"]:.2f}USDT - {asset["WORLD"]:.2f}WORLD - {asset["BUILD"]:.2f}BUILD')
    prints(5, 255, 0, """
        1. BUILD
        2. USDT
        3. WORLD
        """)
    prints(255, 255, 0, f'Chọn coin (1/2/3): ', end='')
    Coin_choice = input()
    if Coin_choice == '1':
        Coin = 'BUILD'
    elif Coin_choice == '2':
        Coin = 'USDT'
    elif Coin_choice == '3':
        Coin = 'WORLD'
    else:
        Coin = 'BUILD'
        
    prints(255, 255, 0, f'Số {Coin} mỗi ván (Gợi ý: {asset[Coin]/111:.2f}): ', end='')
    bet_amount0 = float(input())
    prints(255, 255, 0, 'Hệ số gấp thếp (vd: 10 = x10 khi thua): ')
    trap = float(input())
    delay1 = int(input('Số ván đặt trước khi nghỉ: '))
    delay2 = int(input(f'Số ván nghỉ: '))
    
    # Chọn AI dựa trên loại key
    if key_type == 'vip':
        show_all_ai("vip")
        max_ai = 40
    else:
        show_all_ai("free")
        max_ai = 10
    
    try:
        ai_choice = int(input(f'\n👉 Chọn số AI (1-{max_ai}, mặc định 7): ') or 7)
        if ai_choice < 1 or ai_choice > max_ai:
            ai_choice = 7
    except:
        ai_choice = 7
    
    if ai_choice > 10 and key_type != 'vip':
        prints(255, 165, 0, f'\n⚠️ AI {ai_choice} yêu cầu KEY VIP!')
        prints(255, 255, 255, 'Tự động chuyển sang AI 7 (Smart Safe)')
        time.sleep(2)
        ai_choice = 7
    
    algo_name = AI_LIST[ai_choice]["name"]
    prints(0, 255, 102, f'\n✅ AI: [{ai_choice}] {algo_name}')
    if key_type == 'vip':
        prints(255, 165, 0, f'👑 Chế độ VIP - Truy cập 40 AI')
    else:
        prints(255, 255, 255, f'🔓 Chế độ Free - 10 AI cơ bản')
    time.sleep(2)
    
    hisory = []
    stats = {
        'win': 0,
        'lose': 0,
        'asset0': asset[Coin],
        'streak': 0,
        'max_streak': 0,
    }
    tg = time.time() - 60
    tong = 0
    current_bet = bet_amount0
    
    last_killed_room = None
    clear_screen()
    
    while True:
        try:
            check_security_status()
            
            try:
                expire_dt = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S")
                if datetime.now() >= expire_dt:
                    clear_screen()
                    prints(255, 0, 0, "❌ Hết hạn Key! Vui lòng khởi động lại tool.")
                    time.sleep(5)
                    sys.exit(0)
            except:
                pass
                
            tong += 1
            data10 = top10_vth(s, headers, Coin)
            data100 = top100_vth(s, headers, Coin)
            
            bot_chon = chon_phong_ai(data10, data100, ai_choice, current_key)
            
            ki = data10[0][0] + 1
            
            cached_balance = asset[Coin]
            cycle = delay1 + delay2 if delay1 > 0 else 1
            pos = (tong - 1) % cycle
            
            is_bet_placed = False
            bet_message = ""
            
            if pos < delay1 or delay1 == 0:
                stop = False
                target_amount = float(bet_amount0) if not hisory or hisory[0].get('kq', True) else float(hisory[0]['bet_amount']) * trap
                success, result_msg = bet_vth(s, user_id, user_secretkey, bot_chon, Coin, target_amount)
                if success:
                    is_bet_placed = True
                    current_bet = target_amount
                else:
                    bet_message = f"Lỗi: {result_msg}"
            else:
                stop = True
                bet_message = "Nghỉ cược"

            countdown = 45.0
            last_api_fetch = time.time()
            tick_rate = 0.1
            
            while countdown > 0:
                now = time.time()
                if now - last_api_fetch >= 3.0:
                    try:
                        cached_balance = user_asset(s, headers).get(Coin, cached_balance)
                    except Exception:
                        pass
                    last_api_fetch = now
                
                draw_dashboard(s, headers, stats, Coin, countdown, bot_chon, ki, cached_balance, is_bet_placed, last_killed_room, expire_time, algo_name, current_bet, key_type)
                time.sleep(tick_rate)
                countdown -= tick_rate
                
            print("\n" * 2)
            
            if not is_bet_placed and bet_message:
                prints(255, 0, 0, f"⚠️ {bet_message}")
            elif is_bet_placed:
                prints(0, 255, 102, f"✅ Đã cược {current_bet} {Coin} -> Phòng {bot_chon} {room_info[bot_chon]['icon']} {room_info[bot_chon]['name']}")
                
            result, tg, killed_room = kiem_tra_kq_vth(s, headers, ki, bot_chon, Coin, tg)
            last_killed_room = killed_room
            
            if result == True:
                stats['win'] += 1
                stats['streak'] += 1
                stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                current_bet = bet_amount0
                if is_bet_placed:
                    bet_history.appendleft({
                        'issue': ki, 'room': bot_chon,
                        'room_name': room_info[bot_chon]['name'],
                        'room_icon': room_info[bot_chon]['icon'],
                        'amount': current_bet, 'result': 'win', 'algo': algo_name
                    })
            elif result == False:
                stats['lose'] += 1
                stats['streak'] = 0
                if is_bet_placed:
                    bet_history.appendleft({
                        'issue': ki, 'room': bot_chon,
                        'room_name': room_info[bot_chon]['name'],
                        'room_icon': room_info[bot_chon]['icon'],
                        'amount': current_bet, 'result': 'lose', 'algo': algo_name
                    })
                current_bet *= trap
            
            save_history(bet_history)
            
            if stop == False:
                hisory.insert(0, {'bot_chon': bot_chon, 'kq': result, 'bet_amount': current_bet})
                
            clear_screen()
            
        except KeyboardInterrupt:
            prints(5, 255, 0, f'\n👋 Đã dừng!')
            save_history(bet_history)
            sys.exit(0)

def main():
    # Khởi tạo
    init_local_db()
    
    # Lấy thông tin thiết bị
    hwid = get_device_hwid()
    ip = get_public_ip()
    save_device_info(hwid, ip)
    
    # Kiểm tra bảo mật
    check_security_status()
    
    # Đồng bộ keys từ JSONbin
    prints(0, 255, 243, "🔄 Đang đồng bộ dữ liệu từ máy chủ...")
    sync_keys_from_jsonbin()
    prints(0, 255, 102, "✅ Đồng bộ thành công!")
    time.sleep(1)
    
    # Tự động kiểm tra key
    key_data = check_key_status(hwid)
    
    # Chạy game
    run_game(key_data)

if __name__ == "__main__":
    main()
