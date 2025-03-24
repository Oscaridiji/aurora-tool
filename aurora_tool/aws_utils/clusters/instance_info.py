import boto3

def get_all_instance_classes_from_cluster(cluster_id):
    client = boto3.client("rds")
    instances = client.describe_db_instances()
    return [
        inst["DBInstanceClass"]
        for inst in instances["DBInstances"]
        if inst.get("DBClusterIdentifier") == cluster_id
    ]