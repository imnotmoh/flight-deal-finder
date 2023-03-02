import requests
import os
class DataManager:
    def __init__(self, id=None):
        self.API_AUTH = f"Basic {os.environ.get('sheety_key')}"
        self.API_ADRRESS = "https://api.sheety.co/85845f8b69a7495e6540a37393afe9ec/flightDeals/prices"
        self.user_sheet_api = "https://api.sheety.co/85845f8b69a7495e6540a37393afe9ec/flightDeals/users"
        self.API_GETEND = "https://api.sheety.co/85845f8b69a7495e6540a37393afe9ec/flightDeals/prices"
        self.id = id
        self.response = None
        self.data = None

    # get our spread sheet data
    def get_data(self):
        """gets spread sheet data"""

        self.response = requests.get(self.API_GETEND, headers={"Authorization": f"Basic {os.environ.get('sheety_key')}"})
        self.response.raise_for_status()
        self.data = self.response.json()
        return self.data["prices"]

    def update(self):
        """uploads the iata code to the cities without one in our spread sheet"""
        self.get_data()
        for iata in self.data["prices"]:
            if iata.get("iataCode") == None:
                sear = iata["city"]
                response = requests.get("https://api.tequila.kiwi.com/locations/query", params={"term":sear},
                                headers={"apikey": f"{os.environ.get('tequilla_wid_key')}"})
                raw_code = response.json()
                code = raw_code["locations"][0]["code"]
                response = requests.put(self.API_ADRRESS + f"/{self.id}", json={"price":{"iataCode":code}}, headers={"Authorization": f"Basic {os.environ.get('sheety_key')}"})
                print(response.text)

    def get_user_email(self):
        "gets the json of our user data base"
        user_mail = requests.get(self.user_sheet_api, headers={"Authorization": f"Basic {os.environ.get('sheety_key')}"})
        user_mail_json = user_mail.json()
        user_mails = user_mail_json["users"]
        return user_mails










