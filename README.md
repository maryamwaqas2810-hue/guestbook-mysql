# Guestbook: 3-Tier App with Docker Compose

A simple guestbook web app where visitors leave a name and a message. Messages are stored in MySQL and shown on the page. The focus of this project is **packaging and running a multi-container app** the way it is done in real DevOps work.

## Architecture

```
Browser -> Nginx (reverse proxy) -> Flask + Gunicorn (app) -> MySQL (database)
```

| Tier | Tool | Role |
|---|---|---|
| Web / proxy | Nginx | Only service exposed to the outside (port 8080) |
| Application | Flask + Gunicorn | Handles the form and reads/writes messages |
| Database | MySQL 8.0 | Stores messages in a named volume |

## Project Structure

```
guestbook-mysql/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## How to Run

Requirements: Docker Desktop (with Docker Compose).

```bash
git clone <your-repo-url>
cd guestbook-mysql
cp .env.example .env      # then set your own passwords in .env
docker compose up -d --build
```

Open http://localhost:8080

To stop: `docker compose down` (data is kept in the volume).
To stop and delete the data too: `docker compose down -v`.

## Key Features

- **Healthcheck on MySQL:** the app starts only after the database is actually ready (`depends_on` with `service_healthy`).
- **Persistent data:** messages are stored in a named volume, so they survive container restarts and removal.
- **Secrets outside the code:** credentials live in `.env` (not committed); `.env.example` is the template.
- **Least privilege:** the app connects with its own limited MySQL user, not root.
- **Reduced exposure:** the database and the app have no published ports; only Nginx is reachable.
- **Production-style server:** Gunicorn runs the Flask app instead of the development server.
- **Safe queries and output:** parameterized SQL (protects against SQL injection) and escaped HTML output (protects against XSS).
- **Layer caching:** `requirements.txt` is copied before the code, so rebuilds are fast.

## What I Learned

- How containers talk to each other by service name inside a Compose network
- The difference between a container running and a service being healthy
- How volumes keep data after containers are removed
- Why a reverse proxy sits in front of the application
- Why secrets should never be committed to Git

## Next Steps

- CI/CD pipeline (Jenkins / GitHub Actions)
- Deployment on AWS EC2