from flask import Flask, render_template, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import asyncio
from datetime import datetime, timedelta
import logging
from config import Config
from services import FlightService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_object(Config)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50 per hour", "200 per day"],
)

flight_service = FlightService()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin_city = request.form['from']
        destinations_count = int(request.form['number'])
        return redirect(url_for('input_city', origin=origin_city, number=destinations_count))
    return render_template('index.html', intro=True)


@app.route('/input/<string:origin>/<int:number>', methods=['GET', 'POST'])
def input_city(origin: str, number: int):
    if request.method == 'POST':
        destinations = [request.form[f'to{i}'].lower() for i in range(number)]
        return redirect(url_for('flight_details', origin=origin, destinations=','.join(destinations)))
    return render_template('index.html', cityinput=True, origin=origin, number=number)


@app.route('/flight-details/<string:origin>/<string:destinations>', methods=['GET', 'POST'])
def flight_details(origin: str, destinations: str):
    if request.method == 'POST':
        search_params = {
            'from_time': datetime.strptime(request.form['date_f'], '%Y-%m-%d') if request.form[
                'date_f'] else datetime.now() + timedelta(days=1),
            'to_time': datetime.strptime(request.form['date_t'], '%Y-%m-%d') if request.form[
                'date_t'] else datetime.now() + timedelta(days=180),
            'nights_in_dst_from': int(request.form['nightsdf']) if request.form['nightsdf'] else 7,
            'nights_in_dst_to': int(request.form['nightsdt']) if request.form['nightsdt'] else 28,
            'max_stopovers': int(request.form['stops']) if request.form['stops'] else 0,
            'currency': request.form['currency']
        }

        results = asyncio.run(flight_service.search_flights(origin, destinations.split(','), search_params))
        return render_template('index.html', results=results)
    return render_template('index.html', details=True, origin=origin, destinations=destinations)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG)
