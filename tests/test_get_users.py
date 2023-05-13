import json
import re

import requests
import pytest
from . import tokens

test_data_users = [
    (tokens.fullAccessUser1, {
        "id": "2afb883f-48db-4c26-8248-a88bebf3ba38",
        "display_name": "Jesus Camacho",
        "email": "accms9587@outlook.com",
        "name": "accms9587",
        "avatar_url": None,
        "can_change_password": False,
        "created_at": "2023-05-09T21:07:38.069Z",
        "origin": "appcenter"
    }),
    (tokens.fullAccessUser2, {
        "id": "6af46696-8390-458a-9b4b-04c108165d3a",
        "display_name": "AGNER DE JESUS VILLA FABREGA",
        "email": "adejesusvilla@unicesar.edu.co",
        "name": "adejesusvilla",
        "avatar_url": None,
        "can_change_password": False,
        "created_at": "2023-05-09T17:27:35.178Z",
        "origin": "appcenter"
    })]

test_data_missing_token = [{
    "message": r"Missing valid authentication token. Correlation ID: [a-f\d]{8}-(?:[a-f\d]{4}-){3}[a-f\d]{12}",
    "statusCode": 401,
    "code": "Unauthorized"
}]

test_data_invalid_token = [(tokens.invalid, {
    "message": r"Unauthorized. Correlation ID: [a-f\d]{8}-(?:[a-f\d]{4}-){3}[a-f\d]{12}",
    "statusCode": 401,
    "code": "Unauthorized"
})]


@pytest.mark.parametrize("token, userdata", test_data_users)
def test_get_profile_date_of_user(token, userdata):
    # Act
    response = requests.get('https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 200
    # verify that the json returns the user information
    assert resp_data == userdata


@pytest.mark.parametrize("test_data", test_data_missing_token)
def test_do_not_return_profile_without_token(test_data):
    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["message"], re.IGNORECASE)

    # Act
    response = requests.get('https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 401
    # check that the json contains the error code 401 Unauthorized and the message "Missing valid authentication token"
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["statusCode"]
    assert resp_data["code"] == test_data["code"]


@pytest.mark.parametrize("token, test_data", test_data_invalid_token)
def test_do_not_return_profile_with_invalid_token(token, test_data):

    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["message"], re.IGNORECASE)

    # Act
    response = requests.get('https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 401
    # check that the json contains the error code 401 Unauthorized
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["statusCode"]
    assert resp_data["code"] == test_data["code"]
