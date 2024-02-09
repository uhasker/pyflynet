import argparse
import sqlite3
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def preprocess_df(df: pd.DataFrame, start_date: str, end_date: str):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Filter the DataFrame for rows between the start and end dates
    mask = (df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)
    df = df.loc[mask]

    # Handle NULL/None in 'latency' column by replacing it with a high value
    df['latency'].fillna(5, inplace=True)

    # Calculate Simple Moving Average (SMA) for latency
    df['latency_sma'] = df['latency'].rolling(window=5, min_periods=1).mean()

    return df


def plot_latency(df: pd.DataFrame, figsize_x: int = 32, figsize_y: int = 24, hour_interval: int = 10) -> None:
    average_latency = df['latency'].mean()

    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    ax.plot(df['timestamp'], df['latency_sma'], label='Latency (SMA)', color='blue')
    ax.axhline(y=average_latency, color='r', linestyle='--', label=f'Average Latency ({average_latency:.2f})')

    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Latency (ms)')
    ax.set_title('Ping Latency over Time')
    ax.grid(True)
    ax.legend()

    # Improve x-axis formatting and readability
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=hour_interval))  # adjust interval as needed
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.show()


def plot_latency_distribution_by_hour(df: pd.DataFrame, figsize_x: int = 32, figsize_y: int = 24):
    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    data_to_plot = [df[df['timestamp'].dt.hour == hour]['latency'] for hour in range(24)]

    ax.boxplot(data_to_plot, positions=range(24), showfliers=False)

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Latency (s)')
    ax.set_title('Latency Distribution by Hour of Day')
    ax.set_xticks(range(24))  # Set x-ticks to show every hour
    ax.set_xticklabels(range(24), rotation=90)  # Rotate x-axis labels for readability

    ax.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyflynet_plot")

    parser.add_argument(
        "--db",
        metavar="db",
        type=str,
        help="The name of the SQLite database from which to read the ping results",
        required=True,
    )
    parser.add_argument(
        "--startdate",
        metavar="startdate",
        type=str,
        help="The start date from which to show results (e.g. 2024-01-01)",
        required=True
    )
    parser.add_argument(
        "--enddate",
        metavar="enddate",
        type=str,
        help="The end date up to which to show results (e.g. 2024-02-08)",
        required=True
    )
    parser.add_argument(
        "--figsizex",
        metavar="figsizex",
        type=int,
        default=32,
        help="The size of the figure (x axis)",
    )
    parser.add_argument(
        "--figsizey",
        metavar="figsizey",
        type=int,
        default=24,
        help="The size of the figure (y axis)",
    )

    args = parser.parse_args()

    db = args.db
    start_date = args.startdate
    end_date = args.enddate
    figsize_x = args.figsizex
    figsize_y = args.figsizey

    conn = sqlite3.connect(db)

    query = "SELECT * FROM ping_results"

    df = pd.read_sql_query(query, conn)

    conn.close()

    df = preprocess_df(df, start_date, end_date)
    plot_latency(df, figsize_x, figsize_y)
    plot_latency_distribution_by_hour(df, figsize_x, figsize_y)
