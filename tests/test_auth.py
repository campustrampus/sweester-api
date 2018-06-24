"""
A set of tests to validate the functionality of the auth module.
"""
import pytest
from flask import session

from sweester.utils.db import get_db


def test_register(client, app):
    """
    Tests a users ability to register
    :param client: A user agent used to make requests
    :param app: A copy of the app.
    :return: N/A
    """
    # test that viewing the page renders without template errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers['Location'] == 'http://localhost/auth/login'

    # test that the user was inserted into the database
    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """
    Test that the register function validates input.
    :param client: A user agent used to make requests.
    :param username: A test username.
    :param password: A test password.
    :param message: A test return message.
    :return: N/A
    """
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    """ test that viewing the page renders without template errors """
    assert client.get('/auth/login').status_code == 200

    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """
    Test that the login validates the input.
    :param auth: Authorization client.
    :param username: The test username.
    :param password: The test password.
    :param message: The test return message.
    :return: N/A
    """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """
    Tests that the user is removed from session on logout.
    :param client: A user agent used to make requests.
    :param app: A copy of the app.
    :return: N/A
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
