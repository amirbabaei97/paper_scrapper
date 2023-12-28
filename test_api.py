from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest

from api import app, validate_api_key

client = TestClient(app)

# Test Environment and Setup
def test_api_keys_loaded():
    from api import API_KEYS
    assert API_KEYS, "API_KEYS should be loaded from environment variables"

# Test Startup Event
@pytest.mark.asyncio
async def test_startup_event():
    with patch('api.init_proxies') as mock_init_proxies:
        from api import startup_event
        await startup_event()
        mock_init_proxies.assert_called_once()

# Test API Key Validation
def test_validate_api_key():
    from api import API_KEYS
    valid_key = list(API_KEYS)[0]
    invalid_key = "invalid_api_key"
    assert validate_api_key(valid_key), "Valid API key should return True"
    assert not validate_api_key(invalid_key), "Invalid API key should return False"

# Test Search Endpoint - Invalid API Key
def test_search_with_invalid_api_key():
    response = client.get("/search/?keyword=test", headers={"x-api-key": "invalid_key"})
    assert response.status_code == 401
    assert response.json()['detail'] == "Invalid or missing API key"

# Test Search Endpoint - Missing Keyword
def test_search_with_missing_keyword():
    from api import API_KEYS
    valid_key = list(API_KEYS)[0]
    response = client.get("/search/", headers={"x-api-key": valid_key})
    assert response.status_code == 400
    assert response.json()['detail'] == "Keyword is required"

# Test Search Endpoint - No Working Proxies
def test_search_no_working_proxies():
    from api import API_KEYS
    valid_key = list(API_KEYS)[0]
    with patch('api.get_working_proxy', return_value=None):
        response = client.get("/search/?keyword=test", headers={"x-api-key": valid_key})
        assert response.status_code == 500
        assert response.json()['detail'] == "No working proxies available."

# Test Search Endpoint - Successful Search
def test_successful_search():
    from api import API_KEYS
    valid_key = list(API_KEYS)[0]
    sample_results = [{"title": "Sample Title", "link": "http://example.com"}]
    with patch('api.get_working_proxy', return_value='http://proxyserver:port'):
        with patch('api.search_scholar', return_value=sample_results):
            response = client.get("/search/?keyword=test", headers={"x-api-key": valid_key})
            assert response.status_code == 200
            assert response.json() == sample_results

# Test Search Endpoint - Handle Search Errors
def test_search_with_error():
    from api import API_KEYS
    valid_key = list(API_KEYS)[0]
    with patch('api.search_scholar', side_effect=Exception("Search failed")):
        response = client.get("/search/?keyword=test", headers={"x-api-key": valid_key})
        assert response.status_code == 500
        assert response.json()['detail'] == "Search failed"
