import streamlit as st
import joblib
import numpy as np
from feature import extract_url_features

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load('randomForest.pkl')

classifier = load_model()

st.title("Phishing URL Detection")

# Create a form for URL input
with st.form(key='url_form'):
    url_input = st.text_input("Enter the URL:")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if url_input:
        with st.spinner('Processing...'):
            # Extract features from the new data
            features = extract_url_features(url_input)
            new_data = np.array(features).reshape(1, -1)

            # Predict the class for the new data
            prediction = classifier.predict(new_data)

        # Determine the result based on the prediction and display it in color
        if prediction[0] == 1:
            result = "Phishy URL"
            st.write(f"**Input URL:** {url_input}")
            st.write(f"**Prediction:** :red[{result}]")
        else:
            result = "Legitimate URL"
            st.write(f"**Input URL:** {url_input}")
            st.write(f"**Prediction:** :green[{result}]")
    else:
        st.write("Please enter a URL.")
