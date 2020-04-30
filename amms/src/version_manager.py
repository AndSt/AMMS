import os
from typing import Dict, List
import functools

from src.config import Config, AspiredModel
from src.servables.servable_base import ServableMetaData
from src.loader import Loader


class ModelVersionManager:
    # handles versioning of one model type

    # TODO use attr or similar to define information classes
    def __init__(self, aspired_model: AspiredModel, loader: Loader, model_dir: str = 'data/models'):
        self.aspired_model = aspired_model
        self.model_dir = model_dir
        self.loader = loader

        self.update_policy = {}  # dict of the form {load: {type, url, file_name}, {remove: servable}}
        # TODO think about cases where reloading makes sense, but no update is necessary

    def reload_available_versions(self):
        self.available_models = self.loader.load_available_model_versions_from_shared_folder()
        self.available_models = functools.reduce(lambda m: self.is_valid(m.model_name, m.version),
                                                 self.available_models)

    def is_valid(self, model_name, version):
        # TODO Version logiv
        if model_name == self.aspired_model.model_name and version == self.aspired_model.aspired_version:
            return True
        else:
            return False

    def reload_downloaded_model_versions(self):
        # TODO logging
        downloaded_models = []
        for file_name in os.listdir(self.model_dir):
            if file_name == '.gitkeep':
                continue
            downloaded_model = ServableMetaData.from_filename(file_name)
            downloaded_models.append(downloaded_model)
        self.downloaded_models = downloaded_models

    def update_info(self):
        self.reload_available_versions()
        self.reload_downloaded_model_versions()

    def specify_update_policy(self):
        self.update_policy = {}


class VersionManager:
    """Simple Wrapper around multiple version managers.
    """
    def __init__(self):
        config = Config()
        self.loader = Loader()
        self.model_managers = [ModelVersionManager(aspired_model, self.loader, config.model_dir) for aspired_model in
                               config.aspired_models]

        self.update()

    def update(self):
        for model_manager in self.model_managers:
            model_manager.update_info()
            model_manager.specify_update_policy()

    def retrieve_update_policies(self) -> List[Dict]:
        updates = [model_manager.update_policy for model_manager in self.model_managers]
        return updates
