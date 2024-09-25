import secrets
import string
from contextlib import nullcontext as does_not_raise
from typing import Optional

import pytest
from passlib.context import CryptContext

from src.auth.utils.password_manager import PasswordManager


@pytest.fixture
def custom_crypt_context() -> CryptContext:
    return CryptContext(
        schemes=['bcrypt'],
        deprecated='auto',
    )


@pytest.fixture
def custom_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(256))


class TestPasswordManager:
    @pytest.mark.parametrize(
        [
            'crypt_context',
            'expectation',
        ],
        [
            (
                None,
                does_not_raise(),
            ),
            (
                'custom_crypt_context',
                does_not_raise(),
            ),
        ],
    )
    def test_init(
        self,
        custom_crypt_context,
        crypt_context,
        expectation: Optional[Exception],
    ):
        if crypt_context:
            crypt_context = custom_crypt_context
        with expectation:
            password_manager: PasswordManager = PasswordManager(crypt_context)
            password_manager.hash('test')

    @pytest.mark.parametrize(
        [
            'expectation',
        ],
        [
            (
                does_not_raise(),
            ),
            (
                does_not_raise(),
            ),
            (
                does_not_raise(),
            ),
            (
                does_not_raise(),
            ),
        ],
    )
    def test_hash(
        self,
        custom_password: str,
        expectation: Optional[Exception],
    ):
        with expectation:
            PasswordManager().hash(custom_password)

    @pytest.mark.parametrize(
        [
            'password',
            'expectation',
            'crypt_context',
        ],
        [
            (
                None,
                True,
                None,
            ),
            (
                None,
                True,
                'custom_crypt_context',
            ),
            (
                'wrond_password',
                False,
                None,
            ),
            (
                'new_wrond_password',
                False,
                'custom_crypt_context',
            ),
        ],
    )
    def test_compare(
        self,
        custom_password,
        custom_crypt_context,
        password: str,
        expectation: bool,
        crypt_context,
    ):
        if crypt_context:
            crypt_context = custom_crypt_context
        password = password or custom_password

        password_manager: PasswordManager = PasswordManager(crypt_context)
        hash_password: str = password_manager.hash(custom_password)

        assert password_manager.compare(
            password,
            hash_password,
        ) == expectation
