#!/usr/bin/python
from __future__ import print_function
import os
import sys
import json
import unittest

sys.path.remove(sys.path[0])
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../../swagger-graphene")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../../swagger-graphene/utils")))

from src.config_reader import ConfigReader

class TestHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.list = {"entity": "test", "swagger_url": "url-swagger", "api_url": "url-api"}

    def _dtest_put_get_configs(self):
        result = ConfigReader().put_configs(self.__class__.list)
        self.assertTrue(result)

        entity, swagger_source, api_source = ConfigReader().get_configs(self.__class__.list["entity"])
        self.assertEqual(self.__class__.list["entity"], entity)
        self.assertEqual(self.__class__.list["swagger_url"], swagger_source)
        self.assertEqual(self.__class__.list["api_url"], api_source)


    @classmethod
    def tearDownClass(cls):
        ConfigReader().delete_configs(cls.list["entity"])
if __name__ == '__main__':
    unittest.main()