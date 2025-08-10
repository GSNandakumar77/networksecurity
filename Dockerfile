# 1. Use an official Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies (for AWS CLI, ML packages, etc.)
#RUN apt-get update && apt-get install -y \
 #   awscli \
 #  git \
 #   build-essential \
 #   && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements file and install dependencies
COPY . /app

RUN apt update -y && apt-get install awscli -y

RUN apt-get update && pip install -r requirements.txt

# 8. Command to run FastAPI using Uvicorn
CMD ["python3", "app.py"]
