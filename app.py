
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TMDB Movie Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "movies_cleaned.csv"
DB_PATH = BASE_DIR / "data" / "tmdb_movies.db"

# --------------------------------------------------
# PROFESSIONAL LIGHT THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #F5F7FA;
    color: #1E293B;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #101A35;
    border-right: 1px solid #172442;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 7px 5px;
}

/* Headings */
h1, h2, h3 {
    color: #101A35 !important;
    font-weight: 650 !important;
}

p, label {
    color: #475569;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: #101A35 !important;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: #101A35;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 9px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #FF6900;
    color: white;
    border: none;
}

/* Input fields */
.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 7px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    overflow: hidden;
}

/* Horizontal divider */
hr {
    border-color: #E2E8F0;
}

/* Header */
.dashboard-header {
    background: #FFFFFF;
    padding: 25px 30px;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #FF6900;
    border-radius: 12px;
    margin-bottom: 28px;
}

.dashboard-title {
    font-size: 30px;
    font-weight: 750;
    color: #101A35;
    margin: 0;
}

.dashboard-subtitle {
    font-size: 14px;
    color: #64748B;
    margin-top: 8px;
}

.section-label {
    font-size: 12px;
    color: #FF6900;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    padding: 20px 0 5px 0;
}

/* About page */
.about-hero {
    background: radial-gradient(circle at 92% 12%, rgba(255,105,0,.20), transparent 30%),
                linear-gradient(120deg, #101A35, #172442);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 38px 40px;
    margin: 8px 0 28px 0;
    border-left: 5px solid #FF6900;
}
.about-eyebrow {
    color: #FFB27A;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.about-hero h1 {
    color: #FFFFFF !important;
    font-size: 32px;
    margin: 10px 0;
}
.about-hero p {
    color: #E2E8F0 !important;
    font-size: 15px;
    max-width: 780px;
    line-height: 1.7;
}
.about-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 13px;
    padding: 20px;
    min-height: 145px;
    margin-bottom: 14px;
}
.about-card h4 {
    color: #101A35;
    margin: 0 0 8px 0;
    font-size: 17px;
}
.about-card p {
    color: #64748B !important;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}
.about-tag {
    display: inline-block;
    background: #FFF1E8;
    color: #C94F00;
    border: 1px solid #FFD2B5;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px 6px 4px 0;
    font-size: 13px;
    font-weight: 650;
}
.about-objective {
    background: #F0F7F5;
    border: 1px solid #D7EAE3;
    border-left: 4px solid #2D8A6E;
    border-radius: 12px;
    padding: 20px 22px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD MOVIE DATA
# --------------------------------------------------

@st.cache_data
def load_movies():
    df = pd.read_csv(CSV_PATH)

    numeric_columns = [
        "budget", "revenue", "vote_average",
        "vote_count", "popularity", "runtime"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["release_date"] = pd.to_datetime(
        df["release_date"], errors="coerce"
    )

    df["release_year"] = df["release_date"].dt.year

    return df


if not CSV_PATH.exists():
    st.error(f"Dataset not found: {CSV_PATH}")
    st.stop()

movies = load_movies()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 20px 0;">
        <div style="font-size: 30px;">🎬</div>
        <div style="font-size: 21px; font-weight: 750;">
            TMDB ANALYTICS
        </div>
        <div style="font-size: 12px; color: #CBD5E1;">
            MOVIE DATA INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Select Page",
        ["Dashboard", "Filters", "Query Explorer", "About"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Movie Filters")

    years = movies["release_year"].dropna()

    if years.empty:
        st.error("No valid release years found.")
        st.stop()

    min_year = int(years.min())
    max_year = int(years.max())

    year_range = st.slider(
        "Release Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    languages = sorted(
        movies["original_language"].dropna().unique()
    )

    default_languages = (
        ["en"] if "en" in languages else languages
    )

    selected_languages = st.multiselect(
        "Original Language",
        languages,
        default=default_languages
    )

    st.divider()

    st.caption("TMDB MOVIE ANALYTICS")
    st.caption("Python • Pandas • SQL • Streamlit")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered = movies[
    movies["release_year"].between(*year_range)
    & movies["original_language"].isin(selected_languages)
].copy()


# --------------------------------------------------
# COMMON HEADER
# --------------------------------------------------

st.markdown("""
<div class="dashboard-header">
    <div class="section-label">DATA ANALYTICS PLATFORM</div>
    <div class="dashboard-title">
        🎬 TMDB Movie Analytics
    </div>
    <div class="dashboard-subtitle">
        Explore movie performance, ratings, revenue
        and audience popularity through interactive analytics.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.markdown("## Movie Performance Overview")

    st.caption(
        "Key performance indicators based on your selected filters."
    )

    total_movies = len(filtered)

    avg_rating = filtered["vote_average"].mean()
    total_revenue = filtered["revenue"].sum()
    avg_popularity = filtered["popularity"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Movies",
        f"{total_movies:,}"
    )

    col2.metric(
        "Average Rating",
        f"{avg_rating:.2f}" if pd.notna(avg_rating) else "0.00"
    )

    col3.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    col4.metric(
        "Average Popularity",
        f"{avg_popularity:.2f}"
        if pd.notna(avg_popularity) else "0.00"
    )

    st.write("")

    # Revenue chart
    st.markdown("### Top 10 Highest Revenue Movies")

    top = (
        filtered[filtered["revenue"] > 0]
        .nlargest(10, "revenue")
        .sort_values("revenue", ascending=True)
    )

    if not top.empty:

        fig, ax = plt.subplots(figsize=(12, 5))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        ax.barh(
            top["title"],
            top["revenue"],
            color="#101A35",
            height=0.62
        )

        ax.set_xlabel("Revenue (USD)", color="#475569")
        ax.set_ylabel("")

        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"${x/1e6:.0f}M")
        )

        ax.tick_params(axis="both", labelsize=9, colors="#64748B")
        ax.grid(axis="x", linestyle="--", alpha=0.25)
        ax.set_axisbelow(True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    else:
        st.info("No revenue data available for these filters.")

    st.write("")

    # Rating distribution
    st.markdown("### Movie Rating Distribution")

    ratings = filtered["vote_average"].dropna()

    if not ratings.empty:

        fig, ax = plt.subplots(figsize=(12, 4))

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        ax.hist(
            ratings,
            bins=20,
            color="#FF6900",
            edgecolor="#FFFFFF",
            linewidth=1.2
        )

        ax.set_xlabel("Movie Rating", color="#475569")
        ax.set_ylabel("Number of Movies", color="#475569")

        ax.tick_params(colors="#64748B")
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        ax.set_axisbelow(True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    else:
        st.info("No rating data available.")

    st.write("")

    # Dataset
    st.markdown("### Movie Dataset")

    st.caption(f"Showing {len(filtered):,} movie records.")

    display_df = filtered.drop(columns=["release_year"], errors="ignore")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=420
    )


# --------------------------------------------------
# FILTER EXPLORER PAGE
# --------------------------------------------------

elif page == "Filters":

    st.markdown("## Movie Filter Explorer")

    st.caption(
        "Search and explore movies using your selected filters."
    )

    search = st.text_input(
        "Search Movie Title",
        placeholder="Enter a movie name..."
    )

    result = filtered.copy()

    if search:
        result = result[
            result["title"].str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
        ]

    col1, col2 = st.columns(2)

    col1.metric("Movies Found", f"{len(result):,}")
    col2.metric("Total Dataset Movies", f"{len(movies):,}")

    st.write("")

    st.markdown("### Search Results")

    display_df = result.drop(
        columns=["release_year"],
        errors="ignore"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )


# --------------------------------------------------
# SQL QUERY EXPLORER PAGE
# --------------------------------------------------

elif page == "Query Explorer":

    st.markdown("## SQL Query Explorer")

    st.caption(
        "Explore movie insights using predefined SQL queries."
    )

    queries = {
        "Top 10 Revenue Movies": """
            SELECT title, budget, revenue
            FROM movies
            WHERE revenue > 0
            ORDER BY revenue DESC
            LIMIT 10
        """,

        "Top 10 Popular Movies": """
            SELECT title, popularity, vote_average
            FROM movies
            ORDER BY popularity DESC
            LIMIT 10
        """,

        "Top 10 Highest Rated Movies": """
            SELECT title, vote_average, vote_count
            FROM movies
            WHERE vote_count >= 100
            ORDER BY vote_average DESC
            LIMIT 10
        """
    }

    choice = st.selectbox(
        "Select SQL Analysis",
        list(queries.keys())
    )

    with st.expander("View SQL Query"):
        st.code(queries[choice], language="sql")

    if st.button("Run Query", type="primary"):

        if not DB_PATH.exists():
            st.error("SQLite database not found.")
        else:
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    result = pd.read_sql_query(
                        queries[choice],
                        conn
                    )

                st.success("Query executed successfully.")

                st.markdown("### Query Results")

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

            except Exception as e:
                st.error(f"SQL execution error: {e}")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.markdown("""
    <div class="about-hero">
        <div class="about-eyebrow">About the project</div>
        <h1>TMDB Movie Analytics</h1>
        <p>
            An interactive movie data analysis dashboard built using TMDB data
            to explore trends, performance, and insights in the film industry.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Project Overview")
    st.write(
        "TMDB Movie Analytics brings movie information into one place so that "
        "users can explore commercial performance, audience ratings, popularity, "
        "and release patterns through data analysis."
    )

    st.markdown("## Key Features")
    feature_cols = st.columns(2)

    features = [
        ("Performance Analysis",
         "Explore movie revenue, budget, ratings, and popularity to understand performance."),
        ("Trend Insights",
         "Examine movie release years and discover patterns across the dataset."),
        ("SQL Query Explorer",
         "Run predefined SQL queries to identify top-grossing, popular, and highly rated movies."),
        ("Interactive Filters",
         "Filter the movie dataset by release year and original language.")
    ]

    for index, (heading, description) in enumerate(features):
        with feature_cols[index % 2]:
            st.markdown(
                f'<div class="about-card"><h4>{heading}</h4>'
                f'<p>{description}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("## Technology Stack")
    st.markdown(
        '<span class="about-tag">Python</span>'
        '<span class="about-tag">Pandas</span>'
        '<span class="about-tag">Streamlit</span>'
        '<span class="about-tag">SQL / SQLite</span>'
        '<span class="about-tag">Matplotlib</span>',
        unsafe_allow_html=True
    )

    st.markdown("## Dataset Information")
    dataset_info = pd.DataFrame({
        "Attribute": [
            "Data Source", "Total Movies", "Release Year Range",
            "Key Attributes"
        ],
        "Details": [
            "The Movie Database (TMDB)",
            f"{len(movies):,} movies in the cleaned dataset",
            f"{min_year} – {max_year}",
            "Title, Release Date, Runtime, Budget, Revenue, Popularity, Rating, Language"
        ]
    })
    st.dataframe(dataset_info, use_container_width=True, hide_index=True)

    st.markdown("## Project Objective")
    st.markdown(
        '<div class="about-objective">'
        '<strong>Turn movie data into useful insights.</strong><br>'
        'The objective is to demonstrate an end-to-end analytics workflow: '
        'data preparation, SQL querying, Python-based analysis, visualization, '
        'and an interactive Streamlit application.'
        '</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    TMDB Movie Analytics &nbsp; | &nbsp;
    Developed using Python, Pandas, SQL and Streamlit
    <br><br>
    Data Analytics Project
</div>
""", unsafe_allow_html=True)
