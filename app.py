from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'HTOOL API Proxy is running 24/7!'

@app.route('/verify')
def verify():
    key = request.args.get('key')
    
    if not key:
        return jsonify({'valid': False, 'error': 'Key không được để trống'})
    
    # Gọi file getkey.php trên hosting của bạn
    try:
        url = f"https://htoool.unaux.com/getkey.php?key={key}"
        response = requests.get(url, timeout=10)
        
        # Kiểm tra nếu bị chặn (trả về HTML)
        if response.text.strip().startswith('<'):
            return jsonify({
                'valid': False, 
                'error': 'Hosting đang chặn request. Vui lòng kiểm tra lại.'
            })
        
        return jsonify(response.json())
        
    except requests.exceptions.Timeout:
        return jsonify({'valid': False, 'error': 'Timeout - Server quá chậm'})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
