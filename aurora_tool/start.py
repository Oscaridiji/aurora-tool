import questionary
from aurora_tool.aws_utils.clusters.list import get_all_clusters, get_aurora_cluster_names_by_user
from aurora_tool.aws_utils.auth import check_iam_permissions
from aurora_tool.main import clone_aurora, cluster_info, delete, get_all_available_clusters, get_all_user_clusters


def handle_clone():
    clusters = get_all_available_clusters()
    if not clusters:
        print("No se encontraron clusters en esta cuenta.")
        return

    choices = clusters + ["Volver atrás"]
    source_cluster = questionary.select(
        "¿Qué cluster quieres clonar?", choices=choices
    ).ask()

    if source_cluster == "Volver atrás":
        return

    cluster_name = questionary.text("Nombre del nuevo cluster").ask()
    if cluster_name is None:
        return

    retention_input = questionary.text(
        "¿Días hasta autoeliminación? (0 para nunca)"
    ).ask()
    if retention_input is None:
        return
    retention_days = int(retention_input)

    clone_aurora(source_cluster, cluster_name, retention_days)


def handle_delete():
    clusters = get_all_user_clusters()
    if not clusters:
        print("No se encontraron clusters en esta cuenta para eliminar.")
        return

    choices = clusters + ["Volver atrás"]

    cluster_name = questionary.select(
        "Selecciona el cluster que quieres eliminar:",
        choices=choices,
    ).ask()

    if cluster_name == "Volver atrás":
        return

    confirmacion = questionary.select(
        "¿Esta seguro que desea eliminar el cluster?",
        choices=["Sí", "No"],
    ).ask()

    if confirmacion == "No":
        return

    delete(cluster_name)


def handle_list():
    clusters = get_aurora_cluster_names_by_user()

    choices = clusters + ["Volver atrás"]

    cluster_name = questionary.select(
        "Selecciona el cluster para obtener información:",
        choices=choices,
    ).ask()

    if cluster_name == "Volver atrás":
        return

    cluster_info(cluster_name)


def handle_exit():
    print("¡Hasta la próxima!")
    exit()


# Diccionario de acciones
ACTIONS = {
    "Clonar Cluster": handle_clone,
    "Eliminar": handle_delete,
    "Listar": handle_list,
    "Salir": handle_exit,
}


def main():
    while True:
        try:
            check_iam_permissions()
        except Exception:
            print("Error: Tu usuario no tiene los permisos necesarios.")
            continue

        action = questionary.select(
            "¿Qué operación quieres realizar con Aurora?", choices=list(ACTIONS.keys())
        ).ask()

        action_fn = ACTIONS.get(action)
        if action_fn:
            try:
                action_fn()
            except Exception as e:
                print(f"Error ejecutando la acción '{action}': {str(e)}")


if __name__ == "__main__":
    main()
