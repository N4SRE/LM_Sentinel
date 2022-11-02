import json


class SentinelConfig:

    #  {
    #      "lm_company": "node4",
    #      "az_table": "logic_monitor_audit",
    #      "lookback_period_seconds": 300,
    #      "page_size": 1000 # don't push this above 1000, see https://www.logicmonitor.com/support/rest-api-developers-guide/v1/access-logs/get-access-log-entries
    #  }
    def __init__(self, config_dict: dict) -> None:
        self.lm_company: str = ''
        self.az_table: str = ''
        for key, value in config_dict.items():
            self.__setattr__(key, value)


class SentinelConfigLoader:

    def load_from_disk(self, filename: str) -> SentinelConfig:
        with open(filename) as config_file:
            config = json.loads(config_file.read())
            return SentinelConfig(config)