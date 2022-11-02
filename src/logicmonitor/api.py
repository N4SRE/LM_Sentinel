import time
import requests
import logging

from ..logicmonitor.auth import LM_Auth


# Class to handle LM API operations
class LM_API:
    def __init__(self, company: str, client_id: str, client_key: str, page_size: int): 
        self.company: str       = company
        self.client_id: str     = client_id
        self.client_key: str    = client_key
        self.page_size: int     = page_size

    def getAuditLog(self, period: int):
        all_auditlogs = []
        log_history = str(int(time.time())-60*period) # Generate timestamp for x minutes ago
        log_now = str(int(time.time()))
        endpoint = '/setting/accesslogs'

        offset = 0
        total_results_absolute = 1

        while offset < total_results_absolute:
            querystr = f'v=2&size={self.page_size}&offset={offset}&filter=happenedOn>:{log_history},happenedOn<:{log_now}' # Define filter & result size
            url = f"https://{self.company}.logicmonitor.com/santaba/rest{endpoint}?{querystr}"
            response = requests.get(url, auth=LM_Auth(client_id=self.client_id, client_key=self.client_key))
            response.raise_for_status()
            response_json = response.json()
            total_results = response_json.get('total')
            total_results_absolute = abs(total_results)  # handle negative totals
            logging.info(f"Pulled audit items. Offset: {offset}. Total: {total_results_absolute}.")
            all_auditlogs.extend(response_json.get('items'))
            offset += self.page_size
        
        return all_auditlogs