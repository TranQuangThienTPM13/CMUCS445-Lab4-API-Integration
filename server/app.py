from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# File lưu dữ liệu (trong container)
DATA_DIR = "/app/data"
DATA_FILE = os.path.join(DATA_DIR, "orders.json")

# In-memory list (sẽ được nạp từ file khi khởi động)
orders = []

def load_orders():
    """Đọc dữ liệu từ orders.json nếu có."""
    global orders
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)
            # Nếu file rỗng/không đúng format
            if not isinstance(orders, list):
                orders = []
        except Exception:
            orders = []
    else:
        orders = []

def save_orders():
    """Ghi dữ liệu orders ra orders.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# Nạp dữ liệu ngay khi server start
load_orders()

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    if not data or 'product' not in data or 'amount' not in data:
        return jsonify({"error": "Invalid Data"}), 400

    new_order = {
        "id": (orders[-1]["id"] + 1) if orders else 1,
        "product": data['product'],
        "amount": data['amount'],
        "status": "CONFIRMED"
    }

    orders.append(new_order)
    save_orders()

    print(f"Received Order: {new_order}")
    return jsonify(new_order), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({"total": len(orders), "data": orders})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)