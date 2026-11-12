# TMDB Movie Analytics

## 1. Project Overview

TMDB Movie Analytics is a data analytics project developed to explore, analyze, and visualize movie-related data using Python, Pandas, SQL, and Streamlit.

The project focuses on understanding movie performance and industry trends by analyzing revenue, budget, popularity, ratings, genres, cast, crew, keywords, and release dates.

An interactive Streamlit dashboard allows users to explore movie data through visualizations, filters, and SQL queries.

## 2. Project Objectives

- Analyze movie performance using available movie datasets.
- Identify trends in movie revenue, budget, popularity, and ratings.
- Perform data cleaning and preprocessing.
- Extract meaningful information using SQL queries.
- Analyze movie data using Pandas.
- Present analytical results through an interactive dashboard.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| SQLite | Database management |
| SQL | Data querying and analysis |
| Matplotlib | Data visualization |
| Streamlit | Interactive dashboard development |
| Jupyter Notebook | Data analysis and experimentation |

## 4. Project Structure

```text
TMDB_Movie_Analytics/
│
├── data/
│   ├── movies.csv
│   ├── movies_cleaned.csv
│   ├── genres.csv
│   ├── movie_genres.csv
│   ├── cast.csv
│   ├── crew.csv
│   ├── movie_keywords.csv
│   └── tmdb_movies.db
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_sql_analysis.ipynb
│   ├── 03_pandas_analysis.ipynb
│   └── 04_visualizations.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

## 5. Project Features

### Data Analysis
- Movie dataset cleaning and preprocessing.
- Analysis using Python and Pandas.
- SQL-based data exploration.
- SQLite database integration.

### Interactive Dashboard
- Movie performance overview.
- Revenue and rating visualizations.
- Movie filtering options.
- SQL Query Explorer.
- About page with project information.

## 6. Key Analysis Areas

The project explores the following five analytical areas:

1. **Revenue Analysis:** Identifying movies with the highest revenue.
2. **Popularity Analysis:** Exploring the popularity of movies.
3. **Budget and Revenue Analysis:** Examining movie budgets and revenue patterns.
4. **Release Trend Analysis:** Understanding movie release trends over time.
5. **Rating Analysis:** Exploring movie ratings and highly rated movies.

## 7. How to Run the Project

### Step 1: Open the project folder

Open the `TMDB_Movie_Analytics` folder in Visual Studio Code.

### Step 2: Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit application

```bash
python -m streamlit run app.py
```

### Step 5: Open the dashboard

After running the command, Streamlit displays a Local URL in the terminal.

Open that URL in your web browser to access the application.

## 8. Expected Outcomes

- Better understanding of movie industry data.
- Identification of movie performance patterns.
- Practical experience with Python, Pandas, and SQL.
- Interactive visualization of movie analytics.
- Hands-on experience in building a data analytics dashboard.

## 9. Conclusion

TMDB Movie Analytics demonstrates the application of Python, Pandas, SQL, SQLite, and Streamlit in a real-world data analytics project.

By combining data preprocessing, database querying, analytical techniques, and interactive visualizations, the project provides an accessible way to explore movie datasets and understand movie industry trends.

---

**Project:** TMDB Movie Analytics  
**Category:** Data Analytics  
**Tools:** Python | Pandas | SQL | SQLite | Matplotlib | Streamlit
