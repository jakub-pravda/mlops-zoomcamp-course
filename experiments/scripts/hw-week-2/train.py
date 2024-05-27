# copied from
# https://raw.githubusercontent.com/DataTalksClub/mlops-zoomcamp/main/cohorts/2024/02-experiment-tracking/homework/train.py

import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mlflow.autolog()

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--mlflow_uri",
    default="http://localhost:5000",
    help="MLflow instance uri"
)
def run_train(data_path: str, mlflow_uri: str):
    mlflow.set_tracking_uri(mlflow_uri)
    mlflow.set_experiment('Default')

    with mlflow.start_run():
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)


if __name__ == '__main__':
    run_train()
