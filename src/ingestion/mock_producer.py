import sys
import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

fake = Faker()

def create_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9094'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        logger.info("Kafka Producer initialized successfully.")
        return producer
    except Exception as e:
        logger.fatal(f"Failed to initialize Kafka Producer: {e}")
        sys.exit(1)

def generate_tweet():
    return {
        "id": fake.uuid4(),
        "text": fake.sentence(),
        "created_at": datetime.now().isoformat(),
        "user": fake.user_name(),
        "lang": random.choice(["en", "es", "fr"])
    }

def run_producer():
    producer = create_kafka_producer()
    topic = "tweets"
    
    logger.info(f"Starting producer for topic '{topic}'...")
    try:
        while True:
            tweet = generate_tweet()
            producer.send(topic, value=tweet)
            logger.debug(f"Sent tweet from user {tweet['user']}")
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Producer stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        producer.close()
        logger.info("Producer connection closed.")

if __name__ == "__main__":
    run_producer()
