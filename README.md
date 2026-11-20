# Resume Recommender – MLOps

An end-to-end resume recommendation system that combines resume parsing, job-description ingestion, machine learning-based job categorization, semantic search, and resume-to-job matching.

The project brings together a backend API, an interactive frontend, data-ingestion pipelines, model tracking, vector search, and monitoring infrastructure.

## 1. Project Overview

The system processes resumes and job descriptions to identify relevant job opportunities.

Its main capabilities include:

- **Resume parsing:** Extracts information from PDF, DOCX, TXT, and image-based resumes.
- **Job ingestion:** Collects job descriptions using external job-search APIs.
- **Job categorization:** Uses a trained machine learning classifier to categorize job descriptions.
- **Resume scoring:** Applies a two-stage matching approach involving category matching and job matching.
- **Semantic search:** Uses sentence embeddings and PostgreSQL with pgvector for similarity-based retrieval.
- **AI-powered insights:** Integrates LLM services for additional analysis and insights.
- **Experiment tracking:** Uses MLflow and DagsHub to track model experiments and artifacts.
- **Monitoring:** Uses Prometheus and Grafana for application monitoring.

## 2. Architecture and Technology Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Embeddings | Sentence Transformers |
| Vector Database | PostgreSQL + pgvector |
| Knowledge Graph | Neo4j |
| LLM Integration | Groq and Gemini |
| Experiment Tracking | MLflow |
| MLOps and Data Versioning | DVC |
| Experiment Hosting | DagsHub |
| Data Processing | Python, Pandas |
| Containerization | Docker and Docker Compose |
| Monitoring | Prometheus and Grafana |

## 3. Repository Structure

```text
ResumeRecommender-MLops/
│
├── .github/
│   └── workflows/              # CI/CD workflow definitions (currently disabled)
│
├── app/
│   ├── api/
│   │   └── main.py              # FastAPI application entry point
│   └── services/
│       ├── ai_insight.py        # AI-powered insights
│       └── score_resume.py      # Resume scoring and matching
│
├── artifacts/
│   └── nltk_data.dvc            # DVC pointer for NLTK assets
│
├── data/
│   └── constants/               # Reference datasets and configuration data
│
├── data_ingestion/
│   ├── jd_ingestion/            # Job-description ingestion
│   ├── resume_ingestion/        # Resume parsing and extraction
│   ├── roles_ingestion/         # Job-role ingestion
│   └── processors/              # Data processing and transformation
│
├── grafana/
│   ├── dashboards/              # Monitoring dashboards
│   └── provisioning/            # Grafana provisioning configuration
│
├── models/
│   ├── job_categorizer_model/   # Trained job categorization model
│   ├── all-mpnet-base-v2.dvc   # DVC pointer for embedding model
│   └── .gitignore
│
├── notebooks/                   # Experiments and development notebooks
│
├── prompts/                     # LLM prompts and knowledge extraction templates
│
├── scripts/                     # Utility and model-download scripts
│
├── src/
│   ├── parser/                  # Resume parsing engine
│   ├── vector_db/               # Embedding and vector database operations
│   ├── label_jobs.py            # Job categorization
│   └── update_params.py         # Pipeline parameter updates
│
├── dags/                        # Airflow pipeline definitions
│
├── monitoring/
│   └── prometheus.yml           # Prometheus configuration
│
├── tests/                       # Unit, integration, regression and smoke tests
│
├── ui/
│   └── app.py                   # Streamlit frontend
│
├── utils/                       # Shared utilities
│
├── docker-compose.yml           # Container orchestration
├── Dockerfile.backend           # Backend image
├── Dockerfile.frontend          # Frontend image
├── Dockerfile.grafana           # Grafana image
├── Dockerfile.prometheus        # Prometheus image
│
├── dvc.yaml                     # DVC pipeline definition
├── dvc.lock                     # DVC pipeline lock file
├── params.yaml                  # Pipeline parameters
├── init_db.sql                  # Database initialization schema
├── requirements.txt             # Main Python dependencies
├── requirements-backend.txt     # Backend dependencies
├── requirements-frontend.txt    # Frontend dependencies
└── README.md
```

