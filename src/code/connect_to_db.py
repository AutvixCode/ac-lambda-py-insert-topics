"""This module contains the code to connect to the database."""

import pymysql
import boto3


def get_db_parameters(environment):
    """Get the database parameters from AWS SSM Parameter Store."""
    ssm = boto3.client(
        "ssm",
        region_name="us-east-1",
    )
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
    my_dict["db_port"] = int(
        ssm.get_parameter(Name=f"/rhvix/{environment}/rds_port")["Parameter"]["Value"]
    )
    print(my_dict)
    return my_dict


def connect(environment) -> pymysql.Connection:
    """Connect to the database."""
    parameter_dict = get_db_parameters(environment)
    try:
        conn = pymysql.connect(
            host=parameter_dict["rds_host"],
            user=parameter_dict["name"],
            password=parameter_dict["password"],
            db=parameter_dict["db_name"],
            port=parameter_dict["db_port"],
        )

        return conn
    except:  # pylint: disable=bare-except
        Exception(  # pylint: disable=pointless-exception-statement
            "Error connecting to the database."
        )
        return None
