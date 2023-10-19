from sched import scheduler
import time
import asyncio
import types
import aioschedule
from telebot.async_telebot import AsyncTeleBot
from tokenHelper import TokenBalanceChecker

balance_list = {}

all_groups = {}


class TelegramBot:
    def __init__(self, token):
        self.bot = AsyncTeleBot(token)
        self.balance_checker = TokenBalanceChecker()

        # 绑定命令处理函数
        @self.bot.message_handler(commands=['bind'])
        def bind_address(message):
            self.handle_bind_address(message)

        # 绑定消息处理函数
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            all_groups[message.chat_id] = message.chat_id
            self.handle_message(message)

    def extract_text_after_command(self, text, entities):
        command_text = ""

        if entities:
            for entity in entities:
                if entity['type'] == 'bot_command':
                    offset = entity['offset']
                    length = entity['length']
                    command_text = text[offset + length:].strip()
                    break  # 只提取第一个 bot_command 后的文字
        return command_text

    def handle_bind_address(self, message):
        from_user = message.from_user
        from_user_id = message.from_user.id

        if not from_user.is_bot and not balance_list.get(from_user_id):
            content = self.extract_text_after_command(
                message.text, message.json["entities"])
            if self.balance_checker.check_address(content):
                balance = self.balance_checker.get_token_balance(content)

                balance_list[from_user_id] = {
                    'balance': balance, 'address': content, 'date': message.date}
                self.bot.reply_to(message, "bind address successfully")
            else:
                self.bot.reply_to(message, "invalid address")

    def handle_message(self, message):
        from_user_id = message.from_user.id
        user = balance_list.get(from_user_id)
        balance = 0
        if not user:
            markup = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('去验证FERC资产')
            itembtn2 = types.KeyboardButton('退群')
            markup.add(itembtn1, itembtn2)
            self.bot.reply_to(
                message, "you have no bind address!", reply_markup=markup)
        else:
            balance = user["balance"]
            if user["date"] + 3600 > time.time():
                balance = self.balance_checker.get_token_balance(
                    user['address'])
            balance_list[from_user_id]["balance"] = balance
            balance_list[from_user_id]["date"] = message.date

            if balance < 500:
                self.bot.reply_to(message, "you have no enough balance")

    async def start(self):
        # self.bot.infinity_polling(allowed_updates=telebot.util.update_types)
        await asyncio.gather(self.bot.infinity_polling(), self.scheduler())

    # 发送消息到群
    def sendMessageToGroup(self, content):
        for group in all_groups:
            print(group)
            self.bot.send_message(chat_id=group, text=content)

    async def scheduler(self):
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
