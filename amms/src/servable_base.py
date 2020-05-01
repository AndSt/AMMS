from __future__ import annotations

from typing import Dict
from enum import Enum

from src.model_wrapper import ModelWrapper
from src.config import AspiredModel
from src.version_manager import VersionManager
from src.loader import Loader


class ServableStatus(Enum):
    NOT_LOADED = 0
    NOT_LOADABLE = 1
    LOADING = 2
    IDLE = 3
    PREDICTION = 4


class ServableMetaData:
    def __init__(self, model_name: str, version: str, timestamp: str):
        self.model_name = model_name
        self.version = VersionManager(version)
        self.timestamp = timestamp

    @staticmethod
    def from_file_name(file_name: str = None):
        # TODO logging
        if isinstance(file_name, str) is False:
            raise ValueError('File name needs to be a string.')

        split = file_name.split('-')
        if len(split) != 3:
            raise ValueError('The given file doesn\'t support the model naming scheme.')  # Refer to the docs for scheme

        model_name = split[0]  # get rid of _ character
        version = split[1]
        date = split[2].replace('.pbz2')

        return ServableMetaData(model_name, version, date)

    def is_equal(self, servable_meta_data: ServableMetaData) -> bool:
        if self.model_name == servable_meta_data.model_name and self.version.is_equal(
                servable_meta_data.version) and self.timestamp == servable_meta_data.timestamp:
            return True

        return False

    def is_compatible_and_newer(self, servable_meta_data: ServableMetaData) -> bool:
        if servable_meta_data.model_name != self.model_name:
            return False

        if servable_meta_data.is_equal(self.version):
            if self.timestamp < servable_meta_data.timestamp:
                return True

        if servable_meta_data.version.is_compatible_and_newer(self.version):
            return True

        return False

    def to_file_name(self) -> str:
        file_name = "{}-{}-{}.pbz2".format(self.model_name, self.version.tostr(), self.timestamp)
        return file_name

    def as_dict(self) -> Dict[str, str]:
        return {
            "model_name": self.meta_data.model_name,
            "version": self.meta_data.version.tostr(),
            "train_date": self.meta_data.timestamp
        }


class Servable:
    def __init__(self, aspired_model: AspiredModel, model_dir: str = '/app/data/servables'):


        self.model_dir = model_dir
        self.aspired_model = aspired_model
        self.loader = Loader(aspired_model)

        self.meta_data: ServableMetaData = None
        self.model: ModelWrapper = None
        self.status = ServableStatus.NOT_LOADED

        self.update()

    def predict(self, input):
        if self.status == ServableStatus.IDLE or self.status == ServableStatus.PREDICTION:
            self.status = ServableStatus.PREDICTION
            prediction = self.model.predict(input)
            self.status = ServableStatus.IDLE
            return prediction
        else:
            return {
                'error': 'TODO write better error'
            }

    def update(self):
        """Updates the currently loaded servables.
        Steps:
        1) Retrieve all servables in the specified model repository
        2) Compute the newest available, compatible model version. (See TODO for a compatibiltiy description)
        3) Load model from remote repository via Loader class
        4) Switch the current and the newer model
        """
        servable_files = self.loader.load_available_model_versions()
        servable_metas = [ServableMetaData.from_file_name(file_name=file_name) for file_name in servable_files]
        # Only update if there are available versions
        if len(servable_metas) == 0:
            return

        newest = self.meta_data if self.meta_data is not None else servable_metas[0]
        for available_version in servable_metas:
            if available_version.is_compatible_and_newer(newest):
                newest = available_version

        if newest.is_equal(self.meta_data):
            return

        old_status = self.status
        file_name = newest.to_file_name()
        did_load = self.loader.load(file_name=file_name)
        if did_load is False:
            if self.status != ServableStatus.PREDICTION:
                self.status = old_status
                return
            return

        self.status = ServableStatus.LOADING
        file_path = '{}/{}'.format(self.model_dir, file_name)
        model = ModelWrapper(file_path)
        if model.loaded is False:
            self.status = old_status
        else:
            self.status = ServableStatus.IDLE

    def meta_response(self):
        return {
            'status': self.status,
            'meta_data': self.meta_data.as_dict()
        }
