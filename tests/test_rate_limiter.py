import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from fastapi import Depends
from main import app
from auth.auth_handler import create_tokens
from rate_limiter import rate_limit


@app.get("/test-rate-limit", dependencies=[Depends(rate_limit)])
async def dummy_route():
    return {"message": "passed"}


client = TestClient(app)


@pytest.fixture
def auth_token():
    token_dict = create_tokens("testuser@example.com")
    return token_dict["access_token"]

@patch("rate_limiter.r.zcard", new_callable=AsyncMock)
@patch("rate_limiter.r.zremrangebyscore", new_callable=AsyncMock)
@patch("rate_limiter.r.zadd", new_callable=AsyncMock)
@patch("rate_limiter.r.expire", new_callable=AsyncMock)
def test_anonymous_under_limit(mock_expire, mock_zadd, mock_zrem, mock_zcard):
    mock_zcard.return_value = 1
    response = client.get("/test-rate-limit")
    assert response.status_code == 200

@patch("rate_limiter.r.zcard", new_callable=AsyncMock)
@patch("rate_limiter.r.zremrangebyscore", new_callable=AsyncMock)
@patch("rate_limiter.r.zadd", new_callable=AsyncMock)
@patch("rate_limiter.r.expire", new_callable=AsyncMock)
def test_anonymous_over_limit(mock_expire, mock_zadd, mock_zrem, mock_zcard):
    mock_zcard.return_value = 2

    response = client.get("/test-rate-limit")
    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"


@patch("rate_limiter.r.zcard", new_callable=AsyncMock)
@patch("rate_limiter.r.zremrangebyscore", new_callable=AsyncMock)
@patch("rate_limiter.r.zadd", new_callable=AsyncMock)
@patch("rate_limiter.r.expire", new_callable=AsyncMock)
def test_authenticated_under_limit(mock_expire, mock_zadd, mock_zrem, mock_zcard, auth_token):
    mock_zcard.return_value = 9

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/test-rate-limit", headers=headers)
    assert response.status_code == 200


@patch("rate_limiter.r.zcard", new_callable=AsyncMock)
@patch("rate_limiter.r.zremrangebyscore", new_callable=AsyncMock)
@patch("rate_limiter.r.zadd", new_callable=AsyncMock)
@patch("rate_limiter.r.expire", new_callable=AsyncMock)
def test_authenticated_over_limit(mock_expire, mock_zadd, mock_zrem, mock_zcard, auth_token):
    mock_zcard.return_value = 10

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/test-rate-limit", headers=headers)
    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"