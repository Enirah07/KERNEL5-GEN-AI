import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("chatbot_dataset.csv", encoding="latin1")

# Build context
context_text = ""
for _, row in df.head(30).iterrows():
    context_text += f"Q: {row['question']}\nA: {row['answer']}\n"

st.title("KGISL Admission Chatbot")

st.write("This chatbot is currently running in **demo mode** — it won’t crash.")

user_input = st.text_input("Ask something about admissions:")

if st.button("Ask"):
    if user_input:
        # show dummy context answer
        st.write("### Answer:")
        for _, row in df.iterrows():
            if user_input.lower() in row['question'].lower():
                st.write(f"**Q:** {row['question']}")
                st.write(f"**A:** {row['answer']}")
                break
        else:
            st.write("Sorry, I don’t know the answer yet.")
