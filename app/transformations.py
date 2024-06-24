import pandas as pd

def normalize_json_to_dataframe(json_data):
    # Extract metadata
    try:
        bestsellers_info = {
            "bestsellers_date": json_data['results']['bestsellers_date'],
            "published_date": json_data['results']['published_date'],
            "published_date_description": json_data['results']['published_date_description'],
            "previous_published_date": json_data['results']['previous_published_date'],
            "next_published_date": json_data['results']['next_published_date']
        }
    except TypeError as e:
        print("Error accessing metadata:", e)
        print("JSON data:", json_data)
        raise

    bestsellers_info_df = pd.DataFrame([bestsellers_info])

    # Normalize the lists data
    lists_data = json_data['results']['lists']
    lists_df = pd.json_normalize(lists_data)
    lists_df = lists_df.drop(columns=['books'])
    lists_df['bestseller_info_published_date'] = bestsellers_info['published_date']


    # Normalize the books data
    books_data = []
    for lst in lists_data:
        list_id = lst['list_id']
        for book in lst['books']:
            book_tmp = pd.json_normalize(book)
            book_tmp['list_id'] = list_id
            books_data.append(book_tmp)
    books_data = [book.drop(columns=['buy_links']) for book in books_data]
    books_df = pd.concat(books_data, ignore_index=True)


    # Normalize the buy_links data
    buy_links_data = []
    for lst in lists_data:
        list_id = lst['list_id']
        for book in lst['books']:
            isbn13 = book['primary_isbn13']
            for link in book['buy_links']:
                link_tmp = pd.json_normalize(link)
                link_tmp['list_id'] = list_id
                link_tmp['primary_isbn13'] = isbn13
                buy_links_data.append(link_tmp)

    buy_links_df = pd.concat(buy_links_data, ignore_index=True)

    return bestsellers_info_df, lists_df, books_df, buy_links_df
