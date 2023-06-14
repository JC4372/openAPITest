# Método 2. GET /v0.1/orgs/{org_name}/users

import json
import random
import re
import string
import pytest
import requests
import os
from pymongo import MongoClient

connection_string = os.environ.get('MONGO_CONNECTION_STRING')
client = MongoClient(connection_string)
db = client.get_database("openAPITestDB")
collection = db.get_collection("test_get_org_users")

test_data_users = list(collection.find({"test": "get_list_of_org_users"}))
test_data_org_not_found = list(collection.find({"test": "do_not_return_users_list_of_not_found_org"}))
test_data_org_read_only_token = list(collection.find({"test": "do_not_return_org_users_list_with_read_only_token"}))

client.close()


@pytest.mark.parametrize("test_data", test_data_users)
def test_get_list_of_org_users(test_data):
    request_get_list_users(test_data)


@pytest.mark.parametrize("test_data", test_data_org_read_only_token)
def test_do_not_return_org_users_list_with_read_only_token(test_data):
    request_get_list_users(test_data)


@pytest.mark.parametrize("test_data", test_data_org_not_found)
def test_do_not_return_users_list_of_not_found_org(test_data):
    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["result"]["message"], re.IGNORECASE)

    parameters = test_data["parameters"]
    parameters["org_name"] += ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    url = test_data["url"].format_map(parameters)

    # Act
    response = requests.get(url, headers=test_data["headers"])
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == test_data["statusCode"]
    # check response data
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["result"]["statusCode"]
    assert resp_data["code"] == test_data["result"]["code"]


def request_get_list_users(test_data):
    # Arrange
    parameters = test_data["parameters"]
    url = test_data["url"].format_map(parameters)

    # Act
    response = requests.get(url, headers=test_data["headers"])
    resp_data = json.loads(response.content)
    # Assert
    # verify status code
    assert response.status_code == test_data["statusCode"]
    # verify that the json returns the user list
    assert resp_data == test_data["result"]
