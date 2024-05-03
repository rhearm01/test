import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "C:\\Personal\\USC ADS\\DSCI 510\\_Project\\wildata\\wildlife-insights_de567727-c38d-46a5-b39f-6dee9fb42e97_all-platform-data\\images.csv"
df = pd.read_csv(file_path)

# Convert timestamp to datetime with error handling
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with NaT values
df.dropna(subset=['timestamp'], inplace=True)

# Create a new column to represent the index
df['index'] = df.index

# Sidebar options
st.sidebar.title("Filter Options")
species_name = st.sidebar.text_input("Enter Species Name (optional):")
taxonomy_levels = ['class', 'order', 'family', 'genus', 'species']
taxonomy_filters = {}
for level in taxonomy_levels:
    taxonomy_filters[level] = st.sidebar.multiselect(f"Filter by {level.capitalize()}", df[level].unique())

# Get min and max index values
index_min = df['index'].min()
index_max = df['index'].max()

# Slider for index range
index_range = st.sidebar.slider("Select Index Range:", index_min, index_max, (index_min, index_max))

# Filter the dataset based on user inputs
filtered_df = df.copy()
if species_name:
    filtered_df = filtered_df[filtered_df['species'].str.contains(species_name, case=False)]
for level, values in taxonomy_filters.items():
    if values:
        filtered_df = filtered_df[filtered_df[level].isin(values)]
filtered_df = filtered_df[(filtered_df['index'] >= index_range[0]) & (filtered_df['index'] <= index_range[1])]

# Show the filtered data
st.write("Filtered Data:")
st.write(filtered_df)

# Visualizations
st.title("Visualizations")
if not filtered_df.empty:
    # Bar Chart of Species Distribution
    st.subheader("Species Distribution")
    species_counts = filtered_df['species'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=species_counts.index, y=species_counts.values, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Species")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Histogram of Timestamps
    st.subheader("Timestamp Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df['timestamp'], bins=20, kde=True, color='skyblue')
    plt.xlabel("Timestamp")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Map of Observations (Assuming latitude and longitude columns are available)
    if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
        st.subheader("Map of Observations")
        st.map(filtered_df[['latitude', 'longitude']])

    # Pie Chart of Taxonomic Classification
    st.subheader("Taxonomic Classification")
    for level in taxonomy_levels:
        level_counts = filtered_df[level].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        plt.axis('equal')
        plt.title(f"{level.capitalize()} Distribution")
        st.pyplot(plt)

else:
    st.write("No data available for the selected filters.")
