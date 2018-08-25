#!/opt/local/bin/python

import csv
import json
import boto3
def chunkit(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

kinesis = boto3.client("kinesis")
with open("data-simu.csv") as f:
    reader = csv.DictReader(f)
    records = chunkit([{"PartitionKey": "players", "Data": json.dumps(row)} for row in reader], 500)
    for chunk in records:
        kinesis.put_records(StreamName="ubiquitous-octo-spoon-stream", Records=chunk)
