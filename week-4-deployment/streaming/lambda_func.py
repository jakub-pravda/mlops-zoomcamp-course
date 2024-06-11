import base64
import boto3
import json
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.addHandler(logging.StreamHandler())

kinesis_client = boto3.client('kinesis', region='eu-central-1')

STREAM_NAME='ride_predictions'

dict_vectorizer = None
model = None

with open('../models/lin_reg.bin', 'rb') as f_in:
    LOG.info('Loading model')
    (dict_vectorizer, model) = pickle.load(f_in)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = f'{ride["PULocationID"]}_{ride["DOLocationID"]}'
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    X = dict_vectorizer.transform(features)
    predictions = model.predict(X)
    return float(predictions[0])

def lambda_handler(event, context):
    LOG.info('Running predictions')
    LOG.info(json.dumps(event))
    
    predictions = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
        
        features = prepare_features(ride)
        prediction = predict(features)
        
        LOG.info(ride_event)
        prediction_event = {
            'model': 'ride_duration_model',
            'version:': '26.10',
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }
        
        # Put records to the kinesis
        kinesis_put_result = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id)
        )
        LOG.info('Kinesis put result: ', kinesis_put_result)
        LOG.info('Sent to the kinesis, streaming pipeline: ', STREAM_NAME)
        
        predictions.append(prediction_event)
    
    return {
        'predictions': predictions
    }
