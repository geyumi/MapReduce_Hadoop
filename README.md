# CryptoTrends: Minute-Level Bitcoin Trade Analysis Using Hadoop MapReduce

**Module:** Cloud Computing (EC7205)  
**Assignment:** Large-Scale Data Analysis Using MapReduce  
**Team Members:** EG/2020/3961, EG/2020/4021, EG/2020/4034  

---

## Project Summary

This project analyzes minute-level Bitcoin trading data from the `dataset btcusd_1-min_data.csv` using Hadoop MapReduce. The dataset contains OHLC (Open, High, Low, Close) and Volume data recorded at 1-minute intervals from Jan 2012 to the present.

The project aims to compute meaningful insights such as:

    Average Close Price per Day

The processing is done via **Hadoop MapReduce**.

---


## Dataset

- **Source:** Kaggle  
  https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data/data
- **Rows:** Over 1 lakhs 
- **Fields:** 
        Timestamp: UNIX epoch time (seconds)

        Open: Opening price in USD

        High: Highest price in the minute

        Low: Lowest price in the minute

        Close: Closing price in USD

        Volume: Volume of BTC traded in that minute

---


## Prerequisites
List of tools, libraries, and configurations needed before running the project:

    Java (JDK 8 or higher)

    Apache Hadoop (version 2.x or 3.x)

    HDFS configured and running

---

## Hadoop Setup 

### 1. Download and Extract Hadoop
```bash
wget https://downloads.apache.org/hadoop/common/hadoop-3.1.4/hadoop-3.1.4.tar.gz
tar -xzf hadoop-3.1.4.tar.gz
```

### 2. Configure `.bashrc`
```bash
export HADOOP_HOME=/home/geyumi/Downloads/hadoop-3.1.4   
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

### 3. Verify Hadoop
```bash
hadoop --version
```

### 4. Create HDFS Input Directory and Upload Dataset
```bash
hdfs dfs -mkdir -p /user/geyumi/bitcoin/input
hdfs dfs -put /home/geyumi/SEM07/CLOUD/MapReduce_Hadoop/cleaned_btcusd_data.csv /user/geyumi/bitcoin/input
```

---

---

## Hadoop Configuration Files

The following configuration files were updated in `$HADOOP_HOME/etc/hadoop`:

### `core-site.xml`
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

### `hdfs-site.xml`
```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/geyumi/hadoopdata/hdfs/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///home/geyumi/hadoopdata/hdfs/datanode</value>
  </property>
</configuration>
```

### `mapred-site.xml`
```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
```

### `yarn-site.xml`
```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
</configuration>
```

---


## MapReduce Scripts

### Mapper: `mapper.py`
```python

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
        continue

```

### Reducer: `reducer.py`
```python

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
```

---

## Running the Job

### 1. Make scripts executable
```bash
chmod +x mapper.py
chmod +x reducer.py
```

### 2. Run Hadoop Streaming Job
```bash
hdfs dfs -rm -r /user/geyumi/bitcoin/output/btc_average__close_per_day

hadoop jar /home/geyumi/Downloads/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar \
     -files /home/geyumi/SEM07/CLOUD/MapReduce_Hadoop/mapper.py,/home/geyumi/SEM07/CLOUD/MapReduce_Hadoop/reducer.py \
     -input /user/geyumi/bitcoin/input/cleaned_btcusd_data.csv \
     -output /user/geyumi/bitcoin/output/btc_average_close_per_day \
     -mapper "python3 mapper.py" \
     -reducer "python3 reducer.py"
```

### 3. View Output
```bash
hdfs dfs -cat /user/geyumi/bitcoin/output/btc_average_close_per_day/part-00000

```

---

## Sample Output
```
2012-01-01	4.65
2012-01-02	4.98
2012-01-03	5.09
2012-01-04	5.17
2012-01-05	5.95
2012-01-06	6.62
2012-01-07	6.05
2012-01-08	6.82

```

---

## Interpretation

### Mapper 

    -Parsed each line of the CSV.

    -Skipped the header.

    -Extracted the date (YYYY-MM-DD) and closing price from each row.

    -Emitted a key-value pair:
        date\tclose_price

### Reducer

    -Grouped all closing prices by the same date.

    -Calculated the average closing price per day.

    -Printed the results in the format:
        date\taverage_close_price

---

## Included Files

- `mapper.py`
- `reducer.py`
- `README.md`
- `preprocessing.py`
- Sample output: `part-00000` 
- Screenshots of execution 
- cleaned Dataset (uploaded to HDFS)

---
