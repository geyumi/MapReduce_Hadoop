#!/usr/bin/env python3

import sys
import csv
from datetime import datetime

# Read input line by line from stdin
for row in csv.reader(sys.stdin):
    try:
        # Skip header
        if row[0] == "Date":
            continue

        # Extract Date and Close price
        date_time_str = row[0]
        close_price = float(row[4])  # Close is at index 4

        # Extract only the date (YYYY-MM-DD)
        date = date_time_str.split(" ")[0]

        # Emit in format: date \t close_price
        print(f"{date}\t{close_price}")

    except Exception as e:
        # Handle malformed lines silently
        continue
