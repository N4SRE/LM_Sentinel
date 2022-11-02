import logging
import os
import pprint

from ..config.loader import SentinelConfig
from ..logicmonitor.api import LM_API
from ..sentinel.log_analytics import LogAnalytics

class Sentinel:

  def __init__(self, config: SentinelConfig):
    #vars from the config
    self.config = config
    # sensitive vars from env (akv or local.settings.json)
    self.lm_id      = os.getenv(self.config.vault.get('logicmonitor_id'))
    self.lm_key     = os.getenv(self.config.vault.get('logicmonitor_key'))
    self.az_id      = os.getenv(self.config.vault.get('azure_id'))
    self.az_secret  = os.getenv(self.config.vault.get('azure_secret'))
    # init logicmonitor api class
    self.lm = LM_API(company=self.config.lm_company, client_id=self.lm_id, client_key=self.lm_key)
    # init azure api class
    self.la = LogAnalytics(customer_id=self.az_id, shared_key=self.az_secret, log_type=self.config.az_table)

  def push(self):
    # Grab last 5 minutes of logs
    audit_json = self.lm.getAuditLog(period=self.config.lookback_period_seconds)

    # Send logs into Azure
    self.la.sendtoAzure(audit_json)
