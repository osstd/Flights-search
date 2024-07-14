import aiohttp
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from models import FlightData
import logging
from config import Config

logger = logging.getLogger(__name__)


class TequilaApiClient:
    def __init__(self):
        self.endpoint = Config.TEQUILA_ENDPOINT
        self.api_key = Config.TEQUILA_API_KEY
        self.headers = {'apikey': self.api_key}

    async def get(self, path: str, params: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.endpoint}/{path}", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json(), None
                error_msg = f"API request failed with status code {response.status}"
                logger.error(error_msg)
                return None, error_msg


class FlightSearch:
    def __init__(self, api_client: TequilaApiClient):
        self.api_client = api_client

    async def check_code(self, city_name: str) -> Tuple[Optional[str], Optional[str]]:
        query = {
            'term': city_name,
            'location_types': "city",
        }
        result, error = await self.api_client.get("locations/query", query)
        if result:
            try:
                return result["locations"][0]['code'], None
            except IndexError:
                return None, "No IATA code found for the city"
        return None, error

    async def find_flights(self, origin_city_code: str, destination_city_code: str,
                           from_time: datetime, to_time: datetime, nights_from: int,
                           nights_to: int, stops: int, currency: str) -> Tuple[Optional[FlightData], Optional[str]]:
        query = {
            'fly_from': origin_city_code,
            'fly_to': destination_city_code,
            'date_from': from_time.strftime('%d/%m/%Y'),
            'date_to': to_time.strftime('%d/%m/%Y'),
            'nights_in_dst_from': nights_from,
            'nights_in_dst_to': nights_to,
            'flight_type': 'round',
            'max_stopovers': stops,
            'curr': currency,
        }
        result, error = await self.api_client.get("search", query)
        if result:
            try:
                flight_data = result["data"][0]
                return FlightData(
                    price=flight_data["price"],
                    origin_city=flight_data["route"][0]["cityFrom"],
                    origin_airport=flight_data["route"][0]["flyFrom"],
                    destination_city=flight_data["route"][0]["cityTo"],
                    destination_airport=flight_data["route"][0]["flyTo"],
                    out_date=datetime.utcfromtimestamp(flight_data["route"][0]['dTimeUTC']).strftime(
                        '%Y-%m-%d %H:%M:%S UTC'),
                    return_date=datetime.utcfromtimestamp(flight_data["route"][1]['dTimeUTC']).strftime(
                        '%Y-%m-%d %H:%M:%S UTC'),
                ), None
            except IndexError:
                return None, "No flights found for the given criteria"
        return None, error
