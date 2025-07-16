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
        data['media_type'],
        data['hour'],
        data['sentiment']
    ]).reshape(1, -1)
    prediction = data['word_count']
#    prediction = model.predict(features)[0]
    return jsonify({'predicted_likes': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)

'''
import groq
import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS

groqapikey = "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"
groq_client = groq.Client(api_key=groqapikey)


app = Flask(__name__) # Allow Streamlit (frontend) to call it
CORS(app) # Allow all domains to access this API


@app.route('/chat', methods=['POST'])


def chat():
    chat_history = request.json.get("chat_history", [])

    if False:
        pass

    else:

        messages=[
                {   "role": "system",
                    "content": "You are interacting with a student of IIT Delhi. You are a helpful assistant. Be succinct.\
Give answer in a set of paragraphs like you are texting to him/her and each paragraph is a text message."
                    }
                ]

        messages = messages[:] + chat_history

        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            stream=True
        )

        answer = ""

        finished = True

        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
            if answer.endswith("\n\n"):
                finished = False
                break
                
        
        messages.append({"role": "assistant", "content": answer})
        print(messages)
        return jsonify({"reply": answer, "finished": finished})

    

if __name__ == "__main__":
    app.run(port=5000)
'''