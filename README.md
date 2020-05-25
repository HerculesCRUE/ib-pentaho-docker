
![](./images/logos_feder.png)



| Entregable     | Procesador de datos                                        |
| -------------- | ------------------------------------------------------------ |
| Fecha          | 25/05/2020                                                   |
| Proyecto       | [ASIO](https://www.um.es/web/hercules/proyectos/asio) (Arquitectura Sem醤tica e Infraestructura Ontol骻ica) en el marco de la iniciativa [H閞cules](https://www.um.es/web/hercules/) para la Sem醤tica de Datos de Investigaci髇 de Universidades que forma parte de [CRUE-TIC](http://www.crue.org/SitePages/ProyectoHercules.aspx) |
| M骴ulo         | Pentaho Docker                                             |
| Tipo           | Software                                                     |
| Objetivo       | Generaci贸 de imagen de Docker para Pentaho Data Integration versi贸n 9.0. |
| Estado         | **100%** Imagen de docker generada |
| Pr髕imos pasos | Realizar modificaciones necesarias edurante el desarrollo. |
| Documentaci髇  | [Manual de usuario](https://github.com/HerculesCRUE/ib-asio-docs-/blob/master/entregables_hito_1/12-An%C3%A1lisis/Manual%20de%20usuario/Manual%20de%20usuario.md)<br />[Manual de despliegue](https://github.com/HerculesCRUE/ib-asio-composeset/blob/master/README.md)<br />[Documentaci髇 t閏nica](https://github.com/HerculesCRUE/ib-asio-docs-/blob/master/entregables_hito_1/11-Arquitectura/ASIO_Izertis_Arquitectura.md) |

# Pentaho Docker

Generaci贸 de imagen de Docker para Pentaho Data Integration versi贸n 9.0.

## Configuraci贸n

| Variable                    | Descripci贸n                                                 | Valor por defecto                             |
| --------------------------- | ----------------------------------------------------------- | --------------------------------------------- |
| `CARTE_NAME`                | Nombre del servidor Carte                                   | carte-server                                  |
| `CARTE_NETWORK_INTERFACE`   | Nombre de la interfaz de red                                | eth0                                          |
| `CARTE_HOSTNAME`            | Nombre del host                                             | localhost                                     |
| `CARTE_PORT`                | Puerto de PDI                                               | 8080                                          |
| `CARTE_USER`                | Usuario de PDI                                              | cluster                                       |
| `CARTE_PASSWORD`            | Contrase帽a de PDI                                           | cluster                                       |
| `REPOSITORY_NAME`           | Nombre del repositorio                                      | my_pdi_repo                                   |
| `REPOSITORY_READ_ONLY`      | Indica si el repositorio es de solo lectura, valores N y Y  | N                                             |
| `REPOSITORY_ID`             | ID del repositorio                                          | KettleFileRepository                          |
| `REPOSITORY_DESCRIPTION`    | Descripci贸n del repositorio                                 | File repository                               |
| `REPOSITORY_BASE_DIRECTORY` | Directorio base del repositorio                             | /pentaho-di/repositories/my_pdi_repo/project/ |

## Ejecuci贸n

Para probar la ejecuci贸n de un Job, por ejemplo llamado `main`, se precisa ejecudtar la siguiente URL:

    http://localhost:8080/kettle/runJob/?job=main

## Forks
Otros repos con configuraci贸n de diferentes versiones de PDI

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