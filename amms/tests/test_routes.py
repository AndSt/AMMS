from typing import Dict

from fastapi.testclient import TestClient

from api import app
import time

client = TestClient(app)


def params_to_url(params: Dict):
    url = ''
    for key, value in params.items():
        url += '{}={}&'.format(key, value)
    return url


def test_health_status():
    response = client.get("/health_check")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['version'] == '0.0.1'
    assert time.time() - float(response_json['generated_at']) > 0


def test_meta():
    response = client.get('/meta')
    assert response is not None


def test_predict():
    # TODO get format of request and response right; push automatic testing further
    response = client.get('/meta')
    models = response.json()['models']

    for model in models:
        request = {
            'model_name': model.get('meta_data').get('model_name'),
            'version': model.get('meta_data').get('version')
        }
        request.update(model.get('request_format'))
        print("request", request)
        print(model.get('request_format'))
        response = client.post('/predict', json=model.get('request_format'))
        assert response.status_code == 200
        response = response.json()
        assert len(response.get('preds')) == 1
        assert len(response.get('pred_probas')) == 1
        assert len(response.get('pred_probas')[0]) == 20


def test_routers():
    response = client.get('/meta')
    models = response.json()['models']

    for model in models:
        request = {
            'model_name': model.get('meta_data').get('model_name'),
            'version': model.get('meta_data').get('version')
        }
        response = client.post('/predict?{}'.format(params_to_url(request)), json=model.get('request_format'))
        assert response.status_code == 200