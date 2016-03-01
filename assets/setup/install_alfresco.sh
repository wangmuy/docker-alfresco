#!/usr/bin/env sh
set -e

# vars

ALF_HOME=/opt/alfresco
ALF_BIN=$(basename "${ALF_URL}")
export JAVA_HOME=${ALF_HOME}/java

# get alfresco installer
mkdir -p $ALF_HOME
cd /tmp
curl -O $ALF_URL
chmod +x $ALF_BIN

# install alfresco
./$ALF_BIN --mode unattended --prefix $ALF_HOME --alfresco_admin_password admin

# get rid of installer - makes image smaller
rm $ALF_BIN

# Add account
RUN groupadd alfresco
RUN useradd -s /bin/false -g alfresco -d /opt/alfresco alfresco
RUN chown -R alfresco:alfresco /opt/alfresco
