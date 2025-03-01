FROM python:3.9-slim

# Install ODBC Driver
RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

WORKDIR /app

# Copy and install requirements
COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src .

# Set environment variables with default values
ENV IDEALO_URL=""
ENV WEBHOOK=""
ENV CATEGORY=""
ENV PYTHONUNBUFFERED=1

# Run script every hour
CMD ["python", "-u","main.py"]
