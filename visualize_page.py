# visualize_page.py
import streamlit as st
import pandas as pd
import plotly.express as px
from auth_module import load_predictions

def show_visualization():
    st.title("📊 Heart Disease Prediction Dashboard")

    preds = load_predictions(st.session_state.email)
    if not preds:
        st.info("No predictions yet to visualize.")
        return

    df = pd.DataFrame(preds)
    df["index"] = range(1, len(df)+1)
    # map "High Risk" -> 1, else 0
    df["Actual Risk"] = df["prediction"].apply(lambda x: 1 if x=="High Risk" else 0)
    df["Predicted Risk"] = df["Actual Risk"]  # placeholder: use real model predictions later

    st.subheader("Actual vs Predicted Risk")
    fig = px.line(df, x="index", y=["Actual Risk", "Predicted Risk"], markers=True)
    fig.update_layout(legend_title_text="Series", yaxis=dict(tickmode="array", tickvals=[0,1], ticktext=["Low","High"]))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Feature Importance (Example)")
    features = pd.DataFrame({
        "Feature": ["Age", "Cholesterol", "Max HR", "BP", "ST Depression"],
        "Importance": [0.35, 0.25, 0.2, 0.15, 0.05]
    })
    fig2 = px.bar(features, x="Feature", y="Importance", text="Importance")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🩺 Previous Predictions")
    st.dataframe(df[["timestamp", "age", "chol", "thalach", "prediction", "pdf_filename"]].sort_values(by="timestamp", ascending=False))
