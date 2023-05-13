# Método 2. GET /v0.1/orgs/{org_name}/users

import json
import random
import re
import string

import pytest
import requests
from . import tokens

test_data_users = [
    (tokens.fullAccessUser1, "DevelopmentOrg", [
        {
            "email": "adejesusvilla@unicesar.edu.co",
            "name": "adejesusvilla",
            "display_name": "AGNER DE JESUS VILLA FABREGA",
            "joined_at": "2023-05-09T21:40:01.202Z",
            "role": "member"
        },
        {
            "email": "caldemarvelasquez@unicesar.edu.co",
            "name": "caldemarvelasquez",
            "display_name": "Cristian Velasquez",
            "joined_at": "2023-05-13T02:19:17.460Z",
            "role": "member"
        },
        {
            "email": "accms9587@outlook.com",
            "name": "accms9587",
            "display_name": "Jesus Camacho",
            "joined_at": "2023-05-09T21:36:33.143Z",
            "role": "admin"
        },
        {
            "email": "osparra@unicesar.edu.co",
            "name": "OSPARRA",
            "display_name": "OMAR STEVEN PARRA ROZO",
            "joined_at": "2023-05-13T05:50:31.521Z",
            "role": "member"
        }
    ])]

test_data_org_not_found = [(tokens.fullAccessUser1, {
    "message": r"Not found. Correlation ID: [a-f\d]{8}-(?:[a-f\d]{4}-){3}[a-f\d]{12}",
    "statusCode": 404,
    "code": "Not Found"
})]

test_data_org_read_only_token = [(tokens.readOnly, "DevelopmentOrg", {
    "message": "Forbidden",
    "statusCode": 403,
    "code": "Forbidden"
})]


@pytest.mark.parametrize("token, org_name, users_data", test_data_users)
def test_get_list_of_org_users(token, org_name, users_data):
    # Act
    response = requests.get(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/users', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # verify status code
    assert response.status_code == 200
    # verify that the json returns the user list
    assert resp_data == users_data


@pytest.mark.parametrize("token, test_data", test_data_org_not_found)
def test_do_not_return_users_list_of_not_found_org(token, test_data):
    # Arrange
    # regex expression
    guid_regex = re.compile(test_data["message"], re.IGNORECASE)
    org_random = 'RandomOrg_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # Act
    response = requests.get(f'https://api.appcenter.ms/v0.1/orgs/{org_random}/users', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 404
    # check that the json contains the error code 404 Not Found
    assert guid_regex.match(resp_data["message"])
    assert resp_data["statusCode"] == test_data["statusCode"]
    assert resp_data["code"] == test_data["code"]


@pytest.mark.parametrize("token, org_name, test_data", test_data_org_read_only_token)
def test_do_not_return_org_users_list_with_read_only_token(token, org_name, test_data):
    # Act
    response = requests.get(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/users', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 403
    # check that the json contains the error code 404 Not Found
    assert resp_data == test_data
