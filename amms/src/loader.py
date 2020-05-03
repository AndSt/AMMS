import os
from enum import Enum
from typing import List

import logging
import joblib

from src.version_manager import AspiredModel, LoadType


class LoaderStatus(Enum):
    LOADING = 'LOADING'
    NOT_LOADING = 'NOT_LOADING'


class Loader:
    def __init__(self, aspired_model: AspiredModel, model_dir: str = 'data/models'):
        self.status = LoaderStatus.NOT_LOADING
        self.model_dir = model_dir

        self.aspired_model = aspired_model

    def load_available_models(self) -> List[str]:
        if self.aspired_model.load_type == LoadType.shared or self.aspired_model.load_type == LoadType.local:
            return self.load_available_models_from_folder()

    def load_available_models_from_folder(self) -> List[str]:
        file_names = os.listdir(self.aspired_model.load_url)
        file_names = [file_name for file_name in file_names if file_name.endswith('.pbz2')]
        # Load only servable names holding the correct name
        return file_names

    def load(self, file_name: str):
        self.status = LoaderStatus.LOADING
        if self.aspired_model.load_type == LoadType.shared:
            self.load_from_folder(file_name)

        self.status = LoaderStatus.NOT_LOADING

    def load_from_folder(self, file_name: str):
        try:
            source_path = '{}/{}'.format(self.aspired_model.load_url, file_name)
            target_path = '{}/{}'.format(self.model_dir, file_name)
            logging.debug('The loader want to move file {} to location  {}.'.format(source_path, target_path))
            with open(source_path, 'rb') as shared_handle:
                model = joblib.load(shared_handle)
                with open(target_path, 'wb') as local_handle:
                    joblib.dump(model, local_handle)
        except Exception as e:
            logging.error('The loader wasn\'t able to load the specified file "{}, because: {}".'.format(file_name, e))

    # def load_from_s3(self):
    #     pass
    #     # s3 = boto3.client('s3')
    #     # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
