import time
import threading
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Trạng thái toàn cục để theo dõi tiến trình update
update_state = {
    "status": "Sẵn sàng kiểm tra bản cập nhật...",
    "progress": 0,
    "percent": "0%",
    "state": "idle", # idle, running, success, error
    "error_msg": ""
}

# Giao diện HTML/CSS siêu đẹp tích hợp ngay trong file Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Updater Pro</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background-color: #1e293b; padding: 30px; border-radius: 16px; width: 100%; max-width: 420px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; }
        h1 { font-size: 22px; margin-bottom: 8px; color: #ffffff; }
        .subtitle { font-size: 13px; color: #94a3b8; margin-bottom: 25px; }
        .status-box { background: #0f172a; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155; }
        #status-text { font-size: 14px; font-weight: 600; margin-bottom: 15px; color: #e2e8f0; }
        .progress-container { width: 100%; background-color: #334155; border-radius: 8px; height: 12px; overflow: hidden; margin-bottom: 8px; }
        #progress-bar { width: 0%; height: 100%; background-color: #3b82f6; transition: width 0.4s ease, background-color 0.4s ease; }
        #percent-text { font-size: 12px; color: #94a3b8; text-align: right; }
        .btn-group { display: flex; gap: 10px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 14px; font-weight: bold; cursor: pointer; transition: opacity 0.2s; }
        button:active { transform: scale(0.98); }
        #update-btn { background-color: #3b82f6; color: white; }
        #error-btn { background-color: #ef4444; color: white; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); justify-content: center; align-items: center; }
        .modal-content { background: #1e293b; padding: 25px; border-radius: 12px; width: 85%; max-width: 350px; border: 1px solid #475569; text-align: center; }
        .modal-content h3 { color: #ef4444; margin-bottom: 10px; }
        .modal-content p { font-size: 13px; color: #cbd5e1; margin-bottom: 20px; line-height: 1.5; }
        .modal-content button { background: #3b82f6; width: 100%; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Cập Nhật Công Cụ</h1>
        <p class="subtitle">v1.0.2 &rarr; v2.0.0 (Termux Edition)</p>
        
        <div class="status-box">
            <div id="status-text">Sẵn sàng kiểm tra bản cập nhật...</div>
            <div class="progress-container">
                <div id="progress-bar"></div>
            </div>
            <div id="percent-text">0%</div>
        </div>

        <div class="btn-group">
            <button id="update-btn" onclick="startUpdate(false)">Bắt Đầu Cập Nhật</button>
            <button id="error-btn" onclick="startUpdate(true)">Test Lỗi</button>
        </div>
    </div>

    <!-- Modal thông báo lỗi/thành công -->
    <div id="modal" class="modal">
        <div class="modal-content">
            <h3 id="modal-title">Thông Báo</h3>
            <p id="modal-desc">Nội dung thông báo...</p>
            <button onclick="closeModal()">Đóng</button>
        </div>
    </div>

    <script>
        function updateUI() {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status-text').innerText = data.status;
                    document.getElementById('progress-bar').style.width = data.progress + '%';
                    document.getElementById('percent-text').innerText = data.percent;
                    
                    if (data.state === 'running') {
                        document.getElementById('update-btn').disabled = true;
                        document.getElementById('error-btn').disabled = true;
                        document.getElementById('progress-bar').style.backgroundColor = '#3b82f6';
                    } else if (data.state === 'success' || data.state === 'error') {
                        document.getElementById('update-btn').disabled = false;
                        document.getElementById('error-btn').disabled = false;
                        if (data.state === 'error') {
                            document.getElementById('progress-bar').style.backgroundColor = '#ef4444';
                        }
                    }
                });
        }

        function startUpdate(isError) {
            fetch('/run?error=' + isError)
                .then(() => {
                    let interval = setInterval(() => {
                        updateUI();
                        fetch('/status').then(r => r.json()).then(d => {
                            if (d.state === 'success' || d.state === 'error') {
                                clearInterval(interval);
                                showModal(d.state, d.error_msg);
                            }
                        });
                    }, 500);
                });
        }

        function showModal(state, msg) {
            const modal = document.getElementById('modal');
            const title = document.getElementById('modal-title');
            const desc = document.getElementById('modal-desc');
            
            if (state === 'success') {
                title.style.color = '#22c55e';
                title.innerText = 'Thành Công!';
                desc.innerText = 'Tool của bạn đã được cập nhật lên phiên bản mới nhất v2.0.0!';
            } else {
                title.style.color = '#ef4444';
                title.innerText = 'Lỗi Cập Nhật (0x80070002)';
                desc.innerText = msg;
            }
            modal.style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

def process_update(is_error):
    global update_state
    update_state["state"] = "running"
    
    steps = [
        ("Đang kết nối đến máy chủ...", 10, "10%"),
        ("Đang tải xuống tệp tin mới (1/3)...", 30, "30%"),
        ("Đang tải xuống tệp tin mới (3/3)...", 60, "60%"),
        ("Đang giải nén và cấu hình...", 85, "85%"),
        ("Đang hoàn tất cài đặt...", 100, "100%")
    ]

    for text, prog, perc in steps:
        if is_error and prog >= 30:
            update_state["status"] = "❌ Lỗi: Mất kết nối internet đột ngột!"
            update_state["progress"] = 20
            update_state["percent"] = "20%"
            update_state["state"] = "error"
            update_state["error_msg"] = "Không thể tải xuống gói cập nhật.\nVui lòng kiểm tra lại đường truyền mạng và thử lại sau."
            return
        
        update_state["status"] = text
        update_state["progress"] = prog
        update_state["percent"] = perc
        time.sleep(0.8)

    update_state["status"] = "Cập nhật thành công! Vui lòng khởi động lại."
    update_state["state"] = "success"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    return jsonify(update_state)

@app.route('/run')
def run():
    is_error = reader_bool = request_arg = True if __import__('flask').request.args.get('error') == 'true' else False
    threading.Thread(target=process_update, args=(is_error,), daemon=True).start()
    return jsonify({"status": "started"})

if __name__ == '__main__':
    print("\n[+] Đang khởi động Web UI cho Termux...")
    print("[+] Hãy mở trình duyệt trên điện thoại và truy cập: http://127.0.0.1:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
