import asyncio
from unittest import IsolatedAsyncioTestCase

from ruteni import status
from ruteni.app import Ruteni
from ruteni.extractors import PrefixExtractor
from ruteni.nodes import ExtractorNode, IterableNode
from ruteni.nodes.api import api_nodes
from starlette.middleware.cors import ALL_METHODS
from starlette.testclient import TestClient

from .config import (
    BASE_URL,
    CLIENT_ID,
    USER,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
    clear_database,
    test_env,
)

with test_env:
    from ruteni.plugins.auth.session import api_node as session_api
    from ruteni.plugins.passwords import register_user
    from ruteni.plugins.session import get_user_from_session
    from ruteni.plugins.users import api_node as user_api

SIGNIN_URL = BASE_URL + "/api/auth/v1/signin"
SIGNOUT_URL = BASE_URL + "/api/auth/v1/signout"
USER_INFO_URL = BASE_URL + "/api/user/v1/info"


class SessionAuthTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ruteni = Ruteni(
            ExtractorNode(PrefixExtractor("/api"), IterableNode(api_nodes)),
            services={"ruteni:auth-api", "ruteni:user-api"},
        )

    def tearDown(self) -> None:
        clear_database()

    def test_login(self) -> None:
        with TestClient(self.ruteni) as client:
            asyncio.run(
                register_user(USER_NAME, USER_EMAIL, USER_LOCALE, USER_PASSWORD)
            )

            # signin with wrong methods
            for method in ALL_METHODS:
                if method != "POST":
                    response = client.request(method, SIGNIN_URL)
                    self.assertEqual(
                        response.status_code, status.METHOD_NOT_ALLOWED_405
                    )

            # signin with bad parameters
            response = client.post(
                SIGNIN_URL, json={"email": "", "password": "", "client_id": ""}
            )
            self.assertEqual(response.status_code, status.BAD_REQUEST_400)

            # signin with an unknown email
            response = client.post(
                SIGNIN_URL,
                json={"email": "foo@bar.fr", "password": "", "client_id": CLIENT_ID},
            )
            self.assertEqual(response.status_code, status.UNAUTHORIZED_401)

            # signin with a bad password
            response = client.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": "bad-password",
                    "client_id": CLIENT_ID,
                },
            )
            self.assertEqual(response.status_code, status.UNAUTHORIZED_401)

            # signin with correct credentials
            response = client.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": USER_PASSWORD,
                    "client_id": CLIENT_ID,
                },
            )
            self.assertEqual(response.status_code, status.OK_200)
            self.assertEqual(response.json(), USER)
            self.assertEqual(get_user_from_session(client.cookies["session"]), USER)

            # get user info when authenticated
            response = client.get(USER_INFO_URL)
            self.assertEqual(response.status_code, status.OK_200)
            self.assertEqual(response.json(), USER)

            # signout
            for method in ALL_METHODS:
                if method not in ("GET", "HEAD"):
                    response = client.request(method, SIGNOUT_URL)
                    self.assertEqual(
                        response.status_code, status.METHOD_NOT_ALLOWED_405
                    )

            response = client.get(SIGNOUT_URL)
            self.assertEqual(client.cookies.get_dict(), {})

            # get user info when not authenticated
            response = client.get(USER_INFO_URL)
            self.assertEqual(response.status_code, status.FORBIDDEN_403)


if __name__ == "__main__":
    import unittest

    unittest.main()
