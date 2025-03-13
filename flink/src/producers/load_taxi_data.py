import csv
import json
from kafka import KafkaProducer
import time

def main():
    # Start the timer
    start_time = time.time()

    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    csv_file = '/mnt/c/Users/tinyu/Documents/GitHub/de-zoomcamp-2025/flink-training/data/green_tripdata_2019-10.csv'  # change to your CSV file path if needed

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Each row will be a dictionary keyed by the CSV headers
            # Filter the required columns
            filtered_row = {
                'lpep_pickup_datetime': row['lpep_pickup_datetime'],
                'lpep_dropoff_datetime': row['lpep_dropoff_datetime'],
                'PULocationID': row['PULocationID'],
                'DOLocationID': row['DOLocationID'],
                'passenger_count': row['passenger_count'],
                'trip_distance': row['trip_distance'],
                'tip_amount': row['tip_amount']
            }
            # Send data to Kafka topic "green-trips"
            producer.send('green-trips', value=filtered_row)

    # Make sure any remaining messages are delivered
    producer.flush()
    producer.close()

    # Calculate and print the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {round(elapsed_time)} seconds")

if __name__ == "__main__":
    main()