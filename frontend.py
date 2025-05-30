import streamlit as st
import pandas as pd
import joblib
import os

# Set page configuration
st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {background-color: #4CAF50; color: white;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif;}
    </style>
""", unsafe_allow_html=True)

# Load saved model and data
model = joblib.load('churn_model.pkl')
test_data = pd.read_csv('test_data_with_predictions.csv')

# Calculate AUC-ROC (assuming you saved y_test and y_pred_proba)
# If not, you can recompute it or save it in the notebook
y_test = test_data['Churn_Probability'].apply(lambda x: 1 if x > 0.5 else 0)  # Example threshold
y_pred_proba = test_data['Churn_Probability']
from sklearn.metrics import roc_auc_score
auc_roc = roc_auc_score(y_test, y_pred_proba)

# Title
st.title("Customer Churn Prediction Dashboard")
st.write(f"**Model AUC-ROC**: {auc_roc:.2f}")

# Layout for visualizations
col1, col2 = st.columns(2)

# Display visualizations in columns
with col1:
    st.image('churn_distribution.png', caption='Churn Distribution', use_container_width=True)
    st.image('roc_curve.png', caption='ROC Curve', use_container_width=True)
    st.image('box_plots.png', caption='Box Plots of Numerical Features', use_container_width=True)

with col2:
    st.image('shap_summary.png', caption='SHAP Feature Importance', use_container_width=True)
    st.image('precision_recall_curve.png', caption='Precision-Recall Curve', use_container_width=True)
    st.image('violin_plot.png', caption='Tenure Distribution by Churn', use_container_width=True)

# Display full-width visualizations
st.image('correlation_heatmap.png', caption='Correlation Heatmap', use_container_width=True)
st.image('pair_plot.png', caption='Pair Plot of Numerical Features', use_container_width=True)
st.image('feature_importance.png', caption='XGBoost Feature Importance', use_container_width=True)
st.image('shap_dependence.png', caption='SHAP Dependence for Top Feature', use_container_width=True)

# High-Risk Customers
high_risk = test_data[test_data['Churn_Probability'] > 0.7]
st.subheader("High-Risk Customers (Churn Probability > 0.7)")
st.write(f"Number of high-risk customers: {len(high_risk)}")
st.dataframe(high_risk.head())

# Business Recommendations
st.subheader("Business Recommendations")
recommendations = []
if high_risk['FeedbackSentiment'].mean() < 0:
    recommendations.append("- Improve customer support to address negative feedback.")
if high_risk['tenure'].mean() < test_data['tenure'].mean():
    recommendations.append("- Offer loyalty discounts for short-tenure customers.")
if high_risk['MonthlyCharges'].mean() > test_data['MonthlyCharges'].mean():
    recommendations.append("- Introduce flexible pricing plans for high-cost customers.")
for rec in recommendations:
    st.write(rec)