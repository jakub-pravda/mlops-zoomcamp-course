import mlflow

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    mlflow_host = kwargs['MLFLOW_HOST']
    experiment = kwargs['EXPERIMENT_NAME']
    print('MLflow host: ', mlflow_host)

    mlflow.set_tracking_uri(mlflow_host)
    mlflow.set_experiment(experiment)
    mlflow.sklearn.autolog()
    print('MLflow setup complete')

    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']

    dv = DictVectorizer()

    train_dicts = data[categorical + numerical].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    # Training part
    target = 'duration'
    y_train = data[target].values

    model = LinearRegression()
    model.fit(X_train, y_train)
    print('Intercept:', round(model.intercept_, 2))


    return (dv, model)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
