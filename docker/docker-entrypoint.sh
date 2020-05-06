#!/bin/bash
set -e

if [ "$1" = 'carte.sh' ]; then
  if [ ! -f "$KETTLE_HOME/carte_config.xml" ]; then
    # Set variables to defaults if they are not already set
    : ${CARTE_NAME:=carte-server}
    : ${CARTE_NETWORK_INTERFACE:=eth0}
    : ${CARTE_HOSTNAME:=localhost}
    : ${CARTE_PORT:=8080}
    : ${CARTE_USER:=cluster}
    : ${CARTE_PASSWORD:=cluster}
    : ${CARTE_IS_MASTER:=Y}

    : ${CARTE_INCLUDE_MASTERS:=N}

    : ${CARTE_REPORT_TO_MASTERS:=Y}
    : ${CARTE_MASTER_NAME:=carte-master}
    : ${CARTE_MASTER_HOSTNAME:=localhost}
    : ${CARTE_MASTER_PORT:=8080}
    : ${CARTE_MASTER_USER:=cluster}
    : ${CARTE_MASTER_PASSWORD:=cluster}
    : ${CARTE_MASTER_IS_MASTER:=Y}

    : ${REPOSITORY_NAME:=my_pdi_repo}
    : ${REPOSITORY_READ_ONLY:=N}
    : ${REPOSITORY_ID:=KettleFileRepository}
    : ${REPOSITORY_HIDDEN_FILES:=N}
    : ${REPOSITORY_DESCRIPTION:=File repository}
    : ${REPOSITORY_BASE_DIRECTORY:=$KETTLE_HOME\\/repositories\\/my_pdi_repo\\/project\\/}

    # Copy the right template and replace the variables in it
    if [ "$CARTE_INCLUDE_MASTERS" = "Y" ]; then
      cp /templates/carte_config_slave.xml "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_REPORT_TO_MASTERS/$CARTE_REPORT_TO_MASTERS/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_NAME/$CARTE_MASTER_NAME/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_HOSTNAME/$CARTE_MASTER_HOSTNAME/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_PORT/$CARTE_MASTER_PORT/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_USER/$CARTE_MASTER_USER/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_PASSWORD/$CARTE_MASTER_PASSWORD/" "$KETTLE_HOME/carte_config.xml"
      sed -i "s/CARTE_MASTER_IS_MASTER/$CARTE_MASTER_IS_MASTER/" "$KETTLE_HOME/carte_config.xml"
    else
      cp /templates/carte_config_master.xml "$KETTLE_HOME/carte_config.xml"
    fi
    sed -i "s/CARTE_NAME/$CARTE_NAME/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_NETWORK_INTERFACE/$CARTE_NETWORK_INTERFACE/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_HOSTNAME/$CARTE_HOSTNAME/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_PORT/$CARTE_PORT/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_USER/$CARTE_USER/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_PASSWORD/$CARTE_PASSWORD/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/CARTE_IS_MASTER/$CARTE_IS_MASTER/" "$KETTLE_HOME/carte_config.xml"
    sed -i "s/REPOSITORY_NAME/$REPOSITORY_NAME/" "$KETTLE_HOME/carte_config.xml"
  fi

  if [ ! -f "$KETTLE_HOME/.kettle/repositories.xml" ]; then
    cp /templates/repositories.xml "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s/REPOSITORY_NAME/$REPOSITORY_NAME/" "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s/REPOSITORY_READ_ONLY/$REPOSITORY_READ_ONLY/" "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s/REPOSITORY_ID/$REPOSITORY_ID/" "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s/REPOSITORY_HIDDEN_FILES/$REPOSITORY_HIDDEN_FILES/" "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s/REPOSITORY_DESCRIPTION/$REPOSITORY_DESCRIPTION/" "$KETTLE_HOME/.kettle/repositories.xml"
    sed -i "s~REPOSITORY_BASE_DIRECTORY~$REPOSITORY_BASE_DIRECTORY~g" "$KETTLE_HOME/.kettle/repositories.xml"
  fi
fi

# Run any custom scripts
if [ -d /docker-entrypoint.d ]; then
  for f in /docker-entrypoint.d/*.sh; do
    [ -f "$f" ] && . "$f"
  done
fi

exec "$@"