import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Election Data Upload", layout="centered")

st.title("🧩 Upload election data to the central IEBC voter database")

# Define the path to the initial CSV file
INITIAL_CSV_PATH = "2022-voter-data-master.csv"

# Check if the initial file exists
if not os.path.exists(INITIAL_CSV_PATH):
    st.error(f"Master file '{INITIAL_CSV_PATH}' not found in the directory.")
    st.stop()

# Load the initial CSV
df_initial = pd.read_csv(INITIAL_CSV_PATH)
st.success("Initial file loaded successfully from disk.")

st.subheader("Initial File Headers")
st.write(list(df_initial.columns))

# Step 2: Upload the second CSV (to be mapped)
st.header("1. Upload Second CSV File (to map and merge)")
second_file = st.file_uploader("Upload the second CSV file", type=["csv"], key="second")

if second_file:
    df_second = pd.read_csv(second_file)

    st.subheader("Second File Headers")
    st.write(list(df_second.columns))

    st.header("3. Map Headers")
    st.markdown("Match each column in the second file to a column in the master file.")

    mapping = {}
    for col in df_second.columns:
        mapped_col = st.selectbox(
            f"Map '{col}' to:", 
            options=["-- Skip --"] + list(df_initial.columns),
            key=f"map_{col}"
        )
        if mapped_col != "-- Skip --":
            mapping[col] = mapped_col

    st.write("### Header Mapping:")
    st.json(mapping)

    if st.button(" Update Master File"):
        if not mapping:
            st.warning("Please map at least one column before merging.")
        else:
            # Rename the columns in df_second according to the mapping
            df_mapped = df_second.rename(columns=mapping)

            # Only keep columns that were mapped
            df_mapped = df_mapped[list(mapping.values())]

            # Add missing columns if any
            for col in df_initial.columns:
                if col not in df_mapped.columns:
                    df_mapped[col] = None

            # Merge and save
            df_updated = pd.concat([df_initial, df_mapped[df_initial.columns]], ignore_index=True)
            df_updated.to_csv(INITIAL_CSV_PATH, index=False)

            st.success(f"✅ '{INITIAL_CSV_PATH}' has been updated successfully!")
            st.dataframe(df_updated.tail())

           
            
