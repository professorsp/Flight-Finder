from io import BytesIO

import requests
from PIL import Image

url = "http://127.0.0.1:8000/get_ticket"

r = requests.post(url=url, json={
    "ticket": {
        "name": "Delta Air Lines",
        "iata": "DL",
        "icao": "DAL"
    },
    "from": "IR",
    "to": "JP",
    "flight": "GRSA",
    "date": "2024/05/03",
    "time": "12:30",
    "gate": "8",
    "seat": "1000",
    "fullname": "Mohammad"

})

Image.open(BytesIO(r.content)).show()
