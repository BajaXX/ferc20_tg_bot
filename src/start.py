import time
import telebot

from tokenHelper import TokenBalanceChecker


balance_list = {}

bot = telebot.TeleBot(
    "6542648494:AAFMTRGP1fTnOdMQU4Iq2nRmLkI7MIEhowk")
balance_checker = TokenBalanceChecker()


def extract_text_after_command(text, entities):
    command_text = ""

    if entities:
        for entity in entities:
            if entity['type'] == 'bot_command':
                offset = entity['offset']
                length = entity['length']
                command_text = text[offset + length:].strip()
                break  # 只提取第一个 bot_command 后的文字
    return command_text


# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     print(message)
#     bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['bind'])
def bind_address(message):

    from_user = message.from_user
    from_user_id = message.from_user.id

    print(message.json["from"])
    print(message.json["entities"])

    if not from_user.is_bot and not balance_list.get(from_user_id):
        content = extract_text_after_command(
            message.text, message.json["entities"])
        if balance_checker.check_address(content):
            balance = balance_checker.get_token_balance(content)

            balance_list[from_user_id] = {
                'balance': balance, 'address': content, 'date': message.date}
            bot.reply_to(message, "bind address successfully")
        else:
            bot.reply_to(message, "invalid address")

    print(balance_list)


@bot.message_handler(func=lambda message: True)
def echo_message(message):

    from_user_id = message.from_user.id
    user = balance_list.get(from_user_id)
    balance = 0
    if not user:
        bot.reply_to(message, "you have no bind address")
    else:
        print(user)
        balance = user["balance"]
        if user["date"]+3600 > time.time():
            balance = balance_checker.get_token_balance(user['address'])
        balance_list[from_user_id]["balance"] = balance
        balance_list[from_user_id]["date"] = message.date

        if balance < 500:
            bot.reply_to(message, "you have no enough balance")

    # bot.reply_to(message, message.text)


bot.infinity_polling()


def extract_text_after_command(text, entities):
    command_text = ""

    if entities:
        for entity in entities:
            if entity['type'] == 'bot_command':
                offset = entity['offset']
                length = entity['length']
                command_text = text[offset + length:].strip()
                break  # 只提取第一个 bot_command 后的文字
    return command_text


# address = '0x890978ed364bdcdf7e0aab5e03860088e0af2db6'  # 替换为目标地址
# balance_checker = TokenBalanceChecker()
# balance = balance_checker.get_token_balance(address)
# print(f"Token balance: {balance}")
