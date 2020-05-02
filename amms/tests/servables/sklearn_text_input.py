from typing import Union, List

import numpy as np

from src.servable_base import ServableStatus
from src.model_wrapper import ModelWrapper
from src.data_models.prediction_requests import TextPredictionRequest
from src.data_models.prediciton_responses import PredictionResponse
from pydantic import BaseModel


class SklearnTextInputPredictionInput(BaseModel):
    samples: Union[str, List[str]]


class SklearnTextInputModel(ModelWrapper):
    def __init__(self, file_path):
        super(SklearnTextInputModel, self).__init__(file_path=file_path)

        # loads model from source and checks whether prediction works
        # That's basically runtime testing. This is intended, as a core requirement is to enable the server to load
        # arbitrary local_servables

    def validate_input(self, samples: Union[str, List[str]]):
        # TODO error handling; Do we have to do this or can we deal with this with pedantic?? aka. how to do dynamic pydantic class
        return True

    def predict(self, samples: SklearnTextInputPredictionInput):
        samples = samples.samples
        self.validate_input(samples.samples)

        num_samples = len(samples)
        if num_samples == 1:
            samples = [samples]

        preds = self.model.predict_proba(samples)
        pred_probas = zip(self.model.classes_, preds)
        preds = np.argmax(preds, axis=1)
        self.status = ServableStatus.IDLE
        return {
            'model_name': self.meta_data.model_name,
            "version": self.meta_data.version,
            'timestamp': self.meta_data.timestamp,
            "class": preds[0] if num_samples == 1 else preds.tolist(),
            "class_proba": pred_probas
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        try:
            ret = self.model.predict([text])
            ret2 = self.predict(text)
            if ret and ret2.get('model_name', 0) == self.meta_data.model_name:
                return True
            else:
                return False
        except Exception as e:
            # TODO logging
            return False

    def request_format(self):
        return TextPredictionRequest

    def response_format(self):
        return PredictionResponse
