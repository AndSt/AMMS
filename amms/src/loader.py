import os
from enum import Enum

import joblib
import glob

from src.servables.servable_base import ServableMetaData


class LoaderStatus(Enum):
    LOADING = 1
    NOT_LOADING = 2


class Loader:
    def __init__(self):
        self.status = LoaderStatus.NOT_LOADING

    def reload_available_versions(self):
        self.versions = [
            {
                'version': '1.0.1',
                'date': '25.01.2020'
            },
            {
                'version': '1.0.1',
                'date': '25.03.2020'
            },
            {
                'version': '1.0.5',
                'date': '25.03.2020'
            },
            {
                'version': '2.0.1',
                'date': '25.03.2020'
            }
        ]

    def reload_newest_version(self):
        self.newest_version = {'version': '1.0.1', 'date': '25.03.2020'}

    def load(self):
        if self.load_type == 'local':
            self.load_from_local()
        elif self.load_type == 'shared':
            self.load_from_shared()

    def load_from_local(self) -> bool:
        version = self.newest_version
        date_string = ''.join(version['date'].split('.'))
        version_string = '-'.join(version['version'].split('.'))
        file_name = '{}_version_{}_{}.p'.format(self.model_name, version_string, date_string)

        file = '{}/{}'.format(self.load_url, file_name)
        if os.path.isfile(file) is False:
            return False
        with open('{}/{}'.format(self.load_url, file_name), 'rb') as handle:
            model = joblib.load(handle)

        with open('{}/{}.pbz2'.format(self.model_dir, file_name), 'wb') as handle:
            joblib.dump(model, handle)
        return True

    def load_available_model_versions_from_shared_folder(self, path):

        file_paths = glob.glob('{}/*.pbz2'.format(path))
        model_versions = []
        for file_path in file_paths:
            file_name = file_path.split('/')[-1]
            try:
                servable = ServableMetaData.from_filename(file_name=file_name)
                model_versions.append(servable)
            except Exception as e:
                pass  # TODO logging; keep in mind that .gitkeep is there, shouldn't be logged
        return model_versions

    def load_from_shared(self, source_dir: str, target_dir: str, filename: str):
        try:
            with open('{}/{}'.format(source_dir, filename), 'rb') as shared_handle:
                model = joblib.load(shared_handle)
                with open('{}/{}'.format(target_dir, filename), 'wb') as local_handle:
                    joblib.dump(model, local_handle)
        except Exception as e:
            # TODO logging
            print(e)

    def load_from_s3(self):
        pass
        # s3 = boto3.client('s3')
        # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
