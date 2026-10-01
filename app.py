import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Zomato Restaurant Analytics",
    page_icon="🍽️",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Data/zomato.csv", encoding="latin1")

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Convert numeric columns where available
    numeric_cols = [
        "Aggregate rating",
        "Average Cost for two",
        "Votes",
        "Price range",
        "Longitude",
        "Latitude"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🍽️ Zomato Restaurant Analytics Dashboard")
st.caption(
    "Interactive analysis of restaurant ratings, cuisines, pricing, "
    "online delivery and geographical trends."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Dashboard",
        "Customer & Restaurant Insights",
        "Geographical & Market Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

# Country filter
if "Country" in df.columns:
    countries = sorted(df["Country"].dropna().unique())
    selected_countries = st.sidebar.multiselect(
        "Country",
        countries,
        default=countries
    )
    df_filtered = df[df["Country"].isin(selected_countries)]
else:
    df_filtered = df.copy()

# City filter
if "City" in df_filtered.columns:
    cities = sorted(df_filtered["City"].dropna().unique())

    selected_cities = st.sidebar.multiselect(
        "City",
        cities
    )

    if selected_cities:
        df_filtered = df_filtered[
            df_filtered["City"].isin(selected_cities)
        ]

# Cuisine filter
if "Cuisines" in df_filtered.columns:
    cuisines = sorted(
        df_filtered["Cuisines"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_cuisines = st.sidebar.multiselect(
        "Cuisine",
        cuisines
    )

    if selected_cuisines:
        df_filtered = df_filtered[
            df_filtered["Cuisines"].astype(str).isin(selected_cuisines)
        ]

# --------------------------------------------------
# PAGE 1
# --------------------------------------------------

if page == "Executive Dashboard":

    st.header("📊 Executive Dashboard")

    # KPI calculations
    total_restaurants = len(df_filtered)

    avg_rating = (
        df_filtered["Aggregate rating"].mean()
        if "Aggregate rating" in df_filtered.columns
        else 0
    )

    avg_cost = (
        df_filtered["Average Cost for two"].mean()
        if "Average Cost for two" in df_filtered.columns
        else 0
    )

    total_votes = (
        df_filtered["Votes"].sum()
        if "Votes" in df_filtered.columns
        else 0
    )

    total_cities = (
        df_filtered["City"].nunique()
        if "City" in df_filtered.columns
        else 0
    )

    total_countries = (
        df_filtered["Country"].nunique()
        if "Country" in df_filtered.columns
        else 0
    )

    # KPI cards
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🍽️ Total Restaurants",
        f"{total_restaurants:,}"
    )

    c2.metric(
        "⭐ Average Rating",
        f"{avg_rating:.2f}"
    )

    c3.metric(
        "💰 Average Cost for Two",
        f"{avg_cost:,.0f}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "🗳️ Total Votes",
        f"{total_votes:,.0f}"
    )

    c5.metric(
        "🏙️ Total Cities",
        f"{total_cities:,}"
    )

    c6.metric(
        "🌍 Total Countries",
        f"{total_countries:,}"
    )

    st.markdown("---")

    # Country analysis
    col1, col2 = st.columns(2)

    with col1:

        if "Country" in df_filtered.columns:

            country_counts = (
                df_filtered["Country"]
                .value_counts()
                .reset_index()
            )

            country_counts.columns = [
                "Country",
                "Restaurants"
            ]

            country_counts = country_counts.head(10)

            fig = px.bar(
                country_counts,
                x="Restaurants",
                y="Country",
                orientation="h",
                title="Top Countries by Restaurant Count",
                text="Restaurants"
            )

            fig.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        if "Aggregate rating" in df_filtered.columns:

            rating_df = df_filtered.copy()

            def rating_bucket(x):
                if x == 0:
                    return "Unrated"
                elif x < 2:
                    return "Poor"
                elif x < 3:
                    return "Average"
                elif x < 4:
                    return "Good"
                elif x < 4.5:
                    return "Very Good"
                else:
                    return "Excellent"

            rating_df["Rating Bucket"] = (
                rating_df["Aggregate rating"]
                .apply(rating_bucket)
            )

            rating_counts = (
                rating_df["Rating Bucket"]
                .value_counts()
                .reset_index()
            )

            rating_counts.columns = [
                "Rating Bucket",
                "Restaurants"
            ]

            fig = px.bar(
                rating_counts,
                x="Rating Bucket",
                y="Restaurants",
                title="Restaurant Rating Distribution",
                text="Restaurants"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Online delivery
    if "Has Online delivery" in df_filtered.columns:

        delivery_counts = (
            df_filtered["Has Online delivery"]
            .value_counts()
            .reset_index()
        )

        delivery_counts.columns = [
            "Online Delivery",
            "Restaurants"
        ]

        fig = px.pie(
            delivery_counts,
            names="Online Delivery",
            values="Restaurants",
            hole=0.45,
            title="Restaurants Offering Online Delivery"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# PAGE 2
# --------------------------------------------------

elif page == "Customer & Restaurant Insights":

    st.header("👥 Customer & Restaurant Insights")

    # Rating vs votes
    if "Aggregate rating" in df_filtered.columns and "Votes" in df_filtered.columns:

        col1, col2 = st.columns(2)

        with col1:

            rating_avg = (
                df_filtered
                .groupby("Aggregate rating")
                .agg(
                    Restaurants=("Aggregate rating", "size"),
                    Votes=("Votes", "sum")
                )
                .reset_index()
                .sort_values("Aggregate rating")
            )

            fig = px.line(
                rating_avg,
                x="Aggregate rating",
                y="Votes",
                markers=True,
                title="Votes by Restaurant Rating"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig = px.scatter(
                df_filtered.sample(
                    min(3000, len(df_filtered)),
                    random_state=42
                ),
                x="Aggregate rating",
                y="Votes",
                size="Votes",
                hover_data=["Restaurant Name"]
                if "Restaurant Name" in df_filtered.columns
                else None,
                title="Rating vs Customer Votes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Cost analysis
    if "Average Cost for two" in df_filtered.columns:

        cost_df = (
            df_filtered
            .groupby("Average Cost for two")
            .size()
            .reset_index(name="Restaurants")
            .sort_values(
                "Restaurants",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            cost_df,
            x="Average Cost for two",
            y="Restaurants",
            title="Restaurant Distribution by Average Cost for Two"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Online delivery vs rating
    if (
        "Has Online delivery" in df_filtered.columns
        and "Aggregate rating" in df_filtered.columns
    ):

        delivery_rating = (
            df_filtered
            .groupby("Has Online delivery")["Aggregate rating"]
            .mean()
            .reset_index()
        )

        delivery_rating.columns = [
            "Online Delivery",
            "Average Rating"
        ]

        fig = px.bar(
            delivery_rating,
            x="Online Delivery",
            y="Average Rating",
            title="Average Rating by Online Delivery Availability",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# PAGE 3
# --------------------------------------------------

elif page == "Geographical & Market Analysis":

    st.header("🌍 Geographical & Market Analysis")

    # Top cities
    if "City" in df_filtered.columns:

        city_counts = (
            df_filtered["City"]
            .value_counts()
            .reset_index()
        )

        city_counts.columns = [
            "City",
            "Restaurants"
        ]

        city_counts = city_counts.head(15)

        fig = px.bar(
            city_counts,
            x="Restaurants",
            y="City",
            orientation="h",
            title="Top Cities by Restaurant Count",
            text="Restaurants"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Cuisine analysis
    if "Cuisines" in df_filtered.columns:

        cuisine_series = (
            df_filtered["Cuisines"]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
        )

        cuisine_counts = (
            cuisine_series
            .value_counts()
            .reset_index()
        )

        cuisine_counts.columns = [
            "Cuisine",
            "Restaurants"
        ]

        cuisine_counts = cuisine_counts.head(15)

        fig = px.bar(
            cuisine_counts,
            x="Restaurants",
            y="Cuisine",
            orientation="h",
            title="Top Cuisines",
            text="Restaurants"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Geographical map
    if (
        "Latitude" in df_filtered.columns
        and "Longitude" in df_filtered.columns
    ):

        map_df = df_filtered[
            ["Latitude", "Longitude"]
        ].dropna()

        map_df = map_df.sample(
            min(3000, len(map_df)),
            random_state=42
        )

        st.subheader("📍 Restaurant Locations")

        st.map(
            map_df,
            latitude="Latitude",
            longitude="Longitude"
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Zomato Data Analytics Project | "
    "Python • SQL • PostgreSQL • Power BI • Streamlit"
) 
