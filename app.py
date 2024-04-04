import concurrent.futures
import threading
from tkinter.ttk import Treeview

import requests
from CTkMessagebox import CTkMessagebox
from customtkinter import *
from tkintermapview import TkinterMapView, canvas_path, canvas_position_marker

import style
from ComplateData import ComplateData
from fapi import flight_data

set_appearance_mode("dark")
set_default_color_theme("theme/blue-theme.json")


class graghic(flight_data):
    def __init__(self, api_key: str, root: CTkToplevel):
        style.run()
        super().__init__(api_key)
        self.root = root
        self.root.title("Flight Finder")
        self.top_frame = CTkFrame(self.root, corner_radius=20)
        self.top_frame.pack(side=LEFT, fill=Y)

        self.root.bind("<Return>", lambda event: self.run_requests_thread())
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

        self.apply_button = CTkButton(
            self.button_frame,
            text="Apply",
            height=65,
            command=self.run_requests_thread
        )
        self.apply_button.pack()

        # ==========================================down_frame=================================

        self.down_frame = CTkTabview(self.root, width=1100)
        self.down_frame.pack(fill=BOTH, side=RIGHT, expand=1, padx=20, pady=20)
        self.down_frame.add("Map view")
        self.down_frame.add("Tabel view")

        # Tabel View
        f1 = CTkFrame(self.down_frame.tab("Tabel view"))
        f1.pack(fill=BOTH, expand=1)

        bs = CTkScrollbar(f1, orientation=HORIZONTAL)
        bs.pack(side=BOTTOM, fill="x")

        rs = CTkScrollbar(f1)
        rs.pack(side="right", fill="y")

        columns = (
            "Status", "Date", "Departure airport", "Arrival airport", "Takeoff time", "Landing time", "flight iata",
            "Airline")
        self.treeview = Treeview(
            master=f1,
            columns=columns,
            yscrollcommand=rs.set,
            xscrollcommand=bs.set,
        )
        self.treeview.tag_configure("odd", background="#2B2B2B")
        self.treeview.tag_configure("even", background="#242424")
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=50)
        self.treeview["show"] = "headings"
        self.treeview.pack(fill="both", expand=1, padx=20, pady=20)
        bs.configure(command=self.treeview.xview)
        rs.configure(command=self.treeview.yview)

        self.treeview.bind("<ButtonRelease-1>", lambda env: self.show_all_data(
            [self.data["data"][self.treeview.index(self.treeview.focus())]]))

        # Map View
        def create_map():
            self.map = TkinterMapView(self.down_frame.tab("Map view"), width=1100)
            self.map.pack(fill=BOTH, expand=True, pady=(0, 20))
            self.map.set_zoom(0)
            CTkButton(
                self.down_frame.tab("Map view"),
                text="Show all pathes",
                command=self.showAllPath,
            ).pack()

        threading.Thread(target=create_map).start()

    def Apply(self):
        self.apply_button.configure(state=DISABLED, text="Searching...")
        self.root.unbind("<Return>")

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
            self.data = self.get_json()

            if self.data.get("error") == None:
                self.geoData = self.update_geoData()
                self.mergeData()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.flight_map)
                    executor.submit(self.flight_list)
            else:
                print(f"{self.data.get('error')}")
        except requests.exceptions.ReadTimeout:
            from tkinter import messagebox
            messagebox.showerror("Timeout", "Your request took too long. Please check the internet and try again")

        self.root.bind("<Return>", lambda event: self.run_requests_thread())
        self.apply_button.configure(state=NORMAL, text="Apply")

    def flight_list(self):
        self.treeview.delete(*self.treeview.get_children())
        self.count = self.data["pagination"]["count"]
        tag = "odd"
        for i in range(self.count):
            self.treeview.insert("",
                                 i,
                                 values=(
                                     self.data["data"][i]["flight_status"],
                                     self.data["data"][i]["flight_date"],
                                     self.data["data"][i]["departure"]["airport"],
                                     self.data["data"][i]["arrival"]["airport"],
                                     self.data["data"][i]["departure"]["scheduled"][:16],
                                     self.data["data"][i]["arrival"]["scheduled"][:16],
                                     self.data["data"][i]["flight"]["iata"],
                                     self.data["data"][i]["airline"]["name"]

                                 ), tags=tag
                                 )
            tag = "odd" if tag == "even" else "even"

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
                iata,
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

        self.show_all_data(self.usefull_flight)

    def show_all_data(self, data):
        top = CTkToplevel(self.root)
        com = ComplateData(top, data, self.geoData)

    def markerClick(self, env: canvas_position_marker.CanvasPositionMarker):
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

    def run_requests_thread(self):
        print("run_requests_thread")
        self.requests_thread = threading.Thread(target=self.Apply)
        self.requests_thread.start()


if __name__ == "__main__":
    import sys

    root = CTk()
    root.withdraw()
    t = CTkToplevel(root)
    t.protocol("WM_DELETE_WINDOW", sys.exit)
    aa = graghic(api_key="604bc1fecafa0bc1a212fca237e0d18a", root=t)

    root.mainloop()
