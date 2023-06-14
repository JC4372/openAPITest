# Método 4. POST /v0.1/orgs/{org_name}/teams/{team_name}/users

import json
import pytest
import requests
from pymongo import MongoClient

connection_string = "mongodb://root:mongo123*@mongodb:27017/?authMechanism=DEFAULT"
client = MongoClient(connection_string)
db = client.get_database("openAPITestDB")
collection = db.get_collection("test_post_org_team_users")

test_data_add_user = list(collection.find({"test": "add_user_to_team"}))
test_data_user_already_member = list(collection.find({"test": "do_not_add_user_to_team_if_is_member"}))
test_data_team_not_found = list(collection.find({"test": "do_not_add_user_to_team_no_created"}))


@pytest.mark.parametrize("test_data", test_data_add_user)
def test_add_user_to_team(test_data):
    # Act
    add_user_to_team(test_data)

    # revert the changes made to ensure that the test is repeatable
    revert_action = test_data["revert_action"]
    rev_act_params = revert_action["parameters"]
    rev_act_url = revert_action["url"].format_map(rev_act_params)
    rev_act_header = revert_action["headers"]
    rev_act_status_code = revert_action["statusCode"]
    del_response = requests.delete(rev_act_url, headers=rev_act_header)
    assert del_response.status_code == rev_act_status_code


@pytest.mark.parametrize("test_data", test_data_user_already_member)
def test_do_not_add_user_to_team_if_is_member(test_data):
    # Act
    add_user_to_team(test_data)


@pytest.mark.parametrize("test_data", test_data_team_not_found)
def test_do_not_add_user_to_team_no_created(test_data):
    # Act
    add_user_to_team(test_data)


def add_user_to_team(test_data):
    # Arrange
    parameters = test_data["parameters"]
    url = test_data["url"].format_map(parameters)

    # Act
    response = requests.post(url, headers=test_data["headers"], json=test_data["body"])
    resp_data = json.loads(response.content)

    # Assert
    # verify status code
    assert response.status_code == test_data["statusCode"]
    # verify that the json returns the user information
    assert resp_data == test_data["result"]
