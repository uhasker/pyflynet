import argparse
import time
from typing import Union, Tuple, Optional

import ping3
import sqlite3


def ping(ip_addr: str, timeout: int) -> Tuple[Optional[float], Optional[str]]:
    try:
        result = ping3.ping(ip_addr, timeout=timeout)
        if result is not None:
            return result, None
        else:
            return None, "Ping timed out"
    except Exception as e:
        return None, str(e)


def create_ping_result_table(db_name: str) -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ping_results (
        timestamp FLOAT,
        latency FLOAT,
        error TEXT
    )
    """
    )
    conn.commit()
    conn.close()


def insert_ping_result(
    db_name: str, timestamp: float, latency: Union[float, None], error: Union[str, None]
) -> None:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO ping_results (timestamp, latency, error) VALUES (?, ?, ?)
    """,
        (timestamp, latency, error),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyflynet")

    parser.add_argument(
        "--ip", metavar="ip", type=str, default="8.8.8.8", help="The IP address to ping"
    )
    parser.add_argument(
        "--db",
        metavar="db",
        type=str,
        default="pyflynet.db",
        help="The name of the SQLite database to which to save the ping results",
    )
    parser.add_argument(
        "--every",
        metavar="every",
        type=int,
        default=5,
        help="The delay between pings",
    )
    parser.add_argument(
        "--timeout",
        metavar="timeout",
        type=int,
        default=4,
        help="The timeout for each ping in seconds",
    )

    args = parser.parse_args()

    db = args.db
    ip = args.ip
    every = args.every
    timeout = args.timeout
    print(
        f"Pinging {ip} every {every} seconds with a timeout of {timeout} seconds and saving results to {args.db}"
    )

    create_ping_result_table(db)

    last_ping_time = None

    while True:
        last_ping_time = time.time()
        latency, error = ping(ip, timeout)
        ping_end = time.time()

        next_time = time.time()
        insert_ping_result(db, last_ping_time, latency, error)
        print(f"{last_ping_time}: Latency: {latency}, Error: {error}")

        current_time = time.time()
        elapsed_time = next_time - current_time
        sleep_time = max(every - elapsed_time, 0)

        time.sleep(sleep_time)
