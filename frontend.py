import streamlit as st
import requests

st.set_page_config(page_title="BablAI", page_icon=":robot:", layout="wide")

st.title("Tweet like predictor")

if "messages" not in st.session_state:
    st.session_state.messages = []

tweet = st.text_input("Enter a tweet to predict its like count:")
followers = st.number_input("Enter the number of followers:", min_value=0, step=1)
following = st.number_input("Enter the number of accounts you are following:", min_value=0, step=1)

res = requests.post("http://localhost:5000/chat", json={"chat_history": st.session_state.messages})
'''
user_input = st.chat_input("Ask anything...")

if user_input:
    
    if st.session_state.messages and st.session_state.messages[-1]['role'] == 'user':
        # Club with previous user message
        st.session_state.messages[-1]['content'] += "\n\n" + user_input
        interrupt = True
        for msg in st.session_state.messages:
            role = "You" if msg['role'] == 'user' else "assistant"
            st.chat_message(role).write(msg['content'])
    else:

        st.session_state.messages.append({"role": "user", "content": user_input})
        interrupt = False
        for msg in st.session_state.messages:
            role = "You" if msg['role'] == 'user' else "assistant"
            st.chat_message(role).write(msg['content'])

    try:
        res = requests.post("http://localhost:5000/chat", json={"chat_history": st.session_state.messages})
        reply = res.json().get("reply", "(No response)")
        finished = res.json().get("finished", True)     
            
    except Exception as e:
        reply = "Error: could not reach the server. please try again"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("Bot").write(reply)
    '''

