# /usr/bin/python3
"""This module acts as controller for the app.

This module contains the main_handler function from where app execution will be started.
Main handler fetches the entity from request call that entity for response and get the
requested response.

Attributes:
    T (TypeVar) : Indicate the dynamic(generic) type. It is used where
        a function or parameter contains multiple type.
    logger (logging) : logger for the app

"""
import logging
from typing import TypeVar
from graphql import parse
import graphene
from src.config_reader import ConfigReader
from src.utils.swagger_wrapper import SwaggerWrapper
from src.utils.http_wrapper import HttpWrapper
import os
import json

T = TypeVar('T')

logging.basicConfig(level=logging.DEBUG, filename='/tmp/content.log')
LOGGER = logging.getLogger('aws_xray_sdk').setLevel(logging.DEBUG)

def main_handler(event: dict, context) -> dict:
    """ Main handler from which execution will be started.

    This function is main handler which will be called when request comes.
    It fetch the query from the request, validate it and then fetch the data
    accordingly.

    Args:
        event (dict): This parameter contains the request data.
        context (dict): This parameter contains the lambda execution context

    Returns :
        dict : Contains the response to the query.

    """
    query = event['body']['query']
    entity = payload_to_entity(parse(query))
    root_query = entity_to_schema(entity, query)

    schema = graphene.Schema(query=root_query)
    result = schema.execute(query)
    return {
        'data': result.data,
        'headers': {
            'Content-Type': 'application/json',
        }
    }



def entity_to_schema(entity, payload):

    # Query the database for url info
    entity, swagger_source, api_source = ConfigReader().get_configs(entity)

    # Read swagger json file
    swagger_data = swagger_definitions_from_source(swagger_source)

    # Get data from api
    api_data = HttpWrapper().call_api(api_source)

    fields = SwaggerWrapper(swagger_data['definitions'], api_data).swagger_to_graphene(entity)
    field_object = type(entity, (graphene.ObjectType,), fields)
    root_object = {
        entity: graphene.Field(field_object,
                                          resolver=lambda obj, args, context, info:  field_object(**api_data))
    }
    root_query = type("Query", (graphene.ObjectType,), root_object)


    return root_query


def swagger_definitions_from_source(swagger_source):
    swagger_source = swagger_source.strip()
    # @todo If local file open it else make an http call
    if swagger_source.startswith("file://"):

        swagger_source_filename = os.path.dirname(os.path.abspath(__file__))+"/.."+swagger_source[7:]
        with open(swagger_source_filename) as json_data:
            swagger_data = json.load(json_data)
            return swagger_data
    elif swagger_source.startswith("http://"):
        return HttpWrapper().call_api(swagger_source)
    else:
        # @todo throw exception
        pass



def payload_to_entity(parsed_query):
    parsed_body = parsed_query.loc.source.body
    entity = str.split(parsed_body, "{", 2)
    return "".join(entity[1].split())
