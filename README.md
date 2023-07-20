# postgres-listen-notify

The following steps describe how to set up a Postgres database that you can use as a publish / subscribe system for notifications. This can be used to create decoupled systems.

##### Overview

1. Install postgresql
2. Configure postgresql.conf
3. Create a database
4. Create user
5. Configure pg_hba.conf
6. Open ports
7. Test connection
8. LISTEN / NOTIFY in SQL
9. Listen in Python


##### 1. Install postgresql

You can install postgresql on Ubuntu as follows:

```
sudo apt update
sudo apt install postgresql
```

##### 2. Configure postgresql.conf

Edit `/etc/postgresql/14/main/postgresql.conf` and modify the following setting:

```
listen_addresses = '*'          # what IP address(es) to listen on;
```

##### 3. Create a database

Switch to the postgres user:

```
sudo su - postgres
```

Then launch `psql` and type the following command:

```
CREATE DATABASE hls_demo;
```

##### 4. Create user

Create a user and set a password

```
CREATE USER hls_demo WITH PASSWORD 'YOUR_PASSWORD_GOES_HERE';
```

Now enter `\q` to exit out of `psql` and `exit` to come out of the postgres user.

##### 5. Configure pg_hba.conf

Edit `/etc/postgresql/14/main/pg_hba.conf` and add the following setting:

```
host    hls_demo        hls_demo        0.0.0.0/0               scram-sha-256
```

Restart postgres for this setting to take effect:

```
sudo service postgresql restart
```

##### 6. Open ports

In the AWS console, edit the security group attached to your instance. Add an inbound rule to allow traffic on port 5432 from anywhere (0.0.0.0/0)

##### 7. Test connection

From a different computer (eg. Databricks cluster), type the following command:

```
psql -h 3.232.122.1 -U hls_demo -W -d hls_demo
```

You will be prompted for a password.

##### 8. LISTEN / NOTIFY in SQL

Upon successful login, enter the following commands to connect to the hls_demo database and LISTEN for messages:

```
\c hls_demo
LISTEN hls_channel;
```

You can now post messages using the following command, either from the same machine or from a different machine that is connected to the database:

```
NOTIFY hls_channel, 'Hello world';
```

##### 9. Listen in Python

Set the environment variables `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DATABASE` in `.env`.

Then run the [listen.py](listen.py) script as follows:

```
python listen.py
```