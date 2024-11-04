"""This module is responsible for testing the lambda function."""

import json
from unittest.mock import patch
import pandas as pd
from src.code.connect_to_db import connect
from ..code import lambda_handler
from .conftest import mock_context


def test_dummy_test(mock_ssm_parameters):
    """This test is just to check if the test environment is working."""

    # Mocking the payload
    payload = {
        "stageVariables": {"environment": "test"},
    }

    result = lambda_handler(payload, mock_context())

    assert result["statusCode"] == 200
