import os
import sys
import time

# Khóa hỗ trợ mã màu ANSI trên Windows (nếu cần)
if os.name == 'nt':
    os.system('')

# Bảng mã màu ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
BLINK = "\033[5m"
COLORS = [
    "\033[91m",  # Đỏ
    "\033[93m",  # Vàng
    "\033[92m",  # Xanh lá
    "\033[96m",  # Xanh cyan
    "\033[95m",  # Tím
    "\033[94m",  # Xanh dương
]

def type_writer(text, delay=0.03, color="\033[96m"):
    """Hiệu ứng gõ máy đánh chữ"""
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def rainbow_banner(text):
    """Hiệu ứng đổi màu cầu vồng cho tiêu đề"""
    for color in COLORS:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(color + BOLD + f"\n{'='*60}\n{text.center(60)}\n{'='*60}" + RESET)
        time.sleep(0.2)

# --- CHẠY HIỆU ỨNG THÔNG BÁO ---

# 1. Hiệu ứng tiêu đề cầu vồng nhấp nháy
rainbow_banner(" 🔥 THÔNG BÁO KHẨN CẤP 🔥 ")

print("\n")

# 2. Hiệu ứng gõ chữ cho nội dung chính
type_writer("📢 Xin chào mọi người! Một không gian tuyệt vời đang chờ đón bạn...", 0.04, "\033[93m")
time.sleep(0.5)

type_writer("🚀 Hãy nhanh tay tham gia ngay nhóm mới cực kỳ chất lượng tại đây:", 0.04, "\033[92m")
time.sleep(0.3)

# 3. Hiệu ứng làm nổi bật Link Zalo với màu sắc rực rỡ và hiệu ứng chớp nháy
link_text = " 👉 LINK THAM GIA: https://zalo.me/g/e6bb2ppq4nofewqbfhrk 👈"
for _ in range(3):
    sys.stdout.write(f"\r{COLORS[0]}{BOLD}{BLINK}{link_text}{RESET}")
    sys.stdout.flush()
    time.sleep(0.3)
    sys.stdout.write(f"\r{COLORS[2]}{BOLD}{BLINK}{link_text}{RESET}")
    sys.stdout.flush()
    time.sleep(0.3)
print("\n")

time.sleep(0.5)

# 4. Câu thông báo sáng tạo ở cuối
type_writer("💡 Gợi ý thêm: Cơ hội không đợi ai, số lượng chỗ ngồi có hạn, hãy kết nối ngay để không bỏ lỡ những thông tin độc quyền và các phần quà hấp dẫn nhé! 🎉", 0.03, "\033[95m")

print("\n" + "="*60 + "\n")
