# Método 5. DELETE /v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}

import json
import random
import re
import string
import time

import pytest
import requests
from pymongo import MongoClient

from . import tokens

connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client.get_database("openAPITestDB")
collection = db.get_collection("test_delete_user_of_team")

test_data_delete_user_of_team = list(collection.find({"test": "remove_user_of_team"}))
test_data_user_not_member = list(collection.find({"test": "do_not_delete_user_not_member"}))
test_data_org_not_found = list(collection.find({"test": "do_not_add_user_to_team_no_created"}))


@pytest.mark.parametrize("test_data", test_data_delete_user_of_team)
def test_remove_user_of_team(test_data):
    # Arrange
    # add a user first, then test the delete endpoint
    arrange_action = test_data["arrange"]
    add_usr_params = arrange_action["parameters"]
    add_usr_url = arrange_action["url"].format_map(add_usr_params)

    response = requests.post(add_usr_url, headers=arrange_action["headers"], json=arrange_action["body"])
    assert response.status_code == arrange_action["statusCode"]

    remove_user_from_team(test_data)


@pytest.mark.parametrize("test_data", test_data_user_not_member)
def test_do_not_delete_user_not_member(test_data):
    # Act
    remove_user_from_team(test_data)


def remove_user_from_team(test_data):
    parameters = test_data["parameters"]
    url = test_data["url"].format_map(parameters)
    # Act
    del_response = requests.delete(url, headers=test_data["headers"])
    resp_data = None if del_response.content is b'' else json.loads(del_response.content)
    # Assert
    # verify status code
    assert del_response.status_code == test_data["statusCode"]
    assert resp_data == test_data.get("result")


@pytest.mark.parametrize("test_data", test_data_org_not_found)
def test_do_not_add_user_to_team_no_created(test_data):
    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["result"]["message"], re.IGNORECASE)

    parameters = test_data["parameters"]
    parameters["org_name"] += ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    url = test_data["url"].format_map(parameters)

    # Act
    response = requests.delete(url, headers=test_data["headers"])
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == test_data["statusCode"]
    # check that the json contains the error code 404 Not Found
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["result"]["statusCode"]
    assert resp_data["code"] == test_data["result"]["code"]
