# ===============================
# AI Marketing Campaign Generator
# Advanced Personalization Engine
# ===============================

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# --- SETUP ---
st.set_page_config(page_title="AI Marketing Engine", page_icon="🚀", layout="wide")
load_dotenv()

# Load OpenAI API key from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ No OpenAI API key found. Please add it to your .env file as OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- HELPER FUNCTIONS ---
def analyze_customer_segments(df):
    """Analyze customer data to create behavioral segments"""
    segments = {
        'high_value': df[df['engagement_score'] >= 80],
        'at_risk': df[df['engagement_score'] < 60],
        'new_customers': df[df['customer_segment'] == 'newcomer'],
        'loyal_customers': df[df['loyalty_tier'].isin(['gold', 'platinum'])],
        'international': df[df['country'] != 'US']
    }
    return segments

def calculate_roi_metrics(df):
    """Calculate ROI and conversion metrics"""
    total_customers = len(df)
    high_engagement = len(df[df['engagement_score'] >= 70])
    conversion_rate = (high_engagement / total_customers) * 100 if total_customers > 0 else 0
    
    return {
        'total_customers': total_customers,
        'high_engagement_rate': conversion_rate,
        'avg_engagement': df['engagement_score'].mean(),
        'revenue_potential': df['purchase_history'].sum() * 50  # Assuming $50 avg order value
    }

# --- SIDEBAR NAVIGATION ---
st.sidebar.title(" AI Marketing Engine")
page = st.sidebar.radio("Choose a feature:", [
    "📊 Customer Analytics", 
    "✉️ Email Campaigns", 
    "📱 Social Media Content",
    "🎯 Ad Copy Generator",
    "📈 Performance Dashboard",
    "🔬 A/B Testing Lab"
])

st.sidebar.markdown("---")
st.sidebar.info("🚀 Upload your CSV file with customer data to get started!")

