from aurora_tool.aws_utils.clusters.delete import delete_cluster_resources
from aurora_tool.aws_utils.clusters.list import get_all_clusters, get_aurora_cluster_names_by_user
from aurora_tool.aws_utils.clusters.restore import restore_cluster
from aurora_tool.aws_utils.info_cluster import print_cluster_info
from aurora_tool.aws_utils.tags import tag_for_deletion


def clone_aurora(
    source_cluster, cluster_name, retention_days
):
    print(f"Clonando cluster {source_cluster} como {cluster_name}...")
    cluster_id = restore_cluster(source_cluster, cluster_name)
    if retention_days > 0:
        tag_for_deletion(cluster_id, retention_days)
    print("Clon creado correctamente.")

def get_all_user_clusters():
    return get_aurora_cluster_names_by_user()

def get_all_available_clusters():
    return get_all_clusters()

def delete(cluster_name):
    delete_cluster_resources(cluster_name)
    print("Eliminado.")


def cluster_info(cluster_name):
    print(f"Mostrando información del cluster {cluster_name}...")
    print_cluster_info(cluster_name)
