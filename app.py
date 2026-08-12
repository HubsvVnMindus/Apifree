from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Cấu hình database - LẤY TỪ HOSTING CỦA BẠN
DB_HOST = "sql303.ezyro.com"
DB_NAME = "ezyro_42627914_htool_keys"
DB_USER = "ezyro_42627914"
DB_PASS = "Hunghai443@#"  # ← SỬA MẬT KHẨU THẬT

@app.route('/')
def home():
    return 'HTOOL API is running 24/7!'

@app.route('/verify')
def verify():
    key = request.args.get('key')
    
    if not key:
        return jsonify({'valid': False, 'error': 'Key không được để trống'})
    
    try:
        # Kết nối trực tiếp database
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            connect_timeout=10
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `keys` WHERE key_code = %s", (key,))
        keyData = cursor.fetchone()
        conn.close()
        
        if not keyData:
            return jsonify({'valid': False, 'error': 'Key không tồn tại'})
        
        # keyData = (id, key_code, key_type, status, max_ai, expires_at, note, ...)
        return jsonify({
            'valid': True,
            'data': {
                'key': key,
                'key_type': keyData[2] if len(keyData) > 2 else 'free',
                'max_ai': keyData[4] if len(keyData) > 4 else 10,
                'expires_at': keyData[5] if len(keyData) > 5 else 'forever',
                'note': keyData[6] if len(keyData) > 6 else '',
                'used_count': (keyData[10] if len(keyData) > 10 else 0) + 1,
                'max_uses': keyData[9] if len(keyData) > 9 else None
            }
        })
        
    except pymysql.err.OperationalError as e:
        return jsonify({'valid': False, 'error': f'Lỗi kết nối database: {str(e)}'})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
