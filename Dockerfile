# Use an official Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y wkhtmltopdf \
    curl \
    wget \
    gnupg \
    git \
    unzip \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Install Trivy (security scanner)
RUN wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.1_Linux-64bit.deb \
    && dpkg -i trivy_0.50.1_Linux-64bit.deb \
    && rm trivy_0.50.1_Linux-64bit.deb

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command
CMD ["python", "run_scans.py"]
