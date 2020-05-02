import pytest
import os

from src.config import AspiredModel
from src.loader import Loader

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture()
def loader() -> Loader:
    asp_1 = AspiredModel('name', '1.x', 'shared', '{}/data/shared'.format(dir_path), 'name')
    return Loader(asp_1, '{}/data/loaded'.format(dir_path))


def test_load_available_model_versions(loader):
    file_names = loader.load_available_models()
    assert file_names == ['simple_text-1_0_1-1588436916.135168.pbz2', 'hello_world-1_0_0-1234.pbz2']


def test_load(loader):
    file_names = loader.load_available_models()
    try:
        for file_name in file_names:
            loader.load(file_name)
    except Exception as e:
        assert False
