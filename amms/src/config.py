from __future__ import annotations

import os
import logging
from typing import Dict

import json

from src.version_manager import VersionManager


class AspiredModel:
    """Container holding information about a model version we want to load and how to load it.
    Aspired version format:

    """

    def __init__(self, model_name: str, aspired_version: str, load_type: str, load_url: str, servable_name: str):
        self.model_name = model_name
        self.aspired_version = VersionManager(aspired_version)
        self.load_type = load_type
        self.load_url = load_url
        self.servable_name = servable_name

    @staticmethod
    def from_json(json_dict: Dict[str, str]) -> AspiredModel:
        fields = ['model_name', 'aspired_version', 'load_type', 'load_url', 'servable_name']
        for field in fields:
            if field not in json_dict:
                raise ValueError('The configuration needs to hold a parameter `{}`.'.format(field))
        return AspiredModel(json_dict['model_name'], json_dict['aspired_version'], json_dict['load_type'],
                            json_dict['load_url'], json_dict['servable_name'])

    # def __eq__(self, other: AspiredModel) -> bool:
    #     # TODO properpy do this
    #     if self.model_name == other.model_name and self.aspired_version == other.aspired_version and \
    #             self.load_type == other.load_type and self.load_url == other.load_url and \
    #             self.servable_name == other.servable_name:
    #         return True
    #     return False


class Config:
    def __init__(self, config_file: str = 'data/config/servables.json', model_dir: str = 'data/models'):

        self.config_file = config_file
        with open(config_file, 'r') as handle:
            data = json.load(handle)

        self.aspired_models = []
        self.model_dir = model_dir
        if os.path.isdir(self.model_dir) is False:
            raise NotADirectoryError('The model dir `{}` is not found'.format(self.model_dir))

        self.aspired_models = []
        for aspired_version in data:
            self.aspired_models.append(AspiredModel.from_json(aspired_version))
        if len(self.aspired_models) == 0:
            raise RuntimeError('No model is specified. Thus no model is served.')

        for aspired_model in self.aspired_models:
            others = [am for am in self.aspired_models if id(am) != id(aspired_model)]
            for am_2 in others:
                if am_2.model_name == aspired_model.model_name \
                        and am_2.aspired_version.main_version == aspired_model.aspired_version.main_version:
                    raise RuntimeError('A model with the same top level version cannot be deployed twice.')


def setup_logging(path='data/config/logging.json', default_log_level=logging.INFO, env_key='LOG_CFG_FILE'):
    """Setup logging configuration
    """
    value = os.getenv(env_key, None)
    if value and value.endswith('.json') and os.path.exists(value):
        path = value

    if os.path.exists(path):
        with open(path, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_log_level)
