#!/usr/bin/env python3

import sys

current_date = None
total = 0.0
count = 0

# Process each line from mapper
for line in sys.stdin:
    line = line.strip()
    date, close = line.split('\t')

    try:
        close = float(close)
    except ValueError:
        continue

    # If we're still on the same date, accumulate
    if current_date == date:
        total += close
        count += 1
    else:
        # Output result for the previous date
        if current_date:
            avg = total / count
            print(f"{current_date}\t{avg:.2f}")

        # Reset counters for new date
        current_date = date
        total = close
        count = 1

# Print the last date's average
if current_date:
    avg = total / count
    print(f"{current_date}\t{avg:.2f}")
