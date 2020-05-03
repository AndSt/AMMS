import importlib
from typing import List, Union, Tuple


def underscore_to_camelcase(value: str) -> str:
    if isinstance(value, str) is False:
        raise ValueError('The function expects a string to capitalize')
    if len(value) == 0:
        return ''
    capitalized = ''.join(x.capitalize() or '_' for x in value.split('_'))
    capitalized = capitalized[0].capitalize() + capitalized[1:]
    return capitalized


def dynamic_model_creation(servable_name: str, file_name: str, servable_path: str = 'src.servables'):
    servable_path = '{}.{}'.format(servable_path, servable_name)
    class_name = underscore_to_camelcase(servable_name) + 'Model'

    module = importlib.import_module(servable_path)
    class_ = getattr(module, class_name)
    instance = class_(file_name)

    return instance


def format_class_probas(classes: List[str], pred_probas: List[List[float]]) -> List[List[Tuple[str, int]]]:
    classes = [str(cl) for cl in classes]
    pred_probas = [[float(proba) for proba in pred] for pred in pred_probas]
    response = []
    for pred_proba in pred_probas:
        response.append(list(zip(classes, pred_proba)))

    return response


    # def prediction_data_models(servable_path: str = 'src.local_servables'):
#     config = Config()
#
#     servable_names = []
#     for aspired_model in config.aspired_models:
#         servable_names.append(aspired_model.servable_name)
#     servable_names = list(set(servable_names))  # choose unique local_servables
#
#     request_data_models = []
#     response_data_models = []
#     for servable_name in servable_names:
#         module_path = '{}.{}'.format(servable_path, servable_name)
#         try:
#             module = importlib.import_module(module_path)
#             class_name = underscore_to_camelcase(servable_name) + 'Model'
#             class_ = getattr(module, class_name)
#             request_data_models.append(class_.request_format())
#             response_data_models.append(class_.response_format())
#         except Exception as e:
#             logging.error('Fehler: {}'.format(e))  # TODO error logging
#     print(request_data_models)
#     print(response_data_models)
#     return request_data_models, response_data_models
