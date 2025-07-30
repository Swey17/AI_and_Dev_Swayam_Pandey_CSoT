import streamlit as st
import requests
from flask import jsonify

st.set_page_config(page_title="TweetLikePredictor", page_icon=":robot:", layout="wide")

st.title("Tweet like predictor")

st.session_state.input_data = {}

tweet = st.text_input("Enter the tweet")
# followers = st.number_input("Enter the number of followers:", min_value=0, step=1)
# following = st.number_input("Enter the number of accounts you are following:", min_value=0, step=1)
media_type = st.selectbox("Which media will you add", ['None', 'Photo', 'Video', 'Gif'])
username = st.text_input("Enter username")

if st.button("Predict"):
    input_data = {
        "tweet": tweet,
        # "followers": followers,
        # "following": following,
        "media_type": media_type,
        "username": username
    }
    st.session_state.input_data = input_data

    if not tweet or not username:
        st.error("Please fill in all fields.")
    else:
        st.write("Processing...")
        try:
            res = requests.post("http://localhost:5000/predict", json=input_data)
            likes = res.json().get("predicted_likes", "(No response)")
            st.success(f"Predicted likes: {likes}")

        except Exception as e:
            reply = "Error: could not reach the server. please try again"
            st.error(reply)