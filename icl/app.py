from predict import IndianismPredictor
import streamlit as st
from datetime import datetime

# Instantiate predictor
predictor = IndianismPredictor()

# Streamlit app
st.set_page_config(page_title="Indianism Predictor", layout="centered")

# Custom CSS for modern UI
st.markdown(
    """
    <style>
    .stTextInput label {
        font-size: 18px;
        font-weight: 600;
        color: #4f4f4f;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .output-box {
        background-color: #ffffff;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        font-size: 16px;
        font-family: 'Roboto', sans-serif;
        color: #333333;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #888888;
        font-family: 'Roboto', sans-serif;
    }
    .example-box {
        background-color: #f0f8ff;
        border: 1px dashed #4CAF50;
        padding: 10px;
        border-radius: 8px;
        font-size: 14px;
        color: #333333;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App header
st.title("🌐 Indianism Predictor")
st.caption("A tool to identify Indianisms in English sentences.")

# App description
st.markdown(
    """
    Indianisms are words or phrases characteristic of Indian English, often influenced by local languages or culture. 
    These may be misinterpreted or misunderstood by native English speakers. They are not general grammatical errors 
    but culturally specific usages. Identifying and avoiding Indianisms is important in career skills as it helps 
    communicate more clearly and effectively in global professional environments. Miscommunications arising from 
    Indianisms can lead to misunderstandings, especially in multicultural workplaces.
    """
)

# Example section
st.markdown(
    """
    <div class='example-box'>
    <strong>Examples of Indianisms:</strong>
    <ul>
        <li>"Do the needful"</li>
        <li>"Passing out from college" (instead of graduating)</li>
        <li>"Out of station" (instead of out of town)</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Input box
sentence = st.text_input("Enter a sentence to analyze:", placeholder="Type your sentence here...")

# Predict button
if st.button("Predict Indianism"):
    if sentence:
        with st.spinner("Analyzing..."):
            response = predictor.predict_indianism(sentence)
        # Display the output
        st.markdown(
            f"<div class='output-box'><strong>Prediction:</strong> {response}</div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Please enter a sentence to analyze.")

# Additional feature: Show current time
st.markdown(f"<div class='footer'>Checked at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
