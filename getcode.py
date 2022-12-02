import requests

# Получаем параметры объекта для рисования карты вокруг него.
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


text = input()
print("Веду поиск, ожидайте ...")
geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
response = requests.get(geocoder_uri, params={
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "format": "json",
    "geocode": text
})

toponym = response.json()["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
ll, spn = get_ll_span(toponym)
# Можно воспользоваться готовой функцией,
# которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=sat,skl"
print(static_api_request)