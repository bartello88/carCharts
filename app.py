from flask import Flask, jsonify, render_template
import yaml
app = Flask(__name__)




@app.route('/')
@app.route('/home')
def home():
    regions = loadYaml()
    return render_template('index.html', regions=regions)




if __name__ == '__name__':
    app.run()




def loadYaml():
    with open('config.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        regions = data['config']['regions']
        return regions