import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config
st.set_page_config(page_title="HomeDistribution Attrition & Dashboard", layout="wide")

# Data Paths
DATA_PATH = r'c:\Users\vaibh\Downloads\IITM_AMU\IIT_M\BDM stuff\project\My Project\End Term\Clean and Transformed Data'
PERF_FILE = os.path.join(DATA_PATH, 'Contractor Performance Data.xlsx')

@st.cache_data
def load_data():
    # Load Contractor Performance
    df = pd.read_excel(PERF_FILE, sheet_name='Cleaned')
    # Clean Column Names (removing rupee symbol if present)
    df.columns = [c.replace(' (₹)', '').replace('(₹)', '').strip() for c in df.columns]
    
    # Load End Customer Sales for CLV
    sales_df = pd.read_excel(os.path.join(DATA_PATH, 'SalesData (Apr-24 - Mar-25).xlsx'), sheet_name='Cleaned')
    ec_df = sales_df[sales_df['Buyer Role'] == 'End Customer'].copy()
    
    # Restoring Contractor Risk Score
    if 'At-Risk Score' not in df.columns:
        sales = df['Sales Target Hit']
        comm = df['Contractor Comission']
        ratio = sales / (comm + 1)
        df['At-Risk Score'] = 1 - ( (ratio - ratio.min()) / (ratio.max() - ratio.min()) )
        df['At-Risk Score'] = (df['At-Risk Score'] * 100).round(2)

    # Calculate CLV (Simplified RFM approach)
    clv_data = ec_df.groupby('Buyer Name').agg({
        'Amount (₹)': 'sum',
        'Sale ID.': 'count',
        'Date': lambda x: (pd.to_datetime('today') - pd.to_datetime(x).max()).days
    }).rename(columns={'Amount (₹)': 'Monetary', 'Sale ID.': 'Frequency', 'Date': 'Recency'})
    
    # Simple CLV Score = (Monetary * Frequency) / (Recency + 1)
    clv_data['CLV_Score'] = (clv_data['Monetary'] * clv_data['Frequency']) / (clv_data['Recency'] + 1)
    clv_data = clv_data.sort_values('CLV_Score', ascending=False)
    
    return df, clv_data

try:
    df, clv_df = load_data()
    
    st.title("🏗️ Contractor Retention & Performance Dashboard")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("Filter & Analysis")
    contractor_list = ["All Contractors"] + list(df['Name'].unique())
    selected_contractor = st.sidebar.selectbox("Select Individual Contractor", contractor_list)
    
    commission_adj = st.sidebar.slider("Simulate Commission Adjustment (%)", -5.0, 5.0, 0.0, 0.1)

    # Main Metrics
    if selected_contractor == "All Contractors":
        c_df = df
        st.subheader("Global Contractor Overview")
    else:
        c_df = df[df['Name'] == selected_contractor]
        st.subheader(f"Performance Report: {selected_contractor}")

    col1, col2, col3, col4 = st.columns(4)
    total_sales = c_df['Sales Target Hit'].sum()
    total_comm = c_df['Contractor Comission'].sum()
    avg_risk = c_df['At-Risk Score'].mean()
    
    # Apply Simulation Adjustment from Slider
    simulated_comm = total_comm * (1 + commission_adj / 100)
    # Higher commission = Lower risk (simulated logic)
    simulated_risk = max(0, avg_risk - (commission_adj * 2)) 
    
    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("Commission Paid", f"₹{simulated_comm:,.0f}", delta=f"{commission_adj}% cost shift")
    col3.metric("Simulated Risk Score", f"{simulated_risk:.1f}%", delta=f"{simulated_risk - avg_risk:.1f}%")
    col4.metric("Retention Status", "Active" if simulated_risk < 70 else "At High Risk", delta_color="inverse")

    st.markdown("---")
    
    # Two Column Layout for Charts
    left_chart, right_chart = st.columns(2)
    
    with left_chart:
        st.write("### Sales vs Commission Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='Sales Target Hit', y='Contractor Comission', size='At-Risk Score', hue='At-Risk Score', palette='RdYlGn_r', ax=ax)
        plt.title("Contractor Value Map")
        st.pyplot(fig)
        
    with right_chart:
        st.write("### Highest At-Risk Influencers")
        risk_df = df.sort_values('At-Risk Score', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=risk_df, x='At-Risk Score', y='Name', palette='Reds_r', ax=ax)
        plt.xlabel("Predicted Probability of Attrition (%)")
        st.pyplot(fig)

    st.markdown("---")
    
    # Prediction Integration logic
    st.write("### ML Prediction Logic (What-If Analysis)")
    st.info(f"Currently simulating a {commission_adj}% change in commission. Base Risk: {avg_risk:.1f}% -> Simulated: {simulated_risk:.1f}%. (Higher payouts decrease churn risk in this simulation model).")
    
    if selected_contractor != "All Contractors":
        con_data = c_df.iloc[0]
        # Use simulated risk for assessment
        risk = simulated_risk
        
        if risk > 70:
            st.error(f" **ATTENTION:** {selected_contractor} has a {risk}% risk of attriting. Suggested Action: Review credit terms or increase commission.")
        elif risk > 40:
            st.warning(f" **MONITOR:** {selected_contractor} is showing signs of declining momentum ({risk}% risk).")
        else:
            st.success(f" **STABLE:** {selected_contractor} is a high-loyalty partner ({risk}% risk).")

    # --- CUSTOMER LIFETIME VALUE SECTION ---
    st.markdown("---")
    st.subheader("Direct Customer Relationship Management (CRM)")
    st.markdown("Focusing on direct End Customers to reduce contractor reliance and improve cashflow.")

    clv_col1, clv_col2 = st.columns([2, 1])
    
    with clv_col1:
        st.write("### High-Value Individual Customers")
        # Display top 10 CLV customers
        top_clv = clv_df.head(10).reset_index()
        top_clv.columns = ['Customer Name', 'Total Spend', 'Purchase Frequency', 'Days Since Last Visit', 'CLV Score']
        st.dataframe(top_clv.style.background_gradient(subset=['CLV Score'], cmap='BuGn'))
    
    with clv_col2:
        st.write("### Customer Loyalty Tiers")
        # Segmenting by Frequency
        loyal = len(clv_df[clv_df['Frequency'] > 2])
        one_time = len(clv_df[clv_df['Frequency'] <= 1])
        
        labels = ['Loyal (2+ Visits)', 'One-time Buyers']
        sizes = [loyal, one_time]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=140)
        st.pyplot(fig)

    # Data Table
    with st.expander("View Raw Performance Ledger"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
    st.write("Make sure the Excel file exists in the 'Clean and Transformed Data' folder.")
