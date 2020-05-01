import os
import joblib

from abc import ABC, abstractmethod


class ModelWrapper(ABC):
    def __init__(self, file_path):
        self.loaded = False
        if os.path.isfile('{}/{}'.format(file_path)) is False:
            # TODO logging
            return False
        try:
            with open("{}/{}".format(file_path), "rb") as handle:
                self.model = joblib.load(handle)
                self.test_predict()
                self.loaded = True
        except Exception as e:
            print(e)  # TODO proper error handling

    def validate_input(self):
        return True

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
