import joblib
import os
from enum import Enum


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

    def load_from_shared(self, version):
        pass

    def load_from_s3(self):
        pass
        # s3 = boto3.client('s3')
        # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
