import boto3
from ..auth import get_aws_username
from ..info_cluster import print_cluster_info

def get_user_cluster_count():
    client = boto3.client("rds")
    username = get_aws_username()
    clusters = client.describe_db_clusters()["DBClusters"]
    
    count = 0
    for cluster in clusters:
        tags = client.list_tags_for_resource(ResourceName=cluster["DBClusterArn"])["TagList"]
        tag_dict = {tag["Key"]: tag["Value"] for tag in tags}
        if tag_dict.get("env") == "dev" and tag_dict.get("owner") == username:
            count += 1
    return count

def get_all_clusters():
    client = boto3.client("rds")
    return [c["DBClusterIdentifier"] for c in client.describe_db_clusters()["DBClusters"]]

def get_aurora_cluster_names_by_user():
    client = boto3.client("rds", region_name="eu-west-3")
    username = get_aws_username()
    
    clusters = client.describe_db_clusters()["DBClusters"]
    filtered = []

    for cluster in clusters:
        tags = client.list_tags_for_resource(ResourceName=cluster["DBClusterArn"])["TagList"]
        tag_dict = {tag["Key"]: tag["Value"] for tag in tags}

        if tag_dict.get("env") == "dev" and tag_dict.get("owner") == username:
            filtered.append(cluster["DBClusterIdentifier"])

    return filtered