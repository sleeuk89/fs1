import streamlit as st
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Function to scrape Google's Featured Snippet using Selenium (UK-based)
def get_featured_snippet(keyword):
    # Set up Chrome options for Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without opening the browser window)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    
    # Path to your ChromeDriver (update the path if necessary)
    driver_path = '/path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    
    # UK Google domain for SERP
    url = f"https://www.google.co.uk/search?q={keyword}"
    
    try:
        driver.get(url)
        
        # Wait for Featured Snippet or the first search result to load
        wait = WebDriverWait(driver, 10)
        try:
            # Wait until the snippet appears (this selector may need tweaking)
            snippet_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.BNeawe.iBp4i.AP7Wnd"))
            )
            snippet = snippet_element.text
        except:
            snippet = None

        # If not found, try another selector for other snippet formats
        if not snippet:
            try:
                snippet_element = driver.find_element(By.CSS_SELECTOR, "div.g span.BNeawe.s3v9rd.AP7Wnd")
                snippet = snippet_element.text
            except:
                snippet = None
        
        if snippet:
            return snippet
        else:
            st.warning("No Featured Snippet found for this keyword in Google UK.")
            return None

    except Exception as e:
        st.error(f"Error fetching the Google page: {e}")
        return None
    finally:
        driver.quit()  # Close the browser

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
            st.warning("No Featu
