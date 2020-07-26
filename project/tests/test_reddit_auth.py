# Standard library imports
from unittest.mock import patch

# Third-party imports
from nose.tools import assert_is_not_none

# Local imports
from services import reddit_auth

@patch('services.requests.get')
def test_reddit_auth(mock_get):
  mock_get.return_value.ok = True
  response = reddit_auth()

  assert_is_not_none(response)

    