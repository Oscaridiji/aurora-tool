import boto3
from aurora_tool.aws_utils.auth import get_aws_username
from aurora_tool.aws_utils.info_cluster import print_cluster_info
from aurora_tool.aws_utils.clusters.instance_info import get_all_instance_classes_from_cluster

def restore_cluster(source_cluster, new_cluster):
    client = boto3.client("rds")
    owner = get_aws_username()

    response = client.restore_db_cluster_to_point_in_time(
        DBClusterIdentifier=new_cluster,
        SourceDBClusterIdentifier=source_cluster,
        RestoreType="copy-on-write",
        UseLatestRestorableTime=True,
        Tags=[
            {"Key": "Project", "Value": "Frogtek"},
            {"Key": "env", "Value": "dev"},
            {"Key": "owner", "Value": owner},
        ],
    )

    instance_classes = get_all_instance_classes_from_cluster(source_cluster)
    for idx, instance_class in enumerate(instance_classes):
        instance_id = f"{new_cluster}-instance-{idx+1}"
        client.create_db_instance(
            DBInstanceIdentifier=instance_id,
            DBClusterIdentifier=new_cluster,
            Engine="aurora-mysql",
            DBInstanceClass=instance_class,
            PubliclyAccessible=False,
        )

    print_cluster_info(new_cluster)
    return response["DBCluster"]["DBClusterIdentifier"]