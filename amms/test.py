from src.data_models import LabelScoreResponse
import json
# prediction_request_data_models()

di = LabelScoreResponse.schema()


# PredictionResponse.
#

def gen_example(class_):
    schema = class_.schema()
    example = {}

    for property in schema.get('properties'):
        prop = schema.get('properties').get(property)
        t = dig_in(prop, schema)
        example[property] = t

    print(json.dumps(example))
    return example


def dig_in(property, schema):
    if 'type' not in property:
        if "$ref" in property:
            return get_definition(property['$ref'], schema)
    if property.get('type', False) is 'array':
        return [
            dig_in(property.get('items'), schema)
        ]
    return ''


def get_definition(field, schema):
    field = field.split('/')[-1]
    definition = schema.get('definitions').get(field)
    return def_to_exmpl(definition, schema)


def def_to_exmpl(data, schema):
    if '$ref' in data:
        f = data['$ref'].split('/')[-1]
        return get_definition(f, schema)
    if 'anyOf' in data:
        anys = []
        for any in data['anyOf']:
            anys.append(any['type'])
        return anys

    type = data['type']
    if type == 'object':
        ret = {}
        for property in data['properties']:
            ret[property] = def_to_exmpl(data['properties'][property], schema)
        return ret
    elif type == 'array':
        return []
    else:
        return type


# def gen_obj(obj):
#     title = obj.get('title', False)
#     type = obj.get('type', False)
#     if title is False or type is False:
#         print('error: {}'.format(obj))
#         return
#     if type == 'object':
#         return gen_example()
#
#     elif type == 'array':
#         return gen_example()
#     else:
#         return {title: type}
#
# def gen_array(arr):
#print(ModelsMetaDataResponse.schema_json())
gen_example(LabelScoreResponse)
