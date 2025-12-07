import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Constants
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def get_twitter_schema():
    return StructType([
        StructField("id", StringType(), True),
        StructField("text", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("user", StringType(), True),
        StructField("lang", StringType(), True)
    ])

def create_spark_session():
    try:
        session = SparkSession.builder \
            .appName("SentimentAnalysisIngestion") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .getOrCreate()
        logger.info("Spark Session created successfully.")
        return session
    except Exception as e:
        logger.error(f"Failed to create Spark Session: {e}")
        sys.exit(1)

def process_stream():
    spark = create_spark_session()
    
    logger.info("Initializing Kafka stream...")
    
    try:
        # Read from Kafka
        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "sentiment-cluster-kafka-bootstrap.kafka-system.svc:9092") \
            .option("subscribe", "tweets") \
            .option("startingOffsets", "latest") \
            .load()
        
        logger.debug("Kafka stream loaded successfully.")

        # Parse JSON
        twitter_schema = get_twitter_schema()
        parsed_df = df.select(
            from_json(col("value").cast("string"), twitter_schema).alias("data"),
            col("timestamp")
        ).select("data.*", "timestamp")

        # Basic Transformation
        clean_df = parsed_df.filter(parsed_df.text.isNotNull())

        if DEBUG_MODE:
            logger.debug("Debug mode enabled: Writing stream to console.")
            output_format = "console"
        else:
            logger.info("Writing stream to downstream processors.")
            # Placeholder for actual output (e.g., Qdrant or another topic)
            output_format = "console" 

        query = clean_df \
            .writeStream \
            .outputMode("append") \
            .format(output_format) \
            .start()

        logger.info("Stream processing started.")
        query.awaitTermination()
        
    except Exception as e:
        logger.error(f"Error in stream processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_stream()
