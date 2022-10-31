import base64
import hashlib
import hmac
import time
import requests


# Class to extend auth capabilities of Requests to include LogicMonitor Auth
class LM_Auth(requests.auth.AuthBase):
    def __init__(self, client_id, client_key):
        self.client_id = client_id
        self.client_key = client_key

    def __call__(self, r):
        # Auth process as per https://www.logicmonitor.com/support/rest-api-developers-guide/overview/using-logicmonitors-rest-api
        timestamp = str(int(time.time() * 1000))  # int(1000*datetime.datetime.timestamp(datetime.datetime.utcnow()))
        endpoint = "/"+("/".join("".join((r.path_url.split("?")[0])).split("/")[3:]))  # Extract endpoint from URL
        msg = (r.method + str(timestamp) + str(r.body or '') + endpoint).encode('utf-8') 
        hm = hmac.new(self.client_key.encode('utf-8'), msg=msg, digestmod=hashlib.sha256).hexdigest()
        signature = (base64.b64encode(hm.encode('utf-8'))).decode("utf-8")
        r.headers["Authorization"] = f"LMv1 {self.client_id}:{signature}:{timestamp}"
        return r
