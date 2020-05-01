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
    def from_json(json_dict: Dict[str, str]):
        return AspiredModel(json_dict['model_name'], json_dict['aspired_version'], json_dict['load_type'],
                            json_dict['load_url'], json_dict['servable_name'])


class Config:
    def __init__(self):
        with open('data/config/servables.json', 'r') as handle:
            data = json.load(handle)
        self.aspired_models = []
        self.model_dir = 'data/servables'

        ## TODO correctness checks of model config file
        for aspired_version in data:
            self.aspired_models.append(AspiredModel.from_json(aspired_version))
        self.check_aspired_version_consistency()

    def check_aspired_version_consistency(self) -> bool:
        return True


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
