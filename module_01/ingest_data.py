import subprocess
from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse
import os
import gzip

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv.gz'

    # os.system(f'wget {url} -O {csv_name}')
    subprocess.run(['wget', url, '-O', csv_name])

    # Decompress the file using gzip
    with gzip.open("output.csv.gz", "rb") as f_in, open("output.csv", "wb") as f_out:
        f_out.write(f_in.read())

    # print(pd.__version__)

    df = pd.read_csv(csv_name, nrows=100)
    print(df)

    # convert to datetime
    pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print(pickup_datetime)
    print(dropoff_datetime)

    # write back to data frame
    df.tpep_pickup_datetime = pickup_datetime
    df.tpep_dropoff_datetime = dropoff_datetime

    # connection to postgres 
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # df.to_sql(name='yellow_taxi_data', con=engine, index=False)

    # create schema
    schema = pd.io.sql.get_schema(df, name=table_name, con=engine)
    print(schema)

    # we are doing it in chunks, that way we can avoid memory issues
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pickup_datetime
    df.tpep_dropoff_datetime = dropoff_datetime

    print(len(df))

    # table headers
    df.head(n=0).to_sql(con=engine, name=table_name, if_exists='replace')

    df.to_sql(con=engine, name=table_name, if_exists='replace')



    # crap code but it works
    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(con=engine, name=table_name, if_exists='append')
        t_end = time()
        
        print('inserted another chunk...,took %.3f second' % (t_end - t_start))

if __name__ == '__main__':
    print('Ingesting data')
    parser = argparse.ArgumentParser(
                        prog='Ingest Data',
                        description='Ingest CSV data to Postgres',
                        )

    # args 
    # user, password, host, port, dbname, table_name, url of csv

    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--table_name',help='table name for postgres')
    parser.add_argument('--url',help='url for csv file')

    args = parser.parse_args()
    main(args)
