# university-management-system

## Requirements

- git
- docker
- docker-compose

## Get code

```sh
git clone https://github.com/luovkle/university-management-system
cd university-management-system
```

## Configure environment

### Create .env file

In order to run the services correctly you have to create a **.env** file in the same directory as the **docker-compose.yml**.

#### Structure

```txt
POSTGRES_USER={USER}
POSTGRES_PASSWORD={PASSWORD}
POSTGRES_SERVER={SERVER}
POSTGRES_DB={DB}
```

#### Example

You can actually use the same values as in the example, but consider changing the user and password.

```txt
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=db
POSTGRES_DB=app
```

### CORS

**Warning**: this parameter is not required and in fact if you are not a **javascript** user you may want to ignore it.

#### Structure

```txt
CORS_ORIGINS="{HOST1} {HOST2} {...}"
```

#### Example

```txt
CORS_ORIGINS="http://localhost:3000 http://127.0.0.1:8080"
```

## Running services

### Running for production

```sh
docker-compose -f docker-compose.yml up -d
```

### Running for development

```sh
docker-compose up -d
```
