import streamlit as st
import pandas as pd    
import plotly.express as px


#Title
st.title('Kasarani Voter Dasboard')

#uplad csv file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    #read CSV
    df = pd.read_csv(uploaded_file)


    #Display full dataset
    st.subheader("Full Dataset")
    st.dataframe(df)

    #Filter by WARD
    wards = df["CAW"].unique()
    selected_ward = st.selectbox("Select WARD", ["All"] + list(wards))

    #Filter by Tribe
    tribes = df["TRIBE"].unique()
    selected_tribe = st.selectbox("Select Tribe", ["All"] + list(tribes))

    #Apply filters
    filtered_df = df.copy()


    if selected_ward != "All":
        filtered_df = filtered_df[filtered_df["CAW"] == selected_ward]

    if selected_tribe != "All":
        filtered_df = filtered_df[filtered_df["TRIBE"] == selected_tribe]

    # Display total count
    total_count = len(filtered_df)
    st.subheader(f"Total Count: {total_count} Records")

    #Display filtered dataset
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df)

    # Bar chart: Number of people per Tribe in selected Constituency
    if selected_ward != "All":
        st.subheader(f"Tribe Distribution in {selected_ward}")
        tribe_counts = df[df["CAW"] == selected_ward]["TRIBE"].value_counts().reset_index()
        tribe_counts.columns = ["TRIBE", "Count"]
        fig_bar = px.bar(tribe_counts, x="TRIBE", y="Count", title="Tribe Distribution", color="TRIBE")
        st.plotly_chart(fig_bar)

    # Pie chart: Distribution of Tribes in the selected Constituency
    if selected_ward != "All":
        st.subheader(f"Tribe Percentage in {selected_ward}")
        fig_pie = px.pie(tribe_counts, names="TRIBE", values="Count", title="Tribe Proportions")
        st.plotly_chart(fig_pie)

else:
    st.write("Please upload a file")