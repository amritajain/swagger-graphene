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

from src.index import *

class TestHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.list = {"entity": "test", "swagger_url": "url-swagger", "api_url": "url-api"}
        pass

    def test_main_handler_complicated_query(self):
        query = '''
        {
          Pet {
            id
            name
            tags {
              id
              name
            }
            photoUrls
            status
            category {
              id
              name
            }
          }
        }
        '''
        event = {}
        event['body'] = ({"query": query})
        response = main_handler(event, {})
        print(response)
        self.assertEqual(1, response['data']['Pet']['id'])
        self.assertEqual("buddy", response['data']['Pet']['name'])
        self.assertEqual("cute", response['data']['Pet']['status'])
        self.assertEqual(41, response['data']['Pet']['category']['id'])
        self.assertEqual("catgeoryName", response['data']['Pet']['category']['name'])
        self.assertListEqual(["url1", "url2"], response['data']['Pet']['photoUrls'])
        self.assertEqual(2, len(response['data']['Pet']['tags']))
        self.assertEqual(111, response['data']['Pet']['tags'][0]['id'])
        self.assertEqual("tagName1", response['data']['Pet']['tags'][0]['name'])

    def test_main_handler_documentation_query(self):
        event = {}
        event['body']= ({"query":"  query IntrospectionQuery {    __schema {      queryType { name }      mutationType { name }      subscriptionType { name }      types {        ...FullType      }      directives {        name        description        args {          ...InputValue        }        onOperation        onFragment        onField      }    }  }  fragment FullType on __Type {    kind    name    description    fields(includeDeprecated: true) {      name      description      args {        ...InputValue      }      type {        ...TypeRef      }      isDeprecated      deprecationReason    }    inputFields {      ...InputValue    }    interfaces {      ...TypeRef    }    enumValues(includeDeprecated: true) {      name      description      isDeprecated      deprecationReason    }    possibleTypes {      ...TypeRef    }  }  fragment InputValue on __InputValue {    name    description    type { ...TypeRef }    defaultValue  }  fragment TypeRef on __Type {    kind    name    ofType {      kind      name      ofType {        kind        name        ofType {          kind          name        }      }    }  }"})
        response = main_handler(event, {})

        #self.assertIn("_schema", response['data'].keys())
        self.assertEquals("Query", response['data']['__schema']['queryType']['name'])
        self.assertIn("Pet", response['data']['__schema']['types'][0]['fields'][0]['type']['name'])

    @classmethod
    def tearDownClass(cls):
        #ConfigReader().delete_configs(cls.list["entity"])
        pass

if __name__ == '__main__':
    unittest.main()