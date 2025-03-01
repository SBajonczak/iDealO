# Python Docker App

This project is a Python application that periodically processes URLs using a script called `Checker.py`. The application is containerized using Docker for easy deployment and management.

## Project Structure

- `src/Checker.py`: Main Python script that appends URLs to a list and processes them.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `Dockerfile`: Instructions to build the Docker image, setting up the Python environment and installing dependencies.
- `docker-compose.yml`: Defines the services, networks, and volumes for the Docker application.
- `.dockerignore`: Specifies files and directories to ignore when building the Docker image.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd python-docker-app
   ```

2. **Build the Docker image:**
   ```bash
   docker build -t python-docker-app .
   ```

3. **Run the application:**
   ```bash
   docker-compose up
   ```

## Dependencies

Make sure to install the required Python libraries listed in `requirements.txt` before running the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.