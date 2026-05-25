# Local PostgreSQL for Dekastar

The Django app in `core/` reads its database settings from `core/.env`, so the local PostgreSQL container should use the same values already defined there.

The official PostgreSQL image requires `POSTGRES_PASSWORD` and supports a named volume for persistent data. Mounting the data directory keeps the database state when the container is recreated.

## Start PostgreSQL

Run this from the repository root:

```powershell
docker volume create dekastar-postgres-data

docker run `
  --name dekastar-postgres `
  --detach `
  --publish 5432:5432 `
  --env-file .\core\.env `
  --volume dekastar-postgres-data:/var/lib/postgresql/data `
  postgres:17
```

The `postgres:17` image keeps the standard `/var/lib/postgresql/data` storage path used by the official documentation for PostgreSQL 17 and below.

## Check readiness

```powershell
docker logs -f dekastar-postgres
```

When the container is ready, you should see a message similar to `database system is ready to accept connections`.

## Connect from the app

With the container running, the app can connect through the existing `.env` values without additional changes.

## Install packages
If you haven't already, install the required Python packages for the Django app:

```powershell
pip install -r core/requirements.txt
```


## Run migrations

From the `core/` directory, run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

If you only want to inspect pending work first, use:

```powershell
python manage.py showmigrations
```

## Stop or reset

```powershell
docker stop dekastar-postgres
docker start dekastar-postgres
docker rm -f dekastar-postgres
docker volume rm dekastar-postgres-data
```

Use `docker rm -f` to remove the container, and remove the volume only if you want a clean database reset.