from flask import Flask, jsonify, render_template
import yaml
from car import Car
from data import get_list_of_sessions, final_data, last_actualisation, loadYaml, sessions_per_region, sessions_per_region_of_processed_data, final_data_of_processed_sessions

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    regions, _ = loadYaml()
    return render_template('index.html', regions=regions, )


@app.route('/home/<region>')
def region(region):
    regions, cars = loadYaml()
    carss = ["Audi", "BMW", "VW"]
    return render_template('region.html', region=region, cars=cars, carss=carss, last_actualisation=last_actualisation, sessions_per_region=sessions_per_region, sessions_per_region_of_processed_data=sessions_per_region_of_processed_data)


@app.route('/home/<region>/<car>')
def car(region, car):
    object = final_data
    car_data = None
    for cars in final_data:
        if cars['car_name'] == car:
            car_data = cars
    print("Process")
    car_data_of_prcessed_sessions = None
    for cars in final_data_of_processed_sessions:
        if cars['car_name'] == car:
            car_data_of_prcessed_sessions = cars
    return render_template('car.html', car=car, car_data=car_data, region=region, last_actualisation=last_actualisation, car_data_of_prcessed_sessions=car_data_of_prcessed_sessions)

#------------------------------------
@app.route('/home/test')
def data():
    car = Car('TWN', 'APAC', 345)
    car2 = {
        'name': 'MBV',
        'year': 123
    }
    # object,_= get_list_of_sessions()
    return jsonify(car2)

#------------------------------------
if __name__ == '__name__':
    app.run(DEBUG=True)

