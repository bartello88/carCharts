from flask import Flask, jsonify, render_template
import yaml
app = Flask(__name__)




@app.route('/')
@app.route('/home')
def home():
    regions = loadYaml()
    return render_template('index.html', regions=regions)

@app.route('/home/<region>')
def region(region):

    return render_template('region.html', region=region)

if __name__ == '__name__':
    app.run()




def loadYaml():
    with open('config.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        regions = data['config']['regions']
        return regions