# ===============================
# AI Marketing Campaign Generator
# ===============================

import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- SETUP ---
st.set_page_config(page_title="AI Marketing Demo", page_icon="🤖", layout="wide")
load_dotenv()

# Load OpenAI API key from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ No OpenAI API key found. Please add it to your .env file as OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Choose a feature:", ["📈 Data Overview", "✉️ Email Generator", "💡 Campaign Ideas"])

st.sidebar.markdown("---")
st.sidebar.info("Upload your CSV file with customer data to get started!")

# --- FILE UPLOAD ---
uploaded_file = st.sidebar.file_uploader("📤 Upload Customer CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ============ PAGE 1: DATA OVERVIEW ============
    if page == "📈 Data Overview":
        st.title("📊 Customer Data Overview")
        st.dataframe(df.head())

        # --- Charts ---
        st.markdown("### 🔍 Data Insights")
        col1, col2 = st.columns(2)

        with col1:
            if "product_interest" in df.columns:
                st.markdown("**Top Product Interests**")
                st.bar_chart(df["product_interest"].value_counts())
            else:
                st.warning("⚠️ Column 'product_interest' not found in the dataset.")

        with col2:
            if "region" in df.columns:
                st.markdown("**Customers by Region**")
                st.bar_chart(df["region"].value_counts())
            else:
                st.warning("⚠️ Column 'region' not found in the dataset.")

    # ============ PAGE 2: EMAIL GENERATOR ============
    elif page == "✉️ Email Generator":
        st.title("✉️ AI Email Generator")
        st.write("Generate personalized marketing messages based on your uploaded customer data.")

        col1, col2, col3 = st.columns(3)
        with col1:
            num_messages = st.slider("How many emails?", 1, 5, 3)
        with col2:
            tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Persuasive"])
        with col3:
            channel = st.selectbox("Channel", ["Email", "SMS", "Social Media"])

        if st.button("📧 Generate Emails"):
            with st.spinner("Generating emails..."):
                prompt = f"""
                Generate {num_messages} {tone.lower()} {channel.lower()} messages for customers based on this data:
                {df.head(5).to_string(index=False)}
                Each message should sound natural and fit the tone.
                """
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(f"✅ Generated {num_messages} {channel} messages!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ============ PAGE 3: CAMPAIGN IDEAS ============
    elif page == "💡 Campaign Ideas":
        st.title("💡 AI Campaign Idea Generator")
        st.write("Get creative campaign ideas, slogans, or taglines tailored to your audience data.")

        st.markdown("---")
        num_ideas = st.slider("How many ideas?", 1, 5, 3)
        style = st.selectbox("Style", ["Creative", "Professional", "Playful", "Inspirational"])

        if st.button("🚀 Generate Campaign Ideas"):
            with st.spinner("Brainstorming ideas..."):
                prompt = f"""
                Generate {num_ideas} {style.lower()} marketing campaign ideas based on this dataset:
                {df.head(5).to_string(index=False)}
                Provide short, catchy taglines or concepts.
                """
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(f"✅ Generated {num_ideas} campaign ideas!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.info("👆 Upload a CSV file in the sidebar to begin.")
