# ==================== HTOOL LOADER - TẢI & CHẠY TOOL TỪ GITHUB ====================
import sys
import subprocess
import os
import hashlib
import json
import time

# --- CÀI ĐẶT THƯ VIỆN CẦN THIẾT ---
REQUIRED_LIBS = {
    "requests": "requests",
    "colorama": "colorama"
}

for lib_name, pip_name in REQUIRED_LIBS.items():
    try:
        __import__(lib_name)
    except ImportError:
        print(f"🔄 Đang cài {lib_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

import requests
from colorama import init, Fore, Style
init(autoreset=True)

# ==================== CẤU HÌNH GITHUB ====================
# THAY ĐỔI LINK NÀY THÀNH LINK RAW CỦA BẠN
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/htool29/htool/main"

# Danh sách các file cần tải
FILES_TO_LOAD = {
    "main.py": f"{GITHUB_RAW_BASE}/main.py",
    "config.py": f"{GITHUB_RAW_BASE}/config.py",
    "license_system.py": f"{GITHUB_RAW_BASE}/license_system.py",
    "ai_engine.py": f"{GITHUB_RAW_BASE}/ai_engine.py",
    "game_cdtd.py": f"{GITHUB_RAW_BASE}/game_cdtd.py",
    "dashboard.py": f"{GITHUB_RAW_BASE}/dashboard.py",
    "utils.py": f"{GITHUB_RAW_BASE}/utils.py"
}

VERSION_URL = f"{GITHUB_RAW_BASE}/version.json"
LOCAL_VERSION_FILE = "htool_version.json"

# ==================== FUNCTIONS ====================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ██╗░░██╗████████╗░█████╗░░█████╗░██╗░░░░░               ║
    ║   ██║░░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░               ║
    ║   ███████║░░░██║░░░██║░░██║██║░░██║██║░░░░░               ║
    ║   ██╔══██║░░░██║░░░██║░░██║██║░░██║██║░░░░░               ║
    ║   ██║░░██║░░░██║░░░╚█████╔╝╚█████╔╝███████╗               ║
    ║   ╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝               ║
    ║                                                          ║
    ║              🚀 HTOOL LOADER - ONLINE TOOL               ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner)

def get_local_version():
    """Lấy phiên bản local"""
    if os.path.exists(LOCAL_VERSION_FILE):
        try:
            with open(LOCAL_VERSION_FILE, 'r') as f:
                data = json.load(f)
                return data.get('version', '0.0.0')
        except:
            pass
    return '0.0.0'

