import pytest
from typing import List

from src.servable_base import ServableMetaData, Servable
from src.version_manager import AspiredModel


@pytest.fixture()
def servable_metas():
    vals = [
        ['test_model_1', '1.0.0', '1234time'],
        ['test_model_1', '1.0.0', '1234time'],
        ['test_model_1', '1.2.0', '1235time'],
        ['test_model_1', '2.0.0', '1234time'],
        ['test_model_2', '1.0.0', '1234time'],
    ]
    servable_metas = [ServableMetaData(val[0], val[1], val[2]) for val in vals]
    return servable_metas


@pytest.fixture()
def file_names():
    return [
        'test_model_1-1_0_0-1234time.pbz2',
        'test_model_1-1_0_0-1234time.pbz2',
        'test_model_1-1_2_0-1235time.pbz2',
        'test_model_1-2_0_0-1234time.pbz2',
        'test_model_2-1_0_0-1234time.pbz2'
    ]


def test_servable_meta_from_file_name(servable_metas, file_names):
    for i in range(1, len(servable_metas)):
        for j in range(1, len(servable_metas)):
            if i == j:
                assert ServableMetaData.from_file_name(file_names[i]) == servable_metas[j]
            else:
                assert ServableMetaData.from_file_name(file_names[i]) != servable_metas[j]


def test_servable_meta_is_equal(servable_metas):
    assert servable_metas[0] == servable_metas[1]
    for i in range(1, len(servable_metas)):
        for j in range(2, len(servable_metas)):
            if i != j:
                assert servable_metas[i] != servable_metas[j]


def test_servable_meta_is_compatible_and_newer(servable_metas):
    assert servable_metas[0].is_newer(servable_metas[1]) == False
    assert servable_metas[2].is_newer(servable_metas[0]) == True
    assert servable_metas[3].is_newer(servable_metas[0]) == False

    for i in range(1, len(servable_metas)):
        assert servable_metas[4].is_newer(servable_metas[i]) == False


def test_servable_meta_compatible_newest(servable_metas):
    assert servable_metas[0].newest_version(servable_metas[1:]) == servable_metas[2]


def test_servable_meta_to_file_name(servable_metas, file_names):
    for i in range(1, len(servable_metas)):
        for j in range(2, len(servable_metas)):
            if i == j:
                assert file_names[i] == servable_metas[i].to_file_name()
            else:
                assert file_names[i] != servable_metas[j].to_file_name()
