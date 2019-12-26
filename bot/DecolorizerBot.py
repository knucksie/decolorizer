import telebot
from decolorizer import Decolorizer

bot = telebot.TeleBot('976833115:AAEIOasx0p0wKUr9JHxgtUOZvTnhCxwMMjo')


@bot.message_handler(content_types=['photo'])
def get_message(message):
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    Decolorizer.decolorize(name, name + "_decolorized.jpg")
    img = open(name + "_decolorized.jpg", 'rb')
    bot.send_photo(message.chat.id, img)


bot.polling(none_stop=True, interval=1)