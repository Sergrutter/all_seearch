import sys
from io import BytesIO

import requests
from PIL import Image
from spn import get_spn

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"]

toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

spn_longitude, spn_latitude = get_spn(toponym)
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([spn_longitude, spn_latitude]),
    "l": "map",
    "pt": f"{spn_longitude},{spn_latitude},pm2rdm",
    "apikey": apikey
}

map_api_server = "https://static-maps.yandex.ru/v1"

response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
