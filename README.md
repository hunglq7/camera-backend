# Camera Backend

FastAPI application for camera management system with MySQL database.

## Local Development

### Prerequisites

- Python 3.11+
- MySQL 8.0+

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows
# or
.venv\Scripts\activate         # Windows cmd

# Install dependencies
pip install -r app/requirements.txt

# Run application
python -m app.run
```

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Quick Start

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
```

### Services

- **app**: FastAPI application (port 8000)
- **mysql**: MySQL 8.0 database (port 3306)

### Access Points

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MySQL: localhost:3306 (root/LeHung@79)

### Database

Database and tables are automatically created on first run via `init.sql`.

## API Endpoints

### Cameras

- `GET /cameras/` - List all cameras
- `POST /cameras/` - Add new camera
- `PUT /cameras/{id}/scan` - Scan camera status
- `DELETE /cameras/{id}` - Delete camera

### Tong Hop Camera

- `GET /tong-hop-camera/` - List all records
- `POST /tong-hop-camera/` - Add new record
- `GET /tong-hop-camera/{id}` - Get record by ID
- `PUT /tong-hop-camera/{id}` - Update record
- `DELETE /tong-hop-camera/{id}` - Delete record

## Environment Variables

| Variable    | Default           | Description        |
| ----------- | ----------------- | ------------------ |
| DB_HOST     | 192.168.0.110     | Database host      |
| DB_PORT     | 3306              | Database port      |
| DB_USER     | root              | Database user      |
| DB_PASSWORD | LeHung@79         | Database password  |
| DB_NAME     | camera_management | Database name      |
| HOST        | 192.168.0.110     | API host           |
| PORT        | 8000              | API port           |
| RELOAD      | True              | Enable auto-reload |
