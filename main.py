import boto3
import sys
import argparse
from prettytable import PrettyTable

class text_colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'

def search_alarms(region, search_alarm_query, return_alarms=False):
    client = boto3.client('cloudwatch', region_name=region)
    paginator = client.get_paginator('describe_alarms')

    found_alarms = []
    for page in paginator.paginate():
        found_alarms.extend([alarm for alarm in page['MetricAlarms'] if search_alarm_query in alarm['AlarmName']])

    if not found_alarms:
        print(text_colors.ERROR + f"No alarms in region {region} found containing: {search_alarm_query}")
        return [] if return_alarms else None

    if return_alarms:
        return found_alarms

    table = PrettyTable()
    table.field_names = ["Alarm Name", "Dimension Type", "Dimension Value"]

    for alarm in found_alarms:
        alarm_type = "Unknown"
        dimension_value = "N/A"
        for dimension in alarm['Dimensions']:
            if dimension['Name'] in ['DBInstanceIdentifier', 'DBClusterIdentifier']:
                alarm_type = dimension['Name']
                dimension_value = dimension['Value']
                break

        table.add_row([alarm['AlarmName'], alarm_type, dimension_value])

    print(table)


def copy_cloudwatch_alarm(region, old_alarm_name, new_alarm_name, new_dimension_value):
    client = boto3.client('cloudwatch', region_name=region)

    try:
        response = client.describe_alarms(AlarmNames=[old_alarm_name])

        if not response.get('MetricAlarms'):
            print(f"No alarms found with the name: {old_alarm_name}")
            return

        old_alarm = response['MetricAlarms'][0]

        old_alarm['AlarmName'] = new_alarm_name
        for dimension in old_alarm['Dimensions']:
            if dimension['Name'] in ['DBInstanceIdentifier', 'DBClusterIdentifier']:
                dimension['Value'] = new_dimension_value
                break

        # Remove fields not needed in put_metric_alarm
        fields_to_remove = ['AlarmArn', 'StateValue', 'StateReason', 'StateReasonData', 'StateUpdatedTimestamp', 'StateTransitionedTimestamp', 'AlarmConfigurationUpdatedTimestamp', 'Metrics']
        for field in fields_to_remove:
            old_alarm.pop(field, None)

        client.put_metric_alarm(**old_alarm)
        print(text_colors.OK + f"Alarm {new_alarm_name} created successfully.")

    except Exception as e:
        print(text_colors.ERROR + f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description=text_colors.OK + 'CloudWatch RDS Alarms Manager')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Search subparser
    search_parser = subparsers.add_parser('search', help='Search for alarms')
    search_parser.add_argument('search_alarm_query', help='Partial or full alarm name to search for')

    # Copy subparser
    copy_parser = subparsers.add_parser('copy', help='Copy an alarm')
    copy_parser.add_argument('old_alarm_name', help='Old alarm name to copy from')
    copy_parser.add_argument('new_alarm_name', help='New alarm name to copy to')
    copy_parser.add_argument('new_dimension_value', help='New DB instance identifier or DB cluster identifier for the copied alarm')

    args = parser.parse_args()

    if args.command == 'search':
        search_alarms(args.region, args.search_alarm_query)
    elif args.command == 'copy':
        copy_cloudwatch_alarm(args.region, args.old_alarm_name, args.new_alarm_name, args.new_dimension_value)

if __name__ == "__main__":
    main()
