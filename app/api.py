import requests
import os
import logging
import time

from transformations import normalize_json_to_dataframe

NYT_API_KEY = os.getenv('NYT_API_KEY')
BASE_URL = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
RATE_LIMIT_DELAY = 60  # Delay (secs) to wait after hitting rate limit


def get_books_data(date):
    """
    Fetches the bestsellers data from the New York Times Books API for a given date.
    Saves the data to a JSON file and returns the normalized data as DataFrames.

    Parameters:
    - date: The date for which to fetch the bestsellers data in the format "YYYY-MM-DD".

    Returns:
    - bestsellers_info_df: DataFrame containing the bestsellers metadata.
    - lists_df: DataFrame containing the list information.
    - books_df: DataFrame containing the book information.
    - buy_links_df: DataFrame containing the buy links information.
    """

    url = f"{BASE_URL}?published_date={date}&api-key={NYT_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        file_path = f"data/{date}.json"
        with open(file_path, "w") as f:
            logging.info(f"Saving data to {file_path}")
            f.write(response.text)

        bestsellers_info_df, lists_df, books_df, buy_links_df = normalize_json_to_dataframe(response.json())
        return bestsellers_info_df, lists_df, books_df, buy_links_df

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:  # HTTP status code 429: Too Many Requests
            logging.error("Rate limit exceeded. Retrying after delay...")
            time.sleep(RATE_LIMIT_DELAY)
            return get_books_data(date)  # Retry the request after delay
        else:
            logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None, None, None, None  # Return None or Slack message values in case of error.