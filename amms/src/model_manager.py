import logging

from src.config import Config
from src.servable_base import Servable
from src.data_models.standard import ModelNotFoundResponse


class ModelManager:
    def __init__(self, config_file: str = 'data/config/servables.json', model_dir: str = 'data/models'):
        self.config = Config(config_file=config_file, model_dir=model_dir)
        self.servables = []
        logging.info('Load servables')

    def init_servables(self):
        self.servables = [Servable(aspired_model) for aspired_model in self.config.aspired_models]

    def update(self):
        # TODO error handling; testing
        print('update')
        for servable in self.servables:
            servable.update()

    def predict(self, model_name: str, version: str = None, input=None):
        """Predict. Check if matching model is available.

        """
        for servable in self.servables:
            if model_name != servable.meta_data.model_name:
                continue
            if version is None or version == servable.meta_data.version.tostr():
                return servable.predict(input)
        raise ModelNotFoundResponse('No model available')

    def all_models_meta_data_response(self):
        models = []
        for servable in self.servables:
            models.append(servable.meta_response())
        print(models)
        return {'models': models}

    def model_meta_data_response(self, model_name: str = None, version: str = None):

        for servable in self.servables:
            if model_name != servable.meta_data.model_name:
                continue
            if version is None or servable.meta_data.version == version:
                return servable.meta_response()

        return False
