# /usr/bin/python3

import json
import csv
import os
import boto3
from botocore.exceptions import ClientError

class ConfigReader:
    _source = "local"
    _database_filename = "database.csv"

    def __init__(self, source="local"):
        self.__class__._source = source

    def get_configs(self, entity):
        method = "get_configs_" + self.__class__._source
        return getattr(self, method)(entity)

    def put_configs(self, data):
        method = "put_configs_" + self.__class__._source
        return getattr(self, method)(data)

    def delete_configs(self, entity):
        method = "get_configs_" + self.__class__._source
        return getattr(self, method)(entity)

    def get_configs_local(self, entity):

        line = None
        # Query the database for url info
        try:
            curr_dir = os.path.dirname(os.path.abspath(__file__))+"/../data/" + self._database_filename
            with open(curr_dir) as csv_data:
                local_data = list(csv.reader(csv_data))
                for line in local_data:
                    if entity == line[0]:
                        return line

            if line is None:
                print("error: setup database first, see README")

            return line
        except FileNotFoundError as ex:
            print("error: file not found")
            raise ex


    def get_configs_s3(self, entity):
        line = None
        try:
            s3_client = boto3.resource("s3")
            s3_obj = s3_client.Object(os.environ['source_s3_bucket'], self._database_filename)
            s3_data = s3_obj.get()['Body'].read().decode('utf-8')
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                print("error: file not found")
            else:
                raise ex

        for line in s3_data:
            if entity == line[0]:
                return line

        if line is None:
            print("error: setup database first, see README")

        return line

