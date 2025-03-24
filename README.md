# Aurora CLI Tool


**Aurora CLI Tool** es una herramienta de línea de comandos (CLI) diseñada para automatizar tareas relacionadas con los clusters Aurora de AWS, especialmente para entornos de desarrollo. Permite clonar clusters, eliminarlos o listar su información mediante una interfaz interactiva.

---

### Instalación vía pip

- La forma recomendada de usar **Aurora CLI Tool** es instalándola directamente desde el repositorio remoto con `pip`.

### Pasos

1. **Crear un entorno virtual:**

- python3 -m venv aurora_env

2. **Instalar la herramienta desde GitHub:**

- pip install git+https://github.com/Oscaridiji/aurora-tool.git    

3. **Ejecutar la CLI:**

- aurora-tool

---

## Requisitos y configuración del entorno

- Python 3.8 o superior.
- Acceso a AWS mediante un **usuario IAM**.
- El usuario IAM debe tener permisos definidos en el archivo [`iam_policy.json`](./iam_policy.json) incluido en este proyecto.

### Configurar el acceso a AWS

- Antes de usar la herramienta, asegúrate de tener configurado un perfil de AWS con credenciales válidas. Puedes hacerlo ejecutando:

- Ejecuta el comando:

aws configure

- Esto solicitará:

AWS Access Key ID

AWS Secret Access Key

Región por defecto (por ejemplo: eu-west-3)

Formato de salida (puedes dejarlo vacío)

- Asegúrate de que el usuario IAM tenga una política similar a iam_policy.json, con permisos para listar, clonar, etiquetar y eliminar clusters Aurora.

---

## Funcionalidades

### Clonar clusters Aurora

- Clona cualquier cluster (producción o de otro desarrollador) sin afectar al original.
- Permite establecer una etiqueta de autoeliminación con una fecha futura.
- Restringe la creación si ya existen 5 clusters asociados al usuario.

### Eliminar clusters Aurora

- Solo permite eliminar clusters que hayan sido creados por el usuario (basado en la etiqueta `owner`).
- Protege los recursos de otros usuarios o del entorno de producción.

### Listar clusters Aurora

- Lista únicamente los clusters que pertenecen al usuario actual.
- Muestra información clave: endpoints, puerto, VPC, estado.

### Interfaz interactiva

- La CLI está construida con [`questionary`](https://github.com/tmbo/questionary), ofreciendo menús y formularios en lugar de requerir flags o parámetros manuales.


---

## Autoeliminación con etiqueta `auto-delete-after` (propuesta de mejora)

Cada cluster clonado con esta herramienta incluye una etiqueta personalizada llamada `auto-delete-after`, con una fecha en formato ISO 8601 (por ejemplo: `2025-03-31T12:00:00Z`).

Esta etiqueta permite que se pueda implementar fácilmente un sistema que elimine clusters automáticamente cuando hayan superado esa fecha. Aunque **la herramienta no elimina automáticamente los clusters al vencer**, se deja preparado todo para que esta automatización pueda añadirse en el futuro si se desea.

### Propuesta de implementación: Lambda + EventBridge (opcional)

En caso de querer automatizar esta limpieza de clusters expirados, una opción sencilla sería:

1. **Función Lambda en Python**

   - Que utilice `boto3` para listar todos los clusters con `describe_db_clusters`.
   - Luego recorra sus etiquetas con `list_tags_for_resource`.
   - Si detecta la etiqueta `auto-delete-after` y la fecha ha pasado, puede eliminar el cluster y sus instancias relacionadas.

2. **Ejecución bajo demanda o programada**

   - Esta Lambda puede ejecutarse **bajo demanda** (por ejemplo, desde una herramienta interna o pipeline).
   - O también podría configurarse como tarea programada con EventBridge para que se ejecute cada noche, o en el horario que más convenga.

3. **Permisos necesarios**

   Para esta automatización, bastaría con una política similar a la incluida (`iam_policy.json`), permitiendo las acciones:

   - `rds:DescribeDBClusters`
   - `rds:ListTagsForResource`
   - `rds:DeleteDBCluster`
   - `rds:DeleteDBInstance`
   - `sts:GetCallerIdentity`

---

## Notificaciones automáticas (opcional)

Otra posible mejora sería añadir un sistema de notificaciones cuando se realizan acciones relevantes. Por ejemplo:

- Cuando se clona un cluster.
- Cuando se elimina un cluster manualmente.
- Cuando se autoelimina un cluster expirado.
- Cuando un usuario no puede clonar más clusters por superar el límite de 5.

### Canales posibles

- **Email**: usando Amazon SNS.
- **Slack**: mediante un [Webhook entrante](https://api.slack.com/messaging/webhooks).

---

## Distribución como ejecutable con PyInstaller (opcional)

Para entornos donde no queremos exponer el código fuente o simplemente queremos facilitar la ejecución de la herramienta sin necesidad de entorno virtual, podemos distribuir Aurora CLI Tool como un binario ejecutable.

Esta opción puede ser útil si, por ejemplo, solo los responsables de infraestructura pueden modificar la lógica y los developers simplemente ejecutan la herramienta.


---

## Anonimización de datos (idea de extensión)

Aunque esta herramienta clona la base de datos sin modificar los datos originales, en entornos sensibles se podría añadir una fase opcional de anonimización tras la restauración del cluster.

### Propuesta de implementación (opcional):

- Crear un script SQL o Lambda post-restauración que anonimice ciertas tablas o campos.
- Esta tarea podría ejecutarse de forma automática una vez que el cluster haya sido clonado.

---

Este proyecto fue desarrollado como parte de una prueba técnica para evaluar la automatización de entornos en AWS con Python.