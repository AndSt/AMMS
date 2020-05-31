from __future__ import annotations

import os
import logging
import logging.config as logging_config

import json
from src.version_manager import AspiredModel


class Config:
    def __init__(self, config_file: str = 'data/config/provided_servables.json', model_dir: str = 'data/models'):

        self.config_file = config_file
        with open(config_file, 'r') as handle:
            data = json.load(handle)

        self.aspired_models = []
        self.model_dir = model_dir
        if os.path.isdir(self.model_dir) is False:
            raise NotADirectoryError('The model dir `{}` is not found'.format(self.model_dir))

        self.aspired_models = []
        for aspired_version in data:
            self.aspired_models.append(AspiredModel.from_json_dict(aspired_version))
        if len(self.aspired_models) == 0:
            raise RuntimeError('No model is specified. Thus no model is served.')

        for aspired_model in self.aspired_models:
            others = [am for am in self.aspired_models if id(am) != id(aspired_model)]
            for am_2 in others:
                if am_2.model_name == aspired_model.model_name \
                        and am_2.aspired_version.main_version == aspired_model.aspired_version.main_version:
                    raise RuntimeError('A model with the same top level version cannot be deployed twice.')


# TODO test such that main file is used
def setup_logging(path='data/config/logging.json'):
    """Setup logging configuration
    """
    # value = os.getenv(env_key, None)
    # if value and value.endswith('.json') and os.path.exists(value):
    #     path = value
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = json.load(f)
        logging_config.dictConfig(config)
    else:
        raise FileNotFoundError('The path to the logging configuration doesn\'t exist')