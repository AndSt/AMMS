import logging

from src.config import Config
from src.servable_base import Servable


class ModelManager:
    def __init__(self):
        self.config = Config()
        self.servables = []
        logging.info('Load servables')

    def init_servables(self):
        self.servables = [Servable(aspired_model) for aspired_model in self.config.aspired_models]

    def update(self):
        # TODO error handling; testing
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
        return {
            'model_request': {
                'model_name': model_name,
                'version': version
            },
            'available_models': self.all_models_meta_data_response()
        }

    def all_models_meta_data_response(self):
        models = []
        for loaded_model in self.servables:
            models.append(loaded_model.as_dict())
        return {'servables': models}

    def model_meta_data_response(self, model_name: str = None, version: str = None):
        result = []
        # TODO error handling, if version is false
        if model_name is None or isinstance(model_name, str) is False:
            logging.info('User didn\'t specify the model name correctly')
            raise ValueError('Model needs to be specified.')

        for servable_model_name, servable_version in self.servables:
            if servable_model_name != model_name:
                continue
            if version is None:
                result.append(self.servables[(servable_model_name, servable_version)])
            elif version == servable_model_name:
                result.append(self.servables[(servable_model_name, servable_version)])

        if len(self.servables) == 1:
            return result[0]
        return result
