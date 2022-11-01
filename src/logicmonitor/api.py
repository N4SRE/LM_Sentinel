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
        all_auditlogs = {}
        log_history = str(int(time.time())-60*period) # Generate timestamp for x minutes ago
        log_now = str(int(time.time()))
        endpoint = '/setting/accesslogs'

        pagesize = 300
        offset = 0
        total_results = 1

        while offset < total_results:
            querystr = f'v=2&size={pagesize}&offset={offset}&filter=happenedOn>:{log_history},happenedOn<:{log_now}' # Define filter & result size
            url = f"https://{self.company}.logicmonitor.com/santaba/rest{endpoint}?{querystr}"
            response = requests.get(url, auth=LM_Auth(client_id=self.client_id, client_key=self.client_key))
            total_results = response.get('total')
            all_auditlogs.extend(response.get('items'))
        
        return all_auditlogs.json()