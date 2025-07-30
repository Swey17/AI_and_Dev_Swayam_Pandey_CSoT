import streamlit as st
import requests

st.title("Generate Tweet")

st.session_state.input_data = {}

prompt = st.text_input("What is the tweet about?")

formality = st.slider("Formality", 0, 10, 5)
wittiness = st.slider("Wittiness", 0, 10, 5)
boldness = st.slider("Boldness", 0, 10, 5)

emoji_usage = st.radio("Emoji Usage", ['None', 'Low', 'Medium', 'High'], index=1, horizontal=True)
hashtag_usage = st.radio("Hashtag Usage", ['None', 'Low', 'Medium', 'High'], index=1, horizontal=True)


prompt2 = st.text_input("Any other instructions?")

if st.button("Generate"):
    input_data = {
        "prompt": prompt,
        "formality": formality,
        "wittiness": wittiness,
        "boldness": boldness,
        "emoji_usage": emoji_usage,
        "hashtag_usage": hashtag_usage,
        "prompt2": prompt2
    }
    st.session_state.input_data = input_data

    if not prompt:
        st.error("Please fill in the prompt.")
    else:
        try:
            res = requests.post("http://127.0.0.1:5000/generate", json=input_data)
            st.session_state.generated_tweet = res.json().get("generated_tweet", "(No response)")
            
        except Exception as e:
            reply = f"Error: {e}"
            st.error(reply)
try: 
    st.success(f"Generated Tweet: {st.session_state.generated_tweet}")
    if st.session_state.generated_tweet == "(No response)":
        st.error(res.json().get("error", "No error message provided"))
    tweet = st.session_state.generated_tweet
except: pass

st.text("for predicting likes:")
followers = st.number_input("Enter the number of followers:", min_value=0, step=1)
following = st.number_input("Enter the number of accounts you are following:", min_value=0, step=1)
media_type = st.selectbox("Which media will you add", ['None', 'Photo', 'Video', 'Gif'])

if st.button("Predict Likes"):
    input_data = {
        "tweet": tweet,
        "followers": followers,
        "following": following,
        "media_type": media_type
    }
    st.session_state.input_data = input_data

    try:
        res = requests.post("http://localhost:5000/predict", json=input_data)
        likes = res.json().get("predicted_likes", "(No response)")
        st.success(f"Predicted likes: {likes}")
        if likes == "(No response)":
            st.error(res.json().get("error", "No error message provided"))

    except Exception as e:
        reply = f"Error: {e}"
        st.error(reply)