Some datasets and model assets are maintained separately through DVC and are not stored directly in Git.

## 4. Machine Learning and Data Pipeline

The project contains data-ingestion, processing, categorization, and embedding components.

The general workflow is:

1. Collect job descriptions from external sources.
2. Process and normalize the collected job data.
3. Prepare job-role information and reference datasets.
4. Categorize job descriptions using the trained classifier.
5. Generate embeddings for semantic retrieval.
6. Store and retrieve vector representations using PostgreSQL and pgvector.
7. Parse uploaded resumes and calculate job relevance scores.

The DVC pipeline is defined in `dvc.yaml`, with its associated parameters in `params.yaml`.

**Important:** Run `python src/update_params.py` before `dvc repro` when using the project's month-based parameter update workflow.

## 5. Model Tracking and DVC

The project uses MLflow for experiment tracking and DagsHub for hosting experiment information and model artifacts.

The trained job categorization model is included in:

```text
models/job_categorizer_model/
```

The MPNet embedding model and NLTK assets are tracked through DVC pointer files.

DVC-tracked assets require access to the configured remote storage. The repository's current `.dvc/config` references an S3 remote, so users must have the appropriate access or configure an accessible remote before retrieving those assets.

The project also uses DagsHub-hosted MLflow tracking. Configure the appropriate tracking URI and credentials through environment variables when running experiment-tracking workflows.

## 6. Environment Configuration

The application uses environment variables for API keys, database credentials, and external service configuration.

Depending on the components being used, configuration may include:

- `GROQ_API_KEY`
- `GEMINI_API_KEY`
- `DB_PASSWORD`
- `NEO4J_PASSWORD`
- `MLFLOW_TRACKING_PASSWORD`
- AWS credentials for an authorized DVC S3 remote

Provide the required values through your local environment or an untracked `.env` file.

**Never commit `.env` files, API keys, passwords, or cloud credentials to Git.**

Additional configuration values may be required by individual components.

## 7. Running with Docker

The project includes Dockerfiles for the backend, frontend, Prometheus, and Grafana, along with a Docker Compose configuration.

To build and start the configured services:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

The backend and frontend run as separate services and communicate through the Docker network configured in `docker-compose.yml`.

Check the Compose configuration for the actual service ports and required environment variables before launching the application.

## 8. Monitoring

The project includes Prometheus and Grafana configuration for monitoring.

- **Prometheus:** Collects application and service metrics according to its scrape configuration.
- **Grafana:** Provides dashboards for visualizing monitoring data.
- **Provisioning:** Configures Grafana data sources and dashboard loading.

Monitoring configuration is maintained under:

```text
monitoring/
grafana/
```

## 9. GitHub Actions

Workflow definitions are present under:

```text
.github/workflows/
```

The workflow files currently have the `.yml.disabled` extension and are therefore not active GitHub Actions workflows.

They can be enabled after the required deployment infrastructure, credentials, and repository secrets have been configured and verified.

## 10. Testing

The repository contains tests organized into:

- `tests/unit/` – Unit tests
- `tests/integration/` – Integration tests
- `tests/regression/` – Regression tests
- `tests/smoke/` – Smoke tests

Use the appropriate project environment and configure the required external services before running tests that depend on databases, APIs, or model assets.

## 11. Important Notes

- Keep credentials and environment-specific configuration out of version control.
- DVC-tracked assets require access to the configured storage remote.
- External services such as PostgreSQL, Neo4j, and MLflow must be configured where required.
- Docker service configuration and ports are defined in `docker-compose.yml`.
- GitHub Actions workflows are currently disabled pending infrastructure configuration.

---

**Resume Recommender – MLOps**

An integrated project combining machine learning, semantic search, data engineering, experiment tracking, and application monitoring.
