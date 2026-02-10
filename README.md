# Splitter - Expense Splitting API

A FastAPI-based expense splitting application inspired by Splitwise, with Docker support for easy development and deployment.

## Features

- **User Management**: Create and manage users
- **Group Management**: Create groups for expense sharing
- **Expense Tracking**: Add expenses and split them among group members
- **RESTful API**: Clean and documented API endpoints
- **Database Support**: PostgreSQL with SQLAlchemy ORM
- **Docker Support**: Complete containerized setup
- **Comprehensive Testing**: Unit, integration, and workflow tests

## Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.13+ (for local development)
- Git (optional, for version control)

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd splitter
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the application**:
   ```bash
   docker compose up --build
   ```

4. **Access the application**:
   - API: http://localhost:8000
   - Interactive docs (Swagger): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

### Local Development

1. **Set up Python environment**:
   ```bash
   # Create virtual environment (outside project directory)
   python -m venv venv_splitter
   venv_splitter\Scripts\activate  # On Windows
   # or
   source venv_splitter/bin/activate  # On Unix
   
   # Install dependencies
   pip install -e .
   ```

2. **Set up database**:
   ```bash
   # Start PostgreSQL (using Docker)
   docker run --name splitter_db -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=splitter_db -p 5432:5432 -d postgres:15-alpine
   
   # Or use local PostgreSQL instance
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

4. **Run the application**:
   ```bash
   python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Project Structure

```
splitter/
├── src/                     # Source code
│   └── app/
│       ├── core/           # Core configuration
│       │   ├── config.py   # Application settings
│       │   └── database.py # Database setup
│       ├── models/         # SQLAlchemy models
│       │   ├── user.py
│       │   ├── group.py
│       │   ├── expense.py
│       │   └── ...
│       ├── schemas/        # Pydantic schemas
│       │   ├── user.py
│       │   ├── group.py
│       │   ├── expense.py
│       │   └── ...
│       ├── main.py         # FastAPI application
│       └── __init__.py
├── tests/                  # Test suite
│   ├── test_unit.py        # Unit tests
│   ├── test_api.py         # API tests
│   ├── test_integration.py # Integration tests
│   ├── test_workflows.py   # Workflow tests
│   └── test_complete.py    # Complete test runner
├── alembic/               # Database migrations
├── .env.example          # Environment variables template
├── compose.yml           # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── pyproject.toml        # Python project configuration
└── README.md             # This file
```

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /config` - Configuration info
- `GET /hello/{name}` - Greeting endpoint

### Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Run All Tests
```bash
# Using the complete test runner
python tests/test_complete.py

# Or using pytest directly
pytest tests/ -v
```

### Run Specific Test Suites
```bash
# Unit tests
python tests/test_unit.py

# API tests
pytest tests/test_api.py -v

# Integration tests
pytest tests/test_integration.py -v

# Workflow tests
pytest tests/test_workflows.py -v
```

### Test Coverage
The test suite includes:
- **Unit Tests**: Model validation, schema validation, configuration
- **API Tests**: Endpoint testing, request/response validation
- **Integration Tests**: Database operations, model relationships
- **Workflow Tests**: Complete user workflows, expense splitting

## Development

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=splitter_db
DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/splitter_db

# Application
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# CORS (if needed)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Code Quality
```bash
# Install development dependencies
pip install -e ".[dev]"

# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

## Docker Commands

### Development
```bash
# Start in development mode with hot reload
docker compose up --build

# Start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Production
```bash
# Build and start production containers
docker compose -f compose.yml -f compose.prod.yml up --build -d

# Scale services
docker compose up --build --scale web=2
```

### Database Management
```bash
# Access database
docker compose exec db psql -U postgres -d splitter_db

# Create database backup
docker compose exec db pg_dump -U postgres splitter_db > backup.sql

# Restore database
docker compose exec -T db psql -U postgres splitter_db < backup.sql
```

## Virtual Environment Setup

### Windows (Recommended location)
```bash
# Create venv in parent directory (recommended)
cd ..  # Go to parent directory of splitter
python -m venv venv_splitter
venv_splitter\Scripts\activate
cd splitter
pip install -e .
```

### Unix/macOS
```bash
# Create venv in parent directory (recommended)
cd ..  # Go to parent directory of splitter
python3 -m venv venv_splitter
source venv_splitter/bin/activate
cd splitter
pip install -e .
```

## Useful Commands

### Application Management
```bash
# Start development server
python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python tests/test_complete.py

# Check application health
curl http://localhost:8000/health
```

### Database Operations
```bash
# Initialize database
python -c "from src.app.core.database import engine; from src.app.models import Base; Base.metadata.create_all(bind=engine)"

# Test database connection
python -c "from src.app.core.database import engine; engine.connect()"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/test_complete.py`
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `.env` file configuration
   - Ensure PostgreSQL is running
   - Verify database URL format

2. **Import Errors**
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -e .`
   - Check Python path includes project root

3. **Docker Issues**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild containers: `docker compose down && docker compose up --build`
   - Check logs: `docker compose logs -f`

4. **Test Failures**
   - Ensure test database is accessible
   - Check environment variables
   - Run tests individually to identify issues

### Getting Help

- Check the logs: `docker compose logs -f`
- Run health check: `curl http://localhost:8000/health`
- Verify configuration: `curl http://localhost:8000/config`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.