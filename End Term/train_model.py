import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import sys
import io

# Setup for character encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Paths
DATA_PATH = r'c:\Users\vaibh\Downloads\IITM_AMU\IIT_M\BDM stuff\project\My Project\End Term\Clean and Transformed Data'
sales_file = os.path.join(DATA_PATH, 'SalesData (Apr-24 - Mar-25).xlsx')
performance_file = os.path.join(DATA_PATH, 'Contractor Performance Data.xlsx')

def train_model():
    print("Loading data...")
    # Load Sales Data
    df_sales = pd.read_excel(sales_file, sheet_name='Cleaned')
    df_sales['Date'] = pd.to_datetime(df_sales['Date'])
    
    # Filter for Contractors only
    df_contractors = df_sales[df_sales['Buyer Role'] == 'Contractor'].copy()
    
    # Define "Today" as the max date in the dataset
    max_date = df_contractors['Date'].max()
    
    print(f"Dataset covers until: {max_date}")

    # Feature Engineering per Contractor (using Buyer Name as ID)
    # Note: In a real scenario, we'd use a unique ID, but we'll use Name for now.
    
    # 1. Recency
    recency = df_contractors.groupby('Buyer Name')['Date'].max().apply(lambda x: (max_date - x).days)
    
    # 2. Frequency
    frequency = df_contractors.groupby('Buyer Name').size()
    
    # 3. Monetary
    monetary = df_contractors.groupby('Buyer Name')['Amount (₹)'].sum()
    
    # 4. Momentum (Last 3 months vs Total Monthly Average)
    last_3m_mask = df_contractors['Date'] > (max_date - pd.Timedelta(days=90))
    momentum = df_contractors[last_3m_mask].groupby('Buyer Name')['Amount (₹)'].sum() / (monetary / 12)
    momentum = momentum.fillna(0) # 0 momentum if no sales in last 3 months

    # Combine features
    features = pd.DataFrame({
        'recency': recency,
        'frequency': frequency,
        'monetary': monetary,
        'momentum': momentum
    }).reset_index()

    # Target Label: "Churned" if recency > 60 days
    # (Threshold based on business logic for construction materials where cycles are frequent)
    features['at_risk'] = (features['recency'] > 60).astype(int)

    print(f"Class distribution:\n{features['at_risk'].value_counts()}")

    # Prepare for ML
    X = features[['recency', 'frequency', 'monetary', 'momentum']]
    y = features['at_risk']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(y_test, y_pred))

    # Save components
    joblib.dump(clf, 'attrition_model.joblib')
    features.to_csv('contractor_risk_data.csv', index=False)
    print("\nModel and feature data saved successfully.")

if __name__ == "__main__":
    train_model()
