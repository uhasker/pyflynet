# pyflynet

## What is this?

A simple Python utility to log ping latency and errors for a specified IP address, storing the results in an SQLite database for further analysis.

## Description

This tool sends a ping to a specified IP address at regular intervals and logs the results (timestamp, latency, and any potential error messages) to an SQLite database.
This can be helpful for network troubleshooting, monitoring, and various other use cases where tracking ping response over time is useful.

## Requirements

* Python 3.8+
* SQLite 3
* ping3 Python package

## Usage

### Basic Usage

Run the script with the desired arguments:

```sh
python pyflynet.py --ip $IP_ADDRESS --db $DB_NAME --every $EVERY_SECONDS --timeout $TIMEOUT_SECONDS
```

Run `python pyflynet.py -h` to get help:

```
usage: pyflynet.py [-h] [--ip ip] [--db db] [--every every] [--timeout timeout]

pyflynet

optional arguments:
  -h, --help         show this help message and exit
  --ip ip            The IP address to ping
  --db db            The name of the SQLite database to which to save the ping results
  --every every      The delay between pings
  --timeout timeout  The timeout for each ping in seconds
```

For example, here is you can ping Google's public DNS server every 10 seconds with a timeout of 4 seconds and store the results in pyflynet.db:

```sh
python pyflynet.py --db pyflynet.db --ip 8.8.8.8 --every 10 --timeout 4
```

### Plotting Results

Run the script with the desired arguments:

```sh
python pyflynet_plot.py --db $DB_NAME --startdate $START_DATE --enddate $END_DATE
```

Run `python pyflynet_plot.py` to get help:

```
usage: pyflynet_plot.py [-h] --db db --startdate startdate --enddate enddate [--figsizex figsizex] [--figsizey figsizey]

pyflynet_plot

optional arguments:
  -h, --help            show this help message and exit
  --db db               The name of the SQLite database from which to read the ping results
  --startdate startdate
                        The start date from which to show results (e.g. 2024-01-01)
  --enddate enddate     The end date up to which to show results (e.g. 2024-02-08)
  --figsizex figsizex   The size of the figure (x axis)
  --figsizey figsizey   The size of the figure (y axis)
```

For example, here is you can plot the results from pyflynet.db starting at 2024-01-01 and ending at 2024-02-08:

```sh
python pyflynet_plot.py --db pyflynet.db --startdate 2024-01-01 --enddate 2024-02-08
```

## Run under systemd

Copy the `pyflynet.service` file to `/etc/systemd/system/pyflynet.service`

Replace:

* `$PATH_TO_YOUR_PYFLYNET_DIR` with the path containing the `pyflynet` directory
* `$USERNAME` with the name of your user

Restart the daemon and enable the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable pyflynet
sudo systemctl start pyflynet
```
