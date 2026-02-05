import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
import google.generativeai as genai

# Load API key
API_KEY = st.secrets["API_KEY"]

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load dataset
df = pd.read_csv("kgisl_chatbot_dataset.csv")

# Step 1: Find the closest matching Q/A pair
def retrieve_best_match(user_query):
    best_row = None
    best_score = 0

    for _, row in df.iterrows():
        score = fuzz.ratio(user_query.lower(), row["question"].lower())
        if score > best_score:
            best_score = score
            best_row = row

    if best_score < 40:  # no match found
        return None

    return best_row


# Step 2: Send only one matched row to Gemini (prevents API crash)
def ask_gemini(user_query, matched_row):
    prompt = f"""
Act as an official KGiSL admission helpdesk assistant.

Use the following verified information:

Question: {matched_row['question']}
Answer: {matched_row['answer']}

Now respond to this user query:
{user_query}

Your answer must be:
- clean
- helpful
- short and direct
- avoid mentioning dataset, Q, or A
"""

    response = model.generate_content(prompt)
    return response.text


st.title("KGISL Admission Chatbot")

user_input = st.text_input("Ask something about admissions:")

if user_input:
    matched_row = retrieve_best_match(user_input)

    if matched_row is None:
        st.write("### Answer:")
        st.write("Sorry, I don’t have information about that yet.")
    else:
        final_answer = ask_gemini(user_input, matched_row)
        st.write("### Answer:")
        st.write(final_answer)
