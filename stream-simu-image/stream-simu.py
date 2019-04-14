#!/usr/local/bin/python

import sys
import csv
import json
import boto3
import botocore
import os.path 
from pathlib import Path

bucketname = os.environ['SRC_DATA_BUCKET']
prefix= os.environ['PREFIX']
buffer_size = os.environ['BUFFER_SIZE']
stream_name= os.environ['STREAM_NAME']

s3resource = boto3.resource('s3')
# Example of Kinesis Data Stream
#kinesis = boto3.client('kinesis', region_name='us-west-2')

# Example of Kinesis Firehose
firehose = boto3.client('firehose', region_name='us-west-2')


def part(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def stream(file2stream):
  print("in stream: using file2stream "+file2stream)
  try:
    with open(file2stream) as f:
      reader = csv.DictReader(f)
      # Example of kinesis
      # records = part([{"PartitionKey": "players", "Data": json.dumps(row)} for row in reader], int(buffer_size))
      # Example of Firehose
      print("partitioning the file to "+buffer_size)
      records = part([{"Data": json.dumps(row)} for row in reader], int(buffer_size))
      print("putting records into kinesis firhose "+stream_name)
      for partition in records:
        # print(partition)
        # Example of kinesis
        #kinesis.put_records(StreamName=stream_name, Records=partition)
        # Example of Firehose
        response=firehose.put_record_batch(
             DeliveryStreamName=stream_name,
             Records=partition
        )
        #print("partition streamed repsonse "+str(response))
        sys.stdout.write('.')
        sys.stdout.flush()
      print("file2stream "+file2stream+" was streamed")
  except (IOError, EOFError) as e:
    print("ERROR {}".format(e.args[-1]))


if __name__ == '__main__':
  print("In main")
  print("bucketname="+bucketname)
  print("prefix="+prefix)
  try: 
    bucket = s3resource.Bucket(bucketname)
    while True:
      for filename in bucket.objects.filter(Prefix=prefix):
        print(filename)
        if (filename.key!=prefix):
          file_in_bucket=str(filename.key)
          file2stream='/tmp/'+file_in_bucket
          print("file2stream:"+file2stream)
          if Path(file2stream).is_file():
            print("file exists "+file2stream+"...")
          else:
            print("downloading "+file2stream+"...")
            s3resource.Bucket(bucketname).download_file(file_in_bucket,file2stream)
            print("file "+file2stream+" downloaded")
          print("streaming file "+file2stream)
          stream(file2stream)
  except Exception as e:
    print(str(e))
