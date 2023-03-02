import requests
import os
class FlightSearch:
    def __init__(self, flyfrom: str, to: str, datefrom: str, dateto: str, cheapest):
        self.api_endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.api_key = os.environ.get("tequila_apikey")
        self.flyfrom = flyfrom
        self.stop_overs = 0
        self.to = to
        self.datefrom = datefrom
        self.dateto = dateto
        self.locations = None
        self.cheapest = cheapest
        self.response = None
        self.cheapest_info = None
        self.params = {"to": self.to,
                       "flyFrom": self.flyfrom,
                       "dateFrom": self.datefrom,
                       "dateTo": self.dateto,
                       "curr": "NGN",
                       "max_stopovers":f"{self.stop_overs}",
                       "nights_in_dst_to": 14,
                       "nights_in_dst_from": 14,
                       "flight_type": "round"
                        }


        self.header = {"apikey": self.api_key}
        self.data = None

    # looks for flight from the kiwi api
    def look_for_flights(self):
        "looks for all the flights available and returns the response json"
        self.response = requests.get(self.api_endpoint, params=self.params, headers=self.header)
        self.response.raise_for_status()
        self.data = self.response.json()
        if self.data.get("_results") == 0:
            self.stop_overs += 1
            self.params["max_stopovers"] = f"{self.stop_overs}"
            if self.stop_overs < 4:
                self.look_for_flights()
        else:
            return self.data

    def cheapest_flight(self):
        "looks for the cheapest flight"
        self.look_for_flights()
        for n in self.data["data"]:
            if int(n["price"]) < self.cheapest:
                self.cheapest = n["price"]
                self.cheapest_info = n
        if self.cheapest_info == None:
            self.stop_overs += 1
            self.params["max_stopovers"] = f"{self.stop_overs}"
            if self.stop_overs < 5:
                print(self.stop_overs)
                self.cheapest_flight()



        return (self.cheapest_info)




