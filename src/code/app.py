"""This module is responsible for updating the employee database with the new data"""

import json
import pandas as pd
from aws_lambda_powertools import Logger

try:
    from .connect_to_db import connect
except ImportError as e:
    from connect_to_db import connect

logger = Logger()


def build_query():
    """Builds the SQL query based on the provided parameters"""
    sql_employee = """
    SELECT id_colaborador, permissao FROM dados_colaboradores
    WHERE ativo_rhvix = 1
    OR permissao IN ('Supervisor', 'admin');
    """

    sql_topics = "SELECT idtopico_manual, permissao FROM topico_manual"

    return sql_employee, sql_topics


@logger.inject_lambda_context
def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    This function is responsible for updating the employee database with the new data
    """
    try:
        environment = event["stageVariables"]["environment"]
    except KeyError:
        return {"statusCode": 400, "body": "Environment not found."}

    conn = connect(environment)
    if conn is None:
        return {"statusCode": 500, "body": "Unable to connect to database."}

    query_employee, query_topics = build_query()

    df_employee = pd.read_sql_query(query_employee, conn)
    employees = df_employee.to_dict(orient="records")

    df_topics = pd.read_sql_query(query_topics, conn)
    topics = df_topics.to_dict(orient="records")

    new_cursor = conn.cursor()

    for employee in employees:
        for topic in topics:
            print(employee, topic)

            if employee["permissao"].lower() in topic["permissao"].lower():
                new_cursor.execute(
                    """
                    INSERT INTO leitura_topico_manual (id_colaborador, id_topico, manual_lido) 
                    VALUES (%s, %s, %s)
                    """,
                    (employee["id_colaborador"], topic["idtopico_manual"], 0),
                )

    conn.commit()
    new_cursor.close()


    return {"statusCode": 200, "body": "Data inserted successfully."}
