import boto3
import botocore

def check_iam_permissions():
    client = boto3.client("rds")
    try:
        client.describe_db_clusters(MaxRecords=20)
        client.describe_db_instances()
    except botocore.exceptions.ClientError as e:
        print("Error: Tu usuario no tiene los permisos necesarios para usar esta herramienta.")
        print(f"Detalle: {e.response['Error']['Message']}")
        exit(1)
    except Exception as e:
        print("Error inesperado al verificar permisos.")
        print(str(e))
        exit(1)
    print("Permisos suficientes para operar Aurora.")

def get_aws_username():
    client = boto3.client("sts")
    identity = client.get_caller_identity()
    arn = identity["Arn"]
    return arn.split("/")[-1]
