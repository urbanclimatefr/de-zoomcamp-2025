## Docker and SQL

Notes I used for preparing the videos: [link](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)


## Commands 

All the commands from the video

Downloading the data

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

> Note: now the CSV data is stored in the `csv_backup` folder, not `trip+date` like previously

### Running Postgres with Docker

#### Windows

Running Postgres on Windows (note the full path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "/$(pwd)"/ny_taxi_postgres_data":/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

docker run -it    -e POSTGRES_USER="root"    -e POSTGRES_PASSWORD="root"    -e POSTGRES_DB="ny_taxi"    -v $(pwd)"/ny_taxi_postgres_data:/var/lib/postgresql/data    -p 5432:5431    postgres:13

If you have the following error:

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v e:/zoomcamp/data_engineer/week_1_fundamentals/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data  \
  -p 5432:5432 \
  postgres:13

docker: Error response from daemon: invalid mode: \Program Files\Git\var\lib\postgresql\data.
See 'docker run --help'.
```

Change the mounting path. Replace it with the following:

```
-v /e/zoomcamp/...:/var/lib/postgresql/data
```

#### Linux and MacOS


```bash
docker run -it    -e POSTGRES_USER="root"    -e POSTGRES_PASSWORD="root"     -e POSTGRES_DB="ny_taxi"     -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data    -p 5432:5432    postgres:13

docker run -it    -e POSTGRES_USER="root"    -e POSTGRES_PASSWORD="root"    -e POSTGRES_DB="ny_taxi"    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data    -p 5432:5432    postgres:13 

docker volume create --name dtc_postgres_volume_local -d local

    docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     -v dtc_postgres_volume_local:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:13
```

If you see that `ny_taxi_postgres_data` is empty after running
the container, try these:

* Deleting the folder and running Docker again (Docker will re-create the folder)
* Adjust the permissions of the folder by running `sudo chmod a+rwx ny_taxi_postgres_data`


### CLI for Postgres

Installing `pgcli`

```bash
pip install pgcli
```

If you have problems installing `pgcli` with the command above, try this:

```bash
conda install -c conda-forge pgcli
pip install -U mycli
```

Using `pgcli` to connect to Postgres

```bash
 sudo python3 -m venv /mnt/c/Users/tinyu/Documents/GitHub/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql/

 source /mnt/c/Users/tinyu/Documents/GitHub/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql/bin/activate

pip instal pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi

pip install pandas==2.0.0  
pip install sqlalchemy==1.4.16 
pip install psycopg2-binary
pip install pyarrow ( for parquet file)

    docker run -it \
     -e POSTGRES_USER=root \
     -e POSTGRES_PASSWORD=root \
     -e POSTGRES_DB=ny_taxi \
     -p 5431:5432 \
     postgres:13

pgcli -h localhost -p 5431 -U root -d ny_taxi
```


### NY Trips Dataset

Dataset:

* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
* https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

> According to the [TLC data website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page),
> from 05/13/2022, the data will be in ```.parquet``` format instead of ```.csv```
> The website has provided a useful [link](https://www1.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf) with sample steps to read ```.parquet``` file and convert it to Pandas data frame.
>
> You can use the csv backup located here, https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz, to follow along with the video.
```
$ aws s3 ls s3://nyc-tlc
                           PRE csv_backup/
                           PRE misc/
                           PRE trip data/
```

You can refer the `data-loading-parquet.ipynb` and `data-loading-parquet.py` for code to handle both csv and paraquet files. (The lookup zones table which is needed later in this course is a csv file)
> Note: You will need to install the `pyarrow` library. (add it to your Dockerfile)


### pgAdmin

Running pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

### Running Postgres and pgAdmin together

Create a network

```bash
docker network create pg-network
```

Run Postgres (change the path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)$/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5431 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

docker volume create --name dtc_postgres_volume_local -d local

    docker run -it \
     -e POSTGRES_USER="root" \
     -e POSTGRES_PASSWORD="root" \
     -e POSTGRES_DB="ny_taxi" \
     -v dtc_postgres_volume_local:/var/lib/postgresql/data \
     -p 5432:5431 \
     --network=pg-network \
     --name pg-database \
     postgres:13




Run pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```


### Data ingestion

Running locally

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

Build the image

```bash
docker build -t taxi_ingest:v001 .
```

On Linux you may have a problem building it:

```
error checking context: 'can't stat '/home/name/data_engineering/ny_taxi_postgres_data''.
```

You can solve it with `.dockerignore`:

* Create a folder `data`
* Move `ny_taxi_postgres_data` to `data` (you might need to use `sudo` for that)
* Map `-v $(pwd)/data/ny_taxi_postgres_data:/var/lib/postgresql/data`
* Create a file `.dockerignore` and add `data` there
* Check [this video](https://www.youtube.com/watch?v=tOr4hTsHOzU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) (the middle) for more details 



Run the script with Docker

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

### Docker-Compose 

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```

Note: to make pgAdmin configuration persistent, create a folder `data_pgadmin`. Change its permission via

```bash
sudo chown 5050:5050 data_pgadmin
```

and mount it to the `/var/lib/pgadmin` folder:

```yaml
services:
  pgadmin:
    image: dpage/pgadmin4
    volumes:
      - ./data_pgadmin:/var/lib/pgadmin
    ...
```


When you run docker-compose up, Docker Compose creates a default network for the services defined in your docker-compose.yml file. The network is usually named based on the project directory and some default conventions. Here's an overview of the default network setup:

Default Network Name
By default, Docker Compose creates a network named <project_name>_<default_network_name>, where:
<project_name> is derived from the name of the directory containing the docker-compose.yml file (or can be manually specified with the -p flag).
<default_network_name> is typically default.

procedure:

sudo python3 -m venv /mnt/c/Users/tinyu/Documents/GitHub/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql/

source /mnt/c/Users/tinyu/Documents/GitHub/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql/bin/activate

docker volume create --name dtc_postgres_volume_local -d local

docker-compose up

docker build -t taxi_ingest:v001 .  
  
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

docker run -it \
  --network=2_docker_sql_pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=${URL}


SQL

SELECT
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS up_to_1_mile,
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS between_1_and_3_miles,
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS between_3_and_7_miles,
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS between_7_and_10_miles,
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS over_10_miles
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';


SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS longest_trip_distance
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01'
GROUP BY pickup_day
ORDER BY longest_trip_distance DESC
LIMIT 1;