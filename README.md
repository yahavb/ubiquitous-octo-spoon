# ubiquitous-octo-spoon
Continuous Hotspot Detection of Spatiotemporal Metrics using AWS Kinesis (Data Stream, Data Firehose, and Data Analytics)

In this mini project, we demonstrate how to continuously discover hotspots and other events insights in real-time by streaming, gathering streamed data, and analyzing the data for dynamic emerging objects like players moves patterns. We build real-time, fully-managed, and scalable data processing architecture that enables dynamic event patterns. For simplicity and robustness, we use AWS Kinesis tools for the real-time data pipeline. One can use [Lambda Architecture using Kafka and Spark Streaming] (https://spark.apache.org/docs/latest/streaming-kafka-integration.html) for achieving the same goal. 
  
We use a synthetic data source that was uploaded in advance to S3 that indicates player event metrics. The dataset also includes spatiotemporal data events denoted by `latitude` and `longitude`. 

We start with (1) partitioning the data into fixed data chunks using the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html), and (2) streaming the data to a Kinesis Data Stream. Finally, we provision a Kinesis Data Firehose for continuous collection, transformation, and loading the streamed data into Kinesis Data Analytics that uses pre-defined `HOTSPOT` function for player hotspot detection. 

## The Data Flow
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/data-flow.png)

We use the [Python boto3 library](https://boto3.readthedocs.io/en/latest/reference/services/kinesis.html) to `put` simulated streaming payload into Kinesis Data Stream. To start the simulation, we deployed the script [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py) as a container in [ECS](https://aws.amazon.com/ecs/). Ideally, the simulation script would run using AWS Lambda Function. However, stream-simu.py writes to the OS filesystem when reading files from S3. AWS Lambda does not allow writes to files during function execution. 

The Kinesis Data Stream endpoint continuously capture and temporarily store real-time data and the Kinesis Analytics application continuously read and process data from streaming sources in real-time. 

## The Setup Process 
The continuous hotspot detection system comprises four main components:
* Configure and run a Kinesis Data Stream - `ubiquitous-octo-spoon-stream`
* Write data to the stream using simulated streaming from many players [stream-simu.py](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/stream-simu.py). 
* Configure and run Kinesis Data Analytics for hotspot detection - `ubiquitous-octo-spoon-stream-app`
* Configure Kinesis Data Firehose for delivering hotspots insights to S3 - `ubiquitous-octo-spoon-delivery`

![alt_text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/arch.png)

### Create Kinesis Data Stream
The Data Stream system ingest by multiple data-processing of custom application workloads. Its core functionality is the ability to horizontally scale in the form of shards. A shard is a unit of throughput capacity. To accommodate for higher or lower throughput, some shards need to be defined. In our example, we set the number of shards to `2`
![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/data-stream.png)

To create a data stream, click on create kinesis streams, set the name and the number shards. 

### Write Data to the Stream 
* Deploy the data in S3 bucket. `data-simu.csv` in our case. 
* Create ECS Image Repository
* Create ECS Cluster
* Create ECS Task that specifies the container information for `stream-simu.py`, such as how many containers are part of the task, what VM to be used, and how they are linked together.
* Run the ECS task 

For brevity, we will skip the ECS setup details. 

### Create Analytics Application
The first step in creating the Kinesis Analytics application is connecting to streaming data. Choose the Data Stream created above. In the case of many streams, pay attention to the `In-application stream name`. The first stream name usually follows the pattern `SOURCE_SQL_STREAM_001` where `001` denotes the data streams increments. Finally, click on Discover Schema while data is streamed. 

The final step in the set is to author the SQL queries or add SQL from templates to analyze the streamed source data. Click Go to SQL Editor. 

![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/real-time-analytics.png)

In the Real-time analytics, insert the SQL below. We first capture the fields to be analyzed, `longitude` and `latitude` in our case. Finally, we create a `PUMP` objects that is loaded with the streamed `longitude` and `latitude` data. The `HOTSPOTS` function is a new Kinesis Data Analytics SQL function you can use to idenitfy relatively dense regions in your data without having to explicity build and train complicated machine learning models. In this section we wish to identify subsections of `longitude` and `latitude`. Therefore, the `PUMP` uses `HOTSPOTS` captured in `SOURCE_SQL_STREAM_001`.

```
CREATE OR REPLACE STREAM sql_stream (
    "longitude" DOUBLE,
    "latitude" DOUBLE,
    result VARCHAR(10000)
); 
CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO sql_stream 
    SELECT "longitude", "latitude", result FROM
        TABLE(HOTSPOTS(
            CURSOR(SELECT STREAM * FROM "SOURCE_SQL_STREAM_001"),
            1000,
            0.013,
            20
        )
    );
```
### Create Kinesis Firehose
The final step in our data-pipeline setup is delivering the data to its final destination. We use Kinesis Firehose for this step. Kinesis Firehose currently supports, S3, Redshift, ElasticSearch Service, and Splunk. For simplicity we use S3. 

![alt text](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/data-firehose.png)

The following IAM role is required to enable Kinesis Firehose access to S3. We used [firehose_delivery_role.json](https://github.com/yahavb/ubiquitous-octo-spoon/blob/master/firehose_delivery_role.json)

```
{
   "Effect": "Allow",
   "Action": [
     "s3:Get*",
     "s3:List*"
   ],
   "Resource": "MY_BUCKET"
}
```

## Conclusions
In this mini-project, we built real-time, fully-managed, and scalable data processing architecture that enables dynamic event patterns (HOTSPOTS) using AWS Kinesis.  
Data processing architecture aims to satisfy the needs for a robust system that is fault-tolerant, both against hardware failures and human mistakes, being able to serve a wide range of workloads and use cases, and in which low-latency reads and updates are required. The resulting system should be linearly scalable, and it should scale out rather than up. Setting up a scalable and fault-tolerant data processing architecture involves knowledge and maintenance efforts. AWS Kinesis does all of that for you. It is reliable, easy to use resulting quick turnaround in development and production environments. 

## Credits
* [Real-Time Hotspot Detection in Amazon Kinesis Analytics](https://aws.amazon.com/blogs/aws/real-time-hotspot-detection-in-amazon-kinesis-analytics/)
* [Lambda Architecture using Kafka and Spark Streaming](https://spark.apache.org/docs/latest/streaming-kafka-integration.html)
http://lambda-architecture.net
* [Lambda Architecture](http://lambda-architecture.net)
