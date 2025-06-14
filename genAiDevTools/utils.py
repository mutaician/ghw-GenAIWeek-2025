from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2") 