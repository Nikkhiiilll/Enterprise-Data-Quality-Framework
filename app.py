import streamlit as st
import pandas as pd
from data_quality import DataQuality

st.set_page_config(page_title="Amex Data Quality Dashboard", layout="wide")

st.title("📊 Amex Data Quality & Governance Dashboard")
st.markdown("### Analyze, Profile, and Remediate Data Quality Issues")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📌 Uploaded Dataset")
    st.dataframe(df.head())

    dq = DataQuality(df)
    report = dq.generate_report()

    st.subheader("🔍 Data Quality Report")
    st.json(report)

    if report["missing_values"]:
        st.warning("⚠ Missing Values Found!")
        st.write(report["missing_values"])

    duplicates = dq.check_duplicates()
    if not duplicates.empty:
        st.warning(f"⚠ Found {len(duplicates)} Duplicate Records")
        st.dataframe(duplicates)

    negatives = dq.check_negative_amounts()
    if not negatives.empty:
        st.warning(f"⚠ Found {len(negatives)} Negative Amount Transactions")
        st.dataframe(negatives)

    invalid_dates = dq.check_invalid_dates()
    if not invalid_dates.empty:
        st.warning(f"⚠ Found {len(invalid_dates)} Invalid Dates")
        st.dataframe(invalid_dates)
else:
    st.info("📥 Please upload a CSV file to begin analysis.")

