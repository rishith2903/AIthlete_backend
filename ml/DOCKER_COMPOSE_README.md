This README explains how to run the local development stack using Docker Compose on Windows (PowerShell).

Services:
- ml_api: Flask-based ML API serving pose, workout, nutrition, and chatbot endpoints on port 5000.
- db: PostgreSQL 15 instance for the Spring Boot backend (used later).

Pre-requisites:
- Docker Desktop installed and running on Windows
- PowerShell (admin mode not strictly required, but helpful for firewall prompts)

Run:

Open PowerShell in the project root (c:\Users\rishi\Documents\gymproject) and run:

```powershell
# Build and start services
docker-compose up --build
```

The ML API will be available at http://localhost:5000 and Postgres at localhost:5432. Models persisted in `Backend/ml/models` will be mounted into the container at `/app/models` to allow iterative development without rebuilding.

Stopping:

```powershell
docker-compose down
```

Notes:
- If you modify Python dependencies, rebuild the ml_api image with `docker-compose build ml_api` or `docker-compose up --build`.
- The Postgres container stores data in a Docker volume named `pgdata`.
- For developing the Spring Boot backend, use the Postgres connection:
  jdbc:postgresql://host.docker.internal:5432/gymdb (username: postgres, password: postgres)

Admin Tools included in the Compose stack:
- Adminer: http://localhost:8080 (connect using DB credentials from the `.env` file)
- pgAdmin: http://localhost:5050 (login with PGADMIN_EMAIL / PGADMIN_PASSWORD from `.env`)

The project includes a `.env` file at the repo root with default credentials for local development. Update it if you need different passwords.

If you want me to also add a `docker-compose.override.yml` for local dev conveniences (pgadmin, adminer, or direct mounts), tell me which extras to include.
