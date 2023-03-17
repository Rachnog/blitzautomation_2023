FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add src directory to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Create data directory
RUN mkdir /app/data

# Copy app code
COPY app app/
COPY src src/
COPY config.yml .

# Expose the app's port
EXPOSE 8501

# Start the app
CMD ["streamlit", "run", "--server.port", "8501", "--server.enableCORS=false", "app/app.py"]
