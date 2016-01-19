# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014 Anler Hernández <hello@anler.me>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from unittest.mock import patch, Mock
from taiga_contrib_slack_auth import connector as slack


def test_url_builder():
    assert (slack._build_url("login", "authorize") ==
            "https://api.slack.com/login/oauth/authorize")
    assert (slack._build_url("login","access-token") ==
            "https://api.slack.com/login/oauth/access_token")
    assert (slack._build_url("user", "profile") ==
            "https://api.slack.com/user")
    assert (slack._build_url("user", "emails") ==
            "https://api.slack.com/user/emails")


def test_login_without_settings_params():
    with pytest.raises(slack.slackApiError) as e, \
            patch("taiga_contrib_slack_auth.connector.requests") as m_requests:
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"access_token": "xxxxxxxx"}

        auth_info = slack.login("*access-code*", "**client-id**", "*ient-secret*", slack.HEADERS)
    assert e.value.status_code == 400
    assert "error_message" in e.value.detail


def test_login_success():
    with patch("taiga_contrib_slack_auth.connector.requests") as m_requests, \
            patch("taiga_contrib_slack_auth.connector.CLIENT_ID") as CLIENT_ID, \
            patch("taiga_contrib_slack_auth.connector.CLIENT_SECRET") as CLIENT_SECRET:
        CLIENT_ID = "*CLIENT_ID*"
        CLIENT_SECRET = "*CLIENT_SECRET*"
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"access_token": "xxxxxxxx"}

        auth_info = slack.login("*access-code*", "**client-id**", "*client-secret*", slack.HEADERS)

        assert auth_info.access_token == "xxxxxxxx"
        m_requests.post.assert_called_once_with("https://slack.com/login/oauth/access_token",
                                                headers=slack.HEADERS,
                                                params={'code': '*access-code*',
                                                        'scope': 'user:emails',
                                                        'client_id': '**client-id**',
                                                        'client_secret': '*client-secret*'})


def test_login_whit_errors():
    with pytest.raises(slack.slackApiError) as e, \
            patch("taiga_contrib_slack_auth.connector.requests") as m_requests, \
            patch("taiga_contrib_slack_auth.connector.CLIENT_ID") as CLIENT_ID, \
            patch("taiga_contrib_slack_auth.connector.CLIENT_SECRET") as CLIENT_SECRET:
        CLIENT_ID = "*CLIENT_ID*"
        CLIENT_SECRET = "*CLIENT_SECRET*"
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"error": "Invalid credentials"}

        auth_info = slack.login("*access-code*", "**client-id**", "*ient-secret*", slack.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 200
    assert e.value.detail["error"] == "Invalid credentials"


def test_get_user_profile_success():
    with patch("taiga_contrib_slack_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"id": 1955,
                                        "login": "mmcfly",
                                        "name": "martin seamus mcfly",
                                        "bio": "time traveler"}

        user_profile = slack.get_user_profile(slack.HEADERS)

        assert user_profile.id == 1955
        assert user_profile.username == "mmcfly"
        assert user_profile.full_name == "martin seamus mcfly"
        assert user_profile.bio == "time traveler"
        m_requests.get.assert_called_once_with("https://api.slack.com/user",
                                               headers=slack.HEADERS)


def test_get_user_profile_whit_errors():
    with pytest.raises(slack.slackApiError) as e, \
            patch("taiga_contrib_slack_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 401
        m_response.json.return_value = {"error": "Invalid credentials"}

        auth_info = slack.get_user_profile(slack.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 401
    assert e.value.detail["error"] == "Invalid credentials"


def test_get_user_emails_success():
    with patch("taiga_contrib_slack_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = [{"email": "darth-vader@bttf.com", "primary": False},
                                        {"email": "mmcfly@bttf.com", "primary": True}]

        emails = slack.get_user_emails(slack.HEADERS)

        assert len(emails) == 2
        assert emails[0].email == "darth-vader@bttf.com"
        assert not emails[0].is_primary
        assert emails[1].email == "mmcfly@bttf.com"
        assert emails[1].is_primary
        m_requests.get.assert_called_once_with("https://api.slack.com/user/emails",
                                               headers=slack.HEADERS)


def test_get_user_emails_whit_errors():
    with pytest.raises(slack.slackApiError) as e, \
            patch("taiga_contrib_slack_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 401
        m_response.json.return_value = {"error": "Invalid credentials"}

        emails = slack.get_user_emails(slack.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 401
    assert e.value.detail["error"] == "Invalid credentials"


def test_me():
    with patch("taiga_contrib_slack_auth.connector.login") as m_login, \
            patch("taiga_contrib_slack_auth.connector.get_user_profile") as m_get_user_profile, \
            patch("taiga_contrib_slack_auth.connector.get_user_emails") as m_get_user_emails:
        m_login.return_value = slack.AuthInfo(access_token="xxxxxxxx")
        m_get_user_profile.return_value = slack.User(id=1955,
                                                      username="mmcfly",
                                                      full_name="martin seamus mcfly",
                                                      bio="time traveler")
        m_get_user_emails.return_value = [slack.Email(email="darth-vader@bttf.com", is_primary=False),
                                          slack.Email(email="mmcfly@bttf.com", is_primary=True)]

        email, user = slack.me("**access-code**")

        assert email == "mmcfly@bttf.com"
        assert user.id == 1955
        assert user.username == "mmcfly"
        assert user.full_name == "martin seamus mcfly"
        assert user.bio == "time traveler"

        headers = slack.HEADERS.copy()
        headers["Authorization"] = "token xxxxxxxx"
        m_get_user_profile.assert_called_once_with(headers=headers)
        m_get_user_emails.assert_called_once_with(headers=headers)
