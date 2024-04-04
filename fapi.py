import requests


class flight_data:
    def __init__(self, api_key):
        self.url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}"
        self.header = {
            "dep_iata": None,
            "arr_iata": None,
            "dep_icao": None,
            "arr_icao": None,
            "flight_number": None,
            "flight_iata": None,
            "flight_icao": None,
        }

    def set_fligth_status(self, status=None):
        parametrs = [
            "scheduled",
            "active",
            "landed",
            "cancelled",
            "incident",
            "diverted",
        ]

        if status in parametrs:
            self.header["flight_status"] = status

        else:
            self.header["flight_status"] = None

    def set_dep_iata(self, iata=None):
        self.header["dep_iata"] = iata

    def set_arr_iata(self, iata):
        self.header["arr_iata"] = iata

    def set_dep_icao(self, icao):
        self.header["dep_icao"] = icao

    def set_arr_icao(self, icao):
        self.header["arr_icao"] = icao

    def set_flight_number(self, numebr):
        self.header["flight_number"] = numebr

    def set_flight_iata(self, iata):
        self.header["flight_iata"] = iata

    def set_flight_icao(self, icao):
        self.header["flight_icao"] = icao

    def get_json(self):
        for key in list(self.header.keys()):
            if self.header[key] == None:
                del self.header[key]

        self.respone = requests.get(url=self.url, params=self.header, timeout=60)
        if self.respone.status_code == 200:
            self.result = self.respone.json()
            return self.result
        return {"error": f"{self.respone.status_code}: {self.respone.json()}"}

        """
        try:
            self.respone = requests.get(url=self.url, params=self.header, timeout=6)
            if self.respone.status_code == 200:
                self.result = self.respone.json()
                return self.result
        except requests.exceptions.ConnectionError:
            return {"error": "Connection Error"}
        except requests.exceptions.Timeout:
            return {"error": "Timeout"}
        """

    def write_file(self, path):
        file = open(path, "w")
        file.write(self.respone.text)
        file.close
