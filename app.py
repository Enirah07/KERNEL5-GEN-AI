import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load secrets
API_KEY = st.secrets["API_KEY"]

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load dataset
df = pd.read_csv("kgisl_chatbot_dataset.csv")  # your file name

# Build context (NO Q: A:)
context_text = ""
for _, row in df.iterrows():
    context_text += f"{row['question']} -> {row['answer']}\n"

# Function to ask Gemini
def ask_gemini(user_query):
    prompt = f"""
You are an admission helpdesk assistant for KGiSL College.
Use ONLY the following knowledge to answer:

{context_text}

User question: {user_query}

Answer clearly and directly. Do NOT include 'Q:' or 'A:' in your answer.
Do NOT say you don't know unless nothing is related.
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("KGISL Admission Chatbot")
st.write("This chatbot is currently running and answering real queries.")

user_input = st.text_input("Ask something about admissions:")

if user_input:
    answer = ask_gemini(user_input)
    st.write("### Answer:")
    st.write(answer)
