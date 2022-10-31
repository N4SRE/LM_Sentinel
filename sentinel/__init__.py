import azure.functions as func
import pathlib
import argparse

from ..src.sentinel.pusher import Sentinel
from ..src.config.loader import SentinelConfigLoader


def main(mytimer: func.TimerRequest) -> None:
    config_loader = SentinelConfigLoader()
    config = config_loader.load_from_disk(filename=pathlib.Path(__file__).parent / 'sentinel.config.json')
    
    sentinel = Sentinel(config=config)
    sentinel.push()
