import telebot

# Замените 'YOUR_API_TOKEN' на ваш токен, полученный от @BotFather
API_TOKEN = '8348470380:AAF3FYu-0SJu1v0UXuyjQSBXTbzuRIZICKg'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")

# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
