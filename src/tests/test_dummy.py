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
        "body": json.dumps(
            {
                "initial_date": "2023-12-20",
                "final_date": "2023-12-22",
                "email": ["emerson.neitzel@autvixservicos.com.br"],
                "os": "",
                "cc": "",
                "type_activity": "",
            }
        ),
        "stageVariables": {"environment": "test"},
    }

    # Expected DataFrame
    expected_df = pd.DataFrame(
        [
            ["E22282-DDEE", "NA", "Escritório"],
            ["E22282-DDEE", "NA", "Cliente"],
            ["E23182-SIE", "NA", "Cliente"],
        ],
        columns=["centro_de_custo", "ordem_servico", "tipo_atendimento"],
    )

    # Calling the lambda_handler function
    result = lambda_handler(payload, mock_context())
    result_df = pd.DataFrame(json.loads(result["body"]))
    pd.testing.assert_frame_equal(result_df, expected_df)

    # Asserting other properties of the result, if needed
    assert result["statusCode"] == 200


def test_empty_return(mock_ssm_parameters):
    """This test is just to check if the test environment is working."""

    # Mocking the payload
    payload = {
        "body": json.dumps(
            {
                "initial_date": "2023-12-20",
                "final_date": "2023-12-22",
                "email": ["gustavoschwartz@autvixservicos.com.br"],
                "os": "",
                "cc": "",
                "type_activity": "",
            }
        ),
        "stageVariables": {"environment": "test"},
    }

    # Expected DataFrame
    expected_df = pd.DataFrame(
        [
            ["", "", ""],
        ],
        columns=["centro_de_custo", "ordem_servico", "tipo_atendimento"],
    )

    # Calling the lambda_handler function
    result = lambda_handler(payload, mock_context())
    result_df = pd.DataFrame(json.loads(result["body"]))
    pd.testing.assert_frame_equal(result_df, expected_df)

    # Asserting other properties of the result, if needed
    assert result["statusCode"] == 200
