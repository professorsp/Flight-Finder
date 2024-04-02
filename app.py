import json

import requests
from CTkMessagebox import CTkMessagebox
from customtkinter import *
from tkintermapview import TkinterMapView, canvas_path, canvas_position_marker

from ComplateData import ComplateData
from fapi import flight_data
from libs import CTkListbox

set_appearance_mode("dark")
set_default_color_theme("theme/blue-theme.json")


class graghic(flight_data):
    def __init__(self, api_key: str, root):
        print("start graghic")
        super().__init__(api_key)
        self.root = root
        self.root.title("Flight Finder")
        self.top_frame = CTkFrame(self.root, corner_radius=20)
        self.top_frame.pack(side=LEFT, fill=Y)

        self.root.bind("<Return>", lambda event: self.Apply())
        # ======================================================Fligth frame======================================
        CTkLabel(self.top_frame, text="Fligth").pack()
        self.flight_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.flight_frame.pack(padx=20, pady=(0, 20))

        CTkLabel(self.flight_frame, text="Status").grid(
            row=0, column=0, padx=(10, 0), pady=10
        )
        self.status_input = CTkComboBox(
            self.flight_frame,
            state="readonly",
            values=[
                "None",
                "scheduled",
                "active",
                "landed",
                "cancelled",
                "incident",
                "diverted",
            ],
        )
        self.status_input.set("None")
        self.status_input.grid(row=0, column=1, padx=(0, 10), pady=10)

        CTkLabel(self.flight_frame, text="number").grid(
            row=1, column=0, padx=(10, 0), pady=10
        )
        self.flight_number_input = CTkEntry(self.flight_frame)
        self.flight_number_input.grid(row=1, column=1, padx=(0, 10), pady=10)

        CTkLabel(self.flight_frame, text="iata").grid(
            row=2, column=0, padx=(10, 0), pady=10
        )
        self.flight_iata_input = CTkEntry(self.flight_frame)
        self.flight_iata_input.grid(row=2, column=1, padx=(0, 10), pady=10)

        CTkLabel(self.flight_frame, text="icao").grid(
            row=3, column=0, padx=(10, 0), pady=10
        )
        self.flight_icao_input = CTkEntry(self.flight_frame)
        self.flight_icao_input.grid(row=3, column=1, padx=(0, 10), pady=10)

        # ========================================================Departure  frame=======================================
        CTkLabel(self.top_frame, text="Departure ").pack()
        self.dep_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.dep_frame.pack(padx=20, pady=(0, 20))

        CTkLabel(self.dep_frame, text="dep_iata").grid(
            row=0, column=0, padx=(10, 0), pady=10
        )
        self.dep_iata_input = CTkEntry(self.dep_frame)
        self.dep_iata_input.grid(row=0, column=1, padx=(0, 10), pady=10)

        CTkLabel(self.dep_frame, text="dep_icao").grid(
            row=1, column=0, padx=(10, 0), pady=10
        )
        self.dep_icao_input = CTkEntry(self.dep_frame)
        self.dep_icao_input.grid(row=1, column=1, padx=(0, 10), pady=10)

        # ===============================================================================Arrival frame=====================
        CTkLabel(self.top_frame, text="Arrival").pack()
        self.arr_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.arr_frame.pack(padx=20, pady=(0, 20))

        CTkLabel(self.arr_frame, text="arr_iata").grid(
            row=0, column=0, padx=(10, 0), pady=10
        )
        self.arr_iata_input = CTkEntry(self.arr_frame)
        self.arr_iata_input.grid(row=0, column=1, padx=(0, 10), pady=10)

        CTkLabel(self.arr_frame, text="arr_icao").grid(
            row=1, column=0, padx=(10, 0), pady=10
        )
        self.arr_icao_input = CTkEntry(self.arr_frame)
        self.arr_icao_input.grid(row=1, column=1, padx=(0, 10), pady=10)

        # =========================================================================Button===========================================
        self.button_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.button_frame.pack(padx=20, pady=(0, 20))

        CTkButton(self.button_frame, text="Apply", height=65, command=self.Apply).pack()

        # ==========================================down_frame=================================

        self.down_frame = CTkTabview(self.root, width=1100)
        self.down_frame.pack(fill=BOTH, side=RIGHT, expand=1, padx=20, pady=20)
        self.down_frame.add("Map view")
        self.down_frame.add("Tabel view")

        # Tabel View
        self.listbox = CTkListbox.CTkListbox(
            self.down_frame.tab("Tabel view"),
            font=("Hack Regular", 12),
            command=self.show_fullData,
            width=1100,
        )
        self.listbox.pack(fill=BOTH, expand=True, pady=(0, 20))
        self.listbox.insert(0, "See your search results by clicking the <Apply> button")

        # Map View
        self.map = TkinterMapView(self.down_frame.tab("Map view"), width=1100)
        self.map.pack(fill=BOTH, expand=True, pady=(0, 20))
        self.map.set_zoom(0)
        CTkButton(
            self.down_frame.tab("Map view"),
            text="Show all pathes",
            command=self.showAllPath,
        ).pack()
        print("stop")
    def Apply(self):
        # set_fligth_status
        self.set_fligth_status(self.status_input.get())
        # set_flight_number
        self.flight_number = self.flight_number_input.get()
        if self.flight_number != "":
            if self.flight_number.isdigit():
                self.set_flight_number(self.flight_number)
                self.flight_number_input.configure(bg_color="transparent")
            else:
                CTkMessagebox(
                    icon="info",
                    message="Enter only numbers in the flight number section",
                )
                self.flight_number_input.configure(bg_color="red")
        else:
            self.set_flight_number(None)
            self.flight_number_input.configure(bg_color="transparent")

        # set_flight_iata
        self.flight_iata = self.flight_iata_input.get().strip()
        if self.flight_iata == "":
            self.set_flight_iata(None)
        else:
            self.set_flight_iata(self.flight_iata)

        # set_flight_icao
        self.flight_icao = self.flight_icao_input.get().strip()
        if self.flight_icao == "":
            self.set_flight_icao(None)
        else:
            self.set_flight_icao(self.flight_icao)

        # set_dep_iata
        self.dep_iata = self.dep_iata_input.get().strip()
        if self.dep_iata == "":
            self.set_dep_iata(None)
        else:
            self.set_dep_iata(self.dep_iata)

        # set_dep_icao
        self.dep_icao = self.dep_icao_input.get().strip()
        if self.dep_icao == "":
            self.set_dep_icao(None)
        else:
            self.set_dep_icao(self.dep_icao)

        # set_arr_iata
        self.arr_iata = self.arr_iata_input.get().strip()
        if self.arr_iata == "":
            self.set_arr_iata(None)
        else:
            self.set_arr_iata(self.arr_iata)

        # set_arr_icao
        self.arr_icao = self.arr_icao_input.get().strip()
        if self.arr_icao == "":
            self.set_arr_icao(None)
        else:
            self.set_arr_icao(self.arr_icao)

        try:
            # self.data = self.get_json()
            self.data = json.load(open("data.json"))
        except requests.exceptions.ReadTimeout:
            print("aaaaaaaaaaaaaaaaa")

        if self.data.get("error") == None:
            self.geoData = self.update_geoData()
            # self.geoData = json.load(open("geoData.json"))
            self.mergeData()
            self.flight_map()
            self.flight_list()
        else:
            print(f"{self.data.get('error')}")

    def flight_list(self):
        self.listbox.insert(0, "See your search results by clicking the <Apply> button")
        self.listbox.delete(0, "end")
        self.count = self.data["pagination"]["count"]
        for i in range(self.count):
            date = self.data["data"][i]["flight_date"]

            status = self.data["data"][i]["flight_status"]
            if status != None:
                status = status + (" " * (9 - len(status)))
            else:
                status = "None     "

            number = self.data["data"][i]["flight"]["number"]
            if number != None:
                number = number + (" " * (4 - len(number)))
            else:
                number = "None"

            airline_name = self.data["data"][i]["airline"]["name"]

            iata = self.data["data"][i]["flight"]["iata"]
            if iata != None:
                iata = iata + (" " * (7 - len(iata)))
            else:
                iata = "None" + (" " * 3)

            index = f"{i + 1}/{self.count}->"
            index = index + (" " * (9 - len(index)))

            self.listbox.insert(
                i,
                f"{index} Date: {date}      Status: {status}      Number: {number}      Flight iata:{iata}       Airline name: {airline_name}",
            )

    def show_fullData(self, val: str):
        index = int(val[: (val.index("/"))]) - 1
        self.top_window = CTkToplevel()
        com = ComplateData(self.top_window, [self.data["data"][index]], self.geoData)

    def update_geoData(self):
        iatas = list()
        for i in range(len(self.data["data"])):
            iatas.append(self.data["data"][i]["departure"]["iata"])
            iatas.append(self.data["data"][i]["arrival"]["iata"])

        iatas = ",".join(set(iatas))
        respone = requests.get(
            url=f"http://127.0.0.1:5000/get_airport_data?iatas={iatas}"
        )
        if respone.status_code == 200 or respone.status_code == 400:
            data = respone.json()
            return data

    def flight_map(self):
        self.all_paths = list()
        self.map.delete_all_path()
        self.map.delete_all_marker()
        for iata in self.geoData.keys():
            self.geoData[iata]["marker"] = self.map.set_marker(
                self.geoData[iata]["lat"],
                self.geoData[iata]["lon"],
                self.geoData[iata]["name"],
                data=iata,
                command=self.markerClick,
            )

        for flight in self.data["data"]:
            del flight["flight"]["codeshared"]
            path = self.map.set_path(
                [
                    (self.geoData[flight["departure"]["iata"]]["marker"].position),
                    (self.geoData[flight["arrival"]["iata"]]["marker"].position),
                ],
                command=self.pathClick,
                data=(
                    flight["departure"]["iata"],
                    flight["arrival"]["iata"],
                    flight["flight"],
                ),
            )
            self.all_paths.append(path)

    def pathClick(self, env: canvas_path.CanvasPath):
        self.usefull_flight = list()
        for path in self.map.canvas_path_list:
            if (
                path.position_list == env.position_list
                or path.position_list == env.position_list[::-1]
            ):
                for flight in self.data["data"]:
                    if (
                        flight["departure"]["iata"] == path.data[0]
                        and flight["arrival"]["iata"] == path.data[1]
                        and flight["flight"] == path.data[2]
                    ):
                        self.usefull_flight.append(flight)

        self.top_window = CTkToplevel(self.root)
        com = ComplateData(self.top_window, self.usefull_flight, self.geoData)

    def markerClick(self, env: canvas_position_marker.CanvasPositionMarker):
        # path = canvas_path.CanvasPath()
        usefull = list()
        iata = env.data
        for path in self.all_paths:
            if path.data[0] == iata or path.data[1] == iata:
                usefull.append(path)

        self.map.delete_all_path()
        for path in usefull:
            self.map.set_path(
                path.position_list, data=path.data, command=self.pathClick
            )

    def showAllPath(self):
        for path in self.all_paths:
            self.map.set_path(
                path.position_list, data=path.data, command=self.pathClick
            )

    def mergeData(self):
        for i in range(len(self.data["data"])):
            dep_iata = self.data["data"][i]["departure"]["iata"]
            if self.data["data"][i]["departure"]["timezone"] == None:
                self.data["data"][i]["departure"]["timezone"] = self.geoData[dep_iata][
                    "timezone"
                ]
            if self.data["data"][i]["departure"]["airport"] == None:
                self.data["data"][i]["departure"]["airport"] = self.geoData[dep_iata][
                    "name"
                ]

            arr_iata = self.data["data"][i]["arrival"]["iata"]
            if self.data["data"][i]["arrival"]["timezone"] == None:
                self.data["data"][i]["arrival"]["timezone"] = self.geoData[arr_iata][
                    "timezone"
                ]
            if self.data["data"][i]["arrival"]["airport"] == None:
                self.data["data"][i]["arrival"]["airport"] = self.geoData[arr_iata][
                    "name"
                ]


if __name__ == "__main__":
    root = CTk()
    root.withdraw()
    t = CTkToplevel(root)
    t.protocol("WM_DELETE_WINDOW", root.destroy)
    aa = graghic(api_key="e5411ed9c2d96d6ee05e01743299d85b", root=t)

    root.mainloop()
