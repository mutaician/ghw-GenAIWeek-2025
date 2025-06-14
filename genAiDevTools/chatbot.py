import streamlit as st
from utils import load_model

st.title("Creative Story Helper Chatbot")

model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your story prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = model(
        prompt, 
        max_length=100, 
        do_sample=True, 
        temperature=0.7
    )[0]['generated_text']
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        import torch

        # Load sentiment analysis model
        sentiment_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        sentiment_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

        # Analyze sentiment
        inputs = sentiment_tokenizer(response, return_tensors="pt", truncation=True, max_length=512)
        outputs = sentiment_model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment_score = torch.argmax(scores).item()

        # Map sentiment scores to labels
        sentiment_labels = ["Negative", "Neutral", "Positive"]
        sentiment = sentiment_labels[sentiment_score]

        # Display sentiment badge
        sentiment_color = {
            "Positive": "green",
            "Neutral": "blue",
            "Negative": "red"
        }
        st.markdown(f"<div style='margin-top: 10px;'><span style='background-color: {sentiment_color[sentiment]}; color: white; padding: 5px 10px; border-radius: 5px;'>{sentiment}</span></div>", unsafe_allow_html=True)
