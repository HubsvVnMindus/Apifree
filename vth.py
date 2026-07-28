import time
import threading
import customtkinter as ctk
from tkinter import messagebox

# Cấu hình giao diện tổng thể
ctk.set_appearance_mode("System")  # Chế độ sáng/tối theo hệ thống (Dark/Light)
ctk.set_default_color_theme("blue")  # Màu chủ đạo: blue, green, dark-blue

class UpdateToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ chính
        self.title("System Updater Pro")
        self.geometry("500x420")
        self.resizable(False, False)
        
        # Tiêu đề ứng dụng
        self.title_label = ctk.CTkLabel(
            self, 
            text="Cập Nhật Công Cụ Hệ Thống", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold")
        )
        self.title_label.pack(pady=(30, 10))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Phiên bản hiện tại: v1.0.2  |  Phiên bản mới: v2.0.0", 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Khung chứa trạng thái và thanh tiến trình
        self.card_frame = ctk.CTkFrame(self, corner_radius=15)
        self.card_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Trạng thái hiện tại
        self.status_label = ctk.CTkLabel(
            self.card_frame, 
            text="Sẵn sàng kiểm tra bản cập nhật...", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=(25, 10))

        # Thanh tiến trình (Progress Bar)
        self.progress_bar = ctk.CTkProgressBar(self.card_frame, width=380, height=14, corner_radius=7)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Phần trăm tiến trình
        self.percent_label = ctk.CTkLabel(
            self.card_frame, 
            text="0%", 
            font=ctk.CTkFont(size=12), 
            text_color="gray"
        )
        self.percent_label.pack(pady=(0, 20))

        # Khung chứa nút bấm
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=(10, 30))

        # Nút Bắt đầu Update
        self.update_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Bắt Đầu Cập Nhật", 
            command=self.start_update_thread,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            height=40,
            corner_radius=8
        )
        self.update_btn.pack(side="left", padx=10)

        # Nút Giả lập Lỗi (đáp ứng yêu cầu hiện báo lỗi)
        self.error_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Test Lỗi", 
            command=self.trigger_error_simulation,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#D32F2F", 
            hover_color="#B71C1C",
            width=120,
            height=40,
            corner_radius=8
        )
        self.error_btn.pack(side="left", padx=10)

    def start_update_thread(self):
        """Chạy tiến trình update bằng luồng riêng (Thread) để không bị đơ giao diện"""
        self.update_btn.configure(state="disabled")
        self.error_btn.configure(state="disabled")
        # Chạy hàm chạy ngầm
        threading.Thread(target=self.run_update_process, daemon=True).start()

    def run_update_process(self):
        """Mô phỏng quá trình tải xuống và cập nhật"""
        steps = [
            ("Đang kết nối đến máy chủ...", 0.1),
            ("Đang tải xuống tệp tin mới (0/3)...", 0.3),
            ("Đang tải xuống tệp tin mới (2/3)...", 0.6),
            ("Đang giải nén và cấu hình...", 0.85),
            ("Đang hoàn tất cài đặt...", 1.0)
        ]

        for text, progress in steps:
            self.status_label.configure(text=text)
            self.progress_bar.set(progress)
            self.percent_label.configure(text=f"{int(progress * 100)}%")
            time.sleep(0.8) # Giả lập thời gian chờ

        # Hoàn thành
        self.status_label.configure(text="Cập nhật thành công! Vui lòng khởi động lại.")
        messagebox.showinfo("Thành công", "Tool của bạn đã được cập nhật lên phiên bản mới nhất v2.0.0!")
        
        self.update_btn.configure(state="normal", text="Hoàn tất")
        self.error_btn.configure(state="normal")

    def trigger_error_simulation(self):
        """Hàm giả lập thông báo lỗi hiện đại khi update thất bại"""
        self.update_btn.configure(state="disabled")
        self.error_btn.configure(state="disabled")
        
        # Hiệu ứng đổi màu thanh tiến trình sang màu đỏ khi lỗi
        self.status_label.configure(text="Đang kết nối máy chủ...", text_color="gray")
        self.progress_bar.set(0.2)
        self.percent_label.configure(text="20%")
        time.sleep(0.5)

        self.status_label.configure(text="❌ Lỗi: Mất kết nối internet đột ngột!", text_color="#EF5350")
        
        # Hộp thoại báo lỗi tiêu chuẩn nhưng bắt mắt
        messagebox.showerror(
            "Lỗi Cập Nhật (Error Code: 0x80070002)", 
            "Không thể tải xuống gói cập nhật.\n\nVui lòng kiểm tra lại đường truyền mạng hoặc quyền quản trị (Run as Administrator) và thử lại sau."
        )
        
        # Khôi phục trạng thái nút bấm
        self.status_label.configure(text="Cập nhật thất bại. Vui lòng thử lại.", text_color=("black", "white"))
        self.update_btn.configure(state="normal")
        self.error_btn.configure(state="normal")

if __name__ == "__main__":
    app = UpdateToolApp()
    app.mainloop()
