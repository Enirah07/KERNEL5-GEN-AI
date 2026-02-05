import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

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

    if best_score >= 55:  # threshold to accept match
        return best_match["answer"]

    return "Sorry, I don’t have information about that yet."

# Streamlit UI
st.title("KGISL Admission Chatbot")
st.write("This chatbot is currently running and answering real queries.")

user_input = st.text_input("Ask something about admissions:")

if user_input:
    answer = get_best_dataset_answer(user_input)
    st.write("### Answer:")
    st.write(answer)
