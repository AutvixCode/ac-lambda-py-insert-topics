"""
Folder containing some fixtures of AWS services mocked in moto library
"""

from unittest.mock import Mock
import pytest
from moto import mock_dynamodb, mock_ssm, mock_cognitoidp
import boto3


def mock_context():
    """
    Mock of context object
    """
    mock_context = Mock()
    mock_context.function_name = "my-lambda-function"
    mock_context.aws_request_id = "mock-request-id"
    mock_context.invoked_function_arn = """arn:aws:lambda:us-east-1:
    123456789012:function:my-lambda-function"""
    return mock_context


@pytest.fixture
def mock_dynamodb_table():
    """
    Mock DynamoDB
    """
    with mock_dynamodb():
        dynamo = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamo.create_table(
            TableName="dummy_table",
            KeySchema=[
                {"AttributeName": "dummy_id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "dummy_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        yield table


@pytest.fixture
def mock_ssm_parameters():
    """
    Mocking of SSM parameters
    """
    with mock_ssm():
        ssm = boto3.client("ssm", region_name="us-east-1")
        ssm.put_parameter(
            Name="/rhvix/test/rds_host",
            Value="almoxarivix.cbvvkyqq6dqs.us-east-1.rds.amazonaws.com",
            Type="String",
            Overwrite=True,
        )

        ssm.put_parameter(
            Name="/rhvix/test/rds_username",
            Value="autvixsistemas",
            Type="String",
            Overwrite=True,
        )

        ssm.put_parameter(
            Name="/rhvix/test/rds_password",
            Value="AutvixSistemas2022",
            Type="String",
            Overwrite=True,
        )

        ssm.put_parameter(
            Name="/rhvix/test/rds_dbname",
            Value="RhVix_dev",
            Type="String",
            Overwrite=True,
        )

        ssm.put_parameter(
            Name="/rhvix/test/rds_port", Value="3306", Type="String", Overwrite=True
        )
        yield ssm


@pytest.fixture
def mock_cognito_users():
    """
    Mocking of Cognito User Pool and their users
    """
    with mock_cognitoidp():
        cognito = boto3.client("cognito-idp", region_name="us-east-1")
        cognito.create_user_pool(PoolName="DummyUserPool")
        yield cognito
