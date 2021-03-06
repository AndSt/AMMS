import logging

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.config import Config
from src.servable_base import Servable


class ModelManager:
    def __init__(self, config_file: str = 'data/config/servables.json', model_dir: str = 'data/models'):
        self.config = Config(config_file=config_file, model_dir=model_dir)
        self.servables = []
        logging.info('Load servables.')
        self.servables = [Servable(aspired_model, model_dir) for aspired_model in self.config.aspired_models]

    def update(self):
        for servable in self.servables:
            servable.update()

    # future possibility to delete previously models models
    # Keep in mind: models model means downloaded model; servable means model models in memory
    def clean_up_model_dir(self):
        pass

    def get_servable(self, model_name: str = None, version: str = None):
        # Scenario 1: No servable is loaded
        if len(self.servables) == 0:
            # TODO error handling
            return False

        # Scenario 2: Only 1 servable is loaded
        if len(self.servables) == 1:
            return self.servables[0]

        # Scenario 3: No model given. Then they're either of same type or we cannot know which model to use.
        if model_name is None:
            names = [servable.meta_data.model_name for servable in self.servables]
            if len(set(names)) == 1:
                return Servable.newest_servable(self.servables)
            else:
                # TODO error handling
                print('Error')
                return False

        possible_servables = [servable for servable in self.servables if servable.meta_data.model_name == model_name]

        # Scenario 4: Model given, no version
        if version is None:
            return Servable.newest_servable(possible_servables)
        # TODO check, if only 1 model type

        # Scenario 5: Model and version given
        matching_servable = [servable for servable in possible_servables if servable.meta_data.version == version]
        if len(matching_servable) == 0:
            # TODO error handling
            return False
        return matching_servable

    def all_models_meta_data_response(self):
        models = []
        for servable in self.servables:
            models.append(servable.meta_response())

        logging.info('Number of models models: {}'.format(len(models)))
        return {'models': models}

    def model_meta_data_response(self, model_name: str = None, version: str = None):

        servable = self.get_servable(model_name, version)
        if servable is False:
            response = {
                'error_message': 'Model or version is not found',
                'available_models': self.all_models_meta_data_response()
            }
            return JSONResponse(status_code=404, content=response)
        return servable.meta_response()

    def predict(self, model_name: str = None, version: str = None, input=None):
        """Predict. Check if matching model is available.
        """
        # TODO logging
        servable = self.get_servable(model_name, version)
        if servable is False:
            response = {
                'error_message': 'Model or version is not found',
                'available_models': self.all_models_meta_data_response()
            }
            return JSONResponse(status_code=404, content=response)

        # for the standard /predict route, no data model is known, thus we have to transform
        request_format = servable.model.request_format()
        if isinstance(input, request_format) is False:
            try:
                input = servable.model.request_format()(**input)
            except Exception as e:
                raise RequestValidationError([e])

        return servable.predict(input)
