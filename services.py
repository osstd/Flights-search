from typing import List, Dict, Any
from models import City, FlightResult
from flight_search import FlightSearch, TequilaApiClient
import asyncio
import logging

logger = logging.getLogger(__name__)


class FlightService:
    def __init__(self):
        self.flight_search = FlightSearch(TequilaApiClient())

    async def search_flights(self, origin: str, destinations: List[str], search_params: Dict[str, Any]) -> List[
        FlightResult]:
        origin_code, origin_error = await self.flight_search.check_code(origin)
        if origin_error:
            logger.error(f"Error finding IATA code for origin city {origin}: {origin_error}")
            return [FlightResult(City(origin), error=f"Error finding IATA code: {origin_error}")]

        results = []
        tasks = [self.process_city(City(dest), origin_code, search_params) for dest in destinations]
        city_results = await asyncio.gather(*tasks)
        results.extend(city_results)
        return results

    async def process_city(self, city: City, origin_code: str, search_params: Dict[str, Any]) -> FlightResult:
        city.iata_code, code_error = await self.flight_search.check_code(city.name)
        if code_error:
            logger.error(f"Error finding IATA code for city {city.name}: {code_error}")
            return FlightResult(city, error=f"Error finding IATA code: {code_error}")

        flight, flight_error = await self.flight_search.find_flights(
            origin_code, city.iata_code,
            search_params['from_time'], search_params['to_time'],
            search_params['nights_in_dst_from'], search_params['nights_in_dst_to'],
            search_params['max_stopovers'], search_params['currency']
        )

        if flight_error:
            logger.error(f"Error finding flights for {city.name}: {flight_error}")
            return FlightResult(city, error=flight_error)

        return FlightResult(city, flight_data=flight)
