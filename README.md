![](./images/logos_feder.png)



| Entregable     | Sistema de gestión entre Infraestructura Ontológica y Arquitectura Semántica |
| -------------- | ------------------------------------------------------------ |
| Fecha          | 26/04/2020                                                   |
| Revisado por   | Paloma Terán Pérez                                           |
| Proyecto       | [ASIO](https://www.um.es/web/hercules/proyectos/asio) (Arquitectura Semántica e Infraestructura Ontológica) en el marco de la iniciativa [Hércules](https://www.um.es/web/hercules/) para la Semántica de Datos de Investigación de Universidades que forma parte de [CRUE-TIC](https://www.crue.org/proyecto/hercules/) |
| Módulo         | Procesador de datos                                          |
| Tipo           | Software                                                     |
| Objetivo       | Sistema de gestión de datos del módulo de procesamiento para el proyecto Backend SGI (ASIO). |
| Estado         | **100%**                                                     |
| Próximos pasos |                                                              |

# ASIO - Sistema de gestión entre Infraestructura Ontológica y Arquitectura Semántica



|     | Master |
| --- | ------ |
| Quality Gate | [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=HerculesCRUE_ib-api-exchange&metric=alert_status)](https://sonarcloud.io/dashboard?id=HerculesCRUE_ib-discovery) |
| Coverage | [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=HerculesCRUE_ib-api-exchange&metric=coverage)](https://sonarcloud.io/dashboard?id=HerculesCRUE_ib-api-exchange) |

Sistema de gestión de datos del módulo de procesamiento para el proyecto Backend SGI (ASIO). 

## OnBoarding

Para iniciar el entorno de desarrollo se necesita cumplir los siguientes requisitos:

* OpenJDK 11
* Eclipse JEE 2019-09 con plugins:
  * Spring Tools 4
  * m2e-apt
  * Lombok
* Docker

## Metodología de desarrollo

La metodología de desarrollo es Git Flow.

## Entorno de desarrollo Docker

La inicialización de los elementos adicionales al entorno de desarrollo se realiza con docker. 

En el directorio docker-devenv se ha configurado un fichero docker-compose.yml para poder arrancar el entorno de desarrollo.

Para arrancar el entorno:

```bash
docker-compose up -d
```

Para pararlo:

```bash
docker-compose down
```

## Instalación en entorno real

Será preciso configurar las siguientes variables de entorno cuando se instale en un entorno real:

|Variable|Descripción|Valor por defecto|
|---|---|---|
|`APP_PERSISTENCE_DATASOURCE_USERNAME`|Nombre del usuario de acceso a la base de datos|root|
|`APP_PERSISTENCE_DATASOURCE_PASSWORD`|Contraseña del usuario de acceso a la base de datos|root|
|`APP_PERSISTENCE_DATASOURCE_URL`|URL de acceso a la base de datos MySQL|jdbc:mysql://localhost:3307/app?autoReconnect=true&useUnicode=true&characterEncoding=UTF-8&serverTimezone=UTC&createDatabaseIfNotExist=true|

### Ejecución

Al generarse un JAR bootable la ejecución se realizará mediante el siguiente comando:

```bash
java -jar {jar-name}.jar
```

Sustituyendo `{jar-name}` por el nombre del fichero JAR generado.

No es necesario especificar la clase de inicio de la aplicación, ya que el fichero MANIFEST.MF generado ya contiene la información necesaria. Solamente se especificarán los parametros necesarios.

## Testing y cobertura

Se incluyen los resultados del testing y cobertura en los siguientes enlaces:

* [Testing](https://reports.herculesasioizertis.desa.um.es/api-exchange/surefire/surefire-report.html)
* [Cobertura](https://sonarcloud.io/component_measures?id=HerculesCRUE_ib-api-exchange&metric=coverage&view=list)
* [Testing BDD](docs/testing.md)

##  Documentación adicional

* [Compilación](docs/build.md)
* [Generación Docker](docs/docker.md)
