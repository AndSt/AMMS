from src.model_wrapper import ModelWrapper, ModelStatus
from src.data_models import LabelScoreResponse, TextPredictionRequest, TextRequest


class HelloWorldModel(ModelWrapper):
    def __init__(self, file_path):
        self.file_path = file_path
        self.status = ModelStatus.LOADED
        # super(HelloWorldModel, self).__init__(file_path=file_path)

    def predict(self, samples: TextPredictionRequest):
        # Here is supposed to be a prediction
        return {
            "preds": ['Hello World!'],
            "pred_probas": [[('Hello World!', 0.9), ('Not Hello World!', 0.1)]]
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        try:
            return True
        except Exception as e:
            return False

    def request_format(self):
        return TextRequest

    def response_format(self):
        return LabelScoreResponse
