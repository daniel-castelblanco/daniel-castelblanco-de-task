# README

## Overview

This Python script is designed to fetch and store book data from the New York Times (NYT) API into a PostgreSQL database.

It creates and populates four main tables in the PostgreSQL database:
- **Lists**: Contains information about the NYT bestseller lists.
- **Books**: Stores details of individual books fetched from the NYT API.
- **BuyLinks**: Provides links for purchasing each book.
- **BestsellersInfo**: Holds information of the dates list where published.

 The script can operate in two modes: backfilling historical data or fetching current data. It also performs several SQL queries on the stored data and saves the results to CSV files.

### Report Visualization

For a detailed visualization of the results from the SQL queries, please view the [SQL Queries Report](https://lookerstudio.google.com/reporting/369a0eea-0e2e-427c-8bd7-ed93e7fc2b02).

[![SQL Queries Report](https://github.com/daniel-castelblanco/daniel-castelblanco-de-task/assets/147197232/9baabeeb-5899-4a35-b57d-a138f3ec2c08)](https://lookerstudio.google.com/reporting/369a0eea-0e2e-427c-8bd7-ed93e7fc2b02)



## Prerequisites

- Docker and Docker Compose
- NYT API Key
- PostgreSQL

## Docker Setup

The project is containerized using Docker and Docker Compose. The `docker-compose.yml` file sets up two services: `app` (the Python application) and `db` (PostgreSQL database).

### Environment Variables

Create a `.env` file in the project root with the following content:

```env
NYT_API_KEY=your_api_key
DB_NAME=booksdb
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
START_DATE=your_start_date
END_DATE=your_end_date
BACKFILL=True
```

## Building and Running the Docker Containers 

To build and run the Docker containers, execute the following commands:

```sh
docker-compose down
docker-compose up --build
```

## Python Script

### Description

The main Python script performs the following tasks:

#### Fetch and Store Book Data:

- Fetches book data from the NYT API for a specified date range.
- Stores the fetched data into a PostgreSQL database.
- Can operate in backfill mode to fetch data for historical dates.

#### SQL Queries and CSV Exports:

- Executes several SQL queries on the stored data.
- Saves the results of these queries to CSV files.


## Next Steps

After setting up and running the Python script to fetch, store, and analyze book data, consider the following next steps:

1. **Clean Titles of Books**: Clean titles of books in the data using the primary ISBN-13. Ensure consistent formatting and remove any inconsistencies or errors. 

2. **Enhance table creation**: Define the schema for each table, designate primary keys and create indexes on columns that are frequently use.

3. **Optimize Performance**: Monitor and optimize the performance of SQL queries and database operations for efficiency. Use of Pool to parallelize appended table on database.

4. **Manage Data Security**: Secure sensitive data and credentials by storing them in environment variables or using a secrets management tool. Avoid hardcoding passwords or API keys directly in your codebase to reduce the risk of exposure.


Feel free to customize these next steps based on the specific project goals and requirements.

