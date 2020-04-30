import os
from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict
import joblib


class ServableStatus(Enum):
    NOT_LOADED = 0
    NOT_LOADABLE = 1
    LOADING = 2
    IDLE = 3
    PREDICTION = 4


class ServableMetaData:
    def __init__(self, model_name: str, version: str, timestamp: str):
        self.model_name = model_name
        self.version = version
        self.timestamp = timestamp

    @staticmethod
    def from_filename(file_name: str = None):
        print(file_name)
        if isinstance(file_name, str) is False:
            raise ValueError('File name needs to be a string.')

        split = file_name.split('-')

        model_name = split[0]  # get rid of _ character
        version = split[1]
        date = split[2].replace('.pbz2')

        return ServableMetaData(model_name, version, date)

    def to_file_name(self) -> str:
        file_name = "{}--{}-{}.pbz2".format(self.model_name, self.version, self.timestamp)
        return file_name

    def as_dict(self) -> Dict[str, str]:
        return {
            "model_name": self.meta_data.model_name,
            "version": self.meta_data.version,
            "train_date": self.meta_data.timestamp
        }


class Servable(ABC):
    def __init__(self, model_name: str, version, date: str, model_dir: str = '/app/data/models'):
        self.model_dir = model_dir

        self.meta_data = ServableMetaData(model_name, version, date)
        self.status = ServableStatus.NOT_LOADED

        self.model = None

    def init_model(self):
        loaded = self.load_model()
        if loaded is False:
            self.status = ServableStatus.NOT_LOADABLE
        else:
            test_pred = self.test_predict()
            if test_pred is False:
                self.status = ServableStatus.NOT_LOADABLE
            else:
                self.status = ServableStatus.IDLE

    def load_model(self):
        # TODO logging new model load
        self.status = ServableStatus.LOADING
        file_path = '{}/{}'.format(self.model_dir, self.meta_data.to_file_name())
        if os.path.isfile('{}/{}'.format(file_path)) is False:
            # TODO logging
            return False
        try:
            with open("{}/{}".format(file_path), "rb") as handle:
                self.model = joblib.load(handle)
                return True
        except Exception as e:
            # TODO logging
            return False

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def test_predict(self):
        pass

    def todict(self):
        return self.meta_data.as_dict()
