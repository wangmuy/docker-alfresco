rancher-alfresco
===============

# Table of Contents

- [Introduction](#introduction)
- [Contributing](#contributing)
- [Note](#note)
- [Installation](#installation)
- [Quick Start](#quick-start)
	- [Use Rancher](#use-rancher)
	- [Docker-compose](#docker-compose)
	- [Docker](#docker)
- [Run Alfresco for production purpose](#run-alfresco-for-production-purpose)
	- [External database](#external-database)
		- [Start Database PostgreSQL](#start-database-postgresql)
		- [Start Alfresco](#start-alfresco)
	- [Reverse Proxy](#reverse-proxy)
	- [Mail setting](#mail-setting)
	- [FTP setting](#ftp-setting)
	- [CIFS](#cifs)
	- [LDAP authentification](#ldap-authentification)
- [Parameters](#parameters)
- [Upgrading](#upgrading)
- [References](#references)



# Introduction
Dockerfile to build an Alfresco container image.

[![Docker Repository on Quay](https://quay.io/repository/webcenter/rancher-alfresco/status "Docker Repository on Quay")](https://quay.io/repository/webcenter/rancher-alfresco)


# Contributing
Here is how you can help:
- Send a Pull Request with your awesome new features and bug fixes
- Report [Issues](https://github.com/disaster37/rancher-alfresco/issues)

# Note

This docker image is created to run on Rancher ecosystem. You can also play it directly on top of Docker.

For more information about to run Alfresco on Rancher on few seconds, read my [blog](https://blog.webcenter.fr).


# Installation
Pull the image from the docker index.
```bash
docker pull webcenter/rancher-alfresco:latest
```

or pull a particular version:
```bash
docker pull webcenter/rancher-alfresco:v5.1.0-3
```

Alternatively, you can build the image yourself:
```bash
git clone https://github.com/disaster37/rancher-alfresco.git
cd rancher-alfresco
docker build --tag="$USER/alfresco" .
```


# Quick Start

If you are french, you can read my [blog](https://blog.webcenter.fr) to found more advance usage. For exemple how to deploy Alfresco in few minutes on Rancher for production usage.

## Use Rancher

Go on catalog and search Alfresco. Just click on deploy. Congratulation, you have Alfresco.

## Docker-compose

Download the docker-compose file from my git repository, and run :

```bash
docker-compose up
```

Congratulation, you have Alfresco.

## Docker

Run the alfresco image with the name "alfresco".

```bash
docker run --name='alfresco' -it --rm -p 8080:8080 webcenter/rancher-alfresco
```

**NOTE**: Please allow a few minutes for the application to start, especially if
populating the database for the first time.

Go to `http://localhost:8080` or point to the ip of your docker server.

The default username and password are:
* username: **admin**
* password: **admin**


# Run Alfresco for production purpose

## External database

It's a good way to run the dabase on external container. You can use PostgreSQL (the best way) or MySQL.
If you use official PostgreSQL container or official MySQL Container, it's supported out of the box.

### Start Database PostgreSQL

```bash
docker run -d --name "postgres" \
  -e 'PGDATA=/var/lib/postgresql/data/pgdata' \
  -e 'POSTGRES_DB=alfresco' \
  -e 'POSTGRES_USER=alfresco' \
  -e 'POSTGRES_PASSWORD=password'\
  -v /host/alfresco_database=/var/lib/postgresql/data/pgdata \
  postgres:9.4
```

### Start Alfresco

```bash
docker run -d --name "alfresco" \
  --link postgres:db \
  -p 7070:7070 -p 8080:8080 \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```

## Reverse Proxy
To run Alfresco behind a Reverse Proxy, you need to add extra parameter like this :

```bash
docker run -d --name "alfresco" \
  -e 'REVERSE_PROXY_URL=https://ged.my-domain.com' \
  --link postgres:db \
  -p 7070:7070 -p 8080:8080 \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```

## Mail setting
To allow Alfresco send and receive mail, you need to add extras parameters :

```bash
docker run -d --name "alfresco" \
  -e 'MAIL_HOST=smpt.my-domain.local' \
  -e 'MAIL_PORT=25' \
  -e 'MAIL_PROTOCOL=smtp'\
  -e 'MAIL_USER=login' \
  -e 'MAIL_PASSWORD=password' \
  -p 7070:7070 -p 8080:8080 \
  --link postgres:db \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```

## FTP setting
To enable FTP on ALfresco :

```bash
docker run -d --name "alfresco" \
  -e 'FTP_ENABLED=true' \
  -e 'FTP_PORT=21' \
  -p 21:21 -p 7070:7070 -p 8080:8080 \
  --link postgres:db \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```
## CIFS
To access on alfresco as a Windows share, you must setting CIFS :

```bash
docker run -d --name "alfresco" \
  -e 'CIFS_ENABLED=true' \
  -e 'CIFS_SERVER_NAME=localhost' \
  -e 'CIFS_DOMAIN=WORKGROUP' \
  --link postgres:db \
  -p 445:445 -p 7070:7070 -p 8080:8080 \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```

## LDAP authentification
To enable LDAP authentification, you must use the following parameters :

```bash
docker run -d --name "alfresco" \
  -e 'LDAP_ENABLED=true' \
  -e 'LDAP_AUTH_FORMAT==uid=%s,cn=users,cn=accounts,dc=example,dc=com' \
  -e 'LDAP_HOST=dc.exemple.com' \
  -e 'LDAP_USER=login' \
  -e 'LDAP_PASSWORD=password' \
  -e 'LDAP_ADMINS=administrator' \
  -e 'LDAP_GROUP_SEARCHBASE=cn=groups,cn=accounts,dc=example,dc=com' \
  -e 'LDAP_USER_SEARCHBASE=cn=users,cn=accounts,dc=example,dc=com' \
  -p 445:445 -p 7070:7070 -p 8080:8080 \
  --link postgres:db \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```

## VTI external access
To enable the VTI for remote access, you must use the following parameters :


```bash
docker run -d --name "alfresco" \
  -e 'VTI_HOST=vti.mydomain.com' \
  -e 'VTI_PORT=7070' \
  --link postgres:db \
  -p 445:445 -p 7070:7070 -p 8080:8080 \
  -v /host/alfresco_data=/opt/alfresco/alf_data \
  webcenter/rancher-alfresco:v5.1.0-3
```


# Parameters

Below is the complete list of currently available parameters that can be set
using environment variables.
- **ALFRESCO_HOSTNAME**: hostname of the Alfresco server; default = `127.0.0.1`
- **ALFRESCO_PORT**: port to join Alfresco server; default = `8080`
- **ALFRESCO_PROTOCOL**: protocol to join Alfresco server; default = `http`
- **CIFS_ENABLED**: whether or not to enable CIFS; default = `true`
- **CIFS_SERVER_NAME**: hostname of the CIFS server; default = `localhost`
- **CIFS_DOMAIN**: domain of the CIFS server; default = `WORKGROUP`
- **DATABASE_HOST**: host of the database server; default = `localhost`
- **DATABASE_TYPE**: postgresql or mysql; default = `postgresql`
- **DATABASE_NAME**: name of the database to connect to; default = `alfresco`
- **DATABASE_PASSWORD**: password to use when connecting to the database; default = `admin`
- **DATABASE_USER**: username to use when connecting to the database; default = `alfresco`
- **DATABASE_PORT**: port of the database server; default = `5432`
- **ENVIRONMENT**: UNKNOWN, TEST, PRODUCTION or BACKUP; default = `PRODUCTION`
- **FTP_ENABLED**: whether or not to enable FTP; default = `true`
- **FTP_PORT**: port of the FTP server; default = `21`
- **LDAP_ENABLED**: whether or not to enable LDAP; default = `false`
- **LDAP_AUTH_FORMAT**: default = `uid=%s,cn=users,cn=accounts,dc=example,dc=com`
- **LDAP_HOST**: DNS of LDAP server; default = `ldap.example.com`
- **LDAP__ADMINS**: comma separated list of admin names in ldap; default = `admin`
- **LDAP_USER**: default = `uid=admin,cn=users,cn=accounts,dc=example,dc=com`
- **LDAP_PASSWORD**: default = `password`
- **LDAP_GROUP_SEARCHBASE**: default = `cn=groups,cn=accounts,dc=example,dc=com`
- **LDAP_USER_SEARCHBASE**: default = `cn=users,cn=accounts,dc=example,dc=com`
- **MAIL_HOST**: hostname or IP where email should be sent; default = `localhost`
- **MAIL_PORT**: default = `25`
- **MAIL_USER**: username to connect to the smtp server
- **MAIL_PASSWORD**: password to connect to the smtp server
- **MAIL_SENDER**: what is in the from field; default = `alfresco@alfresco.org`
- **MAIL_PROTOCOL**: smtp or smtps; default = `smtp`
- **MAIL_STARTTLS_ENABLE**: use starttls or not; default = `false`
- **REVERSE_PROXY_URL**: the url use by your reverse proxy (for exemple : https://ged.exemple.com); no default value
- **SHARE_HOSTNAME**: hostname of the share server; default = `127.0.0.1`
- **SHARE_PORT**: port to join Share server; default = `8080`
- **SHARE_PROTOCOL**: protocol to join Share server; default = `http`
- **VTI_HOST**: the domain name to join VTI from external user.
- **VTI_PORT**: the port to join VTI from external user.


# Upgrading
TODO: I might be able to add some options that aid in upgrading.  For now though,
backup, backup, backup, and then follow this guide:
* http://docs.alfresco.com/community/concepts/ch-upgrade.html


# References
* http://www.alfresco.com/community
* http://docs.alfresco.com/community/concepts/welcome-infocenter_community.html
