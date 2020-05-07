# Pentaho Docker (compose)

Docker Compose de ejemplo para levantar un Pentaho Data Integration.

Se precisa copiar el el proyecto de Pentaho dentro de repositories, ya que este directorio se montará en el contenedor. Por ejemplo, dentro de repositories aparecería la estructura:

- repositories
  - asio-um
    - project

Para levantar el contenedor:

```bashfile
docker-compose up -d
```

Para pararlo

```bashfile
docker-compose down
```

## Componentes adicionales

En caso de necesitar componentes extra para el funcionamiento de Pentaho, como por ejemplo bases de datos, kafka, etc. se puede añadir un fichero docker-compose adicional, en este ejemplo se ha creado el fichero `docker-compose-extra.yml`, el cual debe ser levantando junto con el de pentaho, para ello:

```bashfile
docker-compose -f docker-compose.yml -f docker-compose-extra.yml up -d
```

Para pararlo:

```bashfile
docker-compose -f docker-compose.yml -f docker-compose-extra.yml down
```
