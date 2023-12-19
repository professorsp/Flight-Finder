import customtkinter as tkp
from tkintermapview import TkinterMapView
import csv
import numpy as np

search_iata = dict()
with open("airports.csv", "r", encoding="utf-8") as file:
    datafile = csv.DictReader(file)
    for row in datafile:
        if row["iata_code"] != "":
            timezone = f'{row["continent"]}/{row["municipality"]}'
            search_iata[row["iata_code"]] = {
                "name": row["name"],
                "lat": float(row["latitude_deg"]),
                "lon": float(row["longitude_deg"]),
                "timezone": timezone,
            }


class complete_data:
    def __init__(self, index, root, data):
        self.data = data
        self.root = root
        self.index = index

        self.dep_iata = self.data["data"][self.index]["departure"]["iata"]
        self.dep_lat = search_iata[self.dep_iata]["lat"]
        self.dep_lon = search_iata[self.dep_iata]["lon"]
        self.dep_name = self.data["data"][self.index]["departure"]["airport"]
        if self.dep_name == None:
            self.dep_name = search_iata[self.dep_iata]["name"]
            if self.dep_name == None:
                self.dep_name = "None"
        self.dep_timezone = self.data["data"][self.index]["departure"]["timezone"]
        if self.dep_timezone == None:
            self.dep_timezone = search_iata[self.dep_iata]["timezone"]

        self.arr_iata = self.data["data"][self.index]["arrival"]["iata"]
        self.arr_lat = search_iata[self.arr_iata]["lat"]
        self.arr_lon = search_iata[self.arr_iata]["lon"]
        self.arr_name = self.data["data"][self.index]["arrival"]["airport"]
        if self.arr_name == None:
            self.arr_name = search_iata[self.arr_iata]["name"]
            if self.arr_name == None:
                self.arr_name = "None"
        self.arr_timezone = self.data["data"][self.index]["arrival"]["timezone"]
        if self.arr_timezone == None:
            self.arr_timezone = search_iata[self.arr_iata]["timezone"]


        self.window = tkp.CTkToplevel(self.root)
        self.window.resizable(width=False, height=False)

        self.left_frame = tkp.CTkFrame(self.window)
        self.left_frame.grid(row=0, column=0)

        self.top_frame = tkp.CTkFrame(self.left_frame)
        self.top_frame.pack()

        self.dep_frame = tkp.CTkFrame(self.top_frame)
        self.dep_frame.grid(row=0, column=0)

        tkp.CTkLabel(self.dep_frame, text="Departure").pack()

        tkp.CTkLabel(
            self.dep_frame,
            text=f"Airport: {self.dep_name}",
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f"Timezone: {self.dep_timezone}",
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f'iata: {self.data["data"][self.index]["departure"]["iata"]}',
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f'icao: {self.data["data"][self.index]["departure"]["icao"]}',
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f'terminal: {self.data["data"][self.index]["departure"]["terminal"]}',
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f'gate: {self.data["data"][self.index]["departure"]["gate"]}',
        ).pack(padx=10, pady=10)
        tkp.CTkLabel(
            self.dep_frame,
            text=f'delay: {self.data["data"][self.index]["departure"]["delay"]}',
        ).pack(padx=10, pady=10)

        self.arr_frame = tkp.CTkFrame(self.top_frame)
        self.arr_frame.grid(row=0, column=1)
        tkp.CTkLabel(self.arr_frame, text="Arrival").pack()
        tkp.CTkLabel(
            self.arr_frame,
            text=f"Airport: {self.arr_name}",
        ).pack(padx=10, pady=5)
        tkp.CTkLabel(
            self.arr_frame,
            text=f"Timezone: {self.arr_timezone}",
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'iata: {self.data["data"][self.index]["arrival"]["iata"]}',
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'icao: {self.data["data"][self.index]["arrival"]["icao"]}',
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'terminal: {self.data["data"][self.index]["arrival"]["terminal"]}',
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'gate: {self.data["data"][self.index]["arrival"]["gate"]}',
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'baggage: {self.data["data"][self.index]["arrival"]["baggage"]}',
        ).pack(padx=10, pady=8)
        tkp.CTkLabel(
            self.arr_frame,
            text=f'delay: {self.data["data"][self.index]["arrival"]["delay"]}',
        ).pack(padx=10, pady=8)

        # ======================================================================================================
        self.down_frame = tkp.CTkFrame(self.left_frame)
        self.down_frame.pack()

        self.flight_frame = tkp.CTkFrame(self.down_frame)
        self.flight_frame.grid(row=0, column=0)

        tkp.CTkLabel(
            self.flight_frame,
            text=f'Status: {self.data["data"][self.index]["flight_status"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Date: {self.data["data"][self.index]["flight_date"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Number: {self.data["data"][self.index]["flight"]["number"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Flight iata: {self.data["data"][self.index]["flight"]["iata"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Flight icao: {self.data["data"][self.index]["flight"]["icao"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Airline name: {self.data["data"][self.index]["airline"]["name"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Airline iata: {self.data["data"][self.index]["airline"]["iata"]}',
        ).pack()
        tkp.CTkLabel(
            self.flight_frame,
            text=f'Airline icao: {self.data["data"][self.index]["airline"]["icao"]}',
        ).pack()

        # right farme
        self.map_frame = tkp.CTkFrame(self.window)
        self.map_frame.grid(row=0, column=1)

        self.map_widget = TkinterMapView(
            self.map_frame, width=750, height=750, corner_radius=0
        )
        self.map_widget.pack(fill="both", expand=True)


        self.marker1 = self.map_widget.set_marker(
            self.arr_lat,
            self.arr_lon,
            text=f"Arrival airport:\n{self.arr_name}",
        )

        self.marker2 = self.map_widget.set_marker(
            self.dep_lat,
            self.dep_lon,
            text=f"Departure airport:\n{self.dep_name}",
        )

        self.C_lat = (self.arr_lat + self.dep_lat) / 2
        self.C_lon = (self.arr_lon + self.dep_lon) / 2
        self.map_widget.set_position(self.C_lat, self.C_lon)

        des = int(
            np.sqrt(
                ((self.dep_lat - self.arr_lat) * (self.dep_lat - self.arr_lat))
                + ((self.dep_lon - self.arr_lon) * (self.dep_lon - self.arr_lon))
            )
        )

        self.zoom = 9 - (
            np.interp(
                des, [0, 402], [self.map_widget.min_zoom, self.map_widget.max_zoom]
            )
        )
        self.map_widget.set_zoom(zoom=int(self.zoom))

        self.map_widget.set_path([self.marker1.position, self.marker2.position])


if __name__ == "__main__":
    import json

    data = json.load(open("text.json"))
    root = tkp.CTk()
    complete_data(0, root, data)
    root.mainloop()
