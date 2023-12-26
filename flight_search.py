import requests
from datetime import datetime
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = os.environ.get('T_E')
TEQUILA_API_KEY = os.environ.get('T_KEY')
headers = {
    'apikey': TEQUILA_API_KEY,
}


class FlightSearch:
    def check_code(self, city_name):

        query = {
            'term': city_name,
            'location_types': "city",
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=query, headers=headers)
        response.raise_for_status()
        result = response.json()["locations"]
        code = result[0]['code']
        return code

    def find_flights(self, origin_city_code, destination_city_code, from_time, to_time, nights_from, nights_to, stops):
        query = {
            'fly_from': origin_city_code,
            'fly_to': destination_city_code,
            'date_from': from_time.strftime('%d/%m/%Y'),
            'date_to': to_time.strftime('%d/%m/%Y'),
            'nights_in_dst_from': nights_from,
            'nights_in_dst_to': nights_to,
            'flight_type': 'round',
            'max_stopovers': stops,
            'curr': 'USD',
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/search", params=query, headers=headers)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=datetime.utcfromtimestamp(data["route"][0]['dTimeUTC']).strftime('%Y-%m-%d %H:%M:%S UTC'),
            return_date=datetime.utcfromtimestamp(data["route"][1]['dTimeUTC']).strftime('%Y-%m-%d %H:%M:%S UTC'),
        )

        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data
