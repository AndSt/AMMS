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
        self.file_path = file_path
        self.status = ModelStatus.NOT_LOADED
        if os.path.isfile(file_path) is False:
            logging.error('The model doesn\'t exists. Maybe the loader isn\'t finished loading.')
        try:
            self.status = ModelStatus.LOADING
            self.load()
            self.test_predict()
            self.status = ModelStatus.LOADED
        except FileNotFoundError:
            self.status = ModelStatus.NOT_LOADED
            raise FileNotFoundError('Model is not found under: {}'.format(file_path))
        except Exception as e:
            self.status = ModelStatus.NOT_LOADED
            logging.error(e)
            raise Exception(str(e))

    def load(self):
        with open("{}".format(self.file_path), "rb") as handle:
            self.model = joblib.load(handle)

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
