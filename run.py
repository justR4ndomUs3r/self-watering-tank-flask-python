from flask import Flask, render_template
from flask_socketio import  SocketIO, emit
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import zbiornik

app = Flask(__name__)
app.config['SECRET_KEY'] = '123' # change it later X D
app.config['DEBUG'] = True
socketio = SocketIO(app, ping_timeout=600)



@socketio.on('calculate')
def handle_event(json):
    print(json['deszcz'][0])
    data = zbiornik.sym(float(json['z1']), float(json['z2']), float(json['z3']), json['deszcz'],float(json['hm']), float(json['hd']), float(json['pow']), float(json['Tpp']), float(json['kpp']), float(json['Tdd']), float(json['Tii']), float(json['Um']), float(json['Qm']))
    print("ELO")
    emit('done', data)


@app.route('/')
def index():
    data = []
    return render_template('index.html', data=data)

if __name__ == '__main__':
    socketio.run(app)