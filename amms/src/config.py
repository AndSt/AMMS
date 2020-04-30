from typing import Union, Dict

import json


class Config:
    def __init__(self):
        with open('data/model_config.json', 'r') as handle:
            data = json.load(handle)
        self.aspired_models = []
        self.model_dir = 'data/models'
        ## TODO correctness checks of model config file
        for aspired_version in data:
            self.aspired_models.append(AspiredModel.from_json(aspired_version))
        self.check_aspired_version_consistency()

    def check_aspired_version_consistency(self):
        return True


class AspiredModel:
    def __init__(self, model_name: str, aspired_version: str, load_type: str, load_url: str):
        self.model_name = model_name
        self.aspired_version = aspired_version
        self.load_type = load_type
        self.load_url = load_url

    @staticmethod
    def from_json(json_data: Dict[str, str]):
        return AspiredModel(json_data['model_name'], json_data['aspired_version'], json_data['load_type'],
                            json_data['load_url'])
