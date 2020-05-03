from src.model_wrapper import ModelWrapper, ModelStatus
from src.data_models.prediction_requests import TextPredictionRequest
from src.data_models.prediciton_responses import PredictionResponse


class HelloWorldModel(ModelWrapper):
    def __init__(self, file_path):
        self.file_path = file_path
        self.status = ModelStatus.LOADED
        # super(HelloWorldModel, self).__init__(file_path=file_path)

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
        try:
            return True
        except Exception as e:
            return False

    def request_format(self):
        return TextPredictionRequest

    def response_format(self):
        return PredictionResponse
