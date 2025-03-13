FROM python:3.9.1

RUN apt-get install wget
RUN pip install numpy==1.22.3 pandas==2.0.0 sqlalchemy==1.4.16 psycopg2-binary pyarrow 

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]


