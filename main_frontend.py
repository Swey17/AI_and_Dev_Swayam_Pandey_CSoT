import streamlit as st

# Define the pages
predict_front = st.Page("predict_front.py", title="Predict Likes", icon="❤️")
generate_front = st.Page("generate_front.py", title="Generate Tweet", icon="✏️")

# Set up navigation
pg = st.navigation([predict_front, generate_front])

# Run the selected page
pg.run()