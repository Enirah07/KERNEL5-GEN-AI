import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
import google.generativeai as genai

# Load API Key
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load CSV dataset
df = pd.read_csv("kgisl_chatbot_dataset.csv")

# Function to get best dataset answer
def get_best_dataset_answer(user_query):
    best_match = None
    best_score = 0

    for _, row in df.iterrows():
        score = fuzz.ratio(user_query.lower(), row["question"].lower())

        if score > best_score:
            best_score = score
            best_match = row

    if best_score >= 60:  # threshold
        return best_match["answer"]

    return None  # no good match

# Function to ask Gemini only when needed
def ask_gemini(user_query):
    prompt = f"""
You are an admission helpdesk assistant for KGiSL College.
Answer clearly about admissions, fees, hostel, courses, or facilities.

User question: {user_query}

Give a short and accurate answer.
"""
    response = model.generate_content(prompt)
    return response.text


# Streamlit UI
st.title("KGISL Admission Chatbot")
st.write("This chatbot is currently running and answering real queries.")

user_input = st.text_input("Ask something about admissions:")

if user_input:
    # First try dataset
    dataset_answer = get_best_dataset_answer(user_input)

    if dataset_answer:
        st.write("### Answer:")
        st.write(dataset_answer)
    else:
        # Ask Gemini only if dataset cannot answer
        gemini_answer = ask_gemini(user_input)
        st.write("### Answer:")
        st.write(gemini_answer)
