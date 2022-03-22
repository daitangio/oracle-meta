#!/bin/bash
docker inspect oracle/database:19.3.0-ee || { echo  Image does not exist...creating...
    (cd ../docker-images/OracleDatabase/SingleInstance/dockerfiles ; ./buildContainerImage.sh -v 19.3.0 -e )
}
echo DEFAULT  ORACLE_SID is ORCLCDB
docker run --name pocket_oracle \
    -p 1521:1521 -p 5500:5500 \
    -e ORACLE_PWD=oracle \
    -e ORACLE_CHARACTERSET=AL32UTF8\
    -v $HOME/oradata19:/opt/oracle/oradata \
 oracle/database:19.3.0-ee
