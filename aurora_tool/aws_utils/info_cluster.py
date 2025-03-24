import boto3

def print_cluster_info(cluster_id):
    client = boto3.client("rds")
    clusters = client.describe_db_clusters(DBClusterIdentifier=cluster_id)
    cluster = clusters["DBClusters"][0]

    print("\nInformación del Cluster:")
    print(f"- Endpoint writer: {cluster.get('Endpoint')}")
    print(f"- Endpoint reader: {cluster.get('ReaderEndpoint')}")
    print(f"- Puerto: {cluster.get('Port')}")
    print(f"- VPC ID: {cluster.get('DBSubnetGroup')}")
    print(f"- Estado: {cluster.get('Status')}")