# --- FILE UPLOAD ---
uploaded_file = st.sidebar.file_uploader("📤 Upload Customer CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ============ PAGE 1: CUSTOMER ANALYTICS ============
    if page == "📊 Customer Analytics":
        st.title("📊 Advanced Customer Analytics")
        st.markdown("**AI-Powered Customer Segmentation & Behavioral Analysis**")
        
        # Calculate metrics
        metrics = calculate_roi_metrics(df)
        segments = analyze_customer_segments(df)
        
        # Key Metrics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", metrics['total_customers'])
        with col2:
            st.metric("High Engagement Rate", f"{metrics['high_engagement_rate']:.1f}%")
        with col3:
            st.metric("Avg Engagement Score", f"{metrics['avg_engagement']:.1f}")
        with col4:
            st.metric("Revenue Potential", f"${metrics['revenue_potential']:,.0f}")
        
        st.markdown("---")
        
        # Customer Segmentation Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Customer Segments")
            segment_data = {
                'High Value': len(segments['high_value']),
                'At Risk': len(segments['at_risk']),
                'New Customers': len(segments['new_customers']),
                'Loyal Customers': len(segments['loyal_customers']),
                'International': len(segments['international'])
            }
            
            fig = px.pie(values=list(segment_data.values()), 
                        names=list(segment_data.keys()),
                        title="Customer Distribution by Segment")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Engagement Score Distribution")
            fig = px.histogram(df, x='engagement_score', 
                             title="Customer Engagement Distribution",
                             nbins=20)
            st.plotly_chart(fig, use_container_width=True)
        
        # Geographic Analysis
        st.markdown("### 🌍 Geographic Distribution")
        if 'country' in df.columns:
            country_counts = df['country'].value_counts()
            fig = px.bar(x=country_counts.index, y=country_counts.values,
                        title="Customers by Country")
            st.plotly_chart(fig, use_container_width=True)
        
        # Product Interest Analysis
        st.markdown("### 🛍️ Product Interest Analysis")
        if 'product_interest' in df.columns:
            product_counts = df['product_interest'].value_counts()
            fig = px.bar(x=product_counts.index, y=product_counts.values,
                        title="Top Product Interests")
            st.plotly_chart(fig, use_container_width=True)

    # ============ PAGE 2: EMAIL CAMPAIGNS ============
    elif page == "✉️ Email Campaigns":
        st.title("✉️ AI-Powered Email Campaign Generator")
        st.markdown("**Generate personalized email campaigns tailored to customer segments and behaviors**")
        
        # Campaign Configuration
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Campaign Settings")
            campaign_type = st.selectbox("Campaign Type", [
                "Welcome Series", "Product Recommendations", "Abandoned Cart", 
                "Loyalty Rewards", "Seasonal Promotions", "Re-engagement"
            ])
            
            target_segment = st.selectbox("Target Segment", [
                "All Customers", "High Value", "At Risk", "New Customers", 
                "Loyal Customers", "International"
            ])
            
            tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Persuasive", "Urgent"])
            
        with col2:
            st.markdown("### 📊 Personalization Level")
            personalization_level = st.slider("Personalization Depth", 1, 5, 3)
            
            include_offers = st.checkbox("Include Personalized Offers", True)
            include_urgency = st.checkbox("Add Urgency Elements", False)
            include_social_proof = st.checkbox("Include Social Proof", True)
        
        # Generate Campaign
        if st.button("🚀 Generate AI Email Campaign", type="primary"):
            with st.spinner("AI is crafting your personalized campaign..."):
                # Get target customers
                segments = analyze_customer_segments(df)
                if target_segment == "All Customers":
                    target_df = df
                else:
                    target_df = segments[target_segment.lower().replace(" ", "_")]
                
                # Create personalized prompts for each customer
                personalized_emails = []
                
                for idx, customer in target_df.head(5).iterrows():
                    prompt = f"""
                    Create a personalized {campaign_type.lower()} email for this customer:
                    
                    Customer: {customer['customer_name']}
                    Product Interest: {customer['product_interest']}
                    Location: {customer['region']}, {customer['country']}
                    Engagement Score: {customer['engagement_score']}
                    Loyalty Tier: {customer['loyalty_tier']}
                    Purchase History: {customer['purchase_history']} purchases
                    Preferred Language: {customer['preferred_language']}
                    
                    Requirements:
                    - Tone: {tone.lower()}
                    - Personalization Level: {personalization_level}/5
                    - Include offers: {include_offers}
                    - Add urgency: {include_urgency}
                    - Include social proof: {include_social_proof}
                    
                    Generate a complete email with subject line, body, and call-to-action.
                    """
                    
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        personalized_emails.append({
                            'customer': customer['customer_name'],
                            'email': response.choices[0].message.content
                        })
                    except Exception as e:
                        st.error(f"Error generating email for {customer['customer_name']}: {e}")
                
                # Display results
                st.success(f"✅ Generated {len(personalized_emails)} personalized emails!")
                
                for email_data in personalized_emails:
                    with st.expander(f"📧 Email for {email_data['customer']}"):
                        st.markdown(email_data['email'])

    # ============ PAGE 3: SOCIAL MEDIA CONTENT ============
    elif page == "📱 Social Media Content":
        st.title("📱 AI Social Media Content Generator")
        st.markdown("**Create engaging social media posts tailored to your audience segments**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            platform = st.selectbox("Social Platform", ["Instagram", "Facebook", "Twitter/X", "LinkedIn", "TikTok"])
            content_type = st.selectbox("Content Type", ["Product Showcase", "Behind the Scenes", "User Generated Content", "Educational", "Promotional"])
            target_audience = st.selectbox("Target Audience", ["All", "High Value Customers", "New Customers", "International"])
        
        with col2:
            post_count = st.slider("Number of Posts", 1, 10, 3)
            include_hashtags = st.checkbox("Include Hashtags", True)
            include_cta = st.checkbox("Include Call-to-Action", True)
            emoji_style = st.selectbox("Emoji Style", ["Minimal", "Moderate", "Heavy"])
        
        if st.button("📱 Generate Social Media Content", type="primary"):
            with st.spinner("Creating engaging social content..."):
                prompt = f"""
                Create {post_count} {platform} {content_type.lower()} posts for this audience:
                {df.head(10).to_string(index=False)}
                
                Requirements:
                - Platform: {platform}
                - Content Type: {content_type}
                - Target: {target_audience}
                - Include hashtags: {include_hashtags}
                - Include CTA: {include_cta}
                - Emoji style: {emoji_style}
                
                Make each post unique and engaging for the platform.
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(f"✅ Generated {post_count} {platform} posts!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ============ PAGE 4: AD COPY GENERATOR ============
    elif page == "🎯 Ad Copy Generator":
        st.title("🎯 AI Ad Copy Generator")
        st.markdown("**Generate high-converting ad copy for different platforms and customer segments**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ad_platform = st.selectbox("Ad Platform", ["Google Ads", "Facebook Ads", "Instagram Ads", "LinkedIn Ads", "Twitter Ads"])
            ad_objective = st.selectbox("Campaign Objective", ["Brand Awareness", "Traffic", "Conversions", "Lead Generation", "Sales"])
            target_segment = st.selectbox("Target Segment", ["All Customers", "High Value", "New Customers", "Loyal Customers"])
        
        with col2:
            ad_variations = st.slider("Number of Variations", 1, 5, 3)
            headline_style = st.selectbox("Headline Style", ["Direct", "Question", "Benefit-focused", "Urgency-driven"])
            include_emoji = st.checkbox("Include Emojis", True)
        
        if st.button("🎯 Generate Ad Copy", type="primary"):
            with st.spinner("Crafting high-converting ad copy..."):
                # Get target customers for personalization
                segments = analyze_customer_segments(df)
                if target_segment == "All Customers":
                    target_df = df
                else:
                    target_df = segments[target_segment.lower().replace(" ", "_")]
                
                prompt = f"""
                Create {ad_variations} {ad_platform} ad variations for this customer data:
                {target_df.head(5).to_string(index=False)}
                
                Requirements:
                - Platform: {ad_platform}
                - Objective: {ad_objective}
                - Target: {target_segment}
                - Headline Style: {headline_style}
                - Include emojis: {include_emoji}
                
                For each variation, include:
                1. Headline (30-60 characters)
                2. Description (90-150 characters)
                3. Call-to-Action
                4. Key benefits
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(f"✅ Generated {ad_variations} ad variations!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ============ PAGE 5: PERFORMANCE DASHBOARD ============
    elif page == "📈 Performance Dashboard":
        st.title("📈 Marketing Performance Dashboard")
        st.markdown("**Track campaign performance and ROI metrics**")
        
        # Calculate performance metrics
        metrics = calculate_roi_metrics(df)
        segments = analyze_customer_segments(df)
        
        # Performance Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Revenue Potential", f"${metrics['revenue_potential']:,.0f}")
        with col2:
            st.metric("High-Value Customers", len(segments['high_value']))
        with col3:
            st.metric("At-Risk Customers", len(segments['at_risk']))
        with col4:
            st.metric("Avg Customer Value", f"${metrics['revenue_potential']/metrics['total_customers']:,.0f}")
        
        # Performance Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Customer Value Distribution")
            value_data = df.groupby('loyalty_tier').size()
            fig = px.pie(values=value_data.values, names=value_data.index, 
                        title="Customer Distribution by Loyalty Tier")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Engagement vs Purchase History")
            fig = px.scatter(df, x='engagement_score', y='purchase_history', 
                           color='loyalty_tier', size='purchase_history',
                           title="Customer Engagement vs Purchase History")
            st.plotly_chart(fig, use_container_width=True)
        
        # ROI Analysis
        st.markdown("### 💰 ROI Analysis")
        roi_data = {
            'Segment': ['High Value', 'Standard', 'New Customers', 'At Risk'],
            'Customer Count': [len(segments['high_value']), len(segments['loyal_customers']), 
                             len(segments['new_customers']), len(segments['at_risk'])],
            'Avg Engagement': [
                segments['high_value']['engagement_score'].mean() if len(segments['high_value']) > 0 else 0,
                segments['loyal_customers']['engagement_score'].mean() if len(segments['loyal_customers']) > 0 else 0,
                segments['new_customers']['engagement_score'].mean() if len(segments['new_customers']) > 0 else 0,
                segments['at_risk']['engagement_score'].mean() if len(segments['at_risk']) > 0 else 0
            ]
        }
        
        roi_df = pd.DataFrame(roi_data)
        st.dataframe(roi_df, use_container_width=True)

    # ============ PAGE 6: A/B TESTING LAB ============
    elif page == "🔬 A/B Testing Lab":
        st.title("🔬 AI A/B Testing Lab")
        st.markdown("**Test different content variations and measure performance**")
        
        st.markdown("### 🧪 Create A/B Test")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_type = st.selectbox("Test Type", ["Email Subject Lines", "Ad Headlines", "Social Media Posts", "Call-to-Actions"])
            test_duration = st.selectbox("Test Duration", ["1 week", "2 weeks", "1 month", "3 months"])
            target_metric = st.selectbox("Primary Metric", ["Open Rate", "Click Rate", "Conversion Rate", "Engagement Rate"])
        
        with col2:
            variant_count = st.slider("Number of Variants", 2, 5, 2)
            audience_size = st.slider("Audience Size", 100, 10000, 1000)
            confidence_level = st.selectbox("Confidence Level", ["90%", "95%", "99%"])
        
        if st.button("🔬 Generate A/B Test Variants", type="primary"):
            with st.spinner("Creating test variants..."):
                prompt = f"""
                Create {variant_count} {test_type.lower()} variants for A/B testing:
                
                Customer Data: {df.head(5).to_string(index=False)}
                
                Test Parameters:
                - Type: {test_type}
                - Duration: {test_duration}
                - Metric: {target_metric}
                - Audience: {audience_size} customers
                - Confidence: {confidence_level}
                
                For each variant, provide:
                1. The content
                2. Expected performance
                3. Target audience segment
                4. Success metrics
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(f"✅ Generated {variant_count} test variants!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.info("👆 Upload a CSV file in the sidebar to begin.")
