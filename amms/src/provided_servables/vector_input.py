import numpy as np
import logging

from src.model_wrapper import ModelWrapper
from src.data_models import VectorRequest, LabelScoreResponse
from src.utils import format_class_probas


class TextInputModel(ModelWrapper):
    def __init__(self, file_path):
        super(TextInputModel, self).__init__(file_path=file_path)

        # loads model from source and checks whether prediction works
        # That's basically runtime testing. This is intended, as a core requirement is to enable the server to load
        # arbitrary local_servables

    def predict(self, samples: VectorRequest):
        samples = samples.samples
        if isinstance(samples, str):
            samples = [samples]
        # TODO check whether list, np.array, etc.

        preds_probas = self.model.predict_proba(samples).tolist()
        pred_probas = format_class_probas(self.model.classes_, preds_probas)
        preds = np.argmax(preds_probas, axis=1).tolist()
        return {
            "preds": preds,
            "pred_probas": pred_probas
        }

    def test_predict(self):
        try:
            ret = self.predict([[0, 1, 2], [3, 4, 5]])
            LabelScoreResponse(**ret)
            return True
        except Exception as e:
            logging.error('Test Prediction doesn\'t work anyhow: {}'.format(e))
            return False

    def request_format(self):
        return VectorRequest

    def response_format(self):
        return LabelScoreResponse
