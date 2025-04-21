import requests
import hashlib
import hmac
import json
import time

class ZaloPayAPI:

    def __init__(self, app_id, key1, key2, endpoint):
        self.app_id = app_id
        self.key1 = key1
        self.key2 = key2
        self.endpoint = endpoint

    def create_order(self, amount, app_trans_id, app_user, embed_data={}, items=[]):
        order_data = {
            "app_id": self.app_id,
            "app_trans_id": app_trans_id,
            "app_user": app_user,
            "amount": amount,
            "embed_data": json.dumps(embed_data),
            "item": json.dumps(items),
            "description": f"Payment for transaction {app_trans_id}",
            "timestamp": int(time.time() * 1000),
        }

        data = f"{order_data['app_id']}|{order_data['app_trans_id']}|{order_data['app_user']}|{order_data['amount']}|{order_data['timestamp']}|{order_data['embed_data']}|{order_data['item']}"
        order_data["mac"] = hmac.new(self.key1.encode(), data.encode(), hashlib.sha256).hexdigest()

        response = requests.post(self.endpoint, json=order_data)
        return response.json()

    def verify_callback(self, data, mac_received):
        raw_data = f"{data['data']}|{data['timestamp']}"
        mac_calculated = hmac.new(self.key2.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
        return mac_calculated == mac_received
