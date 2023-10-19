import time
from web3 import Web3
import json

from TelegramBot import TelegramBot


class EventHandler:
    def __init__(self, contract_address, abi_file_path, infura_project_id):
        self.contract_address = contract_address
        self.abi_file_path = abi_file_path
        self.infura_project_id = infura_project_id
        self.web3 = Web3(Web3.HTTPProvider(
            f'https://mainnet.infura.io/v3/{infura_project_id}'))
        with open(abi_file_path) as f:
            self.contract_abi = json.load(f)
        self.contract = self.web3.eth.contract(
            address=contract_address, abi=self.contract_abi)

    def handle_event(self, event):
        print("Event:", event)
        TelegramBot.sendMessageToGroup(self, content="新的币部署了")
        # 在这里处理事件数据

    def start_listening(self, event_name):
        event_filter = self.contract.events[event_name].create_filter(
            fromBlock=17841903)
        while True:
            for event in event_filter.get_all_entries():
                self.handle_event(event)
            time.sleep(5)
