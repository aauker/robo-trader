# robo-trader

So far, I run two services, one to stream minute-bar data (stream-alpaca-data) and one to stream news data (stream-alpaca-news) about stocks to an S3 bucket in parquet tables.

I then expose the parquet table as a virtual dataset in dremio, and do some exploratory work to detect large positive swing trades.
