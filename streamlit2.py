import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Load CSV data
df = pd.read_csv("kasarani ethnic.csv")

# Sidebar filters
tribe_selected = st.sidebar.selectbox("Select Tribe", df["TRIBE"].unique())
ward_selected = st.sidebar.selectbox("Select Ward", df["CAW"].unique())

# Filter data
filtered_df = df[(df["TRIBE"] == tribe_selected) & (df["CAW"] == ward_selected)]

# Select specific columns to export
columns_to_export = ["PRIMARY_NAME", "TRIBE", "PHONE_NB", "CONSTITUENCY", "CAW", "POLLING_STATION"]
filtered_export_df = filtered_df[columns_to_export]

# Display filtered data
st.write(f"Showing data for {tribe_selected} in {ward_selected}")
st.dataframe(filtered_df)

# Export function
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered Data")
    processed_data = output.getvalue()
    return processed_data

# Download button
st.download_button(
    label="📥 Export to Excel",
    data=to_excel(filtered_export_df),
    file_name=f"{tribe_selected}_{ward_selected}_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
