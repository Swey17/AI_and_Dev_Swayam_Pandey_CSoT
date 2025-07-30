from flask import Flask, request, jsonify
import joblib
import numpy as np
from textblob import TextBlob
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
import emoji


load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model = joblib.load('model_2_xg.pkl')
        model.set_params(device='cpu')
        encoder_media_type = joblib.load('encoder_media_type_2_xg.pkl')

        data = request.get_json()
        char_count = len(data['tweet'])
        analysis = TextBlob(data['tweet'])
        sentiment_polarity = analysis.sentiment.polarity

        def count_emojis(text):
            return sum(1 for char in text if char in emoji.EMOJI_DATA)

        emoji_count = count_emojis(data['tweet'])
        hashtag_count= data['tweet'].count(r'#\w+')

        media_type_encoded = encoder_media_type.transform(np.array([data['media_type']]).reshape(1, -1))

        
        features = np.hstack([
            np.array([char_count, sentiment_polarity, emoji_count, hashtag_count, data['followers'], data['following']]),
            media_type_encoded[0]
        ]).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({'predicted_likes': int(prediction)})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    gemini_api_key = os.getenv('gemini_api_key')
    try:
        prompt = request.json.get('prompt', '')*10
        formality = request.json.get('formality', 5)*10
        wittiness = request.json.get('wittiness', 5)*10
        boldness = request.json.get('boldness', 5)*10
        emoji_usage = request.json.get('emoji_usage')
        hashtag_usage = request.json.get('hashtag_usage')
        prompt2 = request.json.get('prompt2', '')

        # using gemini to generate tweet
        system_prompt = "You are a helpful assistant that generates tweets based on the user's input. \
            The tweet should be engaging, concise, and suitable for Twitter's character limit. \
            The user will provide a prompt and some parameters to guide the tweet generation." 
        user_prompt = f"'What is the tweet about?': '{prompt}', 'Formality': {formality}%, 'Wittiness': {wittiness}%, 'Boldness': {boldness}%, \
            'Emoji Usage': '{emoji_usage}', 'Hashtag Usage': '{hashtag_usage}', 'Any other instructions?': '{prompt2}'"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            config=types.GenerateContentConfig(system_instruction=system_prompt),
            contents=user_prompt
        )

        generated_tweet = response.text
        return jsonify({'generated_tweet': generated_tweet})
    
    except Exception as e:
        print(f"Error during tweet generation: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)