#!/usr/bin/python
from __future__ import print_function
import os
import sys
import json
import unittest
import graphene
sys.path.remove(sys.path[0])
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../../swagger-graphene")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../../swagger-graphene/utils")))

from src.utils.swagger_wrapper import SwaggerWrapper
from src.utils.http_wrapper import HttpWrapper

class TestHandler(unittest.TestCase):

    def test_swagger_to_graphene_minimal(self):
        entity = "Pet"

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        swagger_json = open(root_dir + '/data/simple_swagger_definition.json').read()

        swagger_definitions = json.loads(swagger_json)

        # Get data from api
        api_source = "https://github.com/amritajain/swagger-graphene/blob/master/data/api-simple-pet"
        api_data = HttpWrapper().call_api(api_source)

        fields = SwaggerWrapper(swagger_definitions['definitions'], api_data).swagger_to_graphene(entity)
        result = type(entity, (graphene.ObjectType,), fields)

        test_data = result.__getattribute__(result, "_meta").local_fields
        self.assertEqual("Int", test_data["id"].type.__name__)
        self.assertEqual("String", test_data["age"].type.__name__)
        self.assertEqual("String", test_data["name"].type.__name__)


    def test_swagger_to_graphene_complex(self):
        entity = "Pet"
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        swagger_json = open(root_dir + '/data/swagger_definition.json').read()

        swagger_definitions = json.loads(swagger_json)

        api_source = "https://github.com/amritajain/swagger-graphene/blob/master/data/api-pet"
        api_data = HttpWrapper().call_api(api_source)


        fields = SwaggerWrapper(swagger_definitions['definitions'], api_data).swagger_to_graphene(entity)
        result = type(entity, (graphene.ObjectType,), fields)

        test_data = result.__getattribute__(result, "_meta").local_fields
        self.assertEqual("Int", test_data["id"].type.__name__)
        self.assertEqual("String", test_data["status"].type.__name__)
        self.assertEqual("String", test_data["name"].type.__name__)

        self.assertEqual("String", test_data["photoUrls"].type._of_type.__name__)
        self.assertEqual("List", test_data["photoUrls"].type.__class__.__name__)

        self.assertEqual("Category", test_data["category"].type._meta.name)
        self.assertIn("id", test_data["category"].type._meta.local_fields.keys())
        self.assertIn("name", test_data["category"].type._meta.local_fields.keys())

        self.assertEqual("Tag", test_data["tags"].type.of_type._meta.name)
        self.assertEqual("List", test_data["tags"].type.__class__.__name__)
        self.assertIn("id", test_data["tags"].type.of_type._meta.fields.keys())
        self.assertIn("name", test_data["tags"].type.of_type._meta.fields.keys())

        self.assertIn("id", test_data.keys())
        self.assertIn("name", test_data.keys())
        self.assertIn("category", test_data.keys())
        self.assertIn("photoUrls", test_data.keys())
        self.assertIn("status", test_data.keys())
        self.assertIn("tags", test_data.keys())

if __name__ == '__main__':
    unittest.main()