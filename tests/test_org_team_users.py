# Método 4. POST /v0.1/orgs/{org_name}/teams/{team_name}/users

import json
import random
import re
import string
import time

import pytest
import requests
from . import tokens

test_data_users = [
    (tokens.fullAccessUser1, "DevelopmentOrg", "BackendTeam",
     {
         "email": "caldemarvelasquez@unicesar.edu.co",
         "name": "caldemarvelasquez",
         "display_name": "Cristian Velasquez",
         "role": "collaborator"
     })]

test_data_user_already_member = [
    (tokens.fullAccessUser1, "DevelopmentOrg", "BackendTeam", "adejesusvilla@unicesar.edu.co",
     {
         "error": {
             "code": "Conflict",
             "message": "Validation error"
         }
     })]

test_data_team_not_found = [
    (tokens.fullAccessUser1, "DevelopmentOrg", "BackendTeamRandomY46346SJH", "adejesusvilla@unicesar.edu.co",
     {
         "error": {
             "code": "NotFound",
             "message": "Could not find a team named \"BackendTeamRandomY46346SJH\""
         }
     }
     )]


@pytest.mark.parametrize("token, org_name, team_name, user_data", test_data_users)
def test_add_user_to_team(token, org_name, team_name, user_data):
    # Arrange
    user_email = user_data["email"]

    # Act
    response = requests.post(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "user_email": user_email
    })
    resp_data = json.loads(response.content)

    # Assert
    # verify status code
    assert response.status_code == 201
    # verify that the json returns the user information
    assert resp_data == user_data

    # revert the changes made to ensure that the test is repeatable
    user_name = user_data["name"]
    del_response = requests.delete(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}',
                                   headers={
                                       "accept": "application/json",
                                       "X-API-Token": token
                                   })
    assert del_response.status_code == 204


@pytest.mark.parametrize("token, org_name, team_name, user_email, test_data", test_data_user_already_member)
def test_do_not_add_user_to_team_if_is_member(token, org_name, team_name, user_email, test_data):
    # Act
    response = requests.post(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "user_email": user_email
    })
    resp_data = json.loads(response.content)

    # Assert
    # check status code
    assert response.status_code == 409
    # check that the json returns a error message: "Validation error" (Conflict)
    assert resp_data == test_data


@pytest.mark.parametrize("token, org_name, team_name, user_email, test_data", test_data_team_not_found)
def test_do_not_add_user_to_team_no_created(token, org_name, team_name, user_email, test_data):
    # Act
    response = requests.post(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "user_email": user_email
    })
    resp_data = json.loads(response.content)

    # Assert
    # verify status code
    assert response.status_code == 404
    # verify that the json returns the user list
    assert resp_data == test_data
