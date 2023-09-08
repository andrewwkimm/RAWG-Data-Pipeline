"""Web app for visualizing the processed data."""

import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    """Loads the data used for the visualizations."""
    data = pd.read_csv("data/video_game_data.csv", parse_dates=["release_date"])
    return data


df = load_data()

st.title("Video Game Data Analysis")
st.write("Explore and visualize video game data.")

# Sidebar filters
st.sidebar.header("Filters")
genre_filter = st.sidebar.multiselect("Select Genre(s)", df["genre"].unique())
rating_range = st.sidebar.slider(
    "Select Rating Range",
    float(df["rating"].min()),
    float(df["rating"].max()),
    (0.0, 5.0),
    step=0.01,
)

# Apply filters
if genre_filter and rating_range:
    filtered_df = df[
        (df["genre"].isin(genre_filter)) & (df["rating"].between(*rating_range))
    ]
elif genre_filter:
    filtered_df = df[df["genre"].isin(genre_filter)]
elif rating_range:
    filtered_df = df[df["rating"].between(*rating_range)]
else:
    filtered_df = df

st.subheader("Filtered Data")
st.write(filtered_df)

st.header("Data Visualizations")

# Bar chart for genre distribution
genre_counts = filtered_df["genre"].value_counts()
st.bar_chart(genre_counts, use_container_width=True)
st.subheader("Genre Distribution")

# Bar chart for number of games released by year
year_counts = filtered_df["release_date"].dt.year.value_counts().sort_index()
fig = px.bar(
    x=year_counts.index,
    y=year_counts.values,
    labels={"x": "Year", "y": "Number of Games"},
    title="Number of Games Released by Year",
)
st.plotly_chart(fig)

# Histogram for ratings
fig = px.histogram(
    filtered_df,
    x="rating",
    title="Distribution of Ratings",
    labels={"x": "Rating", "y": "Frequency"},
)
st.plotly_chart(fig)

# Scatter plot for playtime vs. rating
fig = px.scatter(
    filtered_df,
    x="playtime",
    y="rating",
    title="Playtime vs. Rating",
    labels={"x": "Playtime", "y": "Rating"},
)
st.plotly_chart(fig)
