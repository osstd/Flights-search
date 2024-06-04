import asyncio
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

search = FlightSearch()
origin_city = {'city': '', 'iataCode': ''}

cities = [
    {'city': '', 'iataCode': '', 'result': ""},
    {'city': '', 'iataCode': '', 'result': ""},
    {'city': '', 'iataCode': '', 'result': ""},
    {'city': '', 'iataCode': '', 'result': ""},
    {'city': '', 'iataCode': '', 'result': ""},
]

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin_city['city'] = request.form['from']
        destinations = request.form['number']
        return redirect(url_for('input_city', number=destinations))
    return render_template('index.html', intro=True)


@app.route('/input/<int:number>', methods=['GET', 'POST'])
def input_city(number):
    if request.method == 'POST':
        for number in range(number):
            cities[number]['city'] = request.form[f'to{number}'].lower()
        return redirect(url_for('flight_details'))
    return render_template('index.html', cityinput=True, number=number)


@app.route('/flight-details', methods=['GET', 'POST'])
def flight_details():
    if request.method == 'POST':
        if request.form['date_f']:
            from_time = datetime.strptime(request.form['date_f'], '%Y-%m-%d')
        else:
            from_time = tomorrow
        if request.form['date_t']:
            to_time = datetime.strptime(request.form['date_t'], '%Y-%m-%d')
        else:
            to_time = six_month_from_today
        if request.form['nightsdf']:
            nights_in_dst_from = int(request.form['nightsdf'])
        else:
            nights_in_dst_from = 7
        if request.form['nightsdt']:
            nights_in_dst_to = int(request.form['nightsdt'])
        else:
            nights_in_dst_to = 28
        if request.form['stops']:
            max_stopovers = int(request.form['stops'])
        else:
            max_stopovers = 0
        currency = request.form['currency']
        results_ = asyncio.run(
            flight_search(from_time, to_time, nights_in_dst_from, nights_in_dst_to, max_stopovers, currency))

        return render_template('index.html', cities=results_)
    return render_template('index.html', details=True)


async def flight_search(from_time, to_time, nights_from, nights_to, stops, currency):
    origin_city['iataCode'], err = await search.check_code(origin_city['city'])
    results = []

    if err or not origin_city['iataCode']:
        return [f"{origin_city['city'].capitalize()}: Error finding IATA code, {err}"]

    tasks = []
    for city in cities:
        if city['city']:
            tasks.append(asyncio.create_task(
                process_city(city, from_time, to_time, nights_from, nights_to, stops, currency)))

    city_results = await asyncio.gather(*tasks)
    results.extend(city_results)
    return results


async def process_city(city, from_time, to_time, nights_from, nights_to, stops, currency):
    print(f'started thread for {city["city"]}')
    city['iataCode'], err = await search.check_code(city['city'])
    if not city['iataCode']:
        return f"{city['city'].capitalize()}:\nNo IATA code was found for this city, please check the name and try again"
    elif err:
        return f"{city['city'].capitalize()}:\nError, {err}"

    flight, err = await search.find_flights(origin_city['iataCode'], city['iataCode'], from_time, to_time,
                                            nights_from, nights_to, stops, currency)
    if not flight:
        return f"{city['city'].capitalize()}:\nNo flight results were found for this search criteria"
    elif err:
        return f"{city['city'].capitalize()}:\nError, {err}"
    else:
        return f"{city['city'].capitalize()},\nfound a route!\nOnly {currency}{flight.price} to fly from {flight.origin_city}-" \
               f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, " \
               f"from {flight.out_date} to {flight.return_date}."


if __name__ == '__main__':
    app.run(debug=False)
