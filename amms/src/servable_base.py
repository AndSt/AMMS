from __future__ import annotations

from typing import Dict, List, Optional
from enum import Enum

import logging
from fastapi.exceptions import RequestValidationError

from src.provided_servables.model_wrapper import ModelWrapper, ModelStatus
from src.config import AspiredModel
from src.version_manager import VersionManager
from src.loader import Loader
from src.utils import dynamic_model_creation, pydantic_class_to_example


class ServableStatus(str, Enum):
    NOT_LOADED = 'NOT_LOADED'
    LOADING = 'LOADING'
    IDLE = 'IDLE'
    PREDICTING = 'PREDICTING'


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
        date = split[2].replace('.pbz2', '')

        return ServableMetaData(model_name, version, date)

    def __eq__(self, other: ServableMetaData) -> bool:
        if isinstance(other, ServableMetaData) is False:
            raise ValueError('The equality check expects `other` to be of type `ServableMetaData`')

        if self.model_name == other.model_name and self.version.__eq__(
                other.version) and self.timestamp == other.timestamp:
            return True
        return False

    def is_newer(self, servable_meta_data: ServableMetaData, compatible: bool = True) -> bool:
        if servable_meta_data.model_name != self.model_name:
            return False

        if servable_meta_data.version.__eq__(self.version):
            if self.timestamp < servable_meta_data.timestamp:
                return True

        if servable_meta_data.version.is_newer(self.version, compatible=compatible):
            return True

        return False

    @staticmethod
    def newest_version(servable_meta_datas: List[ServableMetaData], aspired_model: AspiredModel = None) -> Optional[
        ServableMetaData]:
        """
        :return:    False, if there is no newer list element which is compatible
                    ServableMetaData, if there is
        """
        if isinstance(servable_meta_datas, List) is False:
            raise ValueError('A list of type `ServableMetaData is expected`.')

        if len(servable_meta_datas) == 0:
            return None

        if aspired_model:
            servable_meta_datas = [meta_data for meta_data in servable_meta_datas if
                                   aspired_model.is_compatible(meta_data.to_file_name())]

        newest_meta_data = servable_meta_datas[0]
        for servable_meta_data in servable_meta_datas:
            if servable_meta_data.is_newer(newest_meta_data):
                newest_meta_data = servable_meta_data

        return newest_meta_data

    def to_file_name(self) -> str:
        file_name = "{}-{}-{}.pbz2".format(self.model_name, self.version.to_file_str(), self.timestamp)
        return file_name

    def as_dict(self) -> Dict[str, str]:
        return {
            "model_name": self.model_name,
            "version": str(self.version),
            "train_date": self.timestamp
        }


class Servable:
    def __init__(self, aspired_model: AspiredModel, model_dir: str = 'data/models'):
        logging.debug('Initialize servable {}'.format(aspired_model.model_name))
        self.model_dir = model_dir
        self.aspired_model = aspired_model
        self.loader = Loader.from_aspired_model(aspired_model=aspired_model, model_dir=model_dir)

        self.meta_data: ServableMetaData = None
        self.model: ModelWrapper = None
        self.status = ServableStatus.NOT_LOADED

        self.update()

    def predict(self, input):
        logging.debug('Begin prediction')
        if self.status == ServableStatus.IDLE or self.status == ServableStatus.PREDICTING:
            self.status = ServableStatus.PREDICTING
            response = self.model.predict(input)
            self.status = ServableStatus.IDLE
            return response
        raise RequestValidationError('No model available')  # TODO this error is totally wrong

    def update(self):
        """Updates the servables.
        Steps:
        1) Retrieve all servables in the specified model repository
        2) Compute the newest available, compatible model version. (See TODO for a compatibiltiy description)
        3) Load model from remote repository via Loader class
        4) Switch the current and the newer model
        """

        logging.debug('Update servable {}, version {}'.format(self.aspired_model.model_name,
                                                              str(self.aspired_model.aspired_version)))
        servable_files = self.loader.load_available_models()
        if len(servable_files) == 0:
            logging.debug('Servable {} has no available models'.format(self.aspired_model.model_name))
            return

        servable_metas = [ServableMetaData.from_file_name(file_name=file_name) for file_name in servable_files]
        newest_meta_data = ServableMetaData.newest_version(servable_metas, aspired_model=self.aspired_model)
        if self.meta_data is not None:
            if self.meta_data.is_newer(newest_meta_data):
                return

        old_status = self.status
        file_name = newest_meta_data.to_file_name()
        try:
            self.loader.load(file_name=file_name)
        except Exception as e:
            logging.error('Error during loading of model: {}'.format(e))
            pass

        # TODO optimize status behavior to prepare logging
        self.status = ServableStatus.LOADING
        file_path = '{}/{}'.format(self.model_dir, file_name)
        model = dynamic_model_creation(self.aspired_model.servable_name, file_path)

        if model.status == ModelStatus.NOT_LOADED:
            # TODO proper error handling here
            logging.error('Modelstatus scheisse')
            self.status = old_status
        else:
            self.status = ServableStatus.IDLE
            self.model = model
            self.meta_data = newest_meta_data

    @staticmethod
    def newest_servable(servables: List[Servable]):

        meta_datas = [servable.meta_data for servable in servables]
        newest_meta_data = ServableMetaData.newest_version(meta_datas)

        for servable in servables:
            if servable.meta_data == newest_meta_data:
                return servable
        return None

    def meta_response(self):
        request_format = {}
        response_format = {}
        if self.model is not None:
            request_format = self.model.request_format()
            request_format = pydantic_class_to_example(request_format)
            response_format = self.model.response_format()
            response_format = pydantic_class_to_example(response_format)
        return {
            'status': self.status,
            'meta_data': self.meta_data.as_dict(),
            'request_format': request_format,
            'response_format': response_format
        }
