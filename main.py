from data_manager import DataManager
import os
from flight_search import FlightSearch
from datetime import datetime
from send_funnc import send

now = datetime.now()
strdatenow = now.strftime('%d/%m/%Y')
datamanager = DataManager()
cities_to = datamanager.get_data()
emails = datamanager.get_user_email()
# iterates through our set prices to get the max price set for a destination in spread sheet
for i in cities_to:

    flight_search = FlightSearch(flyfrom="LOS", to=i["iataCode"], datefrom=strdatenow, dateto="03/07/2023",
                                 cheapest=i["lowestPrice"])
    cheapest = flight_search.cheapest_flight()

    # checks for error if there are no flights cheaper than the set prices
    try:
        # formats the time key in our flight dict
        time_list = cheapest['local_departure'].split('T')
        # checks if price of the cheapest flight found is cheaper than our set price
        if int(i.get("lowestPrice")) > int(flight_search.cheapest_flight()["price"]):
            print("working")
            messages = f"Subject: Cheap ticket deals\n\nFly from {cheapest['cityFrom']} to {cheapest['cityTo']} for N{cheapest['price']} on {time_list[0]}, Time: {time_list[1].removesuffix('.000Z')} to book click on the link below\n{cheapest['deep_link']}"

            # iterates through our data to find emails of registered users
            for v in emails:
                send(mail="mohudemypython@gmail.com", password=os.environ.get("password"), receive_addrs=v.get("email"),
                      message=messages)
        else:
            print("too expensive")
    except TypeError:
        print(f"no cheap price to this destination({i['city']})")

