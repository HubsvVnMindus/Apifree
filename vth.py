import os
import sys
import time
import random

# Khóa hỗ trợ mã màu ANSI trên Windows
if os.name == 'nt':
    os.system('')

# Bảng mã màu ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLINK = "\033[5m"
COLORS = {
    'red': "\033[91m",
    'green': "\033[92m",
    'yellow': "\033[93m",
    'blue': "\033[94m",
    'magenta': "\033[95m",
    'cyan': "\033[96m",
    'white': "\033[97m",
    'bright_red': "\033[1;91m",
    'bright_green': "\033[1;92m",
    'bright_yellow': "\033[1;93m",
    'bright_cyan': "\033[1;96m",
}

def clear_screen():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def type_writer(text, delay=0.03, color=COLORS['cyan']):
    """Hiệu ứng gõ máy đánh chữ sinh động"""
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(message, duration=2):
    """Hiệu ứng loading với dấu chấm"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f"\r{COLORS['cyan']}{char} {message}{RESET}")
            sys.stdout.flush()
            time.sleep(0.05)

def print_border(char="═", width=65, color=COLORS['cyan']):
    """In đường viền"""
    print(f"{color}{BOLD}{char * width}{RESET}")

def print_centered(text, width=65, color=COLORS['white']):
    """In text căn giữa"""
    print(f"{color}{BOLD}{text.center(width)}{RESET}")

def rainbow_text(text, delay=0.1):
    """Hiệu ứng text đổi màu cầu vồng"""
    colors_list = [COLORS['bright_red'], COLORS['bright_yellow'], COLORS['bright_green'], 
                   COLORS['bright_cyan'], COLORS['magenta'], COLORS['blue']]
    
    for _ in range(3):
        for color in colors_list:
            sys.stdout.write(f"\r{color}{BOLD}{text}{RESET}")
            sys.stdout.flush()
            time.sleep(delay)

def sparkle_effect(text, duration=3):
    """Hiệu ứng lấp lánh cho text quan trọng"""
    sparkles = ["✨", "⭐", "💫", "🌟", "⚡", "🔥", "💎", "🎯"]
    end_time = time.time() + duration
    while time.time() < end_time:
        sparkle = random.choice(sparkles)
        sys.stdout.write(f"\r{COLORS['bright_yellow']}{BOLD}{sparkle} {text} {sparkle}{RESET}")
        sys.stdout.flush()
        time.sleep(0.2)

def draw_box(title, content_lines, box_color=COLORS['cyan']):
    """Vẽ hộp thông báo đẹp"""
    max_width = max(len(line) for line in content_lines) + 4
    max_width = max(max_width, len(title) + 4)
    
    # Top border
    print(f"{box_color}╔{'═' * (max_width - 2)}╗{RESET}")
    
    # Title
    padding = (max_width - len(title) - 2) // 2
    extra = (max_width - len(title) - 2) % 2
    print(f"{box_color}║{' ' * padding}{COLORS['bright_yellow']}{BOLD}{title}{RESET}{box_color}{' ' * (padding + extra)}║{RESET}")
    
    # Separator
    print(f"{box_color}╠{'═' * (max_width - 2)}╣{RESET}")
    
    # Content
    for line in content_lines:
        padding = max_width - len(line) - 2
        print(f"{box_color}║{RESET} {line}{' ' * (padding - 1)}{box_color}║{RESET}")
    
    # Bottom border
    print(f"{box_color}╚{'═' * (max_width - 2)}╝{RESET}")

def animated_link(link_text, duration=5):
    """Hiệu ứng link nhấp nháy nhiều kiểu"""
    styles = [
        f"{COLORS['bright_red']}{BOLD}{BLINK}",
        f"{COLORS['bright_yellow']}{BOLD}{BLINK}",
        f"{COLORS['bright_green']}{BOLD}{BLINK}",
        f"{COLORS['bright_cyan']}{BOLD}{BLINK}",
        f"{COLORS['magenta']}{BOLD}{BLINK}",
        f"{COLORS['blue']}{BOLD}{BLINK}",
    ]
    
    end_time = time.time() + duration
    style_index = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{styles[style_index % len(styles)]}  {link_text}  {RESET}")
        sys.stdout.flush()
        style_index += 1
        time.sleep(0.3)
    print("\n")

def main():
    clear_screen()
    
    # Loading effect
    loading_animation("Đang kết nối đến cộng đồng...", 2)
    clear_screen()
    
    # Header hoành tráng
    print(f"\n{COLORS['cyan']}{BOLD}╔{'═'*63}╗{RESET}")
    rainbow_text("🔥 THÔNG BÁO KHẨN CẤP & KẾT NỐI CỘNG ĐỒNG 🔥", 0.1)
    print(f"{COLORS['cyan']}{BOLD}╚{'═'*63}╝{RESET}\n")
    
    time.sleep(0.5)
    
    # Box thông báo chính
    draw_box("📢 THÔNG BÁO QUAN TRỌNG", [
        "Chào mừng bạn đến với cộng đồng mới!",
        "Nơi giao lưu, học hỏi và phát triển cùng nhau.",
        "Cơ hội kết nối với những người cùng đam mê.",
    ], COLORS['cyan'])
    
    print()
    time.sleep(0.5)
    
    # Message with type writer effect
    type_writer("🚀 Đừng bỏ lỡ cơ hội tham gia nhóm mới của chúng tôi:", 0.03, COLORS['bright_yellow'])
    print()
    time.sleep(0.3)
    
    # Featured link box
    draw_box("🔗 LINK THAM GIA CHÍNH THỨC", [
        "https://zalo.me/g/e6bb2ppq4nofewqbfhrk",
    ], COLORS['bright_green'])
    
    print()
    time.sleep(0.3)
    
    # Animated link
    sparkle_effect("👆 NHẤP VÀO LINK TRÊN ĐỂ THAM GIA NGAY 👆", 3)
    print("\n")
    
    time.sleep(0.5)
    
    # Feature highlights
    features = [
        "🎯 Kiến thức chuyên sâu được chia sẻ mỗi ngày",
        "🤝 Kết nối với cộng đồng năng động",
        "🎁 Cơ hội nhận quà tặng hấp dẫn",
        "💡 Thảo luận và giải đáp thắc mắc 24/7",
        "📈 Cập nhật xu hướng mới nhất",
    ]
    
    draw_box("✨ LỢI ÍCH KHI THAM GIA", features, COLORS['magenta'])
    
    print()
    
    # Final call to action
    print_centered("Số lượng có hạn - Đừng chần chừ!", 65, COLORS['bright_red'])
    print_centered("Tham gia ngay hôm nay để không bỏ lỡ! 🎉", 65, COLORS['bright_yellow'])
    
    print(f"\n{COLORS['cyan']}{'='*65}{RESET}")
    
    # Footer
    print(f"\n{COLORS['dim']}💬 Mọi thắc mắc vui lòng liên hệ qua nhóm Zalo{ RESET}")
    print(f"{COLORS['dim']}© 2024 Cộng đồng kết nối - All rights reserved{ RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['bright_yellow']}👋 Tạm biệt! Hy vọng sẽ gặp bạn trong nhóm Zalo!{RESET}\n")
        sys.exit(0)
