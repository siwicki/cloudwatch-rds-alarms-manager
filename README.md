# cloudwatch-rds-alarms-manager
Simple tool to manage Cloudwatch alarms for RDS service. At the moment this tool is limited only to alerts with Dimensions: `DBClusterIdentifier` and `DBInstanceIdentifier`

## Installation

1. Clone the repository.
2. Go into the directory: `cd cloudwatch-rds-alarms-manager`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Run `pip install boto3 ; pip install prettytable`
6. Done.

## Usage

1. Go into the directory: `cd cloudwatch-rds-alarms-manager`
2. Activate venv: `source venv/bin/activate`
3. Run `python3 main.py -h` for available options.

#### Copy
```
usage: main.py copy [-h] old_alarm_name new_alarm_name new_dimension_value

positional arguments:
  old_alarm_name       Old alarm name to copy from
  new_alarm_name       New alarm name to copy to
  new_dimension_value  New DB instance identifier or DB cluster identifier for the copied alarm

options:
  -h, --help           show this help message and exit
```

#### Search
```
usage: main.py search [-h] search_alarm_query

positional arguments:
  search_alarm_query  Partial or full alarm name to search for

options:
  -h, --help          show this help message and exit
```


## Example:

#### Search functionality:
```
$ python3 main.py search vps-virginia-aurora-22
+----------------------------------------------------------------+----------------------+--------+
|                  Alarm Name                   |    Dimension Type    |     Dimension Value     |
+-----------------------------------------------+----------------------+-------------------------+
|       testcluster1-Low-FreeLocalStorage       | DBClusterIdentifier  |       testcluster1      |
| testinstance-us-east-1c-High-CPU-Utilization  | DBInstanceIdentifier | testinstance-us-east-1c |
| testinstance-us-east-1c-High-SelectThroughput | DBInstanceIdentifier | testinstance-us-east-1c |
| testinstance-us-east-1d-High-CPU-Utilization  | DBInstanceIdentifier | testinstance-us-east-1d |
| testinstance-us-east-1d-High-SelectThroughput | DBInstanceIdentifier | testinstance-us-east-1d |
+-----------------------------------------------+----------------------+-------------------------+
```

#### Copy functionality:

```
$ python3 main.py copy testcluster1-Low-FreeLocalStorage testcluster1-COPY-Low-FreeLocalStorage testcluster1

Alarm testcluster1-COPY-Low-FreeLocalStorage created successfully.
```
