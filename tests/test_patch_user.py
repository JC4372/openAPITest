# Método 3. PATCH /v0.1/user

import json
import pytest
import requests
from pymongo import MongoClient

connection_string = "mongodb://root:mongo123*@mongodb:27017/?authMechanism=DEFAULT"
client = MongoClient(connection_string)
db = client.get_database("openAPITestDB")
collection = db.get_collection("test_patch_user")

test_data_user_display_name = list(collection.find({"test": "update_display_name"}))
test_data_display_name_empty = list(collection.find({"test": "do_not_update_display_name_when_value_is_empty"}))
test_data_display_name_missing = list(collection.find({"test": "do_not_update_display_name_when_missing"}))

client.close()


@pytest.mark.parametrize("test_data", test_data_user_display_name)
def test_update_display_name(test_data):
    # Act
    update_display_name(test_data)

    # revert the changes made to ensure that the test is repeatable
    response = requests.patch(test_data["url"], headers=test_data["headers"], json=test_data["reset_data"])
    assert response.status_code == test_data["statusCode"]


@pytest.mark.parametrize("test_data", test_data_display_name_empty)
def test_do_not_update_display_name_when_value_is_empty(test_data):
    update_display_name(test_data)


@pytest.mark.parametrize("test_data", test_data_display_name_missing)
def test_do_not_update_display_name_when_missing(test_data):
    update_display_name(test_data)


def update_display_name(test_data):
    # Act
    response = requests.patch(test_data["url"], headers=test_data["headers"], json=test_data["body"])
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == test_data["statusCode"]

    # check response body
    assert resp_data == test_data["result"]
