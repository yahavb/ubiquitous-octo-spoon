# ubiquitous-octo-spoon
Streaming files from S3 to Kinesis Firehose 

[Amazon Kinesis Data Firehose](https://aws.amazon.com/kinesis/data-firehose/) offers to ingest and process streaming data, deliver streaming data, analyze streaming data, and ingest and process media streams. In this mini project, we are going to demonstrate how to continuously collect, transform, and load streaming data into destinations such as Amazon S3.
  
We use a synthetic data source located in S3. The dataset includes spatiotemporal data events. This is a simulated data. The method presented herein is not limited to this data set or the data streaming model and can be extended. 

We first start partition the data into fixed data chunks. Then we use the Python boto3 library to `put` the divided data into the Kinesis data streams configured in advance. 

