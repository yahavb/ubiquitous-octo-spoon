# ubiquitous-octo-spoon
Streaming files from S3 to Kinesis Firehose 

[Amazon Kinesis Data Firehose](https://aws.amazon.com/kinesis/data-firehose/) offers to ingest and process streaming data, deliver streaming data, analyze streaming data, and ingest and process media streams. In this mini project, we are going to demonstrate how to continuously collect, transform, and load streaming data into destinations such as Amazon S3.
  
We use a synthetic data source located in S3 that indicates player event metrics. The dataset also, includes spatiotemporal data events denoted by `latitude` and `longitude`. The method presented herein is not limited to this data set or the data streaming model and can be extended. 

We start with (1) partitioning the data into fixed data chunks, and (2) streaming the data to a Kinesis Stream. We are going to use the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html) to `put` streaming payload into Kinesis stream.  

Finally, we will run real-time analytics to discover intersting things about the data like `HOTSPOT`s in the data source used. 

## Create Analytics Application
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/create-analytics-app.png)




## Misc
After creating the delivery stream, send source records using the Firehose PUT API or the Amazon Kinesis Agent.

Firehose PUT APIs
Use the Firehose PutRecord() or PutRecordBatch() API to send source records to the delivery stream.




## Reference