def get_remote_version():
    """Lấy phiên bản từ GitHub"""
    try:
        r = requests.get(VERSION_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get('version', '0.0.0'), data
    except:
        pass
    return '0.0.0', {}

def download_file(url, filename):
    """Tải file từ GitHub"""
    try:
        print(Fore.YELLOW + f"  📥 Đang tải {filename}...", end=' ')
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            # Tạo thư mục nếu cần
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print(Fore.GREEN + "✅ OK")
            return True
        else:
            print(Fore.RED + f"❌ Lỗi HTTP {r.status_code}")
            return False
    except Exception as e:
        print(Fore.RED + f"❌ {str(e)[:50]}")
        return False

def check_and_update():
    """Kiểm tra và cập nhật tool"""
    local_ver = get_local_version()
    remote_ver, version_data = get_remote_version()
    
    print(Fore.CYAN + f"\n📋 Phiên bản hiện tại: {local_ver}")
    print(Fore.CYAN + f"📋 Phiên bản mới nhất: {remote_ver}")
    
    if remote_ver == '0.0.0':
        print(Fore.RED + "❌ Không thể kết nối đến server GitHub!")
        print(Fore.YELLOW + "⚠️ Đang chạy phiên bản local...")
        return True  # Vẫn cho chạy nếu có file local
    
    # So sánh version
    if remote_ver > local_ver or not os.path.exists("main.py"):
        print(Fore.YELLOW + "\n🔄 Đang cập nhật tool từ GitHub...")
        print(Fore.CYAN + "─" * 50)
        
        success_count = 0
        for filename, url in FILES_TO_LOAD.items():
            if download_file(url, filename):
                success_count += 1
        
        print(Fore.CYAN + "─" * 50)
        
        if success_count > 0:
            # Lưu version mới
            with open(LOCAL_VERSION_FILE, 'w') as f:
                json.dump(version_data, f, indent=2)
            print(Fore.GREEN + f"\n✅ Đã cập nhật {success_count}/{len(FILES_TO_LOAD)} file!")
            
            # Hiển thị changelog
            if 'changelog' in version_data:
                print(Fore.YELLOW + "\n📝 Changelog:")
                for change in version_data['changelog']:
                    print(Fore.WHITE + f"  • {change}")
            
            return True
        else:
            print(Fore.RED + "\n❌ Cập nhật thất bại!")
            if os.path.exists("main.py"):
                print(Fore.YELLOW + "⚠️ Đang chạy phiên bản local...")
                return True
            return False
    else:
        print(Fore.GREEN + "✅ Tool đã là phiên bản mới nhất!")
        return True

def run_tool():
    """Chạy tool chính"""
    if not os.path.exists("main.py"):
        print(Fore.RED + "❌ Không tìm thấy file main.py!")
        print(Fore.YELLOW + "👉 Vui lòng kiểm tra kết nối mạng và thử lại!")
        return
    
    try:
        # Import và chạy main
        import main
        if hasattr(main, 'main'):
            main.main()
        else:
            # Nếu không có hàm main, chạy trực tiếp
            exec(open("main.py", encoding='utf-8').read())
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n👋 Đã dừng tool!")
    except Exception as e:
        print(Fore.RED + f"\n❌ Lỗi khi chạy tool: {e}")
        import traceback
        traceback.print_exc()

def show_menu():
    """Hiển thị menu chính"""
    while True:
        clear_screen()
        print_banner()
        
        local_ver = get_local_version()
        print(Fore.YELLOW + f"  📦 Version: {local_ver}")
        print(Fore.CYAN + "═" * 58)
        print(Fore.WHITE + "  [1] 🚀 CHẠY TOOL")
        print(Fore.WHITE + "  [2] 🔄 KIỂM TRA & CẬP NHẬT")
        print(Fore.WHITE + "  [3] 📋 THÔNG TIN PHIÊN BẢN")
        print(Fore.WHITE + "  [4] 🗑️  XÓA CACHE & TẢI LẠI")
        print(Fore.WHITE + "  [5] 🚪 THOÁT")
        print(Fore.CYAN + "═" * 58)
        print(Fore.YELLOW + "👉 Chọn (1/2/3/4/5): ", end='')
        
        choice = input().strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            if check_and_update():
                print(Fore.CYAN + "\n" + "═" * 50)
                print(Fore.GREEN + "🚀 Đang khởi động tool...")
                print(Fore.CYAN + "═" * 50)
                time.sleep(1)
                run_tool()
            else:
                print(Fore.RED + "\n❌ Không thể chạy tool!")
                input(Fore.YELLOW + "\n👉 Nhấn Enter để quay lại...")
        
        elif choice == '2':
            clear_screen()
            print_banner()
            print(Fore.CYAN + "\n🔄 ĐANG KIỂM TRA CẬP NHẬT...")
            print(Fore.CYAN + "═" * 50)
            check_and_update()
            input(Fore.YELLOW + "\n👉 Nhấn Enter để quay lại...")
        
        elif choice == '3':
            clear_screen()
            print_banner()
            local_ver = get_local_version()
            remote_ver, version_data = get_remote_version()
            
            print(Fore.CYAN + "\n📋 THÔNG TIN PHIÊN BẢN")
            print(Fore.CYAN + "═" * 50)
            print(Fore.WHITE + f"  Phiên bản local:  {local_ver}")
            print(Fore.WHITE + f"  Phiên bản GitHub: {remote_ver}")
            
            if version_data:
                print(Fore.WHITE + f"  Tác giả: {version_data.get('author', 'HTOOL')}")
                print(Fore.WHITE + f"  Ngày phát hành: {version_data.get('release_date', 'N/A')}")
                
                if 'features' in version_data:
                    print(Fore.CYAN + "\n  📋 Tính năng:")
                    for feat in version_data['features']:
                        print(Fore.WHITE + f"    • {feat}")
            
            input(Fore.YELLOW + "\n👉 Nhấn Enter để quay lại...")
        
        elif choice == '4':
            clear_screen()
            print_banner()
            print(Fore.YELLOW + "\n⚠️ Bạn có chắc muốn xóa cache và tải lại?")
            print(Fore.RED + "👉 Tất cả file sẽ bị xóa và tải mới từ GitHub!")
            confirm = input(Fore.YELLOW + "👉 Nhập 'YES' để xác nhận: ").strip()
            
            if confirm.upper() == 'YES':
                print(Fore.YELLOW + "\n🗑️ Đang xóa cache...")
                
                deleted = 0
                for filename in FILES_TO_LOAD.keys():
                    if os.path.exists(filename):
                        os.remove(filename)
                        print(Fore.RED + f"  ❌ Đã xóa: {filename}")
                        deleted += 1
                
                if os.path.exists(LOCAL_VERSION_FILE):
                    os.remove(LOCAL_VERSION_FILE)
                
                print(Fore.GREEN + f"\n✅ Đã xóa {deleted} file!")
                print(Fore.CYAN + "\n🔄 Đang tải lại từ GitHub...")
                time.sleep(1)
                check_and_update()
            
            input(Fore.YELLOW + "\n👉 Nhấn Enter để quay lại...")
        
        elif choice == '5':
            print(Fore.RED + "\n👋 Thoát tool!")
            sys.exit(0)

# ==================== MAIN ====================
def main():
    """Hàm chính của Loader"""
    try:
        show_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n👋 Thoát tool!")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Lỗi: {e}")
        input(Fore.YELLOW + "👉 Nhấn Enter để thoát...")
        sys.exit(1)

if __name__ == "__main__":
    main()
