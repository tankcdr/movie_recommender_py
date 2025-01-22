import pandas as pd
from uszipcode import SearchEngine

zip_code_search = SearchEngine()


def get_city_state(zip_str):
    """Get the city and state from a ZIP code using the 'uszipcode' library.

    Args:
        zip_str (string): The zip code in string formmat.

    Returns:
        tuple: A tuple containing the city and state, or None if the ZIP code
        is invalid or not found.
    """
    # zip_str should be a 5-digit ZIP
    if pd.isna(zip_str) or not zip_str.isdigit():
        return None, None
    result = zip_code_search.by_zipcode(zip_str)
    if result:
        # 'major_city' can differ slightly from the official city name
        # 'state' is the state abbreviation
        return result.major_city, result.state
    else:
        return None, None


# 1) Load and transform movies.csv
movies = pd.read_csv("data/movies.csv", encoding="latin-1")

# Extract the year from the title using a regex (4 digits in parentheses)
movies["year"] = movies["title"].str.extract(r"\((\d{4})\)", expand=False)
# Remove the parenthetical year from the title itself
movies["title"] = movies["title"].str.replace(
    r"\(\d{4}\)", "", regex=True).str.strip()
# split genres by "|"
movies["genres"] = movies["genres"].str.split("|")


# 2) Load and transform users.csv
users = pd.read_csv("data/users.csv", encoding="latin-1")
# Ensure zip is a string, then keep only the first 5 characters
users["zip"] = users["zip"].astype(str).str[:5]
users[["city", "state"]] = users["zip"].apply(
    lambda z: pd.Series(get_city_state(z))
)


# 3) Load ratings.csv
ratings = pd.read_csv("data/ratings.csv", encoding="latin-1")
ratings["datetime"] = pd.to_datetime(ratings["timestamp"], unit="s")
# Extract hour of day, day of week(as a name), and month of year
ratings["ratings_hour"] = ratings["datetime"].dt.hour
# e.g., "Monday", "Tuesday", etc.
ratings["ratings_day_of_week"] = ratings["datetime"].dt.day_name()
ratings["ratings_month"] = ratings["datetime"].dt.month
ratings["ratings_year"] = ratings["datetime"].dt.year

# 4) Merge the three DataFrames into one
# using 'inner' to drop any rows with missing data
# First join ratings with users on 'user'
merged_data = pd.merge(ratings, users, how="inner", on="user")
# Then join with movies on 'movie'
merged_data = pd.merge(merged_data, movies, how="inner", on="movie")
merged_data = merged_data.fillna("Unknown")


# 5) Write out the new, transformed DataFrame to a CSV file
merged_data.to_csv("data/movies_transformed.csv",
                   index=False, encoding="latin-1")
print(merged_data.head())
