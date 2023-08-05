import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

features = [
    'energy', 'liveness', 'tempo', 'speechiness',
    'acousticness', 'instrumentalness', 'danceability',
    'duration_ms', 'loudness', 'valence'
]


def train(data, trained_output, scaled_output):
    scaler = StandardScaler()
    nn = MLPClassifier(hidden_layer_sizes=8, max_iter=15000, alpha=1.0)

    x = data[features]
    y = data['mood']

    scaled = scaler.fit_transform(x)
    nn.fit(scaled, y)

    with open(trained_output, 'wb') as f:
        pickle.dump(nn, f)

    with open(scaled_output, 'wb') as f:
        pickle.dump(scaler, f)


def predict(data, trained_path, scaled_path):
    x = data[features]

    with open(trained_path, 'rb') as f:
        nn = pickle.load(f)

    with open(scaled_path, 'rb') as f:
        scaler = pickle.load(f)

    transformed = scaler.transform(x)
    y = nn.predict(transformed)
    result = pd.DataFrame(data['id'])
    result[features] = x
    result['mood'] = y

    return result
