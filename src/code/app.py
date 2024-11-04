"""This module is responsible for updating the employee database with the new data"""
import json
import pandas as pd
from aws_lambda_powertools import Logger

try:
    from .connect_to_db import connect
except ImportError as e:
    from connect_to_db import connect

logger = Logger()


def build_query(**kwargs):
    """Builds the SQL query based on the provided parameters"""
    # Basic SQL SELECT statement
    query = "SELECT distinct centro_de_custo,ordem_servico,tipo_atendimento FROM respostas_planilha"

    # Conditions based on the provided parameters
    conditions = []

    # Date range filtering
    conditions.append(
        f"""data_registrada BETWEEN '{kwargs['init_date']}' AND '{kwargs['fin_date']}'"""
    )

    # Collaborators filtering (assuming the column name is 'collaborator')
    if kwargs["email"] != [] and kwargs["email"][0] != "":
        if len(kwargs["email"]) == 1 and kwargs["email"][0] != "":
            collaborator_condition = f"email = '{kwargs['email'][0]}'"
        else:
            collaborator_condition = " OR ".join(
                [f"email = '{col}'" for col in kwargs["email"]]
            )
        conditions.append(f"({collaborator_condition})")

    # Partition number filtering (assuming the column name is 'partition')
    if kwargs["os"] not in ["", " "]:
        conditions.append(f"ordem_servico = '{kwargs['os']}'")

    if kwargs["cc"] not in ["", " "]:
        conditions.append(f"centro_de_custo = '{kwargs['cc']}'")

    if kwargs["type_acti"] not in ["", " "]:
        conditions.append(f"tipo_atendimento = '{kwargs['type_acti']}'")
    # Combining all conditions using 'AND'
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # You can add more clauses like ORDER BY, GROUP BY, etc., if needed

    return query


@logger.inject_lambda_context
def lambda_handler(event, context):  # pylint: disable=unused-argument
    """
    This function is responsible for updating the employee database with the new data
    """
    environment = event["stageVariables"]["environment"]
    event_body = json.loads(event["body"])
    conn = connect(environment)
    if conn is None:
        return {"statusCode": 500, "body": "Unable to connect to database."}

    query = build_query(
        init_date=event_body["initial_date"],
        fin_date=event_body["final_date"],
        email=event_body["email"],
        os=event_body["os"],
        cc=event_body["cc"],
        type_acti=event_body["type_activity"],
    )
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        conn.close()
        df_empty_values = pd.DataFrame(
            [
                ["", "", ""],
            ],
            columns=["centro_de_custo", "ordem_servico", "tipo_atendimento"],
        )
        # Converter o DataFrame para um dicionário
        df_empty_values_dict = df_empty_values.to_dict(orient="records")
        return {"statusCode": 200, "body": json.dumps(df_empty_values_dict)}
    conn.close()
    df = pd.DataFrame(
        result, columns=["centro_de_custo", "ordem_servico", "tipo_atendimento"]
    )

    # Converter o DataFrame para um dicionário
    df_dict = df.to_dict(orient="records")

    return {"statusCode": 200, "body": json.dumps(df_dict)}
