from datetime import datetime, timedelta
import os
import logging
from api import get_books_data
from database import append_to_postgres, query_db
import pandas as pd
from query_session import ( top_rank_book_2022_query,
                            top_3_lists_unique_books_query,
                            top_5_publishers_query,
                            teams_books_review_query)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_store_books_data(start_date, end_date=None, backfill='True'):
    current_date = start_date
    # raise an error if end_date is less than start_date
    if end_date < start_date:
        raise ValueError("End date should be greater or equal than start date")
    # retrieve data for current date or backfill data
    if backfill == 'True':
        logger.info("Backfilling data from NYT API")
        # Backfilling data
        while current_date <= end_date:
            # save all df to postgres
            bestsellers_info_df, lists_df, books_df, buy_links_df = get_books_data(current_date.strftime("%Y-%m-%d"))
            # save to postgres
            append_to_postgres(bestsellers_info_df, 'BestsellersInfo')
            append_to_postgres(lists_df, 'Lists')
            append_to_postgres(books_df, 'Books')
            append_to_postgres(buy_links_df, 'BuyLinks')
            current_date += timedelta(days=7)  # Assuming weekly updates
            logging.info(f"Data for {current_date} saved to Postgres /n
                            Tables: /n
                            BestsellersInfo uploaded {bestsellers_info_df.shape[0]} rows /n
                            Lists uploaded {lists_df.shape[0]} rows /n
                            Books uploaded {books_df.shape[0]} rows /n
                            BuyLinks uploaded {buy_links_df.shape[0]} rows")

    else:
        logger.info("Fetching current date from NYT API")
        # # Fetching data
        data = get_books_data(current_date.strftime("%Y-%m-%d"))
        bestsellers_info_df, lists_df, books_df, buy_links_df = data
        # save to postgres
        append_to_postgres(bestsellers_info_df, 'BestsellersInfo')
        append_to_postgres(lists_df, 'Lists')
        append_to_postgres(books_df, 'Books')
        append_to_postgres(buy_links_df, 'BuyLinks')
        logging.info(f"Data for {current_date} saved to Postgres /n
                        Tables: /n
                        BestsellersInfo uploaded {bestsellers_info_df.shape[0]} rows /n
                        Lists uploaded {lists_df.shape[0]} rows /n
                        Books uploaded {books_df.shape[0]} rows /n
                        BuyLinks uploaded {buy_links_df.shape[0]} rows")

    # SQL Data Section
    # Query the database for the top book of 2022 rank <=3
    top_book_result = query_db(top_rank_book_2022_query)
    logging.info(f"Top book of 2022: {top_book_result}")
    top_book = pd.DataFrame(top_book_result, columns=['title', 'times_top'])
    top_book.to_csv('sql_results/top_book_2022.csv', index=False)

    # Top 3 lists to have the least number of unique books in their rankings for the entirety of the data
    top_3_lists_unique_books = query_db(top_3_lists_unique_books_query)
    # message with the ti
    logging.info(f"Top 3 lists with the least number of unique books: {top_3_lists_unique_books}")
    top_3_lists_unique_books = pd.DataFrame(top_3_lists_unique_books, columns=['list_id', 'list_name', 'unique_books'])
    top_3_lists_unique_books.to_csv('sql_results/top_3_lists_unique_books.csv', index=False)

    # Top 5 Publishers quaterly rank from 2021 to 2023
    top_5_publishers = query_db(top_5_publishers_query)
    logging.info(f"Top 5 Publishers quarterly rank from 2021 to 2023.")
    top_5_publishers = pd.DataFrame(top_5_publishers, columns=['year', 'quarter', 'publisher', 'total_points', 'quarterly_rank'])
    top_5_publishers.to_csv('sql_results/top_5_publishers.csv', index=False)

    # Team Jake and teams Pete Books reviews for 2023
    teams_books_review = query_db(teams_books_review_query)
    logging.info(f"Team Jake and teams Pete Books reviews for 2023.")
    teams_books_review = pd.DataFrame(teams_books_review, columns=['team', 'title', 'rank', 'created_date'])
    teams_books_review.to_csv('sql_results/teams_books_review.csv', index=False)

if __name__ == "__main__":
    start_date = datetime.strptime(os.getenv('START_DATE', '2023-12-30'), '%Y-%m-%d')
    end_date = datetime.strptime(os.getenv('END_DATE', '2023-12-31'), '%Y-%m-%d')
    backfill = os.getenv('BACKFILL', 'True')
    fetch_store_books_data(start_date, end_date, backfill)



