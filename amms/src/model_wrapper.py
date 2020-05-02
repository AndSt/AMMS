import os
import joblib
from enum import Enum

import logging

from abc import ABC, abstractmethod


class ModelStatus(Enum):
    NOT_LOADED = 'LOADED'
    LOADING = 'LOADING'
    LOADED = 'IS_LOADED'


class ModelWrapper(ABC):
    def __init__(self, file_path):
        self.status = ModelStatus.NOT_LOADED
        if os.path.isfile(file_path) is False:
            # TODO logging
            logging.error('The model doesn\'t exists. Maybe the loader isn\'t finished loading.')
            return False
        try:
            self.status = ModelStatus.LOADING
            with open("{}/{}".format(file_path), "rb") as handle:
                self.model = joblib.load(handle)
                self.test_predict()
                self.status = ModelStatus.LOADED
        except Exception as e:
            print(e)  # TODO proper error handling

    def transform_input(self, input):
        return input

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def test_predict(self):
        pass

    @abstractmethod
    def request_format(self):
        pass

    @abstractmethod
    def response_format(self):
        pass
