from datetime import datetime, timedelta, timezone
from typing import Any, Union

import pytest
from freezegun import freeze_time
from jose import jwt

from src.auth.utils.exceptions import (
    InvalidAccessTokenError,
    TokenExpiredError,
)
from src.auth.utils.tokens.access_token_decoder import AccessTokenDecoder
from tests.auth.utils.tokens.jwt_config import (
    ALGORITHM_HS256,
    ALGORITHM_RS256,
    PUBLIC_KEY_RSA,
    SECRET_KEY_HS256,
    SECRET_KEY_RSA,
    WRONG_PUBLIC_KEY_RSA,
)


def _create_access_token(algorithm: str, payload: dict):
    if algorithm == ALGORITHM_HS256:
        return jwt.encode(payload, SECRET_KEY_HS256, algorithm=algorithm)
    if algorithm == ALGORITHM_RS256:
        return jwt.encode(payload, SECRET_KEY_RSA, algorithm=algorithm)


@pytest.mark.parametrize('verification_key', [
    SECRET_KEY_HS256,
    PUBLIC_KEY_RSA,
])
def test_verification_key_getter(verification_key: Union[str, dict]):
    token_decoder = AccessTokenDecoder(verification_key, '')
    assert token_decoder.verification_key == verification_key


@pytest.mark.parametrize('new_verification_key, exception', [
    (SECRET_KEY_HS256, None),
    (PUBLIC_KEY_RSA, None),
    (34, ValueError),
    ([], ValueError),
])
def test_verification_key_setter(
    new_verification_key: Any,
    exception: Exception,
):
    token_decoder = AccessTokenDecoder('', '')
    if not exception:
        token_decoder.verification_key = new_verification_key
        assert token_decoder.verification_key == new_verification_key
    if exception:
        with pytest.raises(ValueError):
            token_decoder.verification_key = new_verification_key


@pytest.fixture(params=[
    (SECRET_KEY_HS256, ALGORITHM_HS256),
    (PUBLIC_KEY_RSA, ALGORITHM_RS256),
])
def token_decoder(request):
    key, algorithm = request.param
    return AccessTokenDecoder(verification_key=key, algorithm_name=algorithm)


@pytest.mark.parametrize('user_id, exp_delta', [
    (1, timedelta(hours=1)),
    ('dfsfsf', timedelta(hours=2)),
])
def test_decode_token_success(
    token_decoder: AccessTokenDecoder,
    user_id: Any,
    exp_delta: timedelta,
):
    algorithm = token_decoder._algorithm_name
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + exp_delta,
    }
    access_token = _create_access_token(algorithm, payload)

    decoded_payload = token_decoder.decode_token(access_token)
    assert decoded_payload['user_id'] == user_id


@pytest.mark.parametrize('exp_delta', [
    timedelta(seconds=5),
    timedelta(hours=1),
    timedelta(days=2),
])
def test_decode_token_expired(
    token_decoder: AccessTokenDecoder,
    exp_delta: timedelta,
):
    algorithm = token_decoder._algorithm_name
    current_time = datetime.now(timezone.utc)
    payload = {
        'user_id': 1,
        'exp': current_time + exp_delta,
    }
    access_token = _create_access_token(algorithm, payload)
    expiration_time = current_time + exp_delta + timedelta(seconds=1)
    with freeze_time(expiration_time):
        with pytest.raises(TokenExpiredError):
            token_decoder.decode_token(access_token)


def test_decode_token_wrong_verification_key(token_decoder: AccessTokenDecoder):
    algorithm = token_decoder._algorithm_name
    payload = {
        'user_id': 1,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
    }
    access_token = _create_access_token(algorithm, payload)

    if algorithm == ALGORITHM_HS256:
        token_decoder.verification_key = 'wrong key'
    else:
        token_decoder.verification_key = WRONG_PUBLIC_KEY_RSA

    with pytest.raises(InvalidAccessTokenError):
        token_decoder.decode_token(access_token)


@pytest.mark.parametrize('algorithm_name', [
    'HS512',
    'PS256',
])
def test_decode_token_wrong_algorithm(
    token_decoder: AccessTokenDecoder,
    algorithm_name: str,
):
    algorithm = token_decoder._algorithm_name
    payload = {
        'user_id': 1,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
    }
    access_token = _create_access_token(algorithm, payload)

    token_decoder._algorithm_name = algorithm_name

    with pytest.raises(InvalidAccessTokenError):
        token_decoder.decode_token(access_token)
