from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
#model = joblib.load('like_predictor.pkl')

@app.route('/')
def home():
    return "API is running."


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([
        data['word_count'],
        data['char_count'],
        data['has_media'],
        data['hour'],
        data['sentiment']
    ]).reshape(1, -1)
    prediction = data['word_count']
#    prediction = model.predict(features)[0]
    return jsonify({'predicted_likes': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)