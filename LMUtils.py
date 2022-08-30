import base64
import hashlib
import hmac
import time

import requests

# Class to extend auth capabilities of Requests to include LogicMonitor Auth
class LMAuth(requests.auth.AuthBase):
    def __init__(self, id, key):
        self.id = id
        self.key = key

    def __call__(self, r):
        # Auth process as per https://www.logicmonitor.com/support/rest-api-developers-guide/overview/using-logicmonitors-rest-api
        timestamp = str(int(time.time() * 1000))  # int(1000*datetime.datetime.timestamp(datetime.datetime.utcnow()))
        endpoint = "/"+("/".join("".join((r.path_url.split("?")[0])).split("/")[3:]))  # Extract endpoint from URL
        msg = (r.method + str(timestamp) + str(r.body or '') + endpoint).encode('utf-8') 
        hm = hmac.new(self.key.encode('utf-8'), msg=msg, digestmod=hashlib.sha256).hexdigest()
        signature = (base64.b64encode(hm.encode('utf-8'))).decode("utf-8")
        r.headers["Authorization"] = f"LMv1 {self.id}:{signature}:{timestamp}"
        return r


# Class to handle LM API operations
class lmAPI:
    def __init__(self, company, clientID, clientKey):
        self.company = company
        self.clientID = clientID
        self.clientKey = clientKey

    def getAuditLog(self, period):
        prev5min = str(int(time.time())-60*period) # Generate timestamp for x minutes ago
        endpoint = '/setting/accesslogs'
        querystr = f'v=2&size=1000&filter=happenedOn>:{prev5min}' # Define filter & result size
        url = f"https://{self.company}.logicmonitor.com/santaba/rest{endpoint}?{querystr}"
        response = requests.get(url, auth=LMAuth(self.clientID, self.clientKey))
        return response.json()
