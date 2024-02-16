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

        arr_timezone = self.data[0]["arrival"]["timezone"]
        if arr_timezone is not None:
            self.arr_capital = arr_timezone.split("/")[1]

        for flight in self.data:
            tab = flight["flight"]["iata"]
            self.tabView.add(tab)


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
