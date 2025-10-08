import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
import json, re

# --- SETUP ---
st.set_page_config(page_title="AI Marketing Campaign Generator", page_icon="💡")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- HEADER ---
st.title("💼 AI Marketing Campaign Generator")
st.write("Upload any customer dataset to visualize patterns and generate AI-powered marketing content.")

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

    # --- CONTENT GENERATION CONTROLS ---
    st.markdown("### ✉️ Content Generation Controls")
    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        num_to_generate = st.slider("How many messages?", min_value=1, max_value=10, value=3, step=1)
    with colB:
        tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Urgent"], index=0)
    with colC:
        channel = st.selectbox("Channel", ["Email", "SMS", "Headline"], index=0)

    # --- AI MARKETING INSIGHTS ---
    st.markdown("---")
    st.markdown("## 🤖 AI Marketing Insights")

    candidate_text_cols = [
        "headline", "subject", "title", "offer", "product_interest",
        "notes", "message", "copy", "description"
    ]

    source_col = next((c for c in candidate_text_cols if c in df.columns), None)

    if source_col is None:
        st.info(
            "I couldn’t find a text column to base messages on. "
            "Add a column like 'headline', 'subject', 'title', or 'product_interest' to your CSV."
        )
    else:
        st.caption(f"Using **{source_col}** as the source text.")
        selected_rows = df[source_col].dropna().astype(str).head(50).tolist()

        if len(selected_rows) == 0:
            st.warning(f"No usable text found in column **{source_col}**.")
        else:
            if st.button("🚀 Generate Campaign Ideas"):
                with st.spinner("Analyzing and creating messages..."):
                    try:
                        api_key = os.getenv("OPENAI_API_KEY")
                        if not api_key:
                            st.error("No OpenAI API key found. Add OPENAI_API_KEY to your environment or Streamlit secrets.")
                        else:
                            client = OpenAI(api_key=api_key)

                            sample_bullets = "\n".join([f"- {txt}" for txt in selected_rows[:8]])

                            system = (
                                "You are a creative marketing strategist. "
                                "Write short, engaging content tailored for the specified channel and tone."
                            )

                            user = (
                                f"Channel: {channel}\n"
                                f"Tone: {tone}\n"
                                f"Write {num_to_generate} {channel.lower()} message(s) based on these examples:\n"
                                f"{sample_bullets}\n\n"
                                "Return valid JSON in this shape:\n"
                                '{ "items": [ { "subject": "", "preheader": "", "body": "" } ] } '
                                "If channel is SMS, omit subject/preheader and keep body <= 160 chars. "
                                "If channel is Headline, return {\"headline\": \"\"}."
                            )

                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": system},
                                    {"role": "user", "content": user},
                                ],
                                temperature=0.7,
                            )

                            raw = resp.choices[0].message.content
                            match = re.search(r"\{.*\}", raw, re.S)
                            json_text = match.group(0) if match else raw
                            data = json.loads(json_text)
                            items = data.get("items", [])

                            if not items:
                                st.warning("No messages returned. Here’s the raw output:")
                                st.code(raw)
                            else:
                                for i, item in enumerate(items, 1):
                                    with st.container(border=True):
                                        st.markdown(f"**Variant {i}**")
                                        if channel == "Headline":
                                            st.write(item.get("headline", ""))
                                        else:
                                            subj = item.get("subject")
                                            pre = item.get("preheader")
                                            body = item.get("body", "")
                                            if subj: st.write(f"**Subject:** {subj}")
                                            if pre: st.write(f"**Preheader:** {pre}")
                                            st.write(body)
                    except Exception as e:
                        st.exception(e)
else:
    st.info("⬆️ Please upload a CSV file to begin.")
