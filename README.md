# AgriVision AI

AgriVision AI is a smart agriculture platform that combines machine learning, data analytics, and a simple web interface to help users estimate crop yield and manage farm-related insights.

The project is built as a full-stack application with:

- `FastAPI` for the backend API
- `Streamlit` for the frontend dashboard
- `PostgreSQL` for persistence
- `scikit-learn` for crop yield prediction
- `Docker Compose` for local orchestration

## Overview

AgriVision AI was designed to support data-driven agricultural decisions. It provides a prediction workflow for crop yield estimation based on environmental and agricultural inputs such as country, crop type, year, average temperature, rainfall, and pesticide usage.

In addition to prediction, the backend also includes:

- user registration and login with JWT authentication
- farm creation and listing
- simple farm analytics and recommendations
- a data science workspace with notebooks for cleaning, engineering, exploration, and model training

## Key Features

- Crop yield prediction using a trained machine learning model
- User authentication with token-based access
- Farm management endpoints
- Farm analytics with expected yield, efficiency, and risk estimation
- Streamlit interface for an accessible user workflow
- Dockerized development setup
- Included notebooks for the end-to-end ML pipeline

## System Architecture

```text
Streamlit Frontend  -->  FastAPI Backend  -->  PostgreSQL
                              |
                              -->  Trained ML Model (.pkl)
                              -->  CSV Datasets / Notebooks
```

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit, Requests, Pandas, Plotly |
| Backend | FastAPI, Uvicorn, SQLAlchemy, Pydantic |
| Database | PostgreSQL 15 |
| ML / Data | scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Jupyter |
| DevOps | Docker, Docker Compose |

## Project Structure

```text
AgriVision-AI/
+-- backend/
|   +-- app/
|   |   +-- api/           # Auth, farms, analytics, ML endpoints
|   |   +-- db/            # Database connection and session management
|   |   +-- ml/            # Trained model artifacts
|   |   +-- models/        # SQLAlchemy models
|   |   +-- schemas/       # Pydantic schemas
|   |   +-- main.py        # FastAPI app entry point
|   +-- Dockerfile
|   +-- requirements.txt
+-- frontend/
|   +-- app.py             # Streamlit application
|   +-- Dockerfile
|   +-- requirements.txt
+-- data/
|   +-- raw/               # Raw datasets
|   +-- processed/         # Processed datasets
+-- notebooks/             # EDA, cleaning, engineering, training notebooks
+-- docker-compose.yml
+-- .env.example
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AgriVision-AI.git
cd AgriVision-AI
```

### 2. Create the environment file

Copy `.env.example` to `.env` and update the values if needed.

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

Recommended environment variables:

```env
DB_USER=admin
DB_PASSWORD=admin123
DB_HOST=db
DB_PORT=5432
DB_NAME=agrivision
SECRET_KEY=change_this_to_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

### 3. Run with Docker Compose

This is the recommended setup.

```bash
docker compose up --build
```

### 4. Open the application

- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Modules

### Authentication

- `POST /auth/register` - Create a new user
- `POST /auth/login` - Authenticate and receive an access token
- `GET /auth/me` - Retrieve the current authenticated user

### Machine Learning

- `POST /predict-yield/` - Predict crop yield from agricultural inputs

Example prediction payload:

```json
{
  "country": "United Kingdom",
  "crop": "Potatoes",
  "year": 2024,
  "avg_temp": 12.4,
  "rainfall": 1220.0,
  "pesticides": 18000.0
}
```

Example response:

```json
{
  "predicted_yield": 12345.67,
  "unit": "hg/ha"
}
```

## Running Without Docker

If you prefer to run services manually:

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Note: the frontend currently uses the internal Docker API host (`http://api:8000`) inside `frontend/app.py`. If you run the frontend outside Docker, update the backend base URL accordingly.

## Data Science Workflow

The repository includes notebooks covering the ML lifecycle:

- data cleaning
- data engineering
- data mining
- exploratory data analysis
- model training and experimentation

Processed and raw datasets are included under the `data/` directory.

## Environment Variables

| Variable | Description |
|---|---|
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `DB_NAME` | PostgreSQL database name |
| `SECRET_KEY` | JWT signing secret |
| `ALGORITHM` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_HOURS` | Token expiration duration |

## Current Limitations

- The frontend is currently optimized for the Docker network configuration
- No automated test suite is included yet
- No CI/CD workflow is configured yet

## Roadmap

- Add automated tests for API and ML endpoints
- Improve frontend UX and multilingual support
- Add model versioning and retraining workflow
- Introduce role-based access control
- Add deployment configuration for cloud environments

## Contributing

Contributions, issues, and feature suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License

This project is for educational and portfolio purposes unless a separate license is added.
