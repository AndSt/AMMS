import os

from src.model_wrapper import ModelWrapper
from src.data_models import TextPredictionRequest, LabelScoreResponse

# TODO all model tests
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = '{}/data/loaded/hello_world-1_0_1-1234.pbz2'.format(dir_path)


class PassingModel(ModelWrapper):
    def predict(self, samples: TextPredictionRequest):
        return {
            'model_name': 'model'
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        try:
            return True
        except Exception as e:
            return False

    def request_format(self):
        return TextPredictionRequest

    def response_format(self):
        return LabelScoreResponse


class NoRequestFormatModel(ModelWrapper):
    def predict(self, samples: TextPredictionRequest):
        # Here is supposed to be a prediction
        return {
            'model_name': self.meta_data.model_name,
            "version": self.meta_data.version,
            'timestamp': self.meta_data.timestamp,
            "classes": 'Hello World!',
            "classes_proba": [('Hello World!', 0.9), ('Not Hello World!', 0.1)]
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.') -> bool:
        try:
            return True
        except Exception as e:
            return False

    def response_format(self):
        return LabelScoreResponse


class TestPredictionNoBoolModel(ModelWrapper):
    def predict(self, samples: TextPredictionRequest):
        # Here is supposed to be a prediction
        return {
            'model_name': self.meta_data.model_name,
            "version": self.meta_data.version,
            'timestamp': self.meta_data.timestamp,
            "classes": 'Hello World!',
            "classes_proba": [('Hello World!', 0.9), ('Not Hello World!', 0.1)]
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        return 'test'

    def request_format(self):
        return TextPredictionRequest

    def response_format(self):
        return LabelScoreResponse


def test_passing_model():
    model = PassingModel(model_path)


def test_no_request_format_model():
    try:
        model = NoRequestFormatModel(model_path)
        assert False
    except Exception as e:
        print(e)
        assert True


def test_prediction_no_bool_model():
    try:
        model = TestPredictionNoBoolModel(model_path)
        assert False
    except Exception as e:
        print(e)
        assert True
