from typing import Union, List

import numpy as np
import logging

from src.model_wrapper import ModelWrapper
from src.data_models import TextRequest, LabelScoreResponse
from src.utils import format_class_probas


class SklearnTextInputModel(ModelWrapper):
    def __init__(self, file_path):
        super(SklearnTextInputModel, self).__init__(file_path=file_path)

        # loads model from source and checks whether prediction works
        # That's basically runtime testing. This is intended, as a core requirement is to enable the server to load
        # arbitrary local_servables

    def validate_input(self, samples: Union[str, List[str]]):
        # TODO error handling; Do we have to do this or can we deal with this with pedantic?? aka. how to do dynamic pydantic class
        return True

    def predict(self, samples: TextRequest):
        self.validate_input(samples)
        samples = samples.examples
        if isinstance(samples, str):
            samples = [samples]
        # TODO check whether list, np.array, etc.

        preds_probas = self.model.predict_proba(samples).tolist()
        label_probas = format_class_probas(self.model.classes_, preds_probas)
        preds = np.argmax(preds_probas, axis=1).tolist()
        return {
            "preds": preds,
            "pred_probas": label_probas
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        try:
            ret = self.predict(text)
            LabelScoreResponse(**ret)
            return True
        except Exception as e:
            logging.error('Test Prediction doesn\'t work anyhow: {}'.format(e))
            return False

    def request_format(self):
        return TextRequest

    def response_format(self):
        return LabelScoreResponse
