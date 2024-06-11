import logging
import predict
import requests

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.addHandler(logging.StreamHandler())

ride = {
    "PULocationID": 10,
    "DOLocationID": 50,
    "trip_distance": 20,
}

url = 'http://localhost:5026/predict'
response = requests.post(url, json=ride)
LOG.info(f'Prediction response: {response.json()}')