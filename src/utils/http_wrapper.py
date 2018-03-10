"""This module fetches the data from APIs.

This module fetches the data from APIs for the passed requested entity.
Module also decode the data of APIs accordingly to the requested
entityResult type.


Attributes:
    T (TypeVar) : Indicate the dynamic(generic) type. It is used where
        a function or parameter contains multiple type.
    LOGGER (logging) : logger for the module

"""

import json
import logging
from typing import List, Dict, TypeVar
import requests
from requests import Response

LOGGER = logging.getLogger(__name__)
T = TypeVar('T')


class HttpClient:
    """This class fetches the data of APIs for the given parameters.

     Attributes:
         client: Object of requests type to fetch data from http server.
         timeout: Timeout duration for http request.
     """
    #client: requests
    #timeout: int = 20

    def __init__(self, timeout: int = 20):
        """Set the default timeout value.

        Args:
            timeout (:obj :int, `optional`): Timeout duration for http request, default 20.
        """
        self.timeout = timeout

    def get(self, url: str, headers: dict = None, params: dict = None) -> Response:
        """Fetches the api data.

        Args:
            url: Endpoint URL from which data will be fetched.
            headers: Request headers.
            params: Query parameters of the request.

        Returns:
            Response: HTTP response for the request.
        """
        default_headers = {'Accept': 'application/json'}
        if headers:
            default_headers.update(headers)
        resp = requests.get(url, headers=default_headers, timeout=self.timeout, params=params)
        LOGGER.info('request URL {} with params {}, response status code {}'
                    .format(url, params, resp.status_code))
        resp.raise_for_status()
        return resp


class HttpWrapper:
    def __init__(self):
        self.client = HttpClient()

    def call_api(self, request_url) -> T:
        try:
            response = self.client.get(request_url)
            return json.loads(response.text)
            return response
        except Exception as ex:
            error = "Error : " + str(ex) + " in " + __file__ + " function : get_entity"
            return ApiProblem(error, 4001)