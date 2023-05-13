# Método 5. DELETE /v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}

import json
import random
import re
import string
import time

import pytest
import requests
from . import tokens

test_data_delete_user_of_team = [
    (tokens.fullAccessUser1, "DevelopmentOrg", "FrontTeam", "adejesusvilla@unicesar.edu.co", "adejesusvilla")]

test_data_user_not_member = [
    (tokens.fullAccessUser1, "DevelopmentOrg", "FrontTeam", "OSPARRA",
     {
         "error": {
             "code": "NotFound",
             "message": "The user with the name \"OSPARRA\" is not a member of the team FrontTeam"
         }
     }
     )]


@pytest.mark.parametrize("token, org_name, team_name, user_email, user_name", test_data_delete_user_of_team)
def test_remove_user_of_team(token, org_name, team_name, user_email, user_name):
    # Arrange
    # add a user first, then test the delete endpoint
    requests.post(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users', headers={
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Token": token
    }, json={
        "user_email": user_email
    })

    # Act
    del_response = requests.delete(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}',
                                   headers={
                                       "accept": "application/json",
                                       "X-API-Token": token})
    # Assert
    # verify status code
    assert del_response.status_code == 204
    assert del_response.content is b''


@pytest.mark.parametrize("token, org_name, team_name, user_name, test_data", test_data_user_not_member)
def test_do_not_delete_user_not_member(token, org_name, team_name, user_name, test_data):
    # Act
    response = requests.delete(f'https://api.appcenter.ms/v0.1/orgs/{org_name}/teams/{team_name}/users/{user_name}', headers={
        "accept": "application/json",
        "X-API-Token": token
    })
    resp_data = json.loads(response.content)

    # Assert
    # verify status code
    assert response.status_code == 404
    # check that the json returns a error message: "The user with the name "..." is not a member of the team
    # FrontTeam" (Conflict)
    assert resp_data == test_data
