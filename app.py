from flask import Flask, jsonify, render_template
import yaml

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

    return render_template('car.html', car=car)



if __name__ == '__name__':
    app.run()


def loadYaml():
    with open('config.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        regions = data['config']['regions']
        cars = { 'us': {'cars':data['cars']['us']},'eu': {'cars':data['cars']['eu']}, 'lam': {'cars':data['cars']['lam']}, 'apac': {'cars':data['cars']['apac']}, 'zaf': {'cars':data['cars']['zaf']}, 'rus&ukr': {'cars':data['cars']['rus&ukr']}}
        return regions, cars
