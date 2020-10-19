import os

from src.model_manager import ModelManager

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = '{}/data/config/config_1.json'.format(dir_path)
model_dir = '{}/data/models'.format(dir_path)


def test_init():
    mm = ModelManager(config_file, model_dir)


def test_predict():
    pass
