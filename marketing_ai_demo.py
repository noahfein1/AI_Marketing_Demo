import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- SETUP ---
st.set_page_config(page_title="AI Marketing Campaign Generator", page_icon="💡")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- HEADER ---
st.title("💼 AI Marketing Campaign Generator")
st.write("Upload any customer dataset to visualize patterns and generate AI marketing insights.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # --- DYNAMIC CHARTS ---
    st.markdown("## 📊 Data Overview")

    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    col1, col2 = st.columns(2)

    with col1:
        if categorical_cols:
            st.markdown("**Top Categorical Insights**")
            col_choice = st.selectbox("Select a categorical column:", categorical_cols)
            st.bar_chart(df[col_choice].value_counts())
        else:
            st.warning("No categorical columns found in this dataset.")

    with col2:
        if numeric_cols:
            st.markdown("**Numeric Column Overview**")
            num_choice = st.selectbox("Select a numeric column:", numeric_cols)
            st.line_chart(df[num_choice])
        else:
            st.warning("No numeric columns found in this dataset.")

    # --- AI MARKETING INSIGHTS ---
    st.markdown("---")
    st.markdown("## 🤖 AI Marketing Insights")

    task = st.text_area("Describe what you want the AI to analyze or create (e.g. 'Generate campaign ideas targeting athletes in Canada'):")

    if st.button("🚀 Generate AI Insight"):
        with st.spinner("Analyzing data and generating insight..."):
            try:
                # Combine prompt with first few rows of data
                prompt = f"""
                You are an AI marketing strategist.
                Analyze this dataset and provide insights or campaign ideas based on the data below.

                Data sample:
                {df.head(10).to_string()}

                Task:
                {task}
                """
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt
                )
                st.success("✅ Insight Generated!")
                st.markdown("### 📈 Result")
                st.write(response.output_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("⬆️ Please upload a CSV file to begin.")
