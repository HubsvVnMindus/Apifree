from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Cấu hình từ environment variables
DB_HOST = os.environ.get('DB_HOST', 'sql303.ezyro.com')
DB_USER = os.environ.get('DB_USER', 'ezyro_42627914')
DB_PASS = os.environ.get('DB_PASS', 'Hunghai443@#')
DB_NAME = os.environ.get('DB_NAME', 'ezyro_42627914_htool_keys')

@app.route('/verify')
def verify():
    key = request.args.get('key')
    
    if not key:
        return jsonify({"valid": False, "error": "Key không được để trống"})
    
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `keys` WHERE key_code = %s", (key,))
        keyData = cursor.fetchone()
        conn.close()
        
        if not keyData:
            return jsonify({"valid": False, "error": "Key không tồn tại"})
        
        return jsonify({
            "valid": True,
            "data": {
                "key": key,
                "key_type": keyData[2] if len(keyData) > 2 else 'free',
                "max_ai": keyData[4] if len(keyData) > 4 else 10,
                "expires_at": keyData[5] if len(keyData) > 5 else 'forever',
                "note": keyData[6] if len(keyData) > 6 else '',
                "used_count": (keyData[10] if len(keyData) > 10 else 0) + 1,
                "max_uses": keyData[9] if len(keyData) > 9 else None
            }
        })
        
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})

@app.route('/')
def home():
    return "HTOOL API is running 24/7!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
