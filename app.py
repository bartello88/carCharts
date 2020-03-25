from flask import Flask, jsonify, render_template, jsonify
import yaml
from car import Car
from data import get_list_of_sessions, final_data, last_actualisation, loadYaml, data, sessions_per_region

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
    return render_template('region.html', region=region, cars=cars, carss=carss, last_actualisation=last_actualisation, sessions_per_region=sessions_per_region)


@app.route('/home/<region>/<car>')
def car(region, car):
    object = final_data
    car_data = None
    for cars in object:
        if cars['car_name'] == car:
            print(cars)
            print(cars['01'])
            car_data = cars
    return render_template('car.html', car=car, car_data=car_data, region = region, last_actualisation=last_actualisation)

#------------------------------------
@app.route('/home/test')
def data():
    car = Car('TWN', 'APAC', 345)
    object,_= get_list_of_sessions()
    return jsonify(object[0])

#------------------------------------
if __name__ == '__name__':
    app.run(DEBUG=True)

