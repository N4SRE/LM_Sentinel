import time
import requests

from ..logicmonitor.auth import LM_Auth


# Class to handle LM API operations
class LM_API:
    def __init__(self, company: str, client_id: str, client_key: str): 
        self.company: str       = company
        self.client_id: str     = client_id
        self.client_key: str    = client_key

    def getAuditLog(self, period: int):
        log_history = str(int(time.time())-60*period) # Generate timestamp for x minutes ago
        endpoint = '/setting/accesslogs'
        querystr = f'v=2&size=1000&filter=happenedOn>:{log_history}' # Define filter & result size
        url = f"https://{self.company}.logicmonitor.com/santaba/rest{endpoint}?{querystr}"
        response = requests.get(url, auth=LM_Auth(client_id=self.client_id, client_key=self.client_key))
        return response.json()