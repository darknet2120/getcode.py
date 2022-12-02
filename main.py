from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import requests

TOKEN = "5932040216:AAEn5ufnDeduZ77zJxtR-y0wLi2WEQuut0A"

def get_ll_span(address):
    toponym = address
    if not toponym:
        return None, None


    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())

    return (ll, span)

from Wiki import search_wiki

def echo(update, context):
    txt = update.message.text
    if txt.lower() in ['привет', 'салам']:
        txt = "И тебе ку мой друг!"
    elif txt.lower() in ['здоровье', 'жив']:
        txt = "Пока жив роднуля"
    update.message.reply_text(txt)

def start(update, context):
    update.message.reply_text("Это учебный бот.\nДля вывоза помощи наберите /help")


def help(update, context):
    update.message.reply_text("Для вызова помощи наберите /help \nДля поиска в википедии наберите /wiki <текст для поиска>\nКарта по адресу /geocode <Адрес объекта>")


def wikiword(update, context):
    print(context.args)
    word = " ".join(context.args)
    if word:
        update.message.reply_text("Идёт поиск...")
        result, url = search_wiki(word)
        update.message.reply_text(result+url)
    else:
        update.message.reply_text("Необходимо ввести текст для поиска")

def geocoder(update, context):
    update.message.reply_text("Веду поиск, ожидайте ...")
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })

    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_span(toponym)
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    print("Бот запущен")


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("wiki", wikiword))
    dp.add_handler(CommandHandler("geocode", geocoder))

    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
