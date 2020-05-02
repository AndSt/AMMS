import unittest
from src.servable_base import ServableMetaData


class ServableMetaDataTest(unittest.TestCase):

    def setUp(self) -> None:
        self.s1 = ServableMetaData('test_model', '1', '1234')
        self.s2 = ServableMetaData('test_model', '1.0', '1234')
        self.s3 = ServableMetaData('test_model', '1.1', '123456')
        self.s4 = ServableMetaData('test_model', '1.1.2', '123456')
        self.s5 = ServableMetaData('test_model', '2.0.0', '1234')

        self.s6 = ServableMetaData('test_model2', '1.0.2', '1234')

    def is_equal(self):
        self.assertTrue(self.s1.is_equal(self.s1))
        self.assertFalse(self.s1.is_equal(self.s2))
        self.assertFalse(self.s1.is_equal(self.s6))


def test_servable_meta_is_equal():
