import os
from enum import Enum
from typing import List

import logging
import joblib

from src.config import AspiredModel, VersionManager


class LoaderStatus(Enum):
    LOADING = 1
    NOT_LOADING = 2


class Loader:
    def __init__(self, aspired_model: AspiredModel, model_dir: str = 'data/servables'):
        self.status = LoaderStatus.NOT_LOADING
        self.model_dir = model_dir

        self.aspired_model = aspired_model

    def load_available_model_versions(self) -> List[VersionManager]:
        if self.load_type == 'local':
            return self.load_available_model_versions_from_folder()
        elif self.load_type == 'shared':
            return self.load_available_model_versions_from_folder()

    def load_available_model_versions_from_folder(self) -> List[str]:
        file_names = os.listdir(self.aspired_model.load_url)
        file_names = [file_name for file_name in file_names if file_name.endswith('.pbz2')]

        # Load only servable names holding the correct name
        return file_names

    def load(self, file_name: str):
        if self.load_type == 'local':
            return self.load_from_folder(file_name)
        elif self.load_type == 'shared':
            return self.load_from_folder(file_name)

    def load_from_folder(self, file_name: str):
        try:
            with open('{}/{}'.format(self.aspired_model.load_url, file_name), 'rb') as shared_handle:
                model = joblib.load(shared_handle)
                with open('{}/{}'.format(self.model_dir, file_name), 'wb') as local_handle:
                    joblib.dump(model, local_handle)
            return True
        except Exception as e:
            # TODO logging
            logging.error('The loader wasn\'t able to load the specified file "{}".'.format(file_name))
            return False

    def load_from_s3(self):
        pass
        # s3 = boto3.client('s3')
        # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
