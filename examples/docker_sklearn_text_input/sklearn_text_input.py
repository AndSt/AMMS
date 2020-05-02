from typing import Union, List

import numpy as np

from src.servable_base import ServableStatus, Servable
from pydantic import BaseModel


class SklearnTextInputPredictionInput(BaseModel):
    samples: Union[str, List[str]]


class SklearnTextInputServable(Servable):
    def __init__(self, model_name: str, version: str, date: str, model_dir: str):
        super(SklearnTextInputServable, self).__init__(model_name, version, date, model_dir)

        # loads model from source and checks whether prediction works
        # That's basically runtime testing. This is intended, as a core requirement is to enable the server to load
        # arbitrary local_servables
        self.init_model()

    def validate_input(self, samples: Union[str, List[str]]):
        # TODO error handling; Do we have to do this or can we deal with this with pedantic?? aka. how to do dynamic pydantic class
        return True

    def predict(self, samples: SklearnTextInputPredictionInput):
        self.status = ServableStatus.PREDICTION
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

