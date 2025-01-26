FROM python:3.9

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

# ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "python", "ingest_data.py" ]