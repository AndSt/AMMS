import os

from src.config import Config, setup_logging, AspiredModel
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir = '{}/data/loaded'.format(dir_path)


# TODO aspired version equal


def test_correct_configs():
    correct_configs = ['config_1', 'config_2']
    correct_configs = ['{}/data/configs/{}.json'.format(dir_path, config) for config in correct_configs]

    for config in correct_configs:
        c = Config(config, model_dir)
        assert True


def test_no_servables():
    config = '{}/data/configs/config_empty.json'.format(dir_path)
    try:
        c = Config(config, model_dir)
        assert False
    except RuntimeError:
        assert True
    except:
        assert False


def test_duplicated():
    config = '{}/data/configs/config_duplicated_model_version.json'.format(dir_path)
    try:
        c = Config(config, model_dir)
        assert False
    except RuntimeError:
        assert True
    except:
        assert False


def test_no_model_dir():
    config = '{}/data/configs/config_1.json'.format(dir_path)
    try:
        c = Config(config, 'ddd')
        assert False
    except NotADirectoryError:
        assert True
    except:
        assert False


# for the sake of test coverage:

def test_aspired_model():
    json_dict = {
        "model_name": "simple_text",
        "aspired_version": "1.x",
        "load_type": "local",
        "load_url": "data/models",
        "servable_name": "sklearn_text_input"
    }
    am = AspiredModel.from_json(json_dict)
    assert True


def test_setup_logging():
    setup_logging()
    logging.debug('Logged')
    assert True
