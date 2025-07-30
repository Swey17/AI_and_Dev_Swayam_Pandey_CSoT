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
            generated_tweet = res.json().get("generated_tweet", "(No response)")
            st.success(f"Generated Tweet: {generated_tweet}")
            if generated_tweet == "(No response)":
                st.error(res.json().get("error", "No error message provided"))

        except Exception as e:
            reply = f"Error: {e}"
            st.error(reply)