import importlib
from typing import List, Tuple
import logging


def underscore_to_camelcase(value: str) -> str:
    if isinstance(value, str) is False:
        raise ValueError('The function expects a string to capitalize')
    if len(value) == 0:
        return ''
    capitalized = ''.join(x.capitalize() or '_' for x in value.split('_'))
    capitalized = capitalized[0].capitalize() + capitalized[1:]
    return capitalized


def dynamic_model_creation(servable_name: str, file_name: str, servable_path: str = 'src.provided_servables'):
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


def pydantic_class_to_example(pydantic_class):
    schema = pydantic_class.schema()
    print(schema)
    example = {}
    properties = schema.get('properties')
    for property in properties:
        prop = properties.get(property)
        example[property] = dig_in(prop, schema)
    return example


def dig_in(property, schema):
    print(property)
    if 'type' not in property:
        if "$ref" in property:
            pydantic_model = property['$ref'].split('/')[-1]
            return get_definition(pydantic_model, schema)
    if property.get('type', False) == 'array':
        return [
            dig_in(property.get('items'), schema)
        ]
    return property['type']
    return ''


def get_definition(pydantic_model, schema):
    definition = schema.get('definitions').get(pydantic_model)
    return definition_to_exmple(definition, schema)


def definition_to_exmple(data, schema):
    if '$ref' in data:
        pydantic_model = property['$ref'].split('/')[-1]
        return get_definition(pydantic_model, schema)
    if 'anyOf' in data:
        anys = []
        for any in data['anyOf']:
            anys.append(any['type'])
        return anys
    if 'type' not in data:
        logging.error('What is this: {}'.format(data))
    definition_type = data['type']
    if definition_type == 'object':
        ret = {}
        for property in data['properties']:
            ret[property] = definition_to_exmple(data['properties'][property], schema)
        return ret
    elif definition_type == 'array':
        return []
    else:
        logging.debug('type: {}'.format(type(definition_type)))
        return definition_type

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
