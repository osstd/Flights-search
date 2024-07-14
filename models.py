from dataclasses import dataclass
from typing import Optional


@dataclass
class City:
    name: str
    iata_code: Optional[str] = None


@dataclass
class FlightData:
    price: float
    origin_city: str
    origin_airport: str
    destination_city: str
    destination_airport: str
    out_date: str
    return_date: str


@dataclass
class FlightResult:
    city: City
    flight_data: Optional[FlightData] = None
    error: Optional[str] = None
