#!/usr/local/bin/python

import csv
import json
import boto3
import botocore
import os.path 
from pathlib import Path

bucket = 're-invent-2018-gaming-workshop'
#file_in_bucket= 'data-simu-short.csv'
file_in_bucket= 'player_move_events_simu.csv'

buffer_size =200
stream_name="ubiquitous-octo-spoon-stream"

s3resource = boto3.resource('s3')
s3client = boto3.client('s3', region_name='us-west-2')
kinesis = boto3.client('kinesis', region_name='us-west-2')

bucket_url="https://s3.amazonaws.com/"+bucket+"/"


def part(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def stream(file2stream):
  with open(file2stream) as f:
    reader = csv.DictReader(f)
    records = part([{"PartitionKey": "players", "Data": json.dumps(row)} for row in reader], buffer_size)
    for partition in records:
#        print(partition)
        kinesis.put_records(StreamName=stream_name, Records=partition)
        print("partition streamed")


if __name__ == '__main__':
  print("In main")
  try: 
    file2stream='/tmp/'+file_in_bucket
    print("file2stream:"+file2stream)
    if Path(file2stream).is_file():
      print("file exists "+file2stream+"...")
    else:
      print("downloading "+file2stream+"...")
      s3resource.Bucket(bucket).download_file(file_in_bucket,file2stream)
      print("file "+file2stream+" downloaded")
    print("streaming file "+file2stream)
    stream(file2stream)
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
