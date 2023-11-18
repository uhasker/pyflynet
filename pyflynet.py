import argparse
import time
import os
import ping3
import psycopg2
import logging
from typing import Union, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ping(ip_addr: str, timeout: int) -> Tuple[Optional[float], Optional[str]]:
    try:
        result = ping3.ping(ip_addr, timeout=timeout)
        if result is not None:
            return result, None
        else:
            return None, "Ping timed out"
    except Exception as e:
        return None, str(e)

def create_ping_result_table():
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password=os.environ.get("DATABASE_PASS"),
            host="db.beogantahxdrfrqhnqjn.supabase.co",
            port=5432,
            database="postgres"
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ping_results (
                id SERIAL PRIMARY KEY,
                timestamp FLOAT,
                latency FLOAT,
                error TEXT
            )
            """
        )
        conn.commit()
    except Exception as e:
        logging.error("Error creating table: %s", e)
    finally:
        if conn is not None:
            conn.close()


def insert_ping_result(timestamp: float, latency: Union[float, None], error: Union[str, None]) -> None:
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password=os.environ.get("DATABASE_PASS"),
            host="db.beogantahxdrfrqhnqjn.supabase.co",
            port=5432,
            database="postgres"
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ping_results (timestamp, latency, error) VALUES (%s, %s, %s)
            """,
            (timestamp, latency, error),
        )
        conn.commit()
    except Exception as e:
        logging.error("Error inserting ping result: %s", e)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyflynet")

    parser.add_argument("--ip", metavar="ip", type=str, default="8.8.8.8", help="The IP address to ping")
    parser.add_argument("--every", metavar="every", type=int, default=3, help="The delay between pings")
    parser.add_argument("--timeout", metavar="timeout", type=int, default=4, help="The timeout for each ping in seconds")

    args = parser.parse_args()

    ip = args.ip
    every = args.every
    timeout = args.timeout
    logging.info(f"Pinging {ip} every {every} seconds with a timeout of {timeout} seconds")

    create_ping_result_table()

    try:
        while True:
            start_time = time.time()
            latency, error = ping(ip, timeout)
            insert_ping_result(start_time, latency, error)
            logging.info(f"{start_time}: Latency: {latency}, Error: {error}")

            sleep_time = max(every - (time.time() - start_time), 0)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Ping monitoring stopped by user.")