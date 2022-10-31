import json


class SentinelConfig:

    # {
    #     "LM_COMPANY": "node4",
    #     "AZ_TABLE": "logic_monitor_audit",
    #     "LOOKBACK_PERIOD_SECONDS": 300
    # }
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