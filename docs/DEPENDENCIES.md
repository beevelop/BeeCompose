# Service Dependency Graph

**Updated:** 2026-01-21

This document maps dependencies between BeeCompose services and their backing stores.

## Dependency Overview

```
                                    +------------+
                                    |  traefik   | (Reverse Proxy)
                                    +-----+------+
                                          |
              +---------------------------+---------------------------+
              |           |           |           |           |       |
          +---+---+   +---+---+   +---+---+   +---+---+   +---+---+   ...
          | gitlab|   |sentry |   |keycloak|  |metabase|  |bitwarden|
          +---+---+   +---+---+   +---+---+   +---+---+   +---------+
              |           |           |           |
         +----+----+  +---+---+  +----+----+  +---+---+
         |postgres |  |postgres|  |postgres |  |postgres|
         +---------+  |redis   |  +---------+  +---------+
                      |memcached|
                      +---------+
```

## Database Backend Matrix

### PostgreSQL Services

| Service | Container Name | Version |
|---------|---------------|---------|
| cabot | postgres | 17-alpine |
| confluence | postgresql | 17-alpine |
| crowd | postgresql | 17-alpine |
| gitlab | database | kkimurak/sameersbn-postgresql:17 |
| huginn | postgres | 17-alpine |
| jira | postgresql | 17-alpine |
| keycloak | postgres | 17 |
| metabase | database | 15-alpine |
| redash | postgres | 17-alpine |
| sentry | postgres | 17-alpine |
| sonarqube | database | 17-alpine |
| statping | postgres_statping | 17-alpine |
| weblate | postgres | 17-alpine |

### MySQL/MariaDB Services

| Service | Container Name | Version |
|---------|---------------|---------|
| directus | mysql | 8.4 |
| monica | mysql | 8.4 |
| mysql | mysql | 8.4 |
| rundeck | (embedded) | - |
| zabbix | database | mariadb:12.2 |

### Redis Services

| Service | Container Name | Version |
|---------|---------------|---------|
| cabot | (via rabbitmq) | - |
| gitlab | redis | 7-alpine |
| redash | redis | 7-alpine |
| sentry | redis | 7-alpine |
| weblate | redis | 7-alpine |

### Other Databases

| Service | Database | Container Name | Version |
|---------|----------|---------------|---------|
| graylog | MongoDB | mongodb | 8.0 |
| graylog | Elasticsearch | elasticsearch | 7.17.29 |

### Cache Services

| Service | Cache Type | Container Name | Version |
|---------|------------|---------------|---------|
| sentry | Memcached | memcached | 1.6 |
| weblate | Memcached | cache | 1.6-alpine |

## Service Dependency Chains

### Standalone Services (No Dependencies)

These services have no internal service dependencies:

- bitwarden
- dependency-track
- duckling
- minio
- nexus
- phpmyadmin (requires external MySQL)
- shields
- traefik
- tus

### Simple Dependencies (Single Database)

Services with a single database dependency:

| Service | Depends On |
|---------|-----------|
| confluence | PostgreSQL |
| crowd | PostgreSQL |
| directus | MySQL |
| huginn | PostgreSQL |
| jira | PostgreSQL |
| keycloak | PostgreSQL |
| metabase | PostgreSQL |
| monica | MySQL |
| registry | (htpasswd auth only) |
| sonarqube | PostgreSQL |
| statping | PostgreSQL |

### Complex Dependencies (Multiple Services)

#### GitLab
```
gitlab
├── database (PostgreSQL)
└── redis
```

#### Sentry
```
sentry
├── postgres
├── redis
├── memcached
├── server
├── celery-worker
└── celery-cron
```

#### Graylog
```
graylog
├── mongodb
└── elasticsearch
```

#### Redash
```
redash
├── postgres
├── redis
├── server
├── worker
└── nginx
```

#### Cabot
```
cabot
├── postgres
├── rabbitmq
├── web
├── worker
└── beat
```

#### Weblate
```
weblate
├── postgres
├── redis
└── cache (memcached)
```

#### Zabbix
```
zabbix
├── database (MariaDB)
├── server
└── web
```

## Network Dependencies

### External Network: `traefik_default`

All services except the following connect to the external `traefik_default` network:

| Service | Network Configuration |
|---------|----------------------|
| traefik | Creates `traefik_default` (owns it) |
| mysql | Internal only |
| openvpn | Internal only |

### Internal Networks

Each service with multiple containers uses an internal network:

| Service | Internal Network |
|---------|-----------------|
| cabot | cabot |
| confluence | confluence |
| crowd | crowd |
| directus | directus |
| gitlab | gitlab |
| graylog | graylog |
| huginn | huginn |
| jira | jira |
| keycloak | keycloak |
| metabase | metabase |
| monica | monica |
| mysql | mysql |
| openvpn | openvpn |
| redash | redash |
| rundeck | rundeck |
| sentry | sentry |
| shields | shields |
| sonarqube | sonarqube |
| statping | statping |
| weblate | weblate |
| zabbix | zabbix |

## Initialization Order

When deploying multiple services, use this order:

1. **traefik** - Required by all HTTP services
2. **Standalone services** - No dependencies
3. **Database services** - If shared databases are used
4. **Application services** - Depend on databases

## Cross-Service Dependencies

Some services can share databases (not default configuration):

| Shared Database | Potential Consumers |
|----------------|---------------------|
| External PostgreSQL | gitlab, sentry, keycloak, metabase |
| External MySQL | directus, monica, zabbix |
| External Redis | gitlab, sentry, redash |

To enable shared databases, modify environment variables to point to external hosts.
