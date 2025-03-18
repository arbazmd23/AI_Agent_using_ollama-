import streamlit as st
import requests
import json

def generate_survey_questions(product_name, product_description, product_stage, target_audience, industry, survey_purpose):
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint
    
    prompt = f"""
    ### 🧠 Role:
    You are an **expert product researcher and survey question generator** who adapts to any product or industry.

    ---
    ### 🎯 Task:
    Generate **10 highly specific, non-generic survey questions** tailored **exclusively** to the product below. 

    ---
    ### ✅ Product Details:
    - **Product Name:** {product_name}
    - **Product Description:** {product_description}
    - **Product Stage:** {product_stage}
    - **Target Audience:** {target_audience}
    - **Industry:** {industry}
    - **Survey Purpose:** {survey_purpose}

    ---
    ### 🔍 What I want:
    1. **Deep, Insightful Questions Only** (No surface-level questions like "Would you recommend this product?")
    2. Questions that **force the user to give feedback on actual product functionality, usability, and performance.**
    3. **Focus on unique pain points, user experience, performance metrics, and user satisfaction.**
    4. **Avoid repetitive or generic AI-related questions.**
    5. Each question should **target a different aspect of the product's value.**

    ---
    ### 🎯 Structure:
    - 4 Questions on **Product Performance & Features**
    - 3 Questions on **User Experience & Usability**
    - 2 Questions on **Target Audience Needs & Market Fit**
    - 1 Question on **Future Improvements**
    """

    data = {
        "model": "llama3.2",  # Change model if needed (e.g., llama2, phi)
        "prompt": prompt,
        "temperature": 0.8,
        "max_tokens": 800,
        "stream": False
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        survey_questions = result['response']
        questions = [line for line in survey_questions.split("\n") if line.strip() and line[0].isdigit()]
        return questions
    else:
        return [f"Error: {response.status_code} - {response.text}"]

# Streamlit UI
st.title("AI-Powered Survey Question Generator")
st.write("Enter your product details below to generate a custom survey.")

# User Input Fields
product_name = st.text_input("Product Name", "")
product_description = st.text_area("Product Description", "")
product_stage = st.selectbox("Product Stage", ["Pre-Launch", "Beta", "Launched", "Scaling"], index=0)
target_audience = st.text_input("Target Audience", "")
industry = st.text_input("Industry", "")
survey_purpose = st.text_input("Survey Purpose", "")

if st.button("Generate Survey Questions"):
    with st.spinner("Generating questions this process may take some time..."):
        questions = generate_survey_questions(product_name, product_description, product_stage, target_audience, industry, survey_purpose)
        
        st.subheader("Generated Survey Questions:")
        for q in questions:
            st.write(q)
