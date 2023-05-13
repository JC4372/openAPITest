# Método 3. PATCH /v0.1/user

import json
import random
import string

import pytest
import requests
from . import tokens

test_data_users = [
    (tokens.fullAccessUser3, "JESUS MANUEL CAMACHO SARMIENTO", "J CAMACHO", {
        "id": "4e24f0bd-d04e-4fa6-9375-900f1e9c5413",
        "display_name": "J CAMACHO",
        "email": "jmanuelcamacho@unicesar.edu.co",
        "name": "jmanuelcamacho",
        "avatar_url": None,
        "can_change_password": False,
        "origin": "appcenter"
    })
]

test_data_display_name_empty = [(tokens.fullAccessUser3, {
  "error": {
    "code": "BadRequest",
    "message": "Name contains invalid character "
  }
})]

test_data_display_name_missing = [(tokens.fullAccessUser3, {
  "error": {
    "code": "BadRequest",
    "message": "Missing required body parameter \"user\""
  }
})]


@pytest.mark.parametrize("token, old_name, new_name, user_data", test_data_users)
def test_get_list_of_org_users(token, old_name, new_name, user_data):
    # Act
    response = requests.patch(f'https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "display_name": new_name
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 200

    # check that the json returns updated user information
    assert resp_data == user_data

    # revert the changes made to ensure that the test is repeatable
    requests.patch(f'https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "display_name": old_name
    })


@pytest.mark.parametrize("token, test_data", test_data_display_name_empty)
def test_do_not_update_display_name_when_value_is_empty(token, test_data):
    # Act
    response = requests.patch(f'https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "display_name": ""
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 400
    # check that the json contains error message "Name contains invalid character "
    assert resp_data == test_data


@pytest.mark.parametrize("token, test_data", test_data_display_name_missing)
def test_do_not_update_display_name_when_missing(token, test_data):
    # Act
    response = requests.patch(f'https://api.appcenter.ms/v0.1/user', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={

    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 400
    # check that the json contains error message Missing required body parameter "user"
    assert resp_data == test_data
