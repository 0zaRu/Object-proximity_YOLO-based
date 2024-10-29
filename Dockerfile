# Use a Python image
FROM python:3.9-slim

# Install necessary system packages for OpenCV, including libGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy the application files
COPY . /app
WORKDIR /app/src

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "unique-app.py"]
