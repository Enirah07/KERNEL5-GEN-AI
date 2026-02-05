import streamlit as st
import pandas as pd
import google.generativeai as genai

API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

df = pd.read_csv("chatbot_dataset.csv", encoding="latin1")

context_text = ""
for _, row in df.iterrows():
    context_text += f"Q:{row['question']}\nA:{row['answer']}\n"

def ask_gemini(question):
    prompt = f"{context_text}\nUser question: {question}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

st.title("KGISL Admission Chatbot")

user_input = st.text_input("Ask something about admission:")

if st.button("Ask"):
    if user_input:
        answer = ask_gemini(user_input)
        st.write("### Chatbot:", answer)
