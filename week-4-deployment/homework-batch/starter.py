#!/usr/bin/env python

import click
import logging
import os
import pickle
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    logging.info(F'Reading the data from: {filename}')
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def load_model():
    logging.info('Loading the model')
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
        return dv, model

def get_output_data_frame(df, predictions, year, month):
    logging.info('Creating the output data frame')
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predictions'] = predictions
    return df_result

@click.command()
@click.option('--month', help='Taxi data set month', type=int)
@click.option('--year', help='Taxi data set year', type=int)
@click.option('--output', help='Output folder', type=str)
def predict(month, year, output):
    logging.info('Predicting the duration of the rides')

    input_parquet_path = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    
    output_file_path = os.path.join(output, f'{year:04d}-{month:02d}.parquet')

    dv, model = load_model()
    df = read_data(input_parquet_path)
    
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    
    logging.info(f'DF stats => std: {round(y_pred.std(), 2)}, mean: {round(y_pred.mean(), 2)}')

    df_result = get_output_data_frame(df, y_pred, year, month)
    df_result.to_parquet(
        output_file_path,
        engine='pyarrow',
        compression=None,
        index=False
    )

    file_size_mb = (os.path.getsize(output_file_path)) / 1024 / 1024
    logging.info(f'File size MB: {round(file_size_mb, 2)}')
    logging.info(f'Prediction complete. Output file: {output_file_path}')

if __name__ == '__main__':
    predict()
