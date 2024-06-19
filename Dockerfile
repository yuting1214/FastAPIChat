# Use an official Python runtime as a parent image
FROM python:3.9-slim as builder

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in the container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# This is the second stage where we create the runtime image
FROM python:3.9-slim

# Copy the dependencies from the build stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in the container
ADD . /app

# Command to run the uvicorn server
CMD ["python", "-m", "backend.app.main", "--mode", "prod", "--host", "0.0.0.0"]