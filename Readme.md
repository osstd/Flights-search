# Flight Search App

This application helps users search for flights between cities using asynchronous programming to improve performance and
efficiency. It leverages Flask for the web framework and asyncio for concurrency.

## Features

- Asynchronous flight search for multiple destination cities
- User input for origin city, number of destinations, travel dates, duration of stay, and stopovers
- Concurrent processing of flight data to reduce search time
- Integration with Tequila API for flight data

## Requirements

- Python 3.7+
- Flask
- Aiohttp

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/osstd/Flights-search.git
    cd flight-search-app
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set environment variables:

   On Linux or macOS:

    ```bash
    export F_KEY='your_secret_key'
    export T_E='your_tequila_endpoint'
    export T_KEY='your_tequila_api_key'
    ```

   On Windows:

    ```bash
    set F_KEY=your_secret_key
    set T_E=your_tequila_endpoint
    set T_KEY=your_tequila_api_key
    ```

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000/`

3. Follow the steps on the web interface to search for flights:

    - Enter the origin city and number of destination cities
    - Enter the names of the destination cities
    - Specify travel details such as dates, duration of stay, maximum stopovers, and currency
4. Get results

## Asynchronous Programming and Concurrency

### Key Points

- Utilize `asyncio` to manage concurrent tasks efficiently
- The application uses `asyncio.create_task` to create tasks for each city search and `asyncio.gather` to wait for all
  tasks to complete

## Code Overview

### Main Components

Flask Routes:

1. `/`: Home page for entering the origin city and number of destination cities
2. `/input/<int:number>`: Page for inputting destination cities
3. `/flight-details`: Page for specifying flight details and displaying results

main.py async Functions:

1. `flight_search`: Orchestrates the async tasks for searching flights
2. `process_city`: Handles the search for a single city

FlightSearch Class:

1. `check_code`: Asynchronously fetches the IATA code for a city
2. `find_flights`: Asynchronously searches for flights using the IATA codes and specified criteria

## Try Live

[Try It Live](https://flight-checker-vercel.vercel.app/)

## Example

![Demonstration](https://i.imgur.com/YSUgKCG.png)

## Conclusion

This Flight Search App is a practical demonstration of using asynchronous programming in Python to handle concurrent
I/O-bound tasks efficiently. By leveraging Flask for the web framework and aiohttp for making async HTTP requests, the
app ensures a responsive and fast user experience.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
