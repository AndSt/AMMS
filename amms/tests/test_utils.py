import os

from src.utils import underscore_to_camelcase, dynamic_model_creation

dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = '{}/data/loaded/'.format(dir_path)


def test_underscore_to_camelcase():
    tests = [
        ('what_a_test', 'WhatATest'),
        ('sklearn_text_input', 'SklearnTextInput')
    ]

    for test in tests:
        assert underscore_to_camelcase(test[0]) == test[1]


def test_dynamic_class_creation():
    class_filename_combo = [
        ('hello_world', 'hello_world-1_0_0-1234.pbz2'),
        ('sklearn_text_input', 'simple_text-1_0_1-1588436916.135168.pbz2')
    ]
    servable_path = 'tests.servables'
    for combo in class_filename_combo:
        try:
            model = dynamic_model_creation(combo[0], '{}/{}'.format(model_path, combo[1]), servable_path)
            assert True
        except Exception as e:
            print(e)
            assert False
