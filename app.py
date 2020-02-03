from flask import Flask, jsonify, render_template

app = Flask(__name__)




@app.route('/')
@app.route('/home')
def home():
    data = {
        'name': 'Bart',
        'age': '19',
    }
    return render_template('index.html')




if __name__ == '__name__':
    app.run()