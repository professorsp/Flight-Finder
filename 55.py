from fapi import flight_data

api = flight_data()

api.set_arr_iata("your iata")

api.set_arr_icao("your icao")

api.set_dep_iata("your iata")

api.set_dep_icao("your icao")

api.set_flight_iata("your iata")

api.set_flight_icao("your icao")

api.set_flight_number("your number")

api.set_fligth_status("your status")

data = api.get_json()

api.write_file("your path")
