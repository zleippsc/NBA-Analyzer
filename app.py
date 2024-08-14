from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

model = tf.keras.models.load_model('nba-model.keras')
df = pd.read_csv('playerdata.csv')

def makePrediction(players, season) -> int:
    data = np.array([[0.0 for x in range(91)]])
    data[0][0] = season
    for i in range(5):
        player = df.loc[df['player_name'] == players[i]].loc[df['season'] == season]
        for k in range(18):
            data[0][i*18+k+1] = player.iloc[0, k+2]
    pred = round(model.predict(data)[0][0], 3)
    return pred

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = data['input']
    prediction = makePrediction(input_data, 2022)
    response = {'prediction': prediction.tolist()}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
