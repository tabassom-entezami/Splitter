# Splitter - FastAPI Project

A FastAPI-based web application with Docker support for easy development and deployment.

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for version control)

## Getting Started

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd splitter
   ```

2. **Build and start the application** (this will take a few minutes the first time):
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Open your browser and go to: http://localhost:8000
   - Interactive API documentation (Swagger UI) is available at: http://localhost:8000/docs
   - Alternative API documentation (ReDoc) is available at: http://localhost:8000/redoc

## Development

- The application will automatically reload when you make changes to the code in the `app/` directory
- All dependencies are managed through `pyproject.toml`
- The application runs on port 8000 by default (mapped from container port 80)

## Project Structure

```
.
├── app/                  # Application source code
│   └── main.py          # Main FastAPI application
├── .dockerignore        # Files to exclude from Docker build context
├── .gitignore           # Git ignore rules
├── compose.yml          # Docker Compose configuration
├── Dockerfile           # Docker configuration
└── pyproject.toml       # Python project configuration and dependencies
```

## Useful Commands

- Start the application in detached mode:
  ```bash
  docker-compose up -d
  ```

- View logs:
  ```bash
  docker-compose logs -f
  ```

- Stop the application:
  ```bash
  docker-compose down
  ```

- Run tests (if available):
  ```bash
  docker-compose exec web pytest
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.