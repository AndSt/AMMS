from typing import Tuple, List
import os
from src.config import Config, ModelConfig
from src.loader import Loader


class VersionManager:
    def __init__(self):
        self.config = Config()
        self.loader = Loader()
        self.reload_available_versions()
        self.reload_downloaded_versions()

    def reload_downloaded_versions(self):
        downloaded_models = []
        for file_name in os.listdir(self.config.model_dir):
            print(type(file_name))
            print(file_name)
            downloaded_model = ModelConfig.from_filename(file_name)
            downloaded_models.append(downloaded_models)
        self.downloaded_models = downloaded_models

    def reload_available_versions(self):
        self.available_versions = self.loader.reload_available_versions()

    def retrieve_local_versions(self):
        pass

    def retrieve_shared_versions(self):
        pass

    def specify_update_policy(self, loaded_models) -> Tuple[List[ModelConfig], List[ModelConfig]]:
        load_models = [
            {
                'model_name': 'general_fields_payment_mode',
                'version': '1-0-1',
                'date': '25012020'
            }
        ]
        return loaded_models, load_models