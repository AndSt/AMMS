import os
import joblib
from typing import Union, List, Optional

from .servable_base import ServableStatus, Servable
from pydantic import BaseModel


class HelloWorldPredictionInput(BaseModel):
    sample: Optional[str]


class HelloWorldServable(Servable):
    def __init__(self, model_name: str, version: str, date: str, model_dir: str):
        super(HelloWorldServable, self).__init__(model_name, version, date, model_dir)

        # typically here we use self.init_model(); see base class how it's handled. Here we don't want to load a model.

    def validate_input(self, samples: Union[str, List[str]]):
        # TODO error handling; Do we have to do this or can we deal with this with pedantic?? aka. how to do dynamic pydantic class
        return True

    def predict(self, samples: HelloWorldPredictionInput):
        self.status = ServableStatus.PREDICTION
        # Here is supposed to be a prediction
        self.status = ServableStatus.IDLE
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
            # TODO logging
            return False

