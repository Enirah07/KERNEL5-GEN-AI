import streamlit as st
import pandas as pd
import google.generativeai as genai

# Use secret API key
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

# Load dataset
df = pd.read_csv("chatbot_dataset.csv", encoding="latin1")

# Build context (limited to first 30 rows)
context_text = ""
for _, row in df.head(30).iterrows():
    context_text += f"Q:{row['question']}\nA:{row['answer']}\n"

def ask_gemini(question):
    prompt = f"{context_text}\nUser question: {question}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("KGISL Admission Chatbot")

user_input = st.text_input("Ask something about admission:")

if st.button("Ask"):
    if user_input.strip():
        try:
            answer = ask_gemini(user_input)
            st.write("### Chatbot:", answer)
        except Exception as e:
            st.error("Error processing request. Please try again.")
