import pytest
import asyncio
from typing import Optional
from contextlib import nullcontext as does_not_raise
from src.auth.utils.tokens.token_manager import TokenManager
from src.auth.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    PUBLIC_KEY,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALGORITHM_NAME,
)
from uuid import UUID,uuid4


class TestTokenManager:
    @classmethod
    def _TokenManager(cls)->TokenManager:
        return TokenManager(
            ACCESS_TOKEN_EXPIRE_SECONDS,
            TOKEN_ALGORITHM_NAME,
            SECRET_KEY,
            PUBLIC_KEY,
        )

    @pytest.mark.parametrize(
        [
            'verification_key',
        ],
        [
            (
                PUBLIC_KEY,
            ),
            (
                None,
            )
        ]
    )
    def test___init__(
        self,
        verification_key: str,
    ):
        with does_not_raise():
            assert TokenManager(
                ACCESS_TOKEN_EXPIRE_SECONDS,
                TOKEN_ALGORITHM_NAME,
                SECRET_KEY,
                verification_key,
            )

    @pytest.mark.parametrize(
        [
            'new_secret_key',
            'expectation',
        ],
        [
            (
                'NEW_SECRET_KEY',
                does_not_raise(),
            ),
            (
                'NEW_ENOTHER_SECRET_KEY',
                does_not_raise(),
            ),
            (
                0,
                pytest.raises(ValueError),
            ),
        ]
    )
    def test_secret_key(
        self,
        new_secret_key: str | int,
        expectation: Optional[Exception],
    ):
        token_manager: TokenManager = self._TokenManager()
        with expectation:
            token_manager.secret_key = new_secret_key
            assert 1==1
            assert token_manager.secret_key == new_secret_key

    @pytest.mark.parametrize(
        [
            'new_verification_key',
            'expectation',
        ],
        [
            (
                'NEW_PUBLIC_KEY',
                does_not_raise(),
            ),
            (
                'NEW_ENOTHER_PUBLIC_KEY',
                does_not_raise(),
            ),
            (
                0,
                pytest.raises(ValueError),
            ),
        ]
    )
    def test_verification_key(
        self,
        new_verification_key: str | int,
        expectation: Optional[Exception],
    ):
        token_manager: TokenManager = self._TokenManager()
        with expectation:
            token_manager.verification_key = new_verification_key
            assert token_manager.verification_key == new_verification_key
    
    @pytest.mark.parametrize(
        [
            'user_id',
        ],
        [
            (
                uuid4(),
            ),
        ]
    )
    def test_create_token(self, user_id: UUID):
        token_manager: TokenManager = self._TokenManager()
        token_manager.create_token(user_id)
        # print(f'ANSWER_FOR: {user_id}')
        # print(token_manager.create_token(user_id))