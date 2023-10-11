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

Run the script with desired arguments:

```sh
python pyflynet.py --ip $IP_ADDRESS --every $EVERY_SECONDS --timeout $TIMEOUT_SECONDS
```

Run `python pyflynet.py -h` to get help:

```sh
usage: pyflynet.py [-h] [--ip ip] [--db db] [--every every] [--timeout timeout]

pyflynet

optional arguments:
  -h, --help         show this help message and exit
  --ip ip            The IP address to ping
  --db db            The name of the SQLite database to which to save the ping results
  --every every      The delay between pings
  --timeout timeout  The timeout for each ping in seconds
```

### Example

Ping Google's public DNS server every 10 seconds with a timeout of 4 seconds and store the results in pyflynet.db:

```sh
python pyflynet.py --db pyflynet.db --ip 8.8.8.8 --every 10 --timeout 4
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
