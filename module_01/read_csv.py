import pandas as pd

print(pd.__version__)

df = pd.read_csv('./yellow_tripdata_2021-01.csv', nrows=100)
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
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
# df.to_sql(name='yellow_taxi_data', con=engine, index=False)

# create schema
schema = pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine)
print(schema)

# we are doing it in chunks, that way we can avoid memory issues
df_iter = pd.read_csv('./yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

df = next(df_iter)

df.tpep_pickup_datetime = pickup_datetime
df.tpep_dropoff_datetime = dropoff_datetime

print(len(df))

# table headers
df.head(n=0).to_sql(con=engine, name='yellow_taxi_data', if_exists='replace')

df.to_sql(con=engine, name='yellow_taxi_data', if_exists='replace')


from time import time

# crap code but it works
while True:
    t_start = time()
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(con=engine, name='yellow_taxi_data', if_exists='append')
    t_end = time()
    
    print('inserted another chunk...,took %.3f second' % (t_end - t_start))