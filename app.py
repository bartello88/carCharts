from flask import Flask, jsonify, render_template, jsonify
import yaml
from car import Car
from data import get_data, get_list_of_sessions

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    regions, cars = loadYaml()
    return render_template('index.html', regions=regions, )


@app.route('/home/<region>')
def region(region):
    regions, cars = loadYaml()
    carss = ["Audi", "BMW", "VW"]
    return render_template('region.html', region=region, cars=cars, carss=carss)


@app.route('/home/<region>/<car>')
def car(region, car):
    object = get_list_of_sessions()
    car_data = None
    for cars in object:
        if cars['car_name'] == car:
            print(cars)
            car_data = cars
    return render_template('car.html', car=car, car_data=car_data, region = region)

#------------------------------------
@app.route('/home/test')
def data():
    car = Car('TWN', 'APAC', 345)
    object = get_list_of_sessions()
    return jsonify(object[3])

#------------------------------------
if __name__ == '__name__':
    app.run()


def loadYaml():
    with open('config.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        regions = data['config']['regions']
        cars = {'us': {'cars': data['cars']['us']}, 'eu': {'cars': data['cars']['eu']},
                'lam': {'cars': data['cars']['lam']}, 'apac': {'cars': data['cars']['apac']},
                'zaf': {'cars': data['cars']['zaf']}, 'rus&ukr': {'cars': data['cars']['rus&ukr']}}
        return regions, cars
