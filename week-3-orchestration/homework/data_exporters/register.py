import mlflow

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter



@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    mlflow_host = kwargs['MLFLOW_HOST']
    experiment = kwargs['EXPERIMENT_NAME']

    mlflow.set_tracking_uri(mlflow_host)
    mlflow.set_experiment(experiment)

    mlflow.sklearn.log_model(data[0], 'home_03_dict_vectorizer')
    mlflow.sklearn.log_model(data[1], 'home_03_model')


