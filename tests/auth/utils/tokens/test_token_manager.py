from contextlib import nullcontext as does_not_raise
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

import pytest
from freezegun import freeze_time

from src.auth.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    PUBLIC_KEY,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALGORITHM_NAME,
)
from src.auth.models import RefreshSessionModel
from src.auth.schemas.tokens import Tokens
from src.auth.utils.exceptions import (
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    TokenExpiredError,
)
from src.auth.utils.tokens.token_manager import TokenManager


@pytest.fixture
def refresh_session() -> RefreshSessionModel:
    return RefreshSessionModel(
        token_id=2,
        refresh_token=uuid4(),
        expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
        created_at=datetime.now(timezone.utc),
        user_id=uuid4(),
    )


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager(
        ACCESS_TOKEN_EXPIRE_SECONDS,
        TOKEN_ALGORITHM_NAME,
        SECRET_KEY,
        PUBLIC_KEY,
    )


class TestTokenManager:
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
            ),
        ],
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
        ],
    )
    def test_secret_key(
        self,
        token_manager: TokenManager,
        new_secret_key: str | int,
        expectation: Optional[Exception],
    ):
        with expectation:
            token_manager.secret_key = new_secret_key
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
        ],
    )
    def test_verification_key(
        self,
        token_manager: TokenManager,
        new_verification_key: str | int,
        expectation: Optional[Exception],
    ):
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
        ],
    )
    def test_create_token(
        self,
        token_manager: TokenManager,
        user_id: UUID,
    ):
        tokens: Tokens = token_manager.create_token(user_id)
        dec_tokens: dict = token_manager.decode_token(
            tokens.access_token,
        )
        assert dec_tokens['sub'] == user_id

    @pytest.mark.parametrize(
        [
            'user_id',
            'time_left',
            'expectation',
        ],
        [
            (
                None,
                timedelta(seconds=0),
                does_not_raise(),
            ),
            (
                None,
                timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS + 1),
                pytest.raises(TokenExpiredError),
            ),
            (
                uuid4(),
                timedelta(seconds=0),
                pytest.raises(InvalidRefreshTokenError),
            ),
            (
                uuid4(),
                timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS + 1),
                pytest.raises(InvalidRefreshTokenError),
            ),
        ],
    )
    def test_refresh(
        self,
        token_manager: TokenManager,
        refresh_session: RefreshSessionModel,
        user_id: Optional[UUID],
        time_left: timedelta,
        expectation: Optional[Exception],
    ):
        if user_id is None:
            user_id = refresh_session.user_id
        with freeze_time(time_left):
            with expectation:
                token_manager.refresh(
                    refresh_session,
                    user_id,
                )

    @pytest.mark.parametrize(
        [
            'access_token',
            'time_left',
            'expectation',
        ],
        [
            (
                uuid4(),
                timedelta(seconds=0),
                does_not_raise(),
            ),
            (
                uuid4(),
                timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
                does_not_raise(),
            ),
            (
                uuid4(),
                timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS + 1),
                pytest.raises(TokenExpiredError),
            ),
            (
                'None',
                timedelta(seconds=0),
                pytest.raises(InvalidAccessTokenError),
            ),
            (
                'None',
                timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS + 1),
                pytest.raises(InvalidAccessTokenError),
            ),
        ],
    )
    def test_decode_token(
        self,
        token_manager: TokenManager,
        access_token: str | UUID,
        time_left: timedelta,
        expectation: Optional[Exception],
    ):
        if isinstance(access_token, UUID):
            access_token = token_manager.create_token(
                access_token,
            ).access_token

        with freeze_time(time_left):
            with expectation:
                token_manager.decode_token(
                    access_token,
                )
