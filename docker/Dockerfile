ARG PDI_RELEASE=9.0
ARG PDI_VERSION=9.0.0.0-423
ARG PDI_HOME=/opt/pentaho-di
ARG KETTLE_HOME=/pentaho-di

# FROM ubuntu:xenial as builder
FROM ubuntu:xenial as builder

ARG PDI_RELEASE
ARG PDI_VERSION
ARG PDI_HOME
ARG KETTLE_HOME

ENV PDI_RELEASE=$PDI_RELEASE \
    PDI_VERSION=$PDI_VERSION \
    PDI_HOME=$PDI_HOME \
    KETTLE_HOME=$KETTLE_HOME

RUN mkdir -p $PDI_HOME && \
    apt-get update && \
    apt-get -y install curl unzip

#
# You should download pdi-ce-${PDI_VERSION}.zip into this directory
# BEFORE trying to create docker build
# https://sourceforge.net/projects/pentaho/files/Pentaho%20${PDI_RELEASE}/client-tools/pdi-ce-${PDI_VERSION}.zip/download
#

# RUN curl -L -o /tmp/pdi-ce-${PDI_VERSION}.zip \
#         https://sourceforge.net/projects/pentaho/files/Pentaho%20${PDI_RELEASE}/client-tools/pdi-ce-${PDI_VERSION}.zip/download

COPY pdi-ce-${PDI_VERSION}.zip /tmp

RUN curl -L -o /tmp/mariadb-java-client-2.6.0.jar \ 
        https://downloads.mariadb.com/Connectors/java/connector-java-2.6.0/mariadb-java-client-2.6.0.jar

RUN unzip -q /tmp/pdi-ce-${PDI_VERSION}.zip -d $PDI_HOME && \
    rm /tmp/pdi-ce-${PDI_VERSION}.zip && \
    mv /tmp/mariadb-java-client-2.6.0.jar $PDI_HOME/data-integration/lib

FROM openjdk:8-jre-alpine

ARG PDI_RELEASE
ARG PDI_VERSION
ARG PDI_HOME
ARG KETTLE_HOME

ENV PDI_RELEASE=$PDI_RELEASE \
    PDI_VERSION=$PDI_VERSION \
    PDI_HOME=$PDI_HOME \
    KETTLE_HOME=$KETTLE_HOME

RUN apk --no-cache add bash

RUN mkdir -p $PDI_HOME
RUN mkdir $KETTLE_HOME

COPY --from=builder $PDI_HOME $PDI_HOME

ENV PATH=$PDI_HOME/data-integration:$PATH

EXPOSE 8080

RUN mkdir -p $KETTLE_HOME/.kettle $KETTLE_HOME/repositories /docker-entrypoint.d /templates

COPY carte_config*.xml /templates/
COPY repositories.xml /templates/

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["carte.sh", "/pentaho-di/carte_config.xml"]