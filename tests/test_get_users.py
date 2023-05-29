# Método 1. GET /v0.1/user

import json
import re
from pymongo import MongoClient
import requests
import pytest


connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client.get_database("openAPITestDB")
collection = db.get_collection("test_get_users")

test_data_users = list(collection.find({"test": "get_profile_date_of_user"}))
test_data_missing_token = list(collection.find({"test": "do_not_return_profile_without_token"}))
test_data_invalid_token = list(collection.find({"test": "do_not_return_profile_with_invalid_token"}))

client.close()


@pytest.mark.parametrize("test_data", test_data_users)
def test_get_profile_date_of_user(test_data):
    # Act
    response = requests.get(test_data["url"], headers=test_data["headers"])
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == test_data["statusCode"]
    # verify that the json returns the user information
    assert resp_data == test_data["result"]


@pytest.mark.parametrize("test_data", test_data_missing_token)
def test_do_not_return_profile_without_token(test_data):
    do_not_return_profile(test_data)


@pytest.mark.parametrize("test_data", test_data_invalid_token)
def test_do_not_return_profile_with_invalid_token(test_data):
    do_not_return_profile(test_data)


def do_not_return_profile(test_data):
    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["result"]["message"], re.IGNORECASE)

    # Act
    response = requests.get(test_data["url"], headers=test_data["headers"])
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == test_data["statusCode"]
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["result"]["statusCode"]
    assert resp_data["code"] == test_data["result"]["code"]
