from __future__ import annotations

import os
from enum import Enum
from typing import List

import logging
import joblib
from abc import abstractmethod

from src.version_manager import AspiredModel, LoadType


class LoaderStatus(Enum):
    LOADING = 'LOADING'
    NOT_LOADING = 'NOT_LOADING'


class Loader:
    """
    Future: - Think about putting up an abstraction like in tf-serving.
            - Goal is to allow the User to construct his own Loader.
    """

    def __init__(self, aspired_model: AspiredModel, model_dir: str = 'data/models'):

        if os.path.isdir(model_dir) is False:
            raise NotADirectoryError('The direcory `{}` doesn\'t exist'.format(model_dir))

        self.model_dir = model_dir
        self.aspired_model = aspired_model
        self.status = LoaderStatus.NOT_LOADING

    @abstractmethod
    def load_available_models(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def load(self, file_name: str):
        raise NotImplementedError()

    @staticmethod
    def from_aspired_model(aspired_model: AspiredModel, model_dir: str = 'data/models') -> Loader:

        # for now to make clear how new loaders can be added
        if aspired_model.load_type == LoadType.local:
            aspired_model.load_type = LoadType.shared
            return LocalLoader(aspired_model=aspired_model, model_dir=model_dir)
        if aspired_model.load_type == LoadType.shared:
            return LocalLoader(aspired_model=aspired_model, model_dir=model_dir)

        raise NotImplementedError(
            'For the given LoadType, {}, no implemenation is given'.format(str(aspired_model.load_type)))


# def load_from_s3(self):
#     pass
#     # s3 = boto3.client('s3')
#     # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')


class LocalLoader(Loader):
    """In container based solutions local the loader is able to gather resources (models) from a mounted volume.
    In a local setup the local file system can be used for file loading.
    """

    def load_available_models(self) -> List[str]:

        file_names = os.listdir(self.aspired_model.load_url)
        file_names = [file_name for file_name in file_names if
                      file_name.endswith('.pbz2') and self.aspired_model.is_compatible(file_name)]
        # Load only servable names holding the correct name
        return file_names

    def load(self, file_name: str):
        if isinstance(file_name, str) is False:
            raise ValueError('file_name needs to be of type `str` but is type {}'.format(type(file_name)))
        source_path = '{}/{}'.format(self.aspired_model.load_url, file_name)
        target_path = '{}/{}'.format(self.model_dir, file_name)

        if os.path.isfile(source_path) is False:
            raise FileNotFoundError('No model file found under `{}`'.format(source_path))
        self.status = LoaderStatus.LOADING

        logging.debug('The loader starts moving {} to location {}'.format(source_path, target_path))
        with open(source_path, 'rb') as shared_handle:
            model = joblib.load(shared_handle)

            with open(target_path, 'wb') as local_handle:
                joblib.dump(model, local_handle)

        self.status = LoaderStatus.NOT_LOADING
