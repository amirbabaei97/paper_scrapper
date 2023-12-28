import os
from unittest.mock import patch, MagicMock
import pytest
from scraper import init_proxies, test_proxy as original_test_proxy, get_working_proxy, search_scholar, proxies

def test_init_proxies():
    init_proxies()
    from scraper import proxies
    assert len(proxies) == 100, "Proxies should be correctly parsed and loaded from the environment"

@patch('selenium.webdriver.Chrome')
def test_search_scholar_with_invalid_key(mock_driver):
    with pytest.raises(ValueError):
        search_scholar("", None)

import pytest
from scraper import search_scholar

def test_search_scholar():
    # Define a test search key. Choose a common term to ensure results.
    test_search_key = "machine learning"
    
    # Call the search_scholar function with the test search key
    results = search_scholar(test_search_key)

    # Check if the results are in the expected format and contain expected fields
    for result in results:
        assert 'title' in result and result['title'] != "", "Each result should have a title"
        assert 'abstract' in result and result['abstract'] !="", "Each result should have an abstract"
        assert 'article_link' in result and result['article_link'] !="", "Each result should have an article link"
        assert 'authors' in result and result['authors'] !="", "Each result should have authors"
        assert 'citations' in result and result['citations'] !="", "Each result should have citation count"
        assert 'year' in result and result['year'] !="", "Each result should have a publication year"
    
    # Check if at least one result was returned for a common term
    assert len(results) > 0, "At least one result should be returned for common search terms"

