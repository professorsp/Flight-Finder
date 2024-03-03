import subprocess

import requests

import var

command = [
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe",
    "--enable-local-file-access",
    r"ticket\ht1.html",
    r"output.png"
]

url = "https://api.api-ninjas.com/v1/airlines"
header = {
    "X-Api-Key": "zstNXlUS0nzf0ddLeWs/CA==dxHAXgOM4tUfWRC9"
}


def create_ticket(data: dict):
    params = data["ticket"]
    response = requests.get(url, headers=header, params=params)
    airline_data = list(response.json())

    if len(airline_data) != 0:
        logo = f"{airline_data[0].get("logo_url")}"
    else:
        logo = None

    with open(r"ticket/ht1.html", 'w', encoding="utf-8") as file:
        file.write(
            var.ticket_generator(from_=data.get("from"),
                                 to=data.get("to"),
                                 flight=data.get("flight"),
                                 date=data.get("date"),
                                 time=data.get("time"),
                                 gate=data.get("gate"),
                                 seat=data.get("seat"),
                                 airline_logo=logo,
                                 airline_name=f"{params.get("name")}",
                                 fullname=data.get("fullname")))
        file.close()
        subprocess.run(command)
