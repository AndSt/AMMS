import os

from src.model_manager import ModelManager

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = '{}/data/configs/config_1.json'.format(dir_path)
model_dir = '{}/data/loaded'.format(dir_path)


def test_init():
    mm = ModelManager(config_file, model_dir)
    assert True
    try:
        mm = ModelManager()
        assert False
    except:
        assert True


def test_init_servables():
    mm = ModelManager(config_file, model_dir)
    mm.init_servables()


def test_predict():
    pass
