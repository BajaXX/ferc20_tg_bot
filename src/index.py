from TelegramBot import TelegramBot
from EventHandler import EventHandler
import os

# 初始化 TelegramBot
bot = TelegramBot(
    token='6542648494:AAFMTRGP1fTnOdMQU4Iq2nRmLkI7MIEhowk',
)


# 启动 TelegramBot
# bot_thread = threading.Thread(target=bot.start)
# bot_thread.start()
bot.start()
print('TelegramBot started')

# 初始化 EventHandler
abi_file_path = os.path.join(os.path.dirname(
    __file__), 'abis/InscriptionFactory.json')

handler = EventHandler(
    contract_address='0x17fe21fAB4784eCaE27c7bB43d3d3cf3b73e7aA7',
    abi_file_path=abi_file_path,
    infura_project_id='5a45911c58bd4c42b335168f91866991'
)
# 启动监听
handler.start_listening('DeployInscription')
print('Started listening for DeployInscription events')
