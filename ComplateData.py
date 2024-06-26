import re
import threading
from io import BytesIO

import numpy as np
import requests
from PIL import Image
from customtkinter import *
from tkintermapview import TkinterMapView


class ComplateData:
    def __init__(self, root: CTk, data: dict, geoData: dict):
        self.root = root
        self.data = data

        self.geodata = geoData

        self.root.resizable(False, False)
        self.tabView = CTkTabview(self.root, fg_color="#1A5F78")
        self.tabView.pack(fill=BOTH, expand=1)

        for flight in self.data:
            tab = flight["flight"]["iata"]
            self.tabView.add(tab)

            dep_frame = CTkFrame(self.tabView.tab(tab), fg_color="#2596be", corner_radius=35)
            dep_frame.grid(row=0, column=0, sticky=W, padx=5, pady=20)
            CTkLabel(dep_frame, text="Departure", fg_color="#0F88B3", corner_radius=20).grid(row=0, column=0, sticky=NW,
                                                                                             padx=15, pady=5)

            match = re.search(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", flight["departure"]["scheduled"])
            if match:
                time = match.group(2)
                date = match.group(1)
            else:
                time = date = None
            (CTkLabel(dep_frame, text="Data: " + str(date), fg_color="#0F88B3", corner_radius=20)
             .grid(row=1, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="Time: " + str(time), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=0, sticky=NW, padx=15, pady=5))

            dep_airport = flight["departure"]["airport"]
            if dep_airport != None and len(dep_airport) > 20:
                dep_airport = dep_airport[:20] + "  ---\n\n--- " + dep_airport[20:]

            (CTkLabel(dep_frame, text="Airport: " + str(dep_airport), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="Timezone: " + str(flight["departure"]["timezone"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=1, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="IATA: " + str(flight["departure"]["iata"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="ICAO: " + str(flight["departure"]["icao"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="Terminal: " + str(flight["departure"]["terminal"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=1, column=2, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="Gate: " + str(flight["departure"]["gate"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=2, sticky=NW, padx=15, pady=5))
            (CTkLabel(dep_frame, text="delay: " + str(flight["departure"]["delay"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=3, column=2, sticky=NW, padx=15, pady=5))

            arr_frame = CTkFrame(self.tabView.tab(tab), fg_color="#2596be", corner_radius=35)
            arr_frame.grid(row=1, column=0, sticky=W, padx=5, pady=20)
            CTkLabel(arr_frame, text="Arrival", fg_color="#0F88B3", corner_radius=20).grid(row=0, column=0, sticky=NW,
                                                                                           padx=15, pady=5)

            match = re.search(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", flight["arrival"]["scheduled"])
            if match:
                time = match.group(2)
                date = match.group(1)
            else:
                time = date = None
            (CTkLabel(arr_frame, text="Data: " + str(date), fg_color="#0F88B3", corner_radius=20)
             .grid(row=1, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="Time: " + str(time), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=0, sticky=NW, padx=15, pady=5))

            arr_airport = flight["arrival"]["airport"]
            if arr_airport != None and len(arr_airport) > 20:
                arr_airport = arr_airport[:20] + "  ---\n\n--- " + arr_airport[20:]

            (CTkLabel(arr_frame, text="Airport: " + str(arr_airport), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="Timezone: " + str(flight["arrival"]["timezone"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=1, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="IATA: " + str(flight["arrival"]["iata"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="ICAO: " + str(flight["arrival"]["icao"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="Terminal: " + str(flight["arrival"]["terminal"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=1, column=2, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="Gate: " + str(flight["arrival"]["gate"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=2, column=2, sticky=NW, padx=15, pady=5))
            (CTkLabel(arr_frame, text="delay: " + str(flight["arrival"]["delay"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=2, sticky=NW, padx=15, pady=5))

            flight_frame = CTkFrame(self.tabView.tab(tab), fg_color="#2596be", corner_radius=35)
            flight_frame.grid(row=2, column=0, sticky=W, padx=5, pady=20)
            (CTkLabel(flight_frame, text="Flight", fg_color="#0F88B3", corner_radius=20)
             .grid(row=0, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(flight_frame, text="Status: " + str(flight["flight_status"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=1, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(flight_frame, text="Number: " + str(flight["flight"]["number"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=2, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(flight_frame, text="IATA: " + str(flight["flight"]["iata"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=3, column=0, sticky=NW, padx=15, pady=5))
            (CTkLabel(flight_frame, text="ICAO: " + str(flight["flight"]["icao"]), fg_color="#0F88B3", corner_radius=20)
             .grid(row=4, column=0, sticky=NW, padx=15, pady=5))

            CTkLabel(flight_frame, text="Airline", fg_color="#0F88B3", corner_radius=20).grid(row=0, column=1,
                                                                                              sticky=NW, padx=15,
                                                                                              pady=5)
            airlineName = flight["airline"]["name"]
            if airlineName != None and len(airlineName) > 20:
                airlineName = airlineName[:20] + "  ---\n\n--- " + airlineName[20:]

            (CTkLabel(flight_frame, text="Name: " + str(airlineName), fg_color="#0F88B3", corner_radius=20)
             .grid(row=1, column=1, sticky=NW, rowspan=2, padx=15, pady=5))
            (CTkLabel(flight_frame, text="IATA: " + str(flight["airline"]["iata"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=3, column=1, sticky=NW, padx=15, pady=5))
            (CTkLabel(flight_frame, text="ICAO: " + str(flight["airline"]["icao"]), fg_color="#0F88B3",
                      corner_radius=20)
             .grid(row=4, column=1, sticky=NW, padx=15, pady=5))

            if flight["flight_status"]== "scheduled":
                CTkButton(self.tabView.tab(tab), text="Receive flight ticket", fg_color="#54A6B2", text_color="#FFFF00",
                          command=lambda data=flight: self.ticket(data)).grid(row=2, column=0, sticky=E)

            map_frame = CTkFrame(self.tabView.tab(tab), bg_color="black")
            map_frame.grid(row=0, column=1, rowspan=3, padx=15, pady=15)
            map_widget = TkinterMapView(map_frame, width=750, height=750, corner_radius=50, bg_color="#1A5F78")
            map_widget.pack(fill=BOTH, expand=1)

            dep_lat = self.geodata[flight["departure"]["iata"]]["lat"]
            dep_lon = self.geodata[flight["departure"]["iata"]]["lon"]
            arr_lat = self.geodata[flight["arrival"]["iata"]]["lat"]
            arr_lon = self.geodata[flight["arrival"]["iata"]]["lon"]

            Clat = (arr_lat + dep_lat) / 2
            Clon = (arr_lon + dep_lon) / 2
            map_widget.set_position(Clat, Clon)

            map_widget.set_marker(dep_lat, dep_lon, text=f"Departure airport:\n{dep_airport}")
            map_widget.set_marker(arr_lat, arr_lon, text=f"Arrival airport:\n{arr_airport}")

            des = int(
                np.sqrt(
                    ((dep_lat - arr_lat) * (dep_lat - arr_lat))
                    + ((dep_lon - arr_lon) * (dep_lon - arr_lon))
                )
            )

            zoom = 10 - (
                np.interp(
                    des, [0, 402], [map_widget.min_zoom, map_widget.max_zoom]
                )
            )
            map_widget.set_zoom(zoom=int(1))

            map_widget.set_path([(dep_lat, dep_lon), (arr_lat, arr_lon)])

    def ticket(self, data: dict):
        def run():
            url = "http://127.0.0.1:8000/get_ticket"
            match = re.search(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", data["departure"]["scheduled"])
            if match:
                time = match.group(2)
                date = match.group(1)
            else:
                time = date = None

            r = requests.post(url=url, json={
                "ticket": data["airline"],
                "from": "IR",
                "to": "JP",
                "flight": data["flight"]["iata"],
                "date": date.strip(),
                "time": time.strip().replace("-", "/"),
                "gate": data["departure"]["gate"],
                "seat": "1000",
                "fullname": "Mohammad33"

            })

            img = Image.open(BytesIO(r.content))
            #img.save("ticket.png", "PNG")
            img.show()
        threading.Thread(target=run).start()

if __name__ == '__main__':
    import json

    root = CTk(fg_color="#1A5F78")
    data = json.load(open("CompleteData.json"))
    geoData = json.load(open("geoData.json"))
    app = ComplateData(root=root,
                       data=data,
                       geoData=geoData,
                       )
    root.mainloop()
