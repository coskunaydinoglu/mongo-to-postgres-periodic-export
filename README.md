# MongoDB to Postgres data migration demo 

This is demo PoC for data migration from mongodb to relational databases. Postresql is selected as RDBMS. As this is PoC not data transformation is applied. It is implemented as simple as possible.

Simply a collection is exported to csv as a scheduled job. Job is defined in crontab

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* * * * * /bin/bash /app/wrapper.sh >> /var/log/cron.log 2>&1
```

You can change the schedule in cron syntax. For reference you can check here https://crontab.guru/

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)


## Installation

Update the .env file for database connections. Project runs in a docker container. Postgresql is installed into docker container. Mongodb is accessed from external. It is not included in container.

Check env.sample for reference

```
# MongoDB
MONGODB_URI=mongodb://username:password@remote-server-address:27017/database-name
MONGODB_DATABASE=yourdatabase
# PostgreSQL
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpassword
POSTGRES_DB=countly
```

## Usage

Run 
```
docker-compose up --build -d
```

This will install and postgresql and create initial table. You can change postgres-init/init.sql. Initial table is created there.

You can change soruce collection and destination table, data conversion in script.py. script.py is executed depending on the scheduling infor on crontab file

To check the logs you can check  /var/log/cron.log in container via Docker Desktop or command line
```
docker exec mongo-to-postgres-periodic-export-python-script-1 cat /var/log/cron.log
```
