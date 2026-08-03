import os
import sys
import time

# Khóa hỗ trợ mã màu ANSI trên Windows
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

def main():
    # Xóa màn hình cho sạch sẽ
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"\n{COLORS[3]}{BOLD}{'='*65}{RESET}")
    print(f"{COLORS[1]}{BOLD}          🔥 THÔNG BÁO KHẨN CẤP & KẾT NỐI CỘNG ĐỒNG 🔥          {RESET}")
    print(f"{COLORS[3]}{BOLD}{'='*65}{RESET}\n")

    time.sleep(0.5)
    type_writer("📢 Xin chào các bạn! Một không gian giao lưu tuyệt vời đang chờ đón bạn...", 0.03, "\033[93m")
    time.sleep(0.3)
    type_writer("🚀 Hãy nhanh tay tham gia ngay nhóm mới cực kỳ chất lượng tại đây:", 0.03, "\033[92m")
    time.sleep(0.3)

    # Hiệu ứng làm nổi bật Link Zalo chớp nháy
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
    type_writer("💡 Gợi ý thêm: Cơ hội không đợi ai, số lượng thành viên có hạn, hãy kết nối ngay để không bỏ lỡ những thông tin độc quyền và quà tặng hấp dẫn nhé! 🎉", 0.03, "\033[95m")

    print(f"\n{COLORS[3]}{'='*65}{RESET}\n")

if __name__ == "__main__":
    main()
