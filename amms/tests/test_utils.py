import os
import pytest

from src.utils import underscore_to_camelcase, dynamic_model_creation, format_class_probas, pydantic_class_to_example
from src.data_models import TextRequest, LabelScoreResponse

dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = '{}/data/models/'.format(dir_path)


def test_underscore_to_camelcase():
    tests = [
        ('what_a_test', 'WhatATest'),
        ('sklearn_text_input', 'SklearnTextInput'),
        ('', '')
    ]

    for test in tests:
        assert underscore_to_camelcase(test[0]) == test[1]

    with pytest.raises(ValueError):
        underscore_to_camelcase(15)


def test_dynamic_class_creation():
    class_filename_combo = [
        ('hello_world', 'hello_world-1_0_0-1234.pbz2'),
        ('sklearn_text_input', 'simple_text-1_0_2-1588436916.135168.pbz2')
    ]
    servable_path = 'tests.custom_servables'
    for combo in class_filename_combo:
        try:
            model = dynamic_model_creation(combo[0], '{}/{}'.format(model_path, combo[1]), servable_path)
            assert True
        except Exception as e:
            print(e)
            assert False


def test_format_class_probas():
    # TODO write errors for wrong input in utils
    classes = ['1', '2', '3', '4']
    pred_probas_1 = [[1, 2, 3, 4]]
    ret_12 = [[('1', 1.), ('2', 2.), ('3', 3.), ('4', 4.)]]

    assert format_class_probas(classes, pred_probas_1) == ret_12


def test_pydantic_class_to_example():
    text_request_dict = {
        "samples": [
            "string"
        ]
    }
    assert text_request_dict == pydantic_class_to_example(TextRequest)

    label_score_response_dict = {
        "preds": [
            "string"
        ],
        "pred_probas": [
            [
                [
                    [
                        "string",
                        "number"
                    ]
                ]
            ]
        ]
    }
    assert label_score_response_dict == pydantic_class_to_example(LabelScoreResponse)
