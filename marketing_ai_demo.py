import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- SETUP ---
st.set_page_config(page_title="AI Marketing Campaign Generator", page_icon="📈", layout="wide")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- HEADER ---
st.title("📈 AI Marketing Campaign Generator & Analyzer")
st.write("Upload customer data to visualize trends, analyze with AI, and generate personalized marketing content.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload your customer CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df.head())

    # --- CHARTS ---
    st.markdown("### 📈 Data Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top Product Interests**")
        st.bar_chart(df["product_interest"].value_counts())

    with col2:
        st.markdown("**Customers by Region**")
        st.bar_chart(df["region"].value_counts())

    # --- AI TASK ---
    st.markdown("---")
    st.subheader("🧠 AI Marketing Insights")

    task = st.text_area(
        "What would you like the AI to analyze?",
        "Summarize customer interests by region and suggest personalized marketing strategies."
    )

    if st.button("Generate Insights"):
        with st.spinner("Analyzing data with AI..."):
            data_sample = df.head(5).to_dict(orient="records")

            prompt = f"""
            You are a senior marketing data analyst.
            Here is a sample of customer data: {data_sample}

            Task: {task}

            Return a concise, structured marketing report highlighting trends, opportunities, and recommended campaign ideas.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional marketing strategist."},
                        {"role": "user", "content": prompt}
                    ]
                )
                insights = response.choices[0].message.content
                st.write(insights)

                # Save report for download
                with open("marketing_report.txt", "w") as f:
                    f.write(insights)

                with open("marketing_report.txt", "r") as f:
                    st.download_button("⬇️ Download Report", f, file_name="marketing_report.txt")

            except Exception as e:
                st.error(f"Error: {e}")

    # --- MARKETING CONTENT GENERATOR ---
    st.markdown("---")
    st.subheader("🎯 AI Campaign Copy Generator")

    tone = st.selectbox("Choose campaign tone:", ["Friendly", "Excited", "Professional", "Persuasive"])
    platform = st.selectbox("Select platform type:", ["Email", "Instagram", "LinkedIn", "Ad Headline"])
    variant_count = st.slider("Number of variants", 1, 3, 2)

    if st.button("Generate Marketing Copy"):
        with st.spinner("Creating marketing copy..."):
            sample = df.head(3).to_dict(orient="records")

            content_prompt = f"""
            You are an AI marketing copywriter.
            Here is some customer data: {sample}
            Create {variant_count} different {platform} campaign messages in a {tone.lower()} tone.

            Output in JSON with fields:
            {{
              "variant_number": n,
              "subject_or_headline": "",
              "body": "",
              "hashtags": []
            }}
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert ad copywriter."},
                        {"role": "user", "content": content_prompt}
                    ]
                )
                copy = response.choices[0].message.content
                st.write(copy)

            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.info("👆 Upload a CSV file to begin.")

