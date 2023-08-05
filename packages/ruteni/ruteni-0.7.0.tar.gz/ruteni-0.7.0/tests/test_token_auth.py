import asyncio
from datetime import datetime, timezone
from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from ruteni.app import Ruteni
from ruteni.extractors import PrefixExtractor
from ruteni.nodes import ExtractorNode, load_http_node_entry_point
from ruteni.status import (
    BAD_REQUEST_400,
    METHOD_NOT_ALLOWED_405,
    OK_200,
    UNAUTHORIZED_401,
    UNPROCESSABLE_ENTITY_422,
    UNSUPPORTED_MEDIA_TYPE_415,
)
from starlette.middleware.cors import ALL_METHODS
from starlette.testclient import TestClient

from .config import (
    BASE_URL,
    CLIENT_ID,
    SITE_NAME,
    USER,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
    clear_database,
    test_env,
)

SIGNIN_URL = BASE_URL + "/api/jauthn/v1/signin"
SIGNOUT_URL = BASE_URL + "/api/jauthn/v1/signout"

with test_env:
    from ruteni.plugins.auth.token import ACCESS_TOKEN_COOKIE_NAME
    from ruteni.plugins.passwords import register_user
    from ruteni.plugins.token import (
        ACCESS_TOKEN_EXPIRATION,
        REFRESH_TOKEN_EXPIRATION,
        new_refresh_token,
    )
    from ruteni.services.keys import keys


class TokenAuthTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ruteni = Ruteni(
            ExtractorNode(
                PrefixExtractor("/api"),
                load_http_node_entry_point("ruteni", "jauthn-api"),
            ),
            services={"ruteni:keys", "ruteni:user-api"},
        )

    def tearDown(self) -> None:
        clear_database()

    def valid_signin_info(self, content: dict[str, Any]) -> bool:
        return (
            "access_token" in content
            and "refresh_token" in content
            and "user" in content
        )

    def test_login(self) -> None:
        with TestClient(self.ruteni) as client:
            asyncio.run(
                register_user(USER_NAME, USER_EMAIL, USER_LOCALE, USER_PASSWORD)
            )
            response = client.get("/")

            # only POST allowed
            for method in ALL_METHODS:
                if method != "POST":
                    with client.request(method, SIGNIN_URL) as response:
                        self.assertEqual(response.status_code, METHOD_NOT_ALLOWED_405)

            with client.post(SIGNIN_URL, data=b"data") as response:
                self.assertEqual(response.status_code, UNSUPPORTED_MEDIA_TYPE_415)

            # json content type but bad with content
            with client.post(
                SIGNIN_URL,
                data=b"{",
                headers={"Content-Type": "application/json"},
            ) as response:
                self.assertEqual(response.status_code, UNPROCESSABLE_ENTITY_422)

            # multipart content type but with bad content

            with client.post(
                SIGNIN_URL,
                data=b"{",
                headers={"Content-Type": "multipart/form-data"},
            ) as response:
                self.assertEqual(response.status_code, UNPROCESSABLE_ENTITY_422)

            # send json without any field
            with client.post(SIGNIN_URL, json={}) as response:
                self.assertEqual(response.status_code, BAD_REQUEST_400)

            # multipart content type but with empty content
            for data in (b"", ""):
                for content_type in ("multipart/form-data", "application/json"):
                    with client.post(
                        SIGNIN_URL,
                        data=data,
                        headers={"Content-Type": content_type},
                    ) as response:
                        self.assertEqual(response.status_code, UNPROCESSABLE_ENTITY_422)

            for data in (b"", ""):
                with client.post(
                    SIGNIN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                ) as response:
                    self.assertEqual(response.status_code, BAD_REQUEST_400)

            # send json with email and password but a third parameter
            with client.post(
                SIGNIN_URL, json={"email": "", "password": "", "foo": ""}
            ) as response:
                self.assertEqual(response.status_code, BAD_REQUEST_400)

            # send form with email and password but a third parameter
            with client.post(
                SIGNIN_URL, data={"email": "", "password": "", "foo": ""}
            ) as response:
                self.assertEqual(response.status_code, BAD_REQUEST_400)

            # send json with email and password but not all strings
            with client.post(
                SIGNIN_URL,
                json={"email": 1, "password": "", "client_id": 1},
            ) as response:
                self.assertEqual(response.status_code, BAD_REQUEST_400)

            # send form with all fields but wrongs ones
            with client.post(
                SIGNIN_URL,
                data={"email": "qux@foo.fr", "password": "baz", "client_id": CLIENT_ID},
            ) as response:
                self.assertEqual(response.status_code, UNAUTHORIZED_401)

            # send json with email and password but wrongs ones
            with client.post(
                SIGNIN_URL,
                json={
                    "email": "qux@foo.fr",
                    "password": "baz",
                    "client_id": CLIENT_ID,
                },
            ) as response:
                self.assertEqual(response.status_code, UNAUTHORIZED_401)

            # send form with correct email but wrong password
            with client.post(
                SIGNIN_URL,
                data={
                    "email": USER_EMAIL,
                    "password": "bad-password",
                    "client_id": CLIENT_ID,
                },
            ) as response:
                self.assertEqual(response.status_code, UNAUTHORIZED_401)

            # send json with correct email but wrong password
            with client.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": "bad-password",
                    "client_id": CLIENT_ID,
                },
            ) as response:
                self.assertEqual(response.status_code, UNAUTHORIZED_401)

            now = datetime.now(timezone.utc).astimezone()
            timestamp = int(now.timestamp())
            COMMOM_CLAIMS = {
                "sub": "2",
                "iat": timestamp,
                "exp": timestamp + ACCESS_TOKEN_EXPIRATION,
                "rte": timestamp + REFRESH_TOKEN_EXPIRATION,
                "orig_iat": 0,
                "iss": SITE_NAME,
                "email": USER_EMAIL,
                "display_name": USER_NAME,
                "scope": [],
                "client_id": CLIENT_ID,
            }

            # send form with correct email and password as form
            refresh_token = new_refresh_token()
            with patch("ruteni.plugins.token.now", wraps=lambda: now), patch(
                "ruteni.plugins.token.new_refresh_token",
                wraps=lambda: refresh_token,
            ):
                with client.post(
                    SIGNIN_URL,
                    data={
                        "email": USER_EMAIL,
                        "password": USER_PASSWORD,
                        "client_id": CLIENT_ID,
                    },
                ) as response:
                    self.assertEqual(response.status_code, OK_200)
                    content = response.json()
                    self.assertEqual(
                        content,
                        {
                            "access_token": {"jti": "1", **COMMOM_CLAIMS},
                            "refresh_token": refresh_token,
                            "user": USER,
                        },
                    )
                    self.assertTrue(self.valid_signin_info(content))

            # send json with correct email and password as json
            # because refresh tokens must be unique, use a new one
            refresh_token = new_refresh_token()
            with patch("ruteni.plugins.token.now", wraps=lambda: now), patch(
                "ruteni.plugins.token.new_refresh_token",
                wraps=lambda: refresh_token,
            ):
                with client.post(
                    SIGNIN_URL,
                    json={
                        "email": USER_EMAIL,
                        "password": USER_PASSWORD,
                        "client_id": CLIENT_ID,
                    },
                ) as response:
                    self.assertEqual(response.status_code, OK_200)
                    content = response.json()
                    self.assertEqual(
                        content,
                        {
                            "access_token": {"jti": "2", **COMMOM_CLAIMS},
                            "refresh_token": refresh_token,
                            "user": USER,
                        },
                    )
                    self.assertEqual(len(client.cookies.get_dict()), 1)
                    access_token = client.cookies[ACCESS_TOKEN_COOKIE_NAME]
                    self.assertEqual(
                        keys.decrypt(access_token), {"jti": "2", **COMMOM_CLAIMS}
                    )

            # only POST allowed for signout
            for method in ALL_METHODS:
                if method != "POST":
                    with client.request(method, SIGNOUT_URL) as response:
                        self.assertEqual(response.status_code, METHOD_NOT_ALLOWED_405)

            with client.post(
                SIGNOUT_URL, json={"refresh_token": refresh_token}
            ) as response:
                self.assertEqual(response.status_code, OK_200)


if __name__ == "__main__":
    import unittest

    unittest.main()
