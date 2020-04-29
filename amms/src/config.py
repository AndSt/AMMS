from typing import Union

import json


class Config:
    def __init__(self):
        with open('data/config.json', 'r') as handle:
            data = json.load(handle)
        self.aspired_models = []
        self.model_dir = 'data/models'
        for aspired_version in data:
            self.aspired_models.append(AspiredModel(aspired_version))


class AspiredModel:
    def __init__(self, data):
        self.model_name = data['model_name']
        self.aspired_version = data['aspired_version']
        self.load_type = data['load_type']
        self.load_url = data['load_url']


class ModelConfig:
    def __init__(self, model_name, version, date):
        self.model_name = model_name
        self.version = version
        self.date = date
        self.file_name = '{}_version_{}_{}.p'.format(model_name, version, date)

    @staticmethod
    def from_filename(file_name: str = None):
        if isinstance(file_name, str) is False:
            raise ValueError('File name needs to be a string.')

        split = file_name.split('version')

        model_name = split[0][:-1]  # get rid of _ character

        split = split[1].split('_')
        version = split[0]
        date = split[1].split('.')[0]

        return ModelConfig(model_name, version, date)

    def get_dict(self):
        return {
            'model_name': self.model_name,
            'version': self.version,
            'date': self.date
        }
