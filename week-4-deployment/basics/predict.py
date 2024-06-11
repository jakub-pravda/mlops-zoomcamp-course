import logging
import pickle

from flask import Flask, request, jsonify

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.addHandler(logging.StreamHandler())

with open('../models/lin_reg.bin', 'rb') as f_in:
    LOG.info('Loading model')
    (dict_vectorizer, model) = pickle.load(f_in)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = f'{ride["PULocationID"]}_{ride["DOLocationID"]}'
    features['trip_distance'] = ride['trip_distance']
    return features

app = Flask('duration_predictor')

def predict(features):
    X = dict_vectorizer.transform(features)
    predictions = model.predict(X)
    return predictions

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    prediction = predict(features)

    result = {
        'durtation': prediction[0]
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5026)