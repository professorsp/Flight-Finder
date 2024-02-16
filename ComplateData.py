import re
from io import BytesIO

import requests
from PIL import Image, ImageTk
from customtkinter import *


class ComplateData:
    def __init__(self, root: CTk, data: dict, geoData: dict):
        self.root = root
        self.data = data
        self.geodata = geoData

        self.tabView = CTkTabview(self.root)
        self.tabView.pack(fill=BOTH, expand=1)

        dep_timezone = self.data[0]["departure"]["timezone"]
        if dep_timezone is not None:
            self.dep_capital = dep_timezone.split("/")[1]
            self.dep_flag = self.getFlag(self.dep_capital)
            # self.dep_flag = self.dep_flag.resize((600, 450))
            self.dep_flag = self.dep_flag.rotate(90, expand=1)
            self.dep_flag.save("dada.png")

        arr_timezone = self.data[0]["arrival"]["timezone"]
        if arr_timezone is not None:
            self.arr_capital = arr_timezone.split("/")[1]
            self.arr_flag = self.getFlag(self.arr_capital)
            self.arr_flag.resize((600, 450))
            self.arr_flag.rotate(90, expand=1)

        for flight in self.data:
            tab = flight["flight"]["iata"]
            self.tabView.add(tab)

            # dep_frame
            dep_frame = CTkFrame(self.tabView.tab(tab))
            dep_frame.grid(row=0, column=0, padx=5, pady=5)
            CTkLabel(dep_frame,
                     text="",
                     image=CTkImage(self.dep_flag, size=(400, 300)),
                     ).place(x=0, y=0, relwidth=1, relheight=1)

            CTkLabel(dep_frame, text="Departure").pack(anchor="w", pady=2)

            match = re.search(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", flight["departure"]["scheduled"])
            if match:
                time = match.group(1)
                date = match.group(2)
            else:
                time = date = None

            CTkLabel(dep_frame, text="Date: "f"{date}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="Time: "f"{time}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="Airport: "f"{flight["departure"]["airport"]}").pack(anchor="w", pady=2)
            # CTkLabel(dep_frame, text="Timezone: "f"{flight["departure"]["timezone"]}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="IATA: "f"{flight["departure"]["iata"]}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="ICAO: "f"{flight["departure"]["icao"]}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="Terminal: "f"{flight["departure"]["terminal"]}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="Gate: "f"{flight["departure"]["gate"]}").pack(anchor="w", pady=2)
            CTkLabel(dep_frame, text="Delay: "f"{flight["departure"]["delay"]}").pack(anchor="w", pady=2)
            dep_frame.configure(width=500)

            # arr_frame
            arr_frame = CTkFrame(self.tabView.tab(tab))
            arr_frame.grid(row=0, column=1, padx=5, pady=5)
            CTkLabel(arr_frame, text="", image=ImageTk.PhotoImage(self.arr_flag)).place(x=0, y=0,
                                                                                        relwidth=1,
                                                                                        relheight=1)

            CTkLabel(arr_frame, text="Departure").pack(anchor="w", pady=2)
            if match:
                time = match.group(1)
                date = match.group(2)
            else:
                time = date = None

            CTkLabel(arr_frame, text="Date: "f"{date}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="Time: "f"{time}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="Airport: "f"{flight["arrival"]["airport"]}").pack(anchor="w", pady=2)
            # CTkLabel(arr_frame, text="Timezone: "f"{flight["arrival"]["timezone"]}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="IATA: "f"{flight["arrival"]["iata"]}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="ICAO: "f"{flight["arrival"]["icao"]}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="Terminal: "f"{flight["arrival"]["terminal"]}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="Gate: "f"{flight["arrival"]["gate"]}").pack(anchor="w", pady=2)
            CTkLabel(arr_frame, text="Delay: "f"{flight["departure"]["delay"]}").pack(anchor="w", pady=2)

            # fligth_frame
            flight_frame = CTkFrame(self.tabView.tab(tab))
            flight_frame.grid(row=1, column=0, columnspan=2)
            flight_frame.grid_anchor("w")
            CTkLabel(flight_frame, text="", image=ImageTk.PhotoImage(Image.open("plan.jpg").resize((250, 187)))).place(
                x=0, y=0,
                relwidth=1,
                relheight=1)

            CTkLabel(flight_frame, text="Status: "f"{flight["flight_status"]}").grid(row=1, column=0, padx=5, pady=5)
            CTkLabel(flight_frame, text="Number: "f"{flight["flight"]["number"]}").grid(row=3, column=0, padx=5, pady=5)
            CTkLabel(flight_frame, text="IATA: "f"{flight["flight"]["iata"]}").grid(row=4, column=0, padx=5, pady=5)
            CTkLabel(flight_frame, text="ICAO: "f"{flight["flight"]["icao"]}").grid(row=1, column=1, padx=5, pady=5)

            CTkLabel(flight_frame, text="Date: "f"{flight["flight_date"]}").grid(row=2, column=0, padx=5, pady=5)
            CTkLabel(flight_frame, text="Airline: "f"{flight["airline"]["name"]}").grid(row=2, column=1, padx=5, pady=5)

    def getFlag(self, capital: str):

        response = requests.get("https://restcountries.com/v3.1/capital/" + capital)
        response = requests.get(response.json()[0]["flags"]["png"])
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))


if __name__ == '__main__':
    import json

    root = CTk()
    data = json.load(open("CompleteData.json"))
    geoData = json.load(open("geoData.json"))
    app = ComplateData(root=root,
                       data=data,
                       geoData=geoData,
                       )
    root.mainloop()
