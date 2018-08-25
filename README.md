# ubiquitous-octo-spoon
Continuous Hotspot Detection of Spatiotemporal Metrics using AWS Kinesis (Data Stream, Data Firehose, and Data Analytics)

In this mini project, we demonstrate how to continuously discover hotspots by streaming, gathering streamed data, and analyzing the data for emerging objects hotspots.
  
We use a synthetic data source located in S3 that indicates player event metrics. The dataset also includes spatiotemporal data events denoted by `latitude` and `longitude`. 

We start with (1) partitioning the data into fixed data chunks, and (2) streaming the data to a Kinesis Stream. We are going to use the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html) to `put` streaming payload into Kinesis Data Stream. To start the simulation, we deployed the script [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py) as a container within the same region as the region the Kinesis Data Stream, Firehose, and Analytics runs. 

Finally, we provision a Kinesis Data Firehose for continuous collection, transformation, and loading the streamed data into Kinesis Data Analytics that uses pre-defined `HOTSPOT` function for player hotspot detection. 

## The Process 
The continouos hotspot detection system comprises of four main components:
* Simulated streaming from many players [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py)
* Kinesis Data Stream - `ubiquitous-octo-spoon-stream`
* Kinesis Data Firehose - `ubiquitous-octo-spoon-delivery`
* Kinesis Data Analytics - `ubiquitous-octo-spoon-stream-app`

## Create Analytics Application
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/create-analytics-app.png)




## Misc
After creating the delivery stream, send source records using the Firehose PUT API or the Amazon Kinesis Agent.

Firehose PUT APIs
Use the Firehose PutRecord() or PutRecordBatch() API to send source records to the delivery stream.




## Reference
