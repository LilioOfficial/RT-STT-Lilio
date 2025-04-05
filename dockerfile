# Use official Python image as a base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (to leverage Docker's layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Command to run the Python script
CMD ["python", "script.py"]
