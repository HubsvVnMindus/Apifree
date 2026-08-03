import tkinter as tk
import webbrowser
import threading
import time

class ZaloInviteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Thông Báo Đặc Biệt 🔥")
        self.root.geometry("600x450")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # Căn giữa cửa sổ trên màn hình
        self.center_window()

        # Khởi tạo các thành phần giao diện
        self.create_widgets()

        # Chạy hiệu ứng màu sắc và chữ tự động khi khởi động
        threading.Thread(target=self.run_animations, daemon=True).start()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Tiêu đề chính
        self.title_label = tk.Label(
            self.root, 
            text="🌟 THÔNG BÁO KHẨN CẤP 🌟", 
            font=("Arial", 22, "bold"), 
            bg="#1e1e2f", 
            fg="#00ffff"
        )
        self.title_label.pack(pady=25)

        # Khung chứa nội dung thông báo
        self.frame_content = tk.Frame(self.root, bg="#2d2d44", bd=0, relief="flat")
        self.frame_content.pack(pady=10, padx=30, fill="both", expand=True)

        # Nội dung chữ (Dùng Label hiển thị hiệu ứng gõ)
        self.msg_label1 = tk.Label(
            self.frame_content, 
            text="", 
            font=("Arial", 12), 
            bg="#2d2d44", 
            fg="#ffcc00", 
            justify="center",
            wraplength=500
        )
        self.msg_label1.pack(pady=10)

        self.msg_label2 = tk.Label(
            self.frame_content, 
            text="", 
            font=("Arial", 12, "bold"), 
            bg="#2d2d44", 
            fg="#00ffcc", 
            justify="center",
            wraplength=500
        )
        self.msg_label2.pack(pady=5)

        # Nút bấm tham gia nhóm (Modern Button)
        self.btn_join = tk.Button(
            self.root,
            text="🚀 THAM GIA NHÓM ZALO NGAY 🚀",
            font=("Arial", 13, "bold"),
            bg="#00b894",
            fg="#ffffff",
            activebackground="#55efc4",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self.open_zalo_link
        )
        self.btn_join.pack(pady=20)
        
        # Hiệu ứng hover cho nút
        self.btn_join.bind("<Enter>", lambda e: self.btn_join.config(bg="#00cec9"))
        self.btn_join.bind("<Leave>", lambda e: self.btn_join.config(bg="#00b894"))

        # Câu thông báo sáng tạo ở cuối
        self.footer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10, "italic"),
            bg="#1e1e2f",
            fg="#dfe6e9"
        )
        self.footer_label.pack(pady=5)

    def open_zalo_link(self):
        url = "https://zalo.me/g/e6bb2ppq4nofewqbfhrk"
        webbrowser.open(url)

    def run_animations(self):
        # 1. Hiệu ứng đổi màu tiêu đề liên tục (RGB Effect)
        colors = ["#00ffff", "#ff7675", "#55efc4", "#ffeaa7", "#a29bfe", "#fd79a8"]
        
        # 2. Hiệu ứng gõ chữ nội dung 1
        text1 = "📢 Xin chào các bạn! Một không gian giao lưu tuyệt vời và cực kỳ chất lượng đang chờ đón bạn."
        for i in range(len(text1) + 1):
            self.msg_label1.config(text=text1[:i])
            time.sleep(0.02)

        time.sleep(0.3)

        # 3. Hiệu ứng gõ chữ nội dung 2
        text2 = "👉 Click nút bên dưới để vào nhóm Zalo ngay lập tức!"
        for i in range(len(text2) + 1):
            self.msg_label2.config(text=text2[:i])
            time.sleep(0.02)

        time.sleep(0.3)

        # 4. Hiệu ứng gõ chữ câu cuối sáng tạo
        footer_text = "💡 Gợi ý: Cơ hội không đợi ai, số lượng thành viên có hạn, tham gia ngay để nhận tài liệu và quà tặng độc quyền! 🎉"
        for i in range(len(footer_text) + 1):
            self.footer_label.config(text=footer_text[:i])
            time.sleep(0.015)

        # Vòng lặp đổi màu tiêu đề mượt mà sau khi gõ xong chữ
        idx = 0
        while True:
            try:
                self.title_label.config(fg=colors[idx])
                idx = (idx + 1) % len(colors)
                time.sleep(0.5)
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ZaloInviteApp(root)
    root.mainloop()
