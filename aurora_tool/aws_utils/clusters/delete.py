import boto3

def delete_cluster_resources(cluster_name):
    client = boto3.client("rds")

    instances = client.describe_db_instances()
    for instance in instances["DBInstances"]:
        if instance["DBClusterIdentifier"] == cluster_name:
            instance_id = instance["DBInstanceIdentifier"]
            print(f"Eliminando instancia {instance_id} del cluster {cluster_name}...")
            client.delete_db_instance(
                DBInstanceIdentifier=instance_id, SkipFinalSnapshot=True
            )

    print(f"Eliminando cluster {cluster_name}...")
    client.delete_db_cluster(DBClusterIdentifier=cluster_name, SkipFinalSnapshot=True)