import boto3
from .auth import get_aws_username

def tag_for_deletion(cluster_id, days):
    import datetime
    session = boto3.session.Session()
    region = session.region_name
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    arn = f"arn:aws:rds:{region}:{account_id}:cluster:{cluster_id}"
    delete_after = (
        datetime.datetime.utcnow() + datetime.timedelta(days=days)
    ).isoformat()

    client = boto3.client("rds")
    client.add_tags_to_resource(
        ResourceName=arn, Tags=[{"Key": "auto-delete-after", "Value": delete_after}]
    )
