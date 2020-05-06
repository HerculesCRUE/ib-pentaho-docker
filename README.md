# Pentaho Docker

Generació de imagen de Docker para Pentaho Data Integration versión 9.0.

## Configuración

| Variable                    | Descripción                                                 | Valor por defecto                             |
| --------------------------- | ----------------------------------------------------------- | --------------------------------------------- |
| `CARTE_NAME`                | Nombre del servidor Carte                                   | carte-server                                  |
| `CARTE_NETWORK_INTERFACE`   | Nombre de la interfaz de red                                | eth0                                          |
| `CARTE_HOSTNAME`            | Nombre del host                                             | localhost                                     |
| `CARTE_PORT`                | Puerto de PDI                                               | 8080                                          |
| `CARTE_USER`                | Usuario de PDI                                              | cluster                                       |
| `CARTE_PASSWORD`            | Contraseña de PDI                                           | cluster                                       |
| `REPOSITORY_NAME`           | Nombre del repositorio                                      | my_pdi_repo                                   |
| `REPOSITORY_READ_ONLY`      | Indica si el repositorio es de solo lectura, valores N y Y  | N                                             |
| `REPOSITORY_ID`             | ID del repositorio                                          | KettleFileRepository                          |
| `REPOSITORY_DESCRIPTION`    | Descripción del repositorio                                 | File repository                               |
| `REPOSITORY_BASE_DIRECTORY` | Directorio base del repositorio                             | /pentaho-di/repositories/my_pdi_repo/project/ |

## Ejecución

Para probar la ejecución de un Job, por ejemplo llamado `main`, se precisa ejecudtar la siguiente URL:

    http://localhost:8080/kettle/runJob/?job=main

## Forks
Otros repos con configuración de diferentes versiones de PDI

- PDI 8.2
  - https://github.com/peterborkuti/docker-pentaho-di
- PDI 8.0
  - https://github.com/Statflo/docker-pentaho-di
- PDI 7.0
  - https://github.com/FabioBatSilva/docker-pentaho-di
  - https://github.com/zagno/docker-pentaho-di
- PDI 6.1
  - https://github.com/FCNY/docker-pentaho-di
- PDI 5.3
  - https://github.com/aloysius-lim/docker-pentaho-di