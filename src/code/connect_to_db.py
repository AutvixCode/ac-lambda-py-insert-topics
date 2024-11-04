"""Import modules"""
import pymysql
import boto3


def get_db_parameters(environment: str):
    """This function is used to get the parameters from the AWS SSM service."""
    ssm = boto3.client("ssm", region_name="us-east-1")
    my_dict = {}
    my_dict["rds_host"] = ssm.get_parameter(Name=f"/rhvix/{environment}/rds_host")[
        "Parameter"
    ]["Value"]
    my_dict["name"] = ssm.get_parameter(Name=f"/rhvix/{environment}/rds_username")[
        "Parameter"
    ]["Value"]
    my_dict["password"] = ssm.get_parameter(Name=f"/rhvix/{environment}/rds_password")[
        "Parameter"
    ]["Value"]
    my_dict["db_name"] = ssm.get_parameter(Name=f"/rhvix/{environment}/rds_dbname")[
        "Parameter"
    ]["Value"]

    return my_dict


def connect(environment: str) -> pymysql.Connection:
    """
    This function is used to connect to the database.
    """
    parameter_dict = get_db_parameters(environment)
    conn = pymysql.connect(
        host=parameter_dict["rds_host"],
        user=parameter_dict["name"],
        password=parameter_dict["password"],
        db=parameter_dict["db_name"],
    )
    return conn
