import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import time

# Streamlit App Setup
st.title("Featured Snippet SEO Content Generator (UK-based)")
st.markdown("""
    This app helps you generate optimised content to win Featured Snippets on Google UK.
    Simply input a target keyword/topic, and the app will scrape Google's Featured Snippet and generate superior content using OpenAI.
""")

# Input field for OpenAI API key and keyword
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
keyword = st.text_input("Enter target keyword/topic:")

# Function to scrape Google's Featured Snippet for a given keyword (UK-based)
def get_featured_snippet(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    # UK Google domain for SERP
    url = f"https://www.google.co.uk/search?q={keyword}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Attempt to find the featured snippet
        snippet = None
        try:
            snippet = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        except AttributeError:
            st.warning("No Featured Snippet found for this keyword in Google UK.")
        return snippet

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the Google page: {e}")
        return None

# Function to generate optimised content using OpenAI
def generate_optimised_content(question, api_key):
    if not api_key:
        st.error("OpenAI API key is required.")
        return None
    
    openai.api_key = api_key
    prompt = f"Generate an SEO-optimised answer for the following question to win a Featured Snippet:\n\n{question}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except openai.error.AuthenticationError:
        st.error("Invalid OpenAI API key.")
        return None
    except openai.error.OpenAIError as e:
        st.error(f"Error generating content: {e}")
        return None

# Main App Workflow
if st.button("Generate Featured Snippet Content"):
    if not openai_api_key or not keyword:
        st.error("Please enter both the OpenAI API key and a keyword.")
    else:
        st.info("Fetching Google's Featured Snippet from Google UK...")
        
        # Get existing featured snippet from Google UK
        snippet = get_featured_snippet(keyword)
        
        if snippet:
            st.success(f"Existing Featured Snippet from Google UK: {snippet}")
            st.write("#### Generate Optimised Content to Beat This Snippet:")
        
            # Use OpenAI to generate optimised content
            with st.spinner('Generating optimised content...'):
                time.sleep(2)  # Simulate some processing time
                optimised_content = generate_optimised_content(keyword, openai_api_key)
                if optimised_content:
                    st.write(f"**Optimised Content:**\n{optimised_content}")
        else:
            st.warning("No Featured Snippet found. Try a different keyword.")
