from customtkinter import *
import CTkListbox
from CTkMessagebox import CTkMessagebox

from fapi import flight_data
from complete_data import complete_data

import json


class graghic(flight_data):
    def __init__(self, api_key, root: CTk):
        super().__init__(api_key)

        self.root = root
        self.top_frame = CTkFrame(self.root, corner_radius=20)
        self.top_frame.pack()

        # ======================================================Fligth frame======================================
        CTkLabel(self.top_frame, text="Fligth").grid(row=0, column=0)
        self.flight_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.flight_frame.grid(row=1, column=0, padx=20, pady=(0, 10))

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
            row=0, column=2, padx=(10, 0), pady=10
        )
        self.flight_iata_input = CTkEntry(self.flight_frame)
        self.flight_iata_input.grid(row=0, column=3, padx=(0, 10), pady=10)

        CTkLabel(self.flight_frame, text="icao").grid(
            row=1, column=2, padx=(10, 0), pady=10
        )
        self.flight_icao_input = CTkEntry(self.flight_frame)
        self.flight_icao_input.grid(row=1, column=3, padx=(0, 10), pady=10)

        # ========================================================Departure  frame=======================================
        CTkLabel(self.top_frame, text="Departure ").grid(row=0, column=1)
        self.dep_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.dep_frame.grid(row=1, column=1, padx=20, pady=(0, 10))

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
        CTkLabel(self.top_frame, text="Arrival").grid(row=0, column=2)
        self.arr_frame = CTkFrame(self.top_frame, corner_radius=10)
        self.arr_frame.grid(row=1, column=2, padx=20, pady=(0, 10))

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
        self.button_frame.grid(row=1, column=3, padx=20, pady=(0, 10))

        CTkButton(
            self.button_frame, text="Apply", height=100, command=self.Apply
        ).pack()
        # ==========================================down_frame=================================

        self.down_frame = CTkFrame(self.root, width=1100)
        self.down_frame.pack(fill="y", expand=True)

        self.listbox = CTkListbox.CTkListbox(
            self.down_frame,
            font=("Hack Regular", 12),
            command=self.show_value,
            width=1100,
        )
        self.listbox.pack(fill="y", expand=True)
        self.listbox.insert(0, "See your search results by clicking the <Apply> button")

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

        self.data = self.get_json()
        # self.data = json.load(open("tt1.json"))

        if self.data == 0:
            CTkMessagebox(icon="error", message="ConnectionError")
        else:
            # self.write_file("tt2.json")
            self.flight_list()

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

            index = f"{i+1}/{self.count}->"
            index = index + (" " * (9 - len(index)))

            self.listbox.insert(
                i,
                f"{index} Date: {date}      Status: {status}      Number: {number}      Flight iata:{iata}       Airline name: {airline_name}",
            )

    def show_value(self, val: str):
        self.index = val[: (val.index("/"))]
        complete_data((int(self.index)) - 1, self.root, self.data)


if __name__ == "__main__":
    root = CTk()
    root.title("Flight Finder")
    aa = graghic(api_key="9ac30502406f16081b214a4fe0f5587a", root=root)
    root.mainloop()
