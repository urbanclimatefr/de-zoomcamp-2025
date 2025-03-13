from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, TableEnvironment, StreamTableEnvironment
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Duration

def create_aggregated_sink(t_env):
    table_name = 'longest_streaks'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            streak_length BIGINT,
            PRIMARY KEY (PULocationID, DOLocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name

def create_green_trips_source_kafka(t_env):
    table_name = "green_trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime STRING,
            lpep_dropoff_datetime STRING,  
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            event_watermark AS TO_TIMESTAMP(lpep_dropoff_datetime) - INTERVAL '5' SECOND,  
            WATERMARK FOR event_watermark AS event_watermark
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name


def session_aggregation():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(3)

    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        # Create Kafka table for green-trips
        source_table = create_green_trips_source_kafka(t_env)
        aggregated_table = create_aggregated_sink(t_env)

        # Perform session window aggregation
        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            
            PULocationID,
            DOLocationID,
            SESSION_START(DESCRIPTOR(event_watermark), INTERVAL '5' MINUTE) as window_start,
            COUNT(*) AS streak_length
        FROM TABLE(
            SESSION(
                TABLE {source_table},
                DESCRIPTOR(event_watermark),
                INTERVAL '5' MINUTE
            )
        )
        GROUP BY window_start, PULocationID, DOLocationID;
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))

if __name__ == '__main__':
    session_aggregation()