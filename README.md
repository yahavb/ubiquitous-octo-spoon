# ubiquitous-octo-spoon
Continuous Hotspot Detection of Spatiotemporal Metrics using AWS Kinesis (Data Stream, Data Firehose, and Data Analytics)

In this mini project, we demonstrate how to continuously discover hotspots and other events insights in real-time by streaming, gathering streamed data, and analyzing the data for dynamic emerging objects like players moves patterns. For simplicity and robustness, we use AWS Kinesis tools for the real-time data pipeline. One can use [Lambda Architecture using Kafka and Spark Streaming] (https://spark.apache.org/docs/latest/streaming-kafka-integration.html) for achieving the same goal. 
  
We use a synthetic data source that was uploaded in advance to S3 that indicates player event metrics. The dataset also includes spatiotemporal data events denoted by `latitude` and `longitude`. 

We start with (1) partitioning the data into fixed data chunks using the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html), and (2) streaming the data to a Kinesis Stream. Finally, we provision a Kinesis Data Firehose for continuous collection, transformation, and loading the streamed data into Kinesis Data Analytics that uses pre-defined `HOTSPOT` function for player hotspot detection. 

## The Data Flow
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/data-flow.png)
We use the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html) to `put` simulated streaming payload into Kinesis Data Stream. To start the simulation, we deployed the script [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py) as a container in [ECS](https://aws.amazon.com/ecs/). Ideally, the simulation script would run using AWS Lambda Function. However, stream-simu.py writes to the OS filesystem when reading files from S3. AWS Lambda does not allow writes to files during function execution.  

## The Setup Process 
The continouos hotspot detection system comprises of four main components:
* Configure and run a Kinesis Data Stream - `ubiquitous-octo-spoon-stream`
* Write data to the stream using simulated streaming from many players [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py). 
* Configure and run Kinesis Data Firehose delivery system - `ubiquitous-octo-spoon-delivery`
* Configure and run Kinesis Data Analytics for hotspot detection - `ubiquitous-octo-spoon-stream-app`

### Create Kinesis Data Stream
The Data Stream system ingest by multiple data-processing of custom application workloads. Its core functionality is the ability to horizontally scale in form of shards. A shard is a unit of throughput capacity. To accommodate for higher or lower throughput, a number of shards needs to be defined. In our example we set the number of shards to `2`
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/data-stream.png)

To create a data stream, click on create kinesis streams, set the name and the number shards. 

### Write Data to the Stream 
Get access to S3 bucket where `data-simu.csv` is. Download and deploy 

### Create Kinesis Data Firehose

## Create Analytics Application
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/create-analytics-app.png)




## Misc
After creating the delivery stream, send source records using the Firehose PUT API or the Amazon Kinesis Agent.

Firehose PUT APIs
Use the Firehose PutRecord() or PutRecordBatch() API to send source records to the delivery stream.




## Reference
